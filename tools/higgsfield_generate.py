"""higgsfield_generate — submit Higgsfield FNF generation job(s).

Native Python port of ``higgsfieldcli generate --json``. Talks directly to
``FNF_BASE_URL`` via HTTP using the auth headers defined in
``higgsfieldcli/internal/api/client.go``.

**Always batch-shaped.** The tool takes ``requests: [ {model, ...}, ... ]``
even for a single image. Submissions fan out across a thread pool
(``concurrency`` workers, default 8). Non-blocking by default — returns job
IDs within seconds so the chat stays responsive. Caller passes
``async=false`` only when they genuinely want the result inline.

Poll later via ``higgsfield_job_status`` with the returned ``job_ids``.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from tools.higgsfield.auth import (
    config_is_available,
    load_config,
    missing_env_vars,
)
from tools.higgsfield.builders import BUILDERS, supported_models
from tools.higgsfield.client import HiggsfieldClient
from tools.higgsfield.errors import (
    HiggsfieldAPIError,
    HiggsfieldConfigError,
    HiggsfieldError,
    HiggsfieldTimeout,
)
from tools.higgsfield.polling import terminal_result, wait_for_job
from tools.registry import registry, tool_error, tool_result

logger = logging.getLogger(__name__)

DEFAULT_CONCURRENCY = 8


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------


def _submit_one(
    client: HiggsfieldClient,
    request: dict,
    *,
    folder_id: str,
) -> dict:
    """Build params + call create-job. Returns the first job_set on success."""
    model = request.get("model")
    if not model:
        raise ValueError("\"model\" field is required")
    if model not in BUILDERS:
        raise ValueError(
            f"unknown model {model!r}; supported: {', '.join(supported_models())}"
        )
    job_set_type, builder = BUILDERS[model]
    params = builder(
        request,
        client=client,
        folder_id=request.get("folder_id") or folder_id,
    )
    resp = client.create_job(job_set_type, params)
    if not isinstance(resp, dict) or not resp.get("job_sets"):
        raise ValueError(f"unexpected create-job response: {resp!r}")
    js = resp["job_sets"][0]
    return {
        "job_set_id": js.get("job_set_id", ""),
        "job_set_type": js.get("job_set_type", job_set_type),
        "job_ids": list(js.get("job_ids") or []),
    }


def _poll_one(
    client: HiggsfieldClient,
    job_id: str,
    *,
    interval: float,
    timeout: float,
) -> dict:
    try:
        status = wait_for_job(client, job_id, interval=interval, timeout=timeout)
    except HiggsfieldTimeout as exc:
        return {"job_id": job_id, "status": "timeout", "error": str(exc)}
    return terminal_result(client, status)


def _poll_many(
    client: HiggsfieldClient,
    job_ids: list[str],
    *,
    interval: float,
    timeout: float,
    concurrency: int,
) -> list[dict]:
    if not job_ids:
        return []
    workers = max(1, min(concurrency, len(job_ids)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(
            pool.map(
                lambda jid: _poll_one(client, jid, interval=interval, timeout=timeout),
                job_ids,
            )
        )


# ---------------------------------------------------------------------------
# Batch (the only mode)
# ---------------------------------------------------------------------------


def _run_batch(
    client: HiggsfieldClient,
    requests: list[dict],
    *,
    folder_id: str,
    async_submit: bool,
    interval: float,
    timeout: float,
    concurrency: int,
) -> dict[str, Any]:
    workers = max(1, min(concurrency, len(requests)))

    def _submit(idx_req):
        idx, req = idx_req
        if not isinstance(req, dict):
            return {"index": idx, "error": f"requests[{idx}]: expected object"}
        try:
            sub = _submit_one(client, req, folder_id=folder_id)
        except ValueError as exc:
            return {"index": idx, "error": str(exc)}
        except HiggsfieldAPIError as exc:
            return {
                "index": idx,
                "error": str(exc),
                "status_code": exc.status_code,
            }
        except Exception as exc:  # pragma: no cover — defensive
            logger.exception("batch submit[%d] failed", idx)
            return {"index": idx, "error": f"{type(exc).__name__}: {exc}"}
        sub["index"] = idx
        sub["status"] = "created"
        return sub

    with ThreadPoolExecutor(max_workers=workers) as pool:
        submissions = list(pool.map(_submit, enumerate(requests)))

    # Flatten into a simple {job_ids: [...]}; per-item errors go in a separate
    # list only when something failed. Keeps the tool output tight so the LLM
    # sees one obvious field to hand to higgsfield_job_status later.
    job_ids: list[str] = []
    errors: list[dict] = []
    for sub in submissions:
        if "error" in sub:
            errors.append({"index": sub.get("index"), "error": sub["error"]})
            continue
        for jid in sub.get("job_ids") or []:
            job_ids.append(jid)

    if async_submit:
        payload: dict[str, Any] = {"job_ids": job_ids}
        if errors:
            payload["errors"] = errors
        return payload

    # Blocking: poll every submitted job_id concurrently, emit {job_ids, results}.
    poll_workers = max(1, min(concurrency, max(1, len(job_ids))))
    results = _poll_many(
        client,
        job_ids,
        interval=interval,
        timeout=timeout,
        concurrency=poll_workers,
    )
    payload = {"job_ids": job_ids, "results": results}
    if errors:
        payload["errors"] = errors
    return payload


# ---------------------------------------------------------------------------
# Tool handler
# ---------------------------------------------------------------------------


def higgsfield_generate(args: dict, **_kw) -> str:
    requests = args.get("requests")
    if not isinstance(requests, list):
        return tool_error(
            "\"requests\" must be an array of request objects; "
            "wrap even a single image like {\"requests\": [ {\"model\": ..., ...} ]}"
        )
    if not requests:
        return tool_error("\"requests\" must be a non-empty array")

    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    folder_id = args.get("folder_id") or cfg.folder_id
    # Default async=true: submit + return immediately so the chat stays
    # responsive. Caller must explicitly pass async=false to block.
    async_arg = args.get("async")
    if async_arg is None:
        async_arg = args.get("async_submit")
    async_submit = True if async_arg is None else bool(async_arg)
    interval = float(args.get("poll_interval") or 5.0)
    timeout = float(args.get("timeout_seconds") or 900.0)
    concurrency = int(args.get("concurrency") or DEFAULT_CONCURRENCY)
    concurrency = max(1, min(concurrency, 32))

    try:
        with HiggsfieldClient(cfg) as client:
            payload = _run_batch(
                client,
                requests,
                folder_id=folder_id,
                async_submit=async_submit,
                interval=interval,
                timeout=timeout,
                concurrency=concurrency,
            )
            return tool_result(payload)
    except HiggsfieldAPIError as exc:
        return tool_error(str(exc), status_code=exc.status_code, body=exc.body)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_generate failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
#
# Per-item properties live inside ``requests[i]`` — the only top-level fields
# are ``requests`` + batch/polling controls. This prevents the LLM from
# sprinkling empty defaults (``style_input_image: {}``, ``reference_input_images: []``,
# etc.) into the top-level tool call when generating a single image.

_ITEM_PROPERTIES: dict[str, Any] = {
    "model": {
        "type": "string",
        "enum": supported_models(),
        "description": "Which generator to run. Routes to the model-specific request builder.",
    },
    "prompt": {"type": "string"},
    "aspect_ratio": {"type": "string"},
    "quality": {"type": "string"},
    "resolution": {"type": "string"},
    "batch_size": {"type": "integer"},
    "seed": {"type": "integer"},
    "duration": {"type": "integer"},
    "width": {"type": "integer"},
    "height": {"type": "integer"},
    "medias": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["data"],
            "properties": {
                "role": {"type": "string"},
                "data": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "url": {"type": "string"},
                    },
                },
            },
        },
    },
    "images": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["id"],
            "properties": {
                "id": {"type": "string"},
                "type": {"type": "string"},
                "url": {"type": "string"},
            },
        },
    },
    "sub_model": {"type": "string"},
    "mode": {"type": "string"},
    "style_id": {"type": "string"},
    "style_strength": {"type": "number"},
    "soul_id": {"type": "string"},
    "soul_strength": {"type": "number"},
    "negative_prompt": {"type": "string"},
    "enhance_prompt": {"type": "boolean"},
    "model_version": {"type": "string"},
    "character_params": {"type": "object"},
    "preset_id": {"type": "string"},
    "generate_audio": {"type": "boolean"},
    "use_eye_mask": {"type": "boolean"},
    "fixed_lens": {"type": "boolean"},
    "sound": {},
    "cfg_scale": {"type": "number"},
    "multi_shots": {"type": "boolean"},
    "multi_prompt": {"type": "array", "items": {"type": "string"}},
    "multi_shot_mode": {"type": "string"},
    "kling_element_ids": {"type": "array", "items": {"type": "string"}},
    "motion_id": {"type": "string"},
    "scene_cut": {"type": "boolean"},
    "genre": {"type": "string"},
    "speedramp": {"type": "boolean"},
    "steps": {"type": "integer"},
    "cfg": {"type": "number"},
    "is_draw": {"type": "boolean"},
    "is_ugc": {"type": "boolean"},
    "is_product_placement": {"type": "boolean"},
    "is_photo_set": {"type": "boolean"},
    "fashion_factory_id": {"type": "string"},
    "input_image": {"type": "object"},
    "input_image_end": {"type": "object"},
    "draw_input_image": {"type": "object"},
    "end_input_image": {"type": "object"},
    "style_input_image": {"type": "object"},
    "reference_input_images": {"type": "array", "items": {"type": "object"}},
    "input_audio": {"type": "object"},
    "input_videos": {"type": "array", "items": {"type": "object"}},
    "folder_id": {"type": "string"},
    "tool_use_id": {"type": "string"},
}


HIGGSFIELD_GENERATE_SCHEMA = {
    "name": "higgsfield_generate",
    "description": (
        "Submit Higgsfield FNF generation job(s). **Always batch-shaped** — "
        "pass requests as an array, even for a single image: "
        "{\"requests\": [{\"model\": ..., \"prompt\": ...}]}. "
        "All items submit in parallel (concurrency, default 8). "
        "**Non-blocking by default** — returns job IDs within a few seconds so "
        "the chat stays responsive. After submitting, announce 'generation "
        "started' with the job IDs; only call higgsfield_job_status(job_ids=[...]) "
        "when the user asks for the result. "
        "Pass async=false ONLY when the caller explicitly wants the URL inline "
        "and is willing to wait (blocks up to timeout_seconds, default 900). "
        "Supported models: "
        + ", ".join(supported_models())
        + ". Media/image IDs must be pre-existing (upload flow is not exposed as a tool). "
        "Do NOT pass empty defaults for optional fields — omit them."
    ),
    "parameters": {
        "type": "object",
        "required": ["requests"],
        "properties": {
            "requests": {
                "type": "array",
                "minItems": 1,
                "description": "Array of generation requests. One item per image/video. Each item must include 'model' and the model-specific fields (see builders.py).",
                "items": {
                    "type": "object",
                    "required": ["model"],
                    "properties": _ITEM_PROPERTIES,
                },
            },
            "concurrency": {
                "type": "integer",
                "description": "Max parallel submissions / poll workers (default 8, capped at 32).",
            },
            "async": {
                "type": "boolean",
                "description": "DEFAULT true — return job IDs immediately. Pass false only when the caller wants the tool to block and return the finished result URL inline.",
            },
            "poll_interval": {"type": "number"},
            "timeout_seconds": {"type": "number"},
        },
    },
}


def _check_higgsfield_available() -> bool:
    if not config_is_available():
        logger.debug("higgsfield toolset unavailable: %s", missing_env_vars())
        return False
    return True


registry.register(
    name="higgsfield_generate",
    toolset="higgsfield",
    schema=HIGGSFIELD_GENERATE_SCHEMA,
    handler=higgsfield_generate,
    check_fn=_check_higgsfield_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="Submit Higgsfield generation job(s); always batch-shaped.",
    emoji="🎨",
)
