"""higgsfield_ip_check — retroactive IP detection on Higgsfield jobs.

Port of ``higgsfieldcli job-ip-check``. Triggers the FNF IP detector on
completed jobs, polls until each check finishes, and returns structured
``{job_ids, results}`` with ``ip_detected`` per job.

Use when you need to confirm a generation is IP-clean before publishing
(e.g. commercial use). The ``ip_detected`` status that comes back inline
from ``higgsfield_generate`` is only flagged when the *generator* itself
detects IP — this tool runs a separate IP model.
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
from tools.higgsfield.polling import wait_for_ip_check
from tools.registry import registry, tool_error, tool_result

logger = logging.getLogger(__name__)

DEFAULT_CONCURRENCY = 8
DEFAULT_TIMEOUT = 120.0  # seconds, matches Go CLI default


def _trigger_and_check(
    client: HiggsfieldClient,
    job_id: str,
    *,
    poll: bool,
    interval: float,
    timeout: float,
) -> dict:
    """Fire the IP detector; optionally poll until finished. Returns a row."""
    try:
        client.trigger_job_ip_check(job_id)
    except HiggsfieldAPIError as exc:
        return {
            "job_id": job_id,
            "triggered": False,
            "error": str(exc),
            "status_code": exc.status_code,
        }
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("trigger_job_ip_check(%s) failed", job_id)
        return {"job_id": job_id, "triggered": False, "error": str(exc)}

    if not poll:
        return {"job_id": job_id, "triggered": True}

    try:
        status = wait_for_ip_check(
            client, job_id, interval=interval, timeout=timeout,
        )
    except HiggsfieldTimeout as exc:
        return {
            "job_id": job_id,
            "triggered": True,
            "ip_check_finished": False,
            "error": str(exc),
        }
    except HiggsfieldAPIError as exc:
        return {
            "job_id": job_id,
            "triggered": True,
            "error": str(exc),
            "status_code": exc.status_code,
        }
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("wait_for_ip_check(%s) failed", job_id)
        return {"job_id": job_id, "triggered": True, "error": str(exc)}

    return {
        "job_id": status.get("id", job_id),
        "triggered": True,
        "ip_check_finished": bool(status.get("ip_check_finished", False)),
        "ip_detected": bool(status.get("ip_detected", False)),
        "status": status.get("status", ""),
    }


def higgsfield_ip_check(args: dict, **_kw) -> str:
    job_ids_raw = args.get("job_ids")
    if not isinstance(job_ids_raw, list):
        return tool_error(
            "\"job_ids\" must be an array of job IDs; "
            "wrap even a single job like {\"job_ids\": [\"...\"]}"
        )
    job_ids = [str(j) for j in job_ids_raw if j]
    if not job_ids:
        return tool_error("\"job_ids\" must be a non-empty array")

    poll = bool(args.get("poll", True))
    interval = float(args.get("interval") or args.get("poll_interval") or 5.0)
    timeout = float(args.get("timeout_seconds") or DEFAULT_TIMEOUT)
    concurrency = int(args.get("concurrency") or DEFAULT_CONCURRENCY)
    concurrency = max(1, min(concurrency, 32))

    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    try:
        with HiggsfieldClient(cfg) as client:
            workers = max(1, min(concurrency, len(job_ids)))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                results = list(
                    pool.map(
                        lambda jid: _trigger_and_check(
                            client, jid,
                            poll=poll, interval=interval, timeout=timeout,
                        ),
                        job_ids,
                    )
                )
            payload: dict[str, Any] = {"job_ids": job_ids, "results": results}
            errors = [
                {"index": i, "error": r["error"]}
                for i, r in enumerate(results)
                if not r.get("triggered") and "error" in r
            ]
            if errors:
                payload["errors"] = errors
            return tool_result(payload)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_ip_check failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")


HIGGSFIELD_IP_CHECK_SCHEMA: dict[str, Any] = {
    "name": "higgsfield_ip_check",
    "description": (
        "Retroactively run IP/copyright detection on one or more completed "
        "Higgsfield jobs. Triggers the FNF IP detector, optionally polls "
        "until each check finishes, and returns {job_ids, results} with "
        "per-job {ip_check_finished, ip_detected}. Use after a generation "
        "completes to confirm it is IP-clean before publishing. "
        "**Always batch-shaped** — pass job_ids as an array even for one job. "
        "Non-blocking available via poll=false (returns {triggered: true} "
        "right after firing). Default polls up to 120s per job."
    ),
    "parameters": {
        "type": "object",
        "required": ["job_ids"],
        "properties": {
            "job_ids": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string"},
                "description": "Job IDs returned by higgsfield_generate.",
            },
            "poll": {
                "type": "boolean",
                "description": "Default true — wait for ip_check_finished before returning. Pass false to trigger and exit immediately.",
            },
            "interval": {
                "type": "number",
                "description": "Seconds between status checks (default 5).",
            },
            "timeout_seconds": {
                "type": "number",
                "description": "Max seconds to wait per job (default 120).",
            },
            "concurrency": {
                "type": "integer",
                "description": "Max parallel triggers / poll workers (default 8, cap 32).",
            },
        },
    },
}


def _check_available() -> bool:
    if not config_is_available():
        logger.debug("higgsfield toolset unavailable: %s", missing_env_vars())
        return False
    return True


registry.register(
    name="higgsfield_ip_check",
    toolset="higgsfield",
    schema=HIGGSFIELD_IP_CHECK_SCHEMA,
    handler=higgsfield_ip_check,
    check_fn=_check_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="Run IP/copyright detection on completed Higgsfield jobs.",
    emoji="🛡️",
)
