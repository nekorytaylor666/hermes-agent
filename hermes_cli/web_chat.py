"""Vercel AI SDK UIMessage Data Stream Protocol v1 adapter for Hermes.

Bridges ``AIAgent`` callbacks (stream_delta, tool_start, tool_complete,
reasoning, status) onto the AI SDK's UIMessage protocol consumed by
``useChat`` in ``@ai-sdk/react`` v5+.

Wire format (SSE):
    Content-Type: text/event-stream
    x-vercel-ai-ui-message-stream: v1
    Each event:  data: <JSON part>\\n\\n

Part types emitted here (v5):
    start, start-step, text-start, text-delta, text-end,
    reasoning-start, reasoning-delta, reasoning-end,
    tool-input-start, tool-input-available, tool-output-available,
    data-status (custom), finish-step, finish, error
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, Iterable, List, Optional

_log = logging.getLogger(__name__)

_SENTINEL = object()


class UIMessageStreamWriter:
    """Adapts synchronous AIAgent callbacks into async AI-SDK-shaped parts.

    Callbacks fire on the agent's worker thread; we hop each part onto the
    FastAPI event loop via ``run_coroutine_threadsafe`` — same pattern as
    ``acp_adapter/events.py``.
    """

    def __init__(self, queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        self._q = queue
        self._loop = loop
        self._text_id: Optional[str] = None
        self._reasoning_id: Optional[str] = None
        self._closed = False

    def _emit(self, part: Dict[str, Any]) -> None:
        if self._closed:
            return
        try:
            asyncio.run_coroutine_threadsafe(self._q.put(part), self._loop)
        except RuntimeError:
            # Loop already shut down — drop the part silently.
            pass

    def _close_text(self) -> None:
        if self._text_id is not None:
            self._emit({"type": "text-end", "id": self._text_id})
            self._text_id = None

    def _close_reasoning(self) -> None:
        if self._reasoning_id is not None:
            self._emit({"type": "reasoning-end", "id": self._reasoning_id})
            self._reasoning_id = None

    # -- AIAgent callbacks --------------------------------------------------

    def on_text_delta(self, text: str) -> None:
        if not text:
            return
        # A text stream may interleave with reasoning in some providers; we
        # close reasoning when actual answer text starts so the UI renders
        # them as separate parts.
        self._close_reasoning()
        if self._text_id is None:
            self._text_id = str(uuid.uuid4())
            self._emit({"type": "text-start", "id": self._text_id})
        self._emit({"type": "text-delta", "id": self._text_id, "delta": text})

    def on_reasoning_delta(self, text: str) -> None:
        if not text:
            return
        if self._reasoning_id is None:
            self._reasoning_id = str(uuid.uuid4())
            self._emit({"type": "reasoning-start", "id": self._reasoning_id})
        self._emit({
            "type": "reasoning-delta",
            "id": self._reasoning_id,
            "delta": text,
        })

    def on_tool_start(self, call_id: str, name: str, args: Dict[str, Any]) -> None:
        # Tool boundary — finalize in-progress text/reasoning so the UI
        # renders a fresh card. Mirrors Telegram's _NEW_SEGMENT sentinel.
        self._close_text()
        self._close_reasoning()
        self._emit({
            "type": "tool-input-start",
            "toolCallId": call_id,
            "toolName": name,
        })
        self._emit({
            "type": "tool-input-available",
            "toolCallId": call_id,
            "toolName": name,
            "input": _json_safe(args),
        })

    def on_tool_complete(
        self,
        call_id: str,
        name: str,
        args: Dict[str, Any],
        result: Any,
    ) -> None:
        # Hermes tool handlers return JSON strings (tool_result / tool_error
        # both call json.dumps). Parse back to a native object so the UI
        # receives structured output instead of a stringified blob. Any
        # tool that returns plain text (non-JSON) passes through unchanged.
        output: Any = result
        if isinstance(result, str):
            stripped = result.strip()
            if stripped and stripped[0] in "{[":
                try:
                    output = json.loads(result)
                except (ValueError, TypeError):
                    output = result
        self._emit({
            "type": "tool-output-available",
            "toolCallId": call_id,
            "output": _json_safe(output),
        })

    def on_status(self, lifecycle: str, message: str) -> None:
        self._emit({
            "type": "data-status",
            "data": {"lifecycle": lifecycle, "message": message},
        })

    def on_error(self, message: str) -> None:
        self._emit({"type": "error", "errorText": message})

    def on_approval_request(
        self,
        approval_id: str,
        command: str,
        description: str,
        pattern_keys: Optional[list] = None,
    ) -> None:
        """Emit a data-approval part for the frontend to render buttons."""
        self._close_text()
        self._close_reasoning()
        self._emit({
            "type": "data-approval",
            "data": {
                "approvalId": approval_id,
                "command": command,
                "description": description,
                "patternKeys": list(pattern_keys or []),
                "choices": ["once", "session", "always", "deny"],
            },
        })

    # -- Lifecycle ----------------------------------------------------------

    def start(self, message_id: Optional[str] = None) -> None:
        self._emit({
            "type": "start",
            "messageId": message_id or str(uuid.uuid4()),
        })
        self._emit({"type": "start-step"})

    def finish(self) -> None:
        self._close_text()
        self._close_reasoning()
        self._emit({"type": "finish-step"})
        self._emit({"type": "finish"})
        self._closed = True
        # Drop the queue terminator directly (already on the loop thread
        # from the FastAPI generator's finally block is fine too).
        try:
            asyncio.run_coroutine_threadsafe(self._q.put(_SENTINEL), self._loop)
        except RuntimeError:
            pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _json_safe(obj: Any) -> Any:
    """Best-effort convert to a JSON-serializable shape.

    AIAgent's tool results are strings (after ``maybe_persist_tool_result``),
    but arguments may contain types like ``Path``; coerce to str on failure.
    """
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        if isinstance(obj, dict):
            return {str(k): _json_safe(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_json_safe(v) for v in obj]
        return str(obj)


def ui_messages_to_hermes_history(
    messages: Iterable[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Flatten AI-SDK UIMessage[] into Hermes ``{role, content}`` list.

    UIMessage parts:
        {"type": "text", "text": "..."}        → joined into content
        {"type": "reasoning", "text": "..."}    → ignored (re-derivable)
        {"type": "tool-*", ...}                 → ignored for history
        {"type": "file", "url": ..., ...}       → ignored for now
    """
    out: List[Dict[str, Any]] = []
    for m in messages:
        role = m.get("role")
        if role not in ("user", "assistant", "system"):
            continue
        parts = m.get("parts") or []
        text_chunks: List[str] = []
        for p in parts:
            if isinstance(p, dict) and p.get("type") == "text":
                txt = p.get("text")
                if isinstance(txt, str):
                    text_chunks.append(txt)
        # Older or custom clients may send `content` directly.
        if not text_chunks and isinstance(m.get("content"), str):
            text_chunks.append(m["content"])
        content = "".join(text_chunks).strip()
        if not content:
            continue
        out.append({"role": role, "content": content})
    return out


def extract_latest_user_text(messages: Iterable[Dict[str, Any]]) -> Optional[str]:
    """Return the text content of the final user UIMessage, or None."""
    last: Optional[Dict[str, Any]] = None
    for m in messages:
        if m.get("role") == "user":
            last = m
    if not last:
        return None
    parts = last.get("parts") or []
    chunks = [
        p.get("text", "")
        for p in parts
        if isinstance(p, dict) and p.get("type") == "text"
    ]
    if not chunks and isinstance(last.get("content"), str):
        chunks = [last["content"]]
    text = "".join(chunks).strip()
    return text or None


def sse_format(part: Dict[str, Any]) -> str:
    """Serialize one part to an SSE ``data:`` frame."""
    return f"data: {json.dumps(part, ensure_ascii=False)}\n\n"


SENTINEL = _SENTINEL


# ---------------------------------------------------------------------------
# Pending approvals registry — shared between the /api/chat emitter side
# and the /api/chat/approve endpoint that resolves them.
# ---------------------------------------------------------------------------

import threading as _threading  # noqa: E402

_pending_approvals_lock = _threading.Lock()
_pending_approvals: Dict[str, str] = {}
"""approvalId -> session_key (for resolve_gateway_approval lookup)."""


def register_pending_approval(approval_id: str, session_key: str) -> None:
    with _pending_approvals_lock:
        _pending_approvals[approval_id] = session_key


def pop_pending_approval(approval_id: str) -> Optional[str]:
    with _pending_approvals_lock:
        return _pending_approvals.pop(approval_id, None)


def drop_pending_approvals_for_session(session_key: str) -> None:
    """Called when a /api/chat stream ends — clean stale approval IDs."""
    with _pending_approvals_lock:
        stale = [k for k, v in _pending_approvals.items() if v == session_key]
        for k in stale:
            _pending_approvals.pop(k, None)
