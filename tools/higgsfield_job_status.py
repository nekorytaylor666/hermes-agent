"""higgsfield_job_status — poll or fetch Higgsfield job(s).

Complements ``higgsfield_generate``: used to resume jobs submitted with
``async=true``, or after a poll timeout. Accepts a single ``job_id`` or a
batch via ``job_ids: [...]`` (polled concurrently).
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
from tools.higgsfield.client import HiggsfieldClient
from tools.higgsfield.errors import (
    HiggsfieldAPIError,
    HiggsfieldConfigError,
    HiggsfieldError,
    HiggsfieldTimeout,
)
from tools.higgsfield.polling import TERMINAL_STATUSES, terminal_result, wait_for_job
from tools.registry import registry, tool_error, tool_result

logger = logging.getLogger(__name__)

DEFAULT_CONCURRENCY = 8


def _fetch_one(
    client: HiggsfieldClient,
    job_id: str,
    *,
    poll: bool,
    interval: float,
    timeout: float,
) -> dict:
    try:
        if poll:
            status = wait_for_job(client, job_id, interval=interval, timeout=timeout)
        else:
            status = client.get_job_status(job_id)
    except HiggsfieldTimeout as exc:
        return {"job_id": job_id, "status": "timeout", "error": str(exc)}
    except HiggsfieldAPIError as exc:
        return {
            "job_id": job_id,
            "status": "error",
            "error": str(exc),
            "status_code": exc.status_code,
        }
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("fetch job %s failed", job_id)
        return {"job_id": job_id, "status": "error", "error": str(exc)}

    current = status.get("status", "")
    if current in TERMINAL_STATUSES:
        return terminal_result(client, status)
    return {
        "job_id": status.get("id", job_id),
        "status": current,
        "job_set_type": status.get("job_set_type", ""),
        "ip_check_finished": status.get("ip_check_finished", False),
        "ip_detected": status.get("ip_detected", False),
    }


def higgsfield_job_status(args: dict, **_kw) -> str:
    single = args.get("job_id")
    batch = args.get("job_ids")

    if batch is None and not single:
        return tool_error("either \"job_id\" or \"job_ids\" is required")
    if batch is not None and not isinstance(batch, list):
        return tool_error("\"job_ids\" must be an array")

    poll = bool(args.get("poll", True))
    interval = float(args.get("interval") or args.get("poll_interval") or 5.0)
    timeout = float(args.get("timeout_seconds") or 900.0)
    concurrency = int(args.get("concurrency") or DEFAULT_CONCURRENCY)
    concurrency = max(1, min(concurrency, 32))

    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    try:
        with HiggsfieldClient(cfg) as client:
            if batch is not None:
                job_ids = [str(j) for j in batch if j]
                if not job_ids:
                    return tool_error("\"job_ids\" must be a non-empty array")
                workers = max(1, min(concurrency, len(job_ids)))
                with ThreadPoolExecutor(max_workers=workers) as pool:
                    results = list(
                        pool.map(
                            lambda jid: _fetch_one(
                                client, jid,
                                poll=poll, interval=interval, timeout=timeout,
                            ),
                            job_ids,
                        )
                    )
                return tool_result({"results": results})

            # Single
            result = _fetch_one(
                client, str(single),
                poll=poll, interval=interval, timeout=timeout,
            )
            return tool_result(result)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_job_status failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")


HIGGSFIELD_JOB_STATUS_SCHEMA: dict[str, Any] = {
    "name": "higgsfield_job_status",
    "description": (
        "Check the status of Higgsfield generation job(s). Single mode: pass "
        "'job_id'. Batch mode: pass 'job_ids: [...]' — all polled concurrently. "
        "With poll=true (default), waits for each job to reach a terminal "
        "status (completed, canceled, failed, nsfw, ip_detected) or timeout. "
        "Use this to resume jobs submitted with higgsfield_generate(async=true)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "job_id": {"type": "string", "description": "Single job ID to check."},
            "job_ids": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Batch of job IDs to poll concurrently.",
            },
            "poll": {"type": "boolean", "description": "Wait for terminal status (default true)."},
            "interval": {"type": "number", "description": "Seconds between status checks (default 5)."},
            "timeout_seconds": {"type": "number", "description": "Max seconds to wait per job (default 900)."},
            "concurrency": {"type": "integer", "description": "Max parallel poll workers in batch mode (default 8, cap 32)."},
        },
    },
}


def _check_available() -> bool:
    if not config_is_available():
        logger.debug("higgsfield toolset unavailable: %s", missing_env_vars())
        return False
    return True


registry.register(
    name="higgsfield_job_status",
    toolset="higgsfield",
    schema=HIGGSFIELD_JOB_STATUS_SCHEMA,
    handler=higgsfield_job_status,
    check_fn=_check_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="Poll Higgsfield generation job(s); supports concurrent batch polling.",
    emoji="⏳",
)
