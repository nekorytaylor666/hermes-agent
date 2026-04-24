"""Vercel AI SDK ``UIMessageChunk`` builders.

Produces plain dicts matching the Zod schema in
``ai/packages/ai/src/ui-message-stream/ui-message-chunks.ts``.  Each dict
is serialised (``json.dumps``) and either XADD-ed to Redis under a single
``chunk`` field (Higgs transport) or written verbatim as ``data: <chunk>\\n\\n``
SSE frames (web UI).  ``useChat`` parses both flavours natively.

Kept intentionally close to ``fnf-higgsclaw-agent/src/ui_chunks.py`` so the
fnf consumer side stays source-compatible.  Schemas on the browser use
``z.strictObject``; unknown keys fail validation, so keep the keys exactly
as declared here.
"""

from __future__ import annotations

import secrets
from typing import Any, Literal


FinishReason = Literal[
    "stop", "length", "content-filter", "tool-calls", "error", "other",
]

# Scopes ``providerMetadata`` so downstream consumers can detect where a
# chunk originated.  Set to "hermes" for this fork; set to whichever string
# your frontend routes on.
PROVIDER_KEY = "hermes"


def new_id() -> str:
    """Fresh 16-char hex id for text/reasoning blocks."""
    return secrets.token_hex(8)


# ── Lifecycle ──────────────────────────────────────────────────────────────

def start(
    message_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "start"}
    if message_id is not None:
        chunk["messageId"] = message_id
    if metadata is not None:
        chunk["messageMetadata"] = metadata
    return chunk


def start_step() -> dict[str, Any]:
    return {"type": "start-step"}


def finish_step() -> dict[str, Any]:
    return {"type": "finish-step"}


def finish(
    reason: FinishReason = "stop",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "finish", "finishReason": reason}
    if metadata is not None:
        chunk["messageMetadata"] = metadata
    return chunk


def abort(reason: str | None = None) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "abort"}
    if reason is not None:
        chunk["reason"] = reason
    return chunk


def error(error_text: str) -> dict[str, Any]:
    return {"type": "error", "errorText": error_text}


def message_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    return {"type": "message-metadata", "messageMetadata": metadata}


# ── Text ───────────────────────────────────────────────────────────────────

def text_start(
    text_id: str,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "text-start", "id": text_id}
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    return chunk


def text_delta(
    text_id: str,
    delta: str,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "text-delta", "id": text_id, "delta": delta}
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    return chunk


def text_end(
    text_id: str,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "text-end", "id": text_id}
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    return chunk


def text_block(
    content: str,
    provider_metadata: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Emit a full text block as start/delta/end triple."""
    tid = new_id()
    return [
        text_start(tid, provider_metadata),
        text_delta(tid, content),
        text_end(tid),
    ]


# ── Reasoning ──────────────────────────────────────────────────────────────

def reasoning_start(
    reasoning_id: str,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "reasoning-start", "id": reasoning_id}
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    return chunk


def reasoning_delta(
    reasoning_id: str,
    delta: str,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "reasoning-delta", "id": reasoning_id, "delta": delta,
    }
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    return chunk


def reasoning_end(
    reasoning_id: str,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {"type": "reasoning-end", "id": reasoning_id}
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    return chunk


def reasoning_block(
    content: str,
    provider_metadata: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    rid = new_id()
    return [
        reasoning_start(rid, provider_metadata),
        reasoning_delta(rid, content),
        reasoning_end(rid),
    ]


# ── Tool calls ─────────────────────────────────────────────────────────────

def tool_input_start(
    tool_call_id: str,
    tool_name: str,
    *,
    dynamic: bool = True,
    provider_executed: bool | None = None,
    provider_metadata: dict[str, Any] | None = None,
    title: str | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "tool-input-start",
        "toolCallId": tool_call_id,
        "toolName": tool_name,
        "dynamic": dynamic,
    }
    if provider_executed is not None:
        chunk["providerExecuted"] = provider_executed
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    if title is not None:
        chunk["title"] = title
    return chunk


def tool_input_available(
    tool_call_id: str,
    tool_name: str,
    tool_input: Any,
    *,
    dynamic: bool = True,
    provider_executed: bool | None = None,
    provider_metadata: dict[str, Any] | None = None,
    title: str | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "tool-input-available",
        "toolCallId": tool_call_id,
        "toolName": tool_name,
        "input": tool_input,
        "dynamic": dynamic,
    }
    if provider_executed is not None:
        chunk["providerExecuted"] = provider_executed
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    if title is not None:
        chunk["title"] = title
    return chunk


def tool_output_available(
    tool_call_id: str,
    output: Any,
    *,
    tool_name: str | None = None,
    dynamic: bool = True,
    provider_executed: bool | None = None,
    provider_metadata: dict[str, Any] | None = None,
    call_provider_metadata: dict[str, Any] | None = None,
    approval: dict[str, Any] | None = None,
    preliminary: bool | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "tool-output-available",
        "toolCallId": tool_call_id,
        "output": output,
        "dynamic": dynamic,
    }
    if tool_name is not None:
        chunk["toolName"] = tool_name
    if provider_executed is not None:
        chunk["providerExecuted"] = provider_executed
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    if call_provider_metadata is not None:
        chunk["callProviderMetadata"] = call_provider_metadata
    if approval is not None:
        chunk["approval"] = approval
    if preliminary is not None:
        chunk["preliminary"] = preliminary
    return chunk


def tool_output_error(
    tool_call_id: str,
    error_text: str,
    *,
    tool_name: str | None = None,
    dynamic: bool = True,
    provider_executed: bool | None = None,
    provider_metadata: dict[str, Any] | None = None,
    call_provider_metadata: dict[str, Any] | None = None,
    approval: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "tool-output-error",
        "toolCallId": tool_call_id,
        "errorText": error_text,
        "dynamic": dynamic,
    }
    if tool_name is not None:
        chunk["toolName"] = tool_name
    if provider_executed is not None:
        chunk["providerExecuted"] = provider_executed
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    if call_provider_metadata is not None:
        chunk["callProviderMetadata"] = call_provider_metadata
    if approval is not None:
        chunk["approval"] = approval
    return chunk


def tool_approval_request(
    approval_id: str,
    tool_call_id: str,
    *,
    tool_name: str | None = None,
    dynamic: bool = True,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "tool-approval-request",
        "approvalId": approval_id,
        "toolCallId": tool_call_id,
        "dynamic": dynamic,
    }
    if tool_name is not None:
        chunk["toolName"] = tool_name
    if provider_metadata is not None:
        chunk["providerMetadata"] = provider_metadata
    return chunk


def tool_approval_response(
    approval_id: str,
    tool_call_id: str,
    approved: bool,
    *,
    tool_name: str | None = None,
    dynamic: bool = True,
    reason: str | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "tool-approval-response",
        "approvalId": approval_id,
        "toolCallId": tool_call_id,
        "approved": approved,
        "dynamic": dynamic,
    }
    if tool_name is not None:
        chunk["toolName"] = tool_name
    if reason is not None:
        chunk["reason"] = reason
    return chunk


def tool_output_denied(
    tool_call_id: str,
    *,
    tool_name: str | None = None,
) -> dict[str, Any]:
    chunk: dict[str, Any] = {
        "type": "tool-output-denied", "toolCallId": tool_call_id,
    }
    if tool_name is not None:
        chunk["toolName"] = tool_name
    return chunk


# ── Custom / data parts ────────────────────────────────────────────────────

def data_part(
    name: str,
    data: Any,
    *,
    part_id: str | None = None,
    transient: bool = False,
) -> dict[str, Any]:
    """Emit a ``data-<name>`` UI message chunk.

    ``name`` is kebab-case without the ``data-`` prefix (e.g. ``"task-started"``).
    Used for application-specific state that useChat relays to consumers
    via UI data parts.
    """
    chunk: dict[str, Any] = {"type": f"data-{name}", "data": data}
    if part_id is not None:
        chunk["id"] = part_id
    if transient:
        chunk["transient"] = True
    return chunk


def provider_meta(**kwargs: Any) -> dict[str, Any] | None:
    """Shorthand for ``providerMetadata`` scoped under :data:`PROVIDER_KEY`.

    Returns ``None`` when every kwarg is ``None`` so callers can pass the
    result straight through to builders without generating empty
    ``providerMetadata: {}`` entries.
    """
    cleaned = {k: v for k, v in kwargs.items() if v is not None}
    return {PROVIDER_KEY: cleaned} if cleaned else None
