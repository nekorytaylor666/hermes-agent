"""higgsfield_job_status — poll or fetch a single Higgsfield job.

Complements ``higgsfield_generate``: used to resume a job submitted with
``async=true``, or after a poll timeout. Mirrors ``higgsfieldcli status``.
"""

from __future__ import annotations

import logging

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


def higgsfield_job_status(args: dict, **_kw) -> str:
    job_id = args.get("job_id")
    if not job_id:
        return tool_error("\"job_id\" field is required")

    poll = bool(args.get("poll", True))
    interval = float(args.get("interval") or 5.0)
    timeout = float(args.get("timeout_seconds") or 900.0)

    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    try:
        with HiggsfieldClient(cfg) as client:
            if poll:
                try:
                    status = wait_for_job(
                        client, job_id, interval=interval, timeout=timeout
                    )
                except HiggsfieldTimeout as exc:
                    return tool_error(str(exc), job_id=job_id, status="timeout")
            else:
                status = client.get_job_status(job_id)

            current = status.get("status", "")
            if current in TERMINAL_STATUSES:
                return tool_result(terminal_result(client, status))

            # Non-terminal, not polling: return the raw status snapshot.
            return tool_result({
                "job_id": status.get("id", job_id),
                "status": current,
                "job_set_type": status.get("job_set_type", ""),
                "ip_check_finished": status.get("ip_check_finished", False),
                "ip_detected": status.get("ip_detected", False),
            })
    except HiggsfieldAPIError as exc:
        return tool_error(str(exc), status_code=exc.status_code, body=exc.body)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_job_status failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")


HIGGSFIELD_JOB_STATUS_SCHEMA = {
    "name": "higgsfield_job_status",
    "description": (
        "Check the status of a Higgsfield generation job. With poll=true (default) "
        "it blocks until the job reaches a terminal status (completed, canceled, "
        "failed, nsfw, ip_detected) or the timeout elapses. Use this to resume a "
        "job that was submitted with higgsfield_generate(async=true)."
    ),
    "parameters": {
        "type": "object",
        "required": ["job_id"],
        "properties": {
            "job_id": {"type": "string", "description": "Job ID returned from higgsfield_generate."},
            "poll": {"type": "boolean", "description": "When true (default), wait for terminal status."},
            "interval": {"type": "number", "description": "Seconds between status checks (default 5)."},
            "timeout_seconds": {"type": "number", "description": "Max seconds to wait (default 900)."},
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
    description="Poll a Higgsfield generation job to completion.",
    emoji="⏳",
)
