"""Job polling helpers."""

from __future__ import annotations

import logging
import time
from typing import Any

from .client import HiggsfieldClient
from .errors import HiggsfieldTimeout

logger = logging.getLogger(__name__)

TERMINAL_STATUSES = {"completed", "canceled", "failed", "nsfw", "ip_detected"}


def wait_for_job(
    client: HiggsfieldClient,
    job_id: str,
    *,
    interval: float = 5.0,
    timeout: float = 900.0,
) -> dict:
    """Poll ``job_id`` until it reaches a terminal status or ``timeout`` elapses."""
    started = time.monotonic()
    while True:
        status = client.get_job_status(job_id)
        current = status.get("status", "")
        logger.debug("poll job_id=%s status=%s", job_id, current)
        if current in TERMINAL_STATUSES:
            return status
        elapsed = time.monotonic() - started
        if elapsed >= timeout:
            raise HiggsfieldTimeout(job_id, elapsed)
        time.sleep(max(0.5, interval))


def wait_for_ip_check(
    client: HiggsfieldClient,
    job_id: str,
    *,
    interval: float = 5.0,
    timeout: float = 120.0,
) -> dict:
    """Poll job status until ``ip_check_finished`` is True or timeout.

    Mirrors Go's ``pollJobIPCheck``. Separate from ``wait_for_job`` because
    the exit condition is different — we're waiting for the IP detector to
    finish, not for the main job to reach a terminal status.
    """
    started = time.monotonic()
    while True:
        status = client.get_job_status(job_id)
        logger.debug(
            "poll ip_check job_id=%s status=%s ip_finished=%s ip_detected=%s",
            job_id,
            status.get("status", ""),
            status.get("ip_check_finished", False),
            status.get("ip_detected", False),
        )
        if bool(status.get("ip_check_finished")):
            return status
        elapsed = time.monotonic() - started
        if elapsed >= timeout:
            raise HiggsfieldTimeout(job_id, elapsed)
        time.sleep(max(0.5, interval))


def terminal_result(client: HiggsfieldClient, status_payload: dict) -> dict:
    """For a terminal job status, fetch the detail and extract a compact result."""
    job_id = status_payload.get("id", "")
    current = status_payload.get("status", "")
    out: dict[str, Any] = {
        "job_id": job_id,
        "status": current,
        "job_set_type": status_payload.get("job_set_type", ""),
        "ip_check_finished": status_payload.get("ip_check_finished", False),
        "ip_detected": status_payload.get("ip_detected", False),
    }

    try:
        detail = client.get_job(job_id)
    except Exception as exc:  # pragma: no cover — defensive
        logger.debug("failed to fetch job detail for %s: %s", job_id, exc)
        return out

    out["job_set_id"] = detail.get("job_set_id", "")
    if current != "completed":
        return out

    results = detail.get("results") or {}
    raw = results.get("raw") if isinstance(results, dict) else None
    minimal = results.get("min") if isinstance(results, dict) else None
    if raw:
        out["result"] = {"type": raw.get("type", ""), "url": raw.get("url", "")}
    elif detail.get("result"):
        out["result"] = {
            "type": detail["result"].get("type", ""),
            "url": detail["result"].get("url", ""),
        }
    if minimal:
        out["preview"] = {"type": minimal.get("type", ""), "url": minimal.get("url", "")}
    return out
