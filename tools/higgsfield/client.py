"""Synchronous HTTP client for the FNF Higgsfield generation service.

Mirrors ``higgsfieldcli/internal/api/{client,jobs,media}.go``.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from .auth import HiggsfieldConfig, build_headers, load_config
from .errors import HiggsfieldAPIError

logger = logging.getLogger(__name__)


class HiggsfieldClient:
    def __init__(self, cfg: HiggsfieldConfig | None = None):
        self.cfg = cfg or load_config()
        self._http = httpx.Client(
            base_url=self.cfg.base_url,
            headers=build_headers(self.cfg),
            timeout=self.cfg.timeout_seconds,
        )

    def close(self) -> None:
        try:
            self._http.close()
        except Exception:  # pragma: no cover — defensive
            pass

    def __enter__(self) -> "HiggsfieldClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        del exc_type, exc_val, exc_tb
        self.close()

    # ------------------------------------------------------------------
    # Low-level
    # ------------------------------------------------------------------

    def _request(self, method: str, path: str, *, json: Any = None) -> Any:
        headers = {"Content-Type": "application/json"} if json is not None else None
        try:
            resp = self._http.request(method, path, json=json, headers=headers)
        except httpx.TimeoutException as exc:
            raise HiggsfieldAPIError(0, f"request timeout: {exc}", path=path) from exc
        except httpx.HTTPError as exc:
            raise HiggsfieldAPIError(0, f"network error: {exc}", path=path) from exc

        body_text = resp.text
        if resp.status_code < 200 or resp.status_code >= 300:
            raise HiggsfieldAPIError(resp.status_code, body_text, path=path)

        if not body_text:
            return None
        return resp.json()

    # ------------------------------------------------------------------
    # Endpoints used by generate + polling
    # ------------------------------------------------------------------

    def create_job(self, job_set_type: str, params: dict) -> dict:
        """POST /internal/claudesfield/create-job → {job_sets: [...]}"""
        logger.debug("create_job job_set_type=%s", job_set_type)
        return self._request(
            "POST",
            "/internal/claudesfield/create-job",
            json={"job_set_type": job_set_type, "params": params},
        )

    def get_job_status(self, job_id: str) -> dict:
        """GET /internal/claudesfield/jobs/{id}/status"""
        return self._request("GET", f"/internal/claudesfield/jobs/{job_id}/status")

    def get_job(self, job_id: str) -> dict:
        """GET /internal/claudesfield/jobs/{id}"""
        return self._request("GET", f"/internal/claudesfield/jobs/{job_id}")

    def get_input_image(self, image_id: str) -> dict:
        """GET /internal/claudesfield/input-images/{id}?result_type=web_optimized"""
        return self._request(
            "GET",
            f"/internal/claudesfield/input-images/{image_id}?result_type=web_optimized",
        )

    def get_balance(self) -> dict:
        """GET /internal/claudesfield/balance — used as a lightweight auth probe."""
        return self._request("GET", "/internal/claudesfield/balance")
