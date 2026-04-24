"""Higgs platform adapter — Redis streams + Vercel AI SDK ``UIMessageChunk`` wire format.

Drop-in replacement for ``fnf-higgsclaw-agent`` inside the fnf orchestrator
pipeline.  Instead of pushing/editing messages on a platform API, this
adapter reads user messages from a per-chat Redis input stream and publishes
AI-SDK-shaped chunks to a per-chat output stream, plus a fan-in notify
entry on every publish.

Stream layout (one chat per pod, by convention — the adapter can serve
multiple chat_ids in a single process but the Higgsclaw Job model pins
CHAT_ID at startup):

    {STREAM_PREFIX}:{chat_id}:input    user → agent   (XREADGROUP, group=agent-{chat_id})
    {STREAM_PREFIX}:{chat_id}:output   agent → user   (XADD, maxlen=1000)
    {STREAM_PREFIX}:notify             fan-in hints   (XADD, maxlen=10000, one per output XADD)

Env contract (matches fnf/src/services/agent/agent.py::_build_env_vars):

    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_SSL, REDIS_PASSWORD (optional)
    CHAT_ID, STREAM_PREFIX (default "higgs")
    HF_DEV_USER_ID, HF_FOLDER_ID (metadata only)

Design notes:
- ``SUPPORTS_MESSAGE_EDITING = False`` so the gateway's stream consumer
  buffers the whole response and calls :meth:`send` once — each response
  lands as a text-start / text-delta / text-end triple.  Per-delta
  streaming is deferred to a follow-up PR that adds a HiggsStreamConsumer.
- Every ``XADD`` to ``:output`` is paired with an ``XADD`` to ``:notify``
  in a single Redis pipeline so the fnf consumer's notification-driven
  fan-in stays cheap.
- No encryption at this layer.  fnf's ``decode_message`` is a no-op for
  plaintext; when the fnf side starts enforcing encrypted payloads we
  wire in a key exchange here.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
import time
from typing import Any, Dict, Optional

from gateway import ui_chunks
from gateway.config import Platform, PlatformConfig
from gateway.platforms.base import (
    BasePlatformAdapter,
    MessageEvent,
    MessageType,
    SendResult,
    SessionSource,
)

logger = logging.getLogger("gateway.platforms.higgs")


_DEFAULT_STREAM_PREFIX = "higgs"
_DEFAULT_AGENT_GROUP_PREFIX = "agent-"
_DEFAULT_CONSUMER_NAME = "hermes-{pid}"

# Stream cap: matches fnf-higgsclaw-agent conventions so the fnf consumer's
# autoclaim/DLQ windows line up.
_OUTPUT_MAXLEN = 1000
_NOTIFY_MAXLEN = 10000

# Block timeout on XREADGROUP — short enough that SIGTERM / disconnect()
# unblocks within a fraction of a second, long enough to avoid busy-poll.
_INPUT_BLOCK_MS = 5000

# Lifecycle watchdog tick.  Higgsclaw-parity: check ONE_SHOT + idle every
# few seconds, trigger shutdown when conditions are met.
_LIFECYCLE_TICK_SECONDS = 5.0

# Extra drain window after the last turn finishes before SIGTERM-self —
# gives the stream consumer a moment to flush its tail chunk + the
# Redis pipeline to XADD the final notify entry.
_ONE_SHOT_DRAIN_SECONDS = 2.0


def check_higgs_requirements() -> bool:
    """True when the ``redis`` package with async support is importable."""
    try:
        import redis.asyncio  # noqa: F401
        return True
    except ImportError:
        logger.warning(
            "Higgs: redis.asyncio not installed. "
            "Run: pip install 'hermes-agent[higgs]'"
        )
        return False


class HiggsAdapter(BasePlatformAdapter):
    """Redis-streams / AI-SDK adapter for the Higgsclaw orchestrator.

    The adapter does one thing per Redis round-trip:

    * Inbound: ``XREADGROUP :input`` in a long-running task, wrap each
      entry as a :class:`MessageEvent`, call :meth:`handle_message`.
    * Outbound: wrap the platform's ``send*`` calls into AI-SDK chunk
      XADDs; fan in on ``:notify`` via a pipelined XADD in the same
      round-trip.

    Multi-chat is supported in theory (if ``CHAT_ID`` env is empty, the
    adapter subscribes to ``<prefix>:*:input`` via a scanner), but the
    Higgsclaw-deployment uses one chat per pod — keep it simple.
    """

    # Higgs' wire is append-only Redis XADD; there's no "edit" verb.  We
    # keep this False so the default base-class stream consumer path
    # (batch + edit) doesn't apply, and supply a custom per-delta consumer
    # via :meth:`make_stream_consumer` instead.
    SUPPORTS_MESSAGE_EDITING: bool = False

    # Adapter-level lock for lazy Redis init.  Multiple concurrent
    # handle_message bursts can race the first publish.
    _redis_init_lock: asyncio.Lock

    def __init__(self, config: PlatformConfig):
        super().__init__(config, Platform.HIGGS)

        extra = config.extra or {}

        # Redis connection config — env overrides config.yaml for parity
        # with the Higgsclaw orchestrator's env-driven model.
        self._redis_host = os.getenv("REDIS_HOST") or extra.get("host") or "localhost"
        self._redis_port = int(os.getenv("REDIS_PORT") or extra.get("port") or 6379)
        self._redis_db = int(os.getenv("REDIS_DB") or extra.get("db") or 0)
        self._redis_password = os.getenv("REDIS_PASSWORD") or extra.get("password")
        self._redis_ssl = self._parse_bool(
            os.getenv("REDIS_SSL"), extra.get("ssl", False),
        )

        # Stream naming.  CHAT_ID is optional — when unset we read from
        # the notify fan-in in multi-chat mode.  PR 1 assumes single-chat.
        self._stream_prefix = (
            os.getenv("STREAM_PREFIX") or extra.get("stream_prefix")
            or _DEFAULT_STREAM_PREFIX
        )
        self._chat_id = os.getenv("CHAT_ID") or extra.get("chat_id")
        self._user_id = os.getenv("HF_DEV_USER_ID") or extra.get("user_id")
        self._folder_id = os.getenv("HF_FOLDER_ID") or extra.get("folder_id")

        # Consumer identity: unique per pod so autoclaim works after
        # unexpected restarts.
        self._consumer_name = extra.get("consumer_name") or _DEFAULT_CONSUMER_NAME.format(
            pid=os.getpid(),
        )

        # Lifecycle knobs — match higgsclaw's ONE_SHOT / IDLE semantics.
        self._one_shot = self._parse_bool(
            os.getenv("ONE_SHOT"), extra.get("one_shot", False),
        )
        _idle_env = os.getenv("IDLE_TIMEOUT_SECONDS") or os.getenv("IDLE_TIMEOUT")
        self._idle_timeout_seconds = self._parse_int(
            _idle_env, extra.get("idle_timeout_seconds"),
        )

        self._redis: Any = None  # redis.asyncio.Redis — lazy so import costs only when connect()
        self._pool: Any = None
        self._input_task: Optional[asyncio.Task] = None
        self._lifecycle_task: Optional[asyncio.Task] = None
        self._redis_init_lock = asyncio.Lock()

        # Lifecycle state — updated by the input reader; polled by the
        # watchdog.  ``_last_input_at`` is monotonic-clock time; a pod with
        # no inputs ever uses the connect() timestamp as the anchor.
        self._last_input_at: float = time.monotonic()
        self._turns_completed: int = 0
        self._shutdown_reason: Optional[str] = None

    # ── Requirements / capabilities ────────────────────────────────────────

    @staticmethod
    def _parse_bool(value: Any, default: bool) -> bool:
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("1", "true", "yes", "on")

    @staticmethod
    def _parse_int(value: Any, default: Any) -> Optional[int]:
        if value is None:
            return default if isinstance(default, (int, type(None))) else None
        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            return default if isinstance(default, (int, type(None))) else None

    # ── Connection lifecycle ───────────────────────────────────────────────

    async def connect(self) -> bool:
        """Open the Redis pool, ensure consumer groups, spawn the input reader."""
        if not check_higgs_requirements():
            self._set_fatal_error(
                "missing_deps",
                "Higgs: redis.asyncio not installed (pip install 'hermes-agent[higgs]')",
                retryable=False,
            )
            return False

        if not self._chat_id:
            logger.warning(
                "Higgs: CHAT_ID env not set — running in multi-chat listener mode "
                "is not implemented yet; the adapter will connect but won't "
                "receive messages.  Set CHAT_ID to the chat UUID this pod "
                "serves.",
            )

        try:
            await self._ensure_redis()
        except Exception as exc:
            self._set_fatal_error(
                "redis_connect_failed",
                f"Higgs: could not reach Redis at {self._redis_host}:{self._redis_port} — {exc}",
                retryable=True,
            )
            return False

        if self._chat_id:
            try:
                await self._ensure_consumer_group(self._input_stream_key(self._chat_id))
            except Exception as exc:
                logger.warning(
                    "Higgs: XGROUP CREATE failed on input stream for chat %s: %s",
                    self._chat_id, exc,
                )
            self._input_task = asyncio.create_task(
                self._input_reader_loop(), name="higgs-input-reader",
            )

        # Lifecycle watchdog: only arm when ONE_SHOT or IDLE is configured
        # — otherwise the adapter runs indefinitely like any other platform.
        if self._one_shot or self._idle_timeout_seconds:
            self._last_input_at = time.monotonic()
            self._lifecycle_task = asyncio.create_task(
                self._lifecycle_watchdog(), name="higgs-lifecycle-watchdog",
            )

        self._mark_connected()
        logger.info(
            "Higgs adapter connected at redis://%s:%d/%d (prefix=%r, chat_id=%r, consumer=%r)",
            self._redis_host, self._redis_port, self._redis_db,
            self._stream_prefix, self._chat_id, self._consumer_name,
        )
        return True

    async def disconnect(self) -> None:
        if self._lifecycle_task is not None:
            self._lifecycle_task.cancel()
            try:
                await self._lifecycle_task
            except (asyncio.CancelledError, Exception):
                pass
            self._lifecycle_task = None

        if self._input_task is not None:
            self._input_task.cancel()
            try:
                await self._input_task
            except (asyncio.CancelledError, Exception):
                pass
            self._input_task = None

        if self._redis is not None:
            try:
                await self._redis.aclose()
            except Exception:
                pass
            self._redis = None
        if self._pool is not None:
            try:
                await self._pool.disconnect()
            except Exception:
                pass
            self._pool = None

        self._mark_disconnected()
        logger.info("Higgs adapter disconnected")

    async def _ensure_redis(self) -> None:
        if self._redis is not None:
            return
        async with self._redis_init_lock:
            if self._redis is not None:
                return
            import redis.asyncio as aioredis
            from redis.asyncio.connection import ConnectionPool, SSLConnection

            pool_kwargs: Dict[str, Any] = {
                "host": self._redis_host,
                "port": self._redis_port,
                "db": self._redis_db,
                "password": self._redis_password,
                "decode_responses": True,
                # Must be strictly greater than ``_INPUT_BLOCK_MS / 1000``
                # or XREADGROUP with block=N races the socket timeout at
                # the same N and logs spurious timeout warnings even when
                # the server is healthy.  30 s gives comfortable headroom
                # for ping/xack/xadd calls too.
                "socket_timeout": 30.0,
                "socket_connect_timeout": 5.0,
                "socket_keepalive": True,
                "health_check_interval": 15,
            }
            if self._redis_ssl:
                pool_kwargs["connection_class"] = SSLConnection
                pool_kwargs["ssl_cert_reqs"] = "none"

            self._pool = ConnectionPool(**pool_kwargs)
            self._redis = aioredis.Redis(connection_pool=self._pool)
            await self._redis.ping()

    # ── Stream naming ──────────────────────────────────────────────────────

    def _input_stream_key(self, chat_id: str) -> str:
        return f"{self._stream_prefix}:{chat_id}:input"

    def _output_stream_key(self, chat_id: str) -> str:
        return f"{self._stream_prefix}:{chat_id}:output"

    @property
    def _notify_stream_key(self) -> str:
        return f"{self._stream_prefix}:notify"

    def _agent_group(self, chat_id: str) -> str:
        return f"{_DEFAULT_AGENT_GROUP_PREFIX}{chat_id}"

    async def _ensure_consumer_group(self, stream_key: str) -> None:
        import redis.asyncio as aioredis

        group = self._agent_group(self._chat_id or "")
        try:
            await self._redis.xgroup_create(stream_key, group, id="0", mkstream=True)
            logger.info("Higgs: created consumer group %s on %s", group, stream_key)
        except aioredis.ResponseError as exc:
            if "BUSYGROUP" in str(exc):
                return
            raise

    # ── Input reader loop ──────────────────────────────────────────────────

    async def _input_reader_loop(self) -> None:
        """Long-running XREADGROUP loop on the single input stream.

        Runs until the task is cancelled (disconnect) or the adapter is
        marked with a fatal error.  Each entry is wrapped as a
        :class:`MessageEvent` and dispatched via :meth:`handle_message`,
        then ACKed.  Exceptions inside ``handle_message`` are caught and
        logged so one bad message doesn't wedge the loop — fnf's autoclaim
        will still see the ACK.
        """
        assert self._chat_id is not None
        stream_key = self._input_stream_key(self._chat_id)
        group = self._agent_group(self._chat_id)

        try:
            while self._running:
                try:
                    entries = await self._redis.xreadgroup(
                        groupname=group,
                        consumername=self._consumer_name,
                        streams={stream_key: ">"},
                        count=1,
                        block=_INPUT_BLOCK_MS,
                    )
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    logger.warning("Higgs: XREADGROUP error on %s: %s", stream_key, exc)
                    # Brief backoff; the Redis pool will reconnect transparently
                    # once the host is reachable again.
                    await asyncio.sleep(1.0)
                    continue

                if not entries:
                    continue

                for _name, batch in entries:
                    for message_id, fields in batch:
                        await self._dispatch_input(message_id, fields)
        except asyncio.CancelledError:
            pass

    async def _dispatch_input(self, message_id: str, fields: Dict[str, str]) -> None:
        """Decode one input entry and hand it to the gateway."""
        assert self._chat_id is not None
        stream_key = self._input_stream_key(self._chat_id)
        group = self._agent_group(self._chat_id)

        try:
            text = self._extract_input_text(fields)
            self._last_input_at = time.monotonic()
            if not text:
                await self._redis.xack(stream_key, group, message_id)
                return

            source = self.build_source(
                chat_id=self._chat_id,
                chat_name=self._chat_id,
                chat_type="dm",
                user_id=self._user_id,
            )
            event = MessageEvent(
                text=text,
                message_type=MessageType.TEXT,
                source=source,
                message_id=str(message_id),
                raw_message=dict(fields),
            )

            try:
                await self.handle_message(event)
                # handle_message returns when the agent turn has been
                # queued and (in the blocking case) completed.  For
                # ONE_SHOT we treat each handled input as one "turn".
                self._turns_completed += 1
            except Exception as exc:
                logger.exception(
                    "Higgs: handle_message failed for %s: %s", message_id, exc,
                )
            await self._redis.xack(stream_key, group, message_id)
        except Exception:
            # Last-line defence: even the ACK path shouldn't kill the loop.
            logger.exception("Higgs: dispatch failed for %s", message_id)

    @staticmethod
    def _extract_input_text(fields: Dict[str, str]) -> str:
        """Tolerant decoder for input entries.

        Supports three historical shapes so this adapter is source-compatible
        with both Hermes-native publishers and the fnf orchestrator:

        * fnf / higgsclaw wire (current prod): ``{type: "message",
          payload: "{\\"content\\": \\"...\\"}"}`` — a two-field XADD where
          ``type`` discriminates and ``payload`` is a JSON string. Types
          other than ``message`` (``approval``, ``system``) carry control
          data, not a user turn — we ignore them here and let a future
          router pick them up.
        * Plain text: ``{text: "..."}``.
        * UIMessage / chunk envelopes: ``{message: "{...}"}`` or
          ``{chunk: "..."}`` with either a bare text or a parts-array shape.
        """
        # fnf wire: dispatch on the "type" discriminator.
        msg_type = fields.get("type")
        raw_payload = fields.get("payload")
        if msg_type and raw_payload is not None:
            if msg_type != "message":
                # Not a user turn — let higher-level routers (approvals /
                # system actions) handle these.  Returning empty string
                # causes the caller to ACK and skip.
                return ""
            try:
                payload = json.loads(raw_payload)
            except (TypeError, ValueError):
                return str(raw_payload)
            if isinstance(payload, str):
                return payload
            if isinstance(payload, dict):
                for key in ("content", "text", "body"):
                    value = payload.get(key)
                    if isinstance(value, str) and value:
                        return value

        if "text" in fields and fields["text"]:
            return str(fields["text"])
        for key in ("message", "chunk", "content"):
            raw = fields.get(key)
            if not raw:
                continue
            try:
                payload = json.loads(raw)
            except (TypeError, ValueError):
                return str(raw)
            if isinstance(payload, str):
                return payload
            if isinstance(payload, dict):
                if isinstance(payload.get("text"), str):
                    return payload["text"]
                if isinstance(payload.get("content"), str):
                    return payload["content"]
                parts = payload.get("parts") or []
                if isinstance(parts, list):
                    pieces = [
                        p.get("text") for p in parts
                        if isinstance(p, dict) and p.get("type") == "text"
                    ]
                    if pieces:
                        return "".join(pieces)
        return ""

    # ── Outbound publishing ────────────────────────────────────────────────

    async def _publish_chunks(
        self,
        chat_id: str,
        chunks: list[dict[str, Any]],
    ) -> Optional[str]:
        """XADD every chunk to ``:output`` and fan a single notify entry.

        Uses one Redis pipeline so the per-publish round-trip stays at one.
        Returns the XADD message-id of the last chunk (useful as
        ``SendResult.message_id`` — callers can correlate later edits
        back to a specific text block).
        """
        await self._ensure_redis()
        out_key = self._output_stream_key(chat_id)
        notify_key = self._notify_stream_key

        pipe = self._redis.pipeline(transaction=False)
        for chunk in chunks:
            pipe.xadd(
                out_key,
                {"chunk": json.dumps(chunk, ensure_ascii=False)},
                maxlen=_OUTPUT_MAXLEN,
                approximate=True,
            )
        # One notify entry per publish batch — the consumer only needs to
        # know "this chat has something waiting", not how much.
        pipe.xadd(
            notify_key,
            {"chat_id": chat_id},
            maxlen=_NOTIFY_MAXLEN,
            approximate=True,
        )
        results = await pipe.execute()
        # Last chunk's message_id (pipeline returns results in order; the
        # final entry is the notify XADD id which we ignore).
        if len(results) >= 2:
            return str(results[-2])
        return None

    # ── BasePlatformAdapter — required overrides ───────────────────────────

    async def send(
        self,
        chat_id: str,
        content: str,
        reply_to: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SendResult:
        if not content:
            return SendResult(success=False, error="empty content")
        try:
            msg_id = await self._publish_chunks(
                chat_id, ui_chunks.text_block(content),
            )
            return SendResult(success=True, message_id=msg_id)
        except Exception as exc:
            logger.exception("Higgs: send failed for chat %s", chat_id)
            return SendResult(success=False, error=str(exc), retryable=True)

    async def get_chat_info(self, chat_id: str) -> Dict[str, Any]:
        return {
            "chat_id": chat_id,
            "name": chat_id,  # no human-readable name available at this layer
            "type": "dm",
            "user_id": self._user_id,
            "folder_id": self._folder_id,
        }

    def make_stream_consumer(
        self,
        chat_id: str,
        config: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Return a :class:`HiggsStreamConsumer` for per-delta XADD publishing.

        Overrides the base-class default (which would skip streaming for
        ``SUPPORTS_MESSAGE_EDITING=False``) — Higgs emits AI-SDK
        ``text-delta`` chunks per drain tick instead of edit-based
        batching, so streaming is very much on even without edit support.
        """
        # Import locally so the higgs_stream_consumer module is only
        # loaded when streaming is actually active for this adapter.
        from gateway.platforms.higgs_stream_consumer import HiggsStreamConsumer
        return HiggsStreamConsumer(
            adapter=self, chat_id=chat_id, config=config, metadata=metadata,
        )

    # ── BasePlatformAdapter — optional overrides ──────────────────────────

    async def send_typing(self, chat_id: str, metadata=None) -> None:
        # AI SDK frontends render state from chunks directly — no equivalent
        # of a typing indicator is needed.  Left as a no-op.
        pass

    async def send_image(
        self,
        chat_id: str,
        image_url: str,
        caption: Optional[str] = None,
        reply_to: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SendResult:
        chunks: list[dict[str, Any]] = []
        if caption:
            chunks.extend(ui_chunks.text_block(caption))
        chunks.append(ui_chunks.data_part(
            "file",
            {"mediaType": "image/png", "url": image_url},
        ))
        try:
            msg_id = await self._publish_chunks(chat_id, chunks)
            return SendResult(success=True, message_id=msg_id)
        except Exception as exc:
            logger.exception("Higgs: send_image failed for chat %s", chat_id)
            return SendResult(success=False, error=str(exc), retryable=True)

    async def send_image_file(
        self,
        chat_id: str,
        image_path: str,
        caption: Optional[str] = None,
        reply_to: Optional[str] = None,
        **kwargs,
    ) -> SendResult:
        # Without a static asset host, we emit the raw path as a data-file
        # part — the frontend can decide whether to fetch it via a signed
        # URL, a sidecar proxy, or display it as a label.  When a future
        # PR adds upload-to-S3 / fsx, this method grows a proper URL.
        chunks: list[dict[str, Any]] = []
        if caption:
            chunks.extend(ui_chunks.text_block(caption))
        chunks.append(ui_chunks.data_part(
            "file",
            {"mediaType": "image/local", "path": image_path},
        ))
        try:
            msg_id = await self._publish_chunks(chat_id, chunks)
            return SendResult(success=True, message_id=msg_id)
        except Exception as exc:
            logger.exception("Higgs: send_image_file failed for chat %s", chat_id)
            return SendResult(success=False, error=str(exc), retryable=True)

    async def send_voice(
        self,
        chat_id: str,
        audio_path: str,
        caption: Optional[str] = None,
        reply_to: Optional[str] = None,
        **kwargs,
    ) -> SendResult:
        chunks: list[dict[str, Any]] = []
        if caption:
            chunks.extend(ui_chunks.text_block(caption))
        chunks.append(ui_chunks.data_part(
            "file",
            {"mediaType": "audio/ogg", "path": audio_path},
        ))
        try:
            msg_id = await self._publish_chunks(chat_id, chunks)
            return SendResult(success=True, message_id=msg_id)
        except Exception as exc:
            logger.exception("Higgs: send_voice failed for chat %s", chat_id)
            return SendResult(success=False, error=str(exc), retryable=True)

    # ── Lifecycle watchdog ─────────────────────────────────────────────────

    async def _lifecycle_watchdog(self) -> None:
        """Poll ONE_SHOT / IDLE triggers and initiate self-shutdown.

        Deliberately mirrors higgsclaw's behaviour: after the configured
        condition is met we ``SIGTERM`` our own process so the gateway
        supervisor's normal graceful-shutdown path drains every platform
        (not just this adapter).  Inside K8s, kubelet observes the exit
        and marks the Job complete; TTL sweeps the pod.
        """
        try:
            while self._running:
                await asyncio.sleep(_LIFECYCLE_TICK_SECONDS)
                reason = self._shutdown_condition()
                if reason:
                    self._shutdown_reason = reason
                    logger.info(
                        "Higgs: lifecycle trigger fired (%s) — initiating shutdown",
                        reason,
                    )
                    # Small drain window so any in-flight XADD pipeline
                    # completes before we tear Redis down.
                    await asyncio.sleep(_ONE_SHOT_DRAIN_SECONDS)
                    self._send_self_sigterm()
                    return
        except asyncio.CancelledError:
            pass

    def _shutdown_condition(self) -> Optional[str]:
        """Return the reason string when ONE_SHOT or idle triggers fire.

        Returns None when the adapter should keep running.
        """
        if self._one_shot and self._turns_completed >= 1:
            return "one_shot_complete"
        if self._idle_timeout_seconds and self._idle_timeout_seconds > 0:
            elapsed = time.monotonic() - self._last_input_at
            if elapsed >= self._idle_timeout_seconds:
                return f"idle_timeout ({elapsed:.0f}s >= {self._idle_timeout_seconds}s)"
        return None

    def _send_self_sigterm(self) -> None:
        """Signal the gateway supervisor to start graceful shutdown.

        Prefers SIGTERM to ``os.getpid()`` since the gateway already has
        signal handlers that drain all platforms (not just this one).
        Falls back to ``_mark_disconnected`` + a fatal-error hint if
        SIGTERM cannot be delivered (e.g. sandboxed test runs).
        """
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception as exc:
            logger.warning("Higgs: SIGTERM self failed: %s — marking adapter disconnected", exc)
            self._mark_disconnected()
            self._set_fatal_error(
                "higgs_lifecycle_exit",
                f"Higgs adapter exited: {self._shutdown_reason}",
                retryable=False,
            )

    async def send_exec_approval(
        self,
        chat_id: str,
        command: str,
        session_key: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SendResult:
        """Publish a tool-approval-request chunk.

        The gateway's ``register_gateway_notify`` / ``resolve_gateway_approval``
        pair blocks the agent thread until a user response arrives.  In the
        Higgs deployment the user resolves approvals by writing a response
        (e.g. ``{"type": "tool-approval-response", "approved": true, ...}``)
        onto the ``:input`` stream — the ``_extract_input_text`` + agent's
        message-handling path parses it and calls ``resolve_gateway_approval``.
        """
        approval_id = ui_chunks.new_id()
        chunk = ui_chunks.tool_approval_request(
            approval_id=approval_id,
            tool_call_id=f"bash-{approval_id}",
            tool_name="bash",
            provider_metadata=ui_chunks.provider_meta(
                command=command,
                description=description,
                session_key=session_key,
            ),
        )
        try:
            msg_id = await self._publish_chunks(chat_id, [chunk])
            return SendResult(success=True, message_id=msg_id)
        except Exception as exc:
            logger.exception("Higgs: send_exec_approval failed for chat %s", chat_id)
            return SendResult(success=False, error=str(exc), retryable=True)
