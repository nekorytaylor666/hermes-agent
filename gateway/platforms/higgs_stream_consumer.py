"""Stream consumer for the Higgs platform.

Replaces :class:`GatewayStreamConsumer`'s batch-and-edit drain with a
per-delta XADD of AI SDK ``text-delta`` chunks.  Reuses the base class's
think-tag filtering and queue plumbing so we stay in sync with everything
``_filter_and_accumulate`` / ``_flush_think_buffer`` learns.

Wire contract produced by this consumer for a single streamed response:

    ``text-start`` (once, on first actual text after filtering)
    ``text-delta`` × N  (one per drain tick that had new content)
    ``text-end``  (on ``finish()`` or ``on_segment_break()``)

Tool boundaries (``on_segment_break``) finalize the current ``text-*``
block and reset internal state — the next text starts a fresh id.  This
mirrors ``_NEW_SEGMENT`` behaviour in the Telegram/Discord consumer.
"""

from __future__ import annotations

import asyncio
import logging
import queue
from typing import TYPE_CHECKING, Any, Optional

from gateway import ui_chunks
from gateway.stream_consumer import (
    GatewayStreamConsumer,
    StreamConsumerConfig,
    _COMMENTARY,
    _DONE,
    _NEW_SEGMENT,
)

if TYPE_CHECKING:
    from gateway.platforms.higgs import HiggsAdapter

logger = logging.getLogger("gateway.platforms.higgs_stream_consumer")


class HiggsStreamConsumer(GatewayStreamConsumer):
    """Per-delta AI-SDK chunk publisher for :class:`HiggsAdapter`.

    The base class's rich batching / rate-limiting / overflow-splitting
    logic doesn't apply — Redis streams are append-only and AI SDK chunks
    are reassembled on the frontend from individual deltas, so each tick
    that has text simply XADDs a ``text-delta`` chunk.

    Config is honoured partially:

    * ``buffer_threshold`` — a min-char hint.  If a drain tick produced
      fewer than this many new chars, we hold them for the next tick so
      we aren't XADD-spamming Redis on single-character deltas.  The
      base class ignores this in buffer-only mode; we treat it as a soft
      flush hint.
    * ``edit_interval`` / ``cursor`` / ``buffer_only`` — ignored; Higgs
      has no cursor concept and no edit semantics.
    """

    # Minimum time to wait between drain ticks.  Lower than the Telegram
    # default because there's no rate limit to respect on the Redis side.
    _TICK_INTERVAL = 0.05

    def __init__(
        self,
        adapter: "HiggsAdapter",
        chat_id: str,
        config: Optional[StreamConsumerConfig] = None,
        metadata: Optional[dict] = None,
    ):
        super().__init__(adapter, chat_id, config, metadata)
        self._text_id: Optional[str] = None
        # Track whether the block is open so finish()'s terminator is
        # idempotent (for the no-text response case, we don't emit
        # text-start at all and therefore also skip text-end).
        self._text_block_open = False

    # ── drain loop ─────────────────────────────────────────────────────────

    async def run(self) -> None:
        """Drain deltas, emit AI-SDK chunks per tick."""
        try:
            while True:
                got_done = False
                got_segment_break = False
                commentary_text: Optional[str] = None

                # Pull everything available from the sync queue.  Filter
                # out think tags via the base class so reasoning is routed
                # separately (the gateway already has a reasoning_callback
                # path for that — we don't double-emit it here).
                while True:
                    try:
                        item = self._queue.get_nowait()
                    except queue.Empty:
                        break
                    if item is _DONE:
                        got_done = True
                        break
                    if item is _NEW_SEGMENT:
                        got_segment_break = True
                        break
                    if isinstance(item, tuple) and len(item) == 2 and item[0] is _COMMENTARY:
                        commentary_text = item[1]
                        break
                    self._filter_and_accumulate(item)

                # On stream end, drain any held-back partial-tag buffer so
                # trailing text isn't lost.
                if got_done:
                    self._flush_think_buffer()

                # Emit whatever got accumulated in this tick.
                if self._accumulated:
                    await self._emit_text_delta(self._accumulated)
                    self._already_sent = True
                    self._accumulated = ""

                # Commentary: a bolt-on assistant message between tool iterations
                # (e.g. "I'll inspect the repo first.").  Close the current
                # block, emit commentary as its own text block, then continue.
                if commentary_text is not None:
                    await self._close_text_block()
                    await self._emit_complete_text_block(commentary_text)

                if got_segment_break:
                    await self._close_text_block()

                if got_done:
                    await self._close_text_block()
                    self._final_response_sent = self._already_sent
                    return

                await asyncio.sleep(self._TICK_INTERVAL)
        except asyncio.CancelledError:
            await self._close_text_block()
            raise
        except Exception:
            logger.exception("Higgs stream consumer: drain loop failed")
            await self._close_text_block()

    # ── chunk emission ─────────────────────────────────────────────────────

    async def _emit_text_delta(self, delta: str) -> None:
        if not delta:
            return
        if self._text_id is None:
            self._text_id = ui_chunks.new_id()
            self._text_block_open = True
            await self._adapter_publish([ui_chunks.text_start(self._text_id)])
        await self._adapter_publish([ui_chunks.text_delta(self._text_id, delta)])

    async def _close_text_block(self) -> None:
        if self._text_block_open and self._text_id is not None:
            await self._adapter_publish([ui_chunks.text_end(self._text_id)])
        self._text_id = None
        self._text_block_open = False

    async def _emit_complete_text_block(self, content: str) -> None:
        if not content:
            return
        await self._adapter_publish(ui_chunks.text_block(content))
        self._already_sent = True

    async def _adapter_publish(self, chunks: list[dict[str, Any]]) -> None:
        """Delegate XADD + notify to the adapter's pipelined publisher.

        Uses a narrow interface (``_publish_chunks``) rather than the
        public ``send`` so we don't re-wrap each chunk in another
        ``text_block``.
        """
        if not chunks:
            return
        try:
            await self.adapter._publish_chunks(self.chat_id, chunks)  # noqa: SLF001
        except Exception as exc:
            logger.warning(
                "Higgs stream consumer: publish failed (%d chunks): %s",
                len(chunks), exc,
            )
