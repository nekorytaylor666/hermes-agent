"""langfuse plugin — Langfuse tracing for hermes-agent sessions.

Uses Langfuse SDK v4 with full session, user, and span support:

- ``on_session_start`` / first hook -> root **span** with session_id + user_id
- ``pre_llm_call``       -> captures sender_id as user_id for the trace
- ``pre_api_request``    -> nested **generation** observation
- ``post_api_request``   -> update + end generation with usage
- ``pre_tool_call``      -> nested **tool** observation
- ``post_tool_call``     -> update + end tool observation
- ``on_session_end``     -> update + end root span, flush
- ``on_session_finalize`` -> flush + cleanup
"""

from __future__ import annotations

import logging
import os
import time
import threading
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Langfuse client (lazy-init)
# ---------------------------------------------------------------------------

_langfuse = None
_init_attempted = False
_lock = threading.Lock()


def _get_client():
    """Lazy-init the Langfuse client on first use."""
    global _langfuse, _init_attempted
    if _init_attempted:
        return _langfuse
    with _lock:
        if _init_attempted:
            return _langfuse
        _init_attempted = True
        try:
            from langfuse import Langfuse
        except ImportError:
            logger.warning(
                "langfuse plugin: langfuse package not installed. "
                "Run: pip install langfuse"
            )
            return None

        public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        if not public_key or not secret_key:
            logger.warning(
                "langfuse plugin: LANGFUSE_PUBLIC_KEY and/or "
                "LANGFUSE_SECRET_KEY not set — tracing disabled."
            )
            return None

        base_url = os.getenv(
            "LANGFUSE_BASE_URL", "https://cloud.langfuse.com"
        )
        _langfuse = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=base_url,
        )
        logger.info("langfuse plugin: client initialised (%s)", base_url)
        return _langfuse


# ---------------------------------------------------------------------------
# Per-session state
# ---------------------------------------------------------------------------

class _SessionState:
    """Mutable state for one hermes session's Langfuse trace."""
    __slots__ = ("trace", "propagation_ctx", "user_id", "generations", "spans", "tool_keys")

    def __init__(self):
        self.trace = None                    # root LangfuseSpan
        self.propagation_ctx = None          # _propagate_attributes context manager
        self.user_id: str = ""               # set from pre_llm_call sender_id
        self.generations: Dict[str, Any] = {}  # gen_key -> generation observation
        self.spans: Dict[str, Any] = {}      # span_key -> tool observation
        self.tool_keys: Dict[tuple, str] = {}  # (tool_name, tool_call_id) -> span_key


_sessions: Dict[str, _SessionState] = {}
_state_lock = threading.Lock()


def _ensure_trace(
    session_id: str,
    model: str = "",
    platform: str = "",
    user_id: str = "",
) -> Optional[_SessionState]:
    """Return (or lazily create) the session state with a root trace.

    ``on_session_start`` only fires for brand-new sessions. Continued
    sessions skip it, so we create the root span on-demand from
    whichever hook fires first.
    """
    with _state_lock:
        state = _sessions.get(session_id)
        if state is not None and state.trace is not None:
            # Update user_id if we learn it later (from pre_llm_call)
            if user_id and not state.user_id:
                state.user_id = user_id
            return state

    client = _get_client()
    if not client:
        return None

    try:
        from langfuse._client.propagation import _propagate_attributes

        state = _SessionState()
        state.user_id = user_id

        # Propagate session_id and user_id as trace-level attributes
        propagate_kwargs: Dict[str, Any] = {
            "session_id": session_id,
            "trace_name": "hermes-session",
        }
        if user_id:
            propagate_kwargs["user_id"] = user_id

        ctx = _propagate_attributes(**propagate_kwargs)
        ctx.__enter__()
        state.propagation_ctx = ctx

        # Create root span inside the propagation context
        state.trace = client.start_observation(
            name="hermes-session",
            as_type="span",
            metadata={
                "session_id": session_id,
                "model": model,
                "platform": platform,
            },
        )

        with _state_lock:
            # Double-check for race
            existing = _sessions.get(session_id)
            if existing is not None and existing.trace is not None:
                state.trace.end()
                ctx.__exit__(None, None, None)
                if user_id and not existing.user_id:
                    existing.user_id = user_id
                return existing
            _sessions[session_id] = state

        logger.info(
            "langfuse: trace started session_id=%s user_id=%s",
            session_id, user_id or "(unknown)",
        )
        return state

    except Exception as exc:
        logger.warning("langfuse: _ensure_trace error: %s", exc)
        return None


def _cleanup_session(session_id: str) -> Optional[_SessionState]:
    """Remove and return the session state, cleaning up the propagation ctx."""
    with _state_lock:
        state = _sessions.pop(session_id, None)
    if state and state.propagation_ctx:
        try:
            state.propagation_ctx.__exit__(None, None, None)
        except Exception:
            pass
        state.propagation_ctx = None
    return state


# ---------------------------------------------------------------------------
# Hook callbacks
# ---------------------------------------------------------------------------

def _on_session_start(
    session_id: str = "",
    model: str = "",
    platform: str = "",
    **_: Any,
) -> None:
    """Create a new Langfuse trace for the session."""
    _ensure_trace(session_id, model, platform)


def _on_pre_llm_call(
    session_id: str = "",
    sender_id: str = "",
    user_message: str = "",
    model: str = "",
    platform: str = "",
    **_: Any,
) -> None:
    """Capture user_id + user_message and set them on the trace."""
    state = _ensure_trace(session_id, model, platform, user_id=sender_id)
    if not state or not state.trace:
        return

    try:
        # Set user_id directly on the OTel span so Langfuse picks it up
        if sender_id and state.trace._otel_span.is_recording():
            state.trace._otel_span.set_attribute("user.id", sender_id)
            state.user_id = sender_id

        # Set user input on the root trace
        if user_message:
            state.trace.update(input=user_message)
    except Exception:
        pass


def _on_post_llm_call(
    session_id: str = "",
    assistant_response: str = "",
    user_message: str = "",
    **_: Any,
) -> None:
    """Capture assistant response as the trace output."""
    with _state_lock:
        state = _sessions.get(session_id)
    if not state or not state.trace:
        logger.info("langfuse: post_llm_call skipped — no trace for session_id=%s", session_id)
        return
    try:
        output = assistant_response or ""
        if len(output) > 8192:
            output = output[:8192] + "... [truncated]"
        state.trace.update(output=output)
        logger.info("langfuse: post_llm_call set output (%d chars) session_id=%s", len(output), session_id)
    except Exception as exc:
        logger.warning("langfuse: post_llm_call error: %s", exc)


def _on_session_end(
    session_id: str = "",
    completed: bool = True,
    interrupted: bool = False,
    model: str = "",
    platform: str = "",
    **_: Any,
) -> None:
    """End the root session span and flush."""
    state = _cleanup_session(session_id)
    if not state or not state.trace:
        return
    try:
        status = "interrupted" if interrupted else ("completed" if completed else "error")
        state.trace.update(
            metadata={
                "session_id": session_id,
                "user_id": state.user_id,
                "model": model,
                "platform": platform,
                "status": status,
                "completed": completed,
                "interrupted": interrupted,
            },
        )
        state.trace.end()
        logger.info("langfuse: trace ended session_id=%s status=%s", session_id, status)
    except Exception as exc:
        logger.warning("langfuse: on_session_end error: %s", exc)

    # Flush so traces appear in the dashboard promptly
    client = _get_client()
    if client:
        try:
            client.flush()
        except Exception:
            pass


def _on_session_finalize(session_id: str = "", **_: Any) -> None:
    """Flush the Langfuse client and clean up any leaked state."""
    # End any trace that wasn't properly closed
    state = _cleanup_session(session_id)
    if state and state.trace:
        try:
            state.trace.end()
        except Exception:
            pass

    client = _get_client()
    if client:
        try:
            client.flush()
        except Exception as exc:
            logger.debug("langfuse: flush error: %s", exc)


# -- API request hooks (LLM generations) -----------------------------------

def _on_pre_api_request(
    session_id: str = "",
    model: str = "",
    provider: str = "",
    api_call_count: int = 0,
    approx_input_tokens: int = 0,
    max_tokens: int = 0,
    message_count: int = 0,
    tool_count: int = 0,
    task_id: str = "",
    platform: str = "",
    messages: Optional[list] = None,
    **_: Any,
) -> None:
    """Start a nested generation observation for the LLM API call."""
    state = _ensure_trace(session_id, model, platform)
    if not state or not state.trace:
        return

    try:
        # Use actual messages as input if available
        gen_input: Any
        if messages:
            gen_input = messages
        else:
            gen_input = {"message_count": message_count, "tool_count": tool_count}

        gen = state.trace.start_observation(
            name=f"llm-call-{api_call_count}",
            as_type="generation",
            model=model,
            input=gen_input,
            metadata={
                "provider": provider,
                "api_call_count": api_call_count,
                "max_tokens": max_tokens,
                "task_id": task_id,
            },
            model_parameters={"max_tokens": max_tokens},
            usage_details={"input": approx_input_tokens},
        )
        gen_key = f"{session_id}:{api_call_count}"
        with _state_lock:
            state.generations[gen_key] = gen
    except Exception as exc:
        logger.warning("langfuse: pre_api_request error: %s", exc)


def _on_post_api_request(
    session_id: str = "",
    model: str = "",
    provider: str = "",
    api_duration: float = 0.0,
    finish_reason: str = "",
    usage: Optional[Dict[str, int]] = None,
    response_model: str = "",
    assistant_content_chars: int = 0,
    assistant_tool_call_count: int = 0,
    api_call_count: int = 0,
    assistant_text: str = "",
    assistant_tool_calls: Optional[list] = None,
    **_: Any,
) -> None:
    """End the current generation with usage metrics and actual output."""
    with _state_lock:
        state = _sessions.get(session_id)
    if not state:
        return

    gen_key = f"{session_id}:{api_call_count}"
    with _state_lock:
        gen = state.generations.pop(gen_key, None)
    if not gen:
        return

    try:
        usage_data = usage or {}
        level = "ERROR" if finish_reason == "error" else "DEFAULT"

        # Build actual output: text + tool calls
        gen_output: Any
        if assistant_text or assistant_tool_calls:
            gen_output = {}
            if assistant_text:
                gen_output["text"] = assistant_text
            if assistant_tool_calls:
                gen_output["tool_calls"] = assistant_tool_calls
            gen_output["finish_reason"] = finish_reason
        else:
            gen_output = {
                "finish_reason": finish_reason,
                "content_chars": assistant_content_chars,
                "tool_calls": assistant_tool_call_count,
            }

        gen.update(
            output=gen_output,
            metadata={
                "provider": provider,
                "response_model": response_model,
                "duration_s": api_duration,
            },
            level=level,
            usage_details={
                "input": usage_data.get("input_tokens", 0),
                "output": usage_data.get("output_tokens", 0),
            },
        )
        gen.end()
    except Exception as exc:
        logger.warning("langfuse: post_api_request error: %s", exc)


# -- Tool call hooks -------------------------------------------------------

def _on_pre_tool_call(
    tool_name: str = "",
    args: Optional[Dict[str, Any]] = None,
    session_id: str = "",
    task_id: str = "",
    tool_call_id: str = "",
    **_: Any,
) -> None:
    """Start a nested tool observation for a tool call."""
    state = _ensure_trace(session_id)
    if not state or not state.trace:
        return

    try:
        span_key = tool_call_id or f"{tool_name}:{time.monotonic()}"
        obs = state.trace.start_observation(
            name=f"tool:{tool_name}",
            as_type="tool",
            input=args or {},
            metadata={
                "tool_name": tool_name,
                "task_id": task_id,
                "tool_call_id": tool_call_id,
            },
        )
        with _state_lock:
            state.spans[span_key] = obs
            state.tool_keys[(tool_name, tool_call_id)] = span_key
    except Exception as exc:
        logger.warning("langfuse: pre_tool_call error: %s", exc)


def _on_post_tool_call(
    tool_name: str = "",
    args: Optional[Dict[str, Any]] = None,
    result: Any = None,
    session_id: str = "",
    task_id: str = "",
    tool_call_id: str = "",
    **_: Any,
) -> None:
    """End the tool observation with the result."""
    with _state_lock:
        state = _sessions.get(session_id)
    if not state:
        return

    lookup = (tool_name, tool_call_id)
    with _state_lock:
        span_key = state.tool_keys.pop(lookup, None)
        if not span_key:
            return
        obs = state.spans.pop(span_key, None)

    if not obs:
        return

    try:
        result_str = str(result) if result is not None else ""
        if len(result_str) > 4096:
            result_str = result_str[:4096] + "... [truncated]"

        obs.update(output=result_str)
        obs.end()
    except Exception as exc:
        logger.warning("langfuse: post_tool_call error: %s", exc)


# ---------------------------------------------------------------------------
# Plugin registration
# ---------------------------------------------------------------------------

def register(ctx) -> None:
    ctx.register_hook("on_session_start", _on_session_start)
    ctx.register_hook("pre_llm_call", _on_pre_llm_call)
    ctx.register_hook("post_llm_call", _on_post_llm_call)
    ctx.register_hook("on_session_end", _on_session_end)
    ctx.register_hook("on_session_finalize", _on_session_finalize)
    ctx.register_hook("pre_api_request", _on_pre_api_request)
    ctx.register_hook("post_api_request", _on_post_api_request)
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    logger.info("langfuse plugin: registered all hooks")
