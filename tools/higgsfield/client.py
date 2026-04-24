"""Synchronous HTTP client for the FNF Higgsfield generation service.

Mirrors ``higgsfieldcli/internal/api/{client,jobs,media}.go``.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from .auth import HiggsfieldConfig, build_headers, derive_inspiration_url, load_config
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

    def trigger_job_ip_check(self, job_id: str) -> None:
        """POST /internal/claudesfield/jobs/{id}/ip-detect — fire the IP detector.

        Fire-and-forget; the result lands on the job status endpoint under
        ``ip_check_finished`` / ``ip_detected``. Mirrors Go's
        ``Client.TriggerJobIPCheck``.
        """
        self._request(
            "POST",
            f"/internal/claudesfield/jobs/{job_id}/ip-detect",
        )

    def list_elements(self, params: dict) -> dict:
        """GET /internal/claudesfield/reference-elements — list with filters.

        ``params`` keys: category, categories (comma-joined), filter,
        pinned (bool), ip_detected (bool), size (int), cursor (str).
        """
        from urllib.parse import urlencode

        query: dict[str, str] = {"size": str(int(params.get("size") or 20))}
        for key in ("category", "categories", "filter", "cursor"):
            val = params.get(key)
            if val:
                query[key] = str(val)
        for key in ("pinned", "ip_detected"):
            val = params.get(key)
            if val is not None:
                query[key] = "true" if bool(val) else "false"
        return self._request(
            "GET",
            f"/internal/claudesfield/reference-elements?{urlencode(query)}",
        )

    def get_element(self, element_id: str) -> dict:
        """GET /internal/claudesfield/reference-elements/{id}"""
        return self._request(
            "GET",
            f"/internal/claudesfield/reference-elements/{element_id}",
        )

    def create_element(self, body: dict) -> dict:
        """POST /internal/claudesfield/reference-elements — create new element."""
        return self._request(
            "POST",
            "/internal/claudesfield/reference-elements",
            json=body,
        )

    def inspiration(self, query: str, top_k: int = 5) -> dict:
        """POST <INSPIRATION_BASE_URL or derived>/rag — RAG search over design templates.

        The inspiration endpoint lives on a sibling service from FNF (different
        path, possibly different host), so this bypasses the client's base_url
        via a full-URL request. Auth headers (dev user / folder / JWT) are
        forwarded unchanged — same as Go's ``Client.Inspiration``.
        """
        endpoint = derive_inspiration_url(self.cfg)
        headers = {"Content-Type": "application/json", **build_headers(self.cfg)}
        try:
            resp = self._http.post(
                endpoint,
                json={"query": query, "top_k": top_k},
                headers=headers,
            )
        except httpx.TimeoutException as exc:
            raise HiggsfieldAPIError(0, f"request timeout: {exc}", path=endpoint) from exc
        except httpx.HTTPError as exc:
            raise HiggsfieldAPIError(0, f"network error: {exc}", path=endpoint) from exc

        if resp.status_code < 200 or resp.status_code >= 300:
            raise HiggsfieldAPIError(resp.status_code, resp.text, path=endpoint)
        if not resp.text:
            return {}
        return resp.json()

    def get_balance(self) -> dict:
        """GET /internal/claudesfield/balance — used as a lightweight auth probe."""
        return self._request("GET", "/internal/claudesfield/balance")
