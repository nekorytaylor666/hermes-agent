"""Build the auth/config envelope from environment variables.

Mirrors ``higgsfieldcli/internal/config`` and the header set in
``higgsfieldcli/internal/api/client.go``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from .errors import HiggsfieldConfigError


@dataclass(frozen=True)
class HiggsfieldConfig:
    base_url: str
    folder_id: str
    jwt_token: str = ""
    dev_user_id: str = ""
    internal_api_key: str = ""
    timeout_seconds: float = 30.0
    environment: str = ""


def _parse_timeout(raw: str | None, default: float) -> float:
    if not raw:
        return default
    raw = raw.strip()
    if not raw:
        return default
    # Accept either "30" (seconds) or a Go-style duration like "30s", "1m", "2m30s".
    unit_mult = {"ms": 0.001, "s": 1.0, "m": 60.0, "h": 3600.0}
    # Plain number?
    try:
        return float(raw)
    except ValueError:
        pass
    # Walk suffixed components.
    total = 0.0
    i = 0
    while i < len(raw):
        j = i
        while j < len(raw) and (raw[j].isdigit() or raw[j] == "."):
            j += 1
        if j == i:
            raise ValueError(f"invalid FNF_TIMEOUT: {raw!r}")
        value = float(raw[i:j])
        k = j
        while k < len(raw) and raw[k].isalpha():
            k += 1
        unit = raw[j:k] or "s"
        if unit not in unit_mult:
            raise ValueError(f"invalid FNF_TIMEOUT unit: {unit!r}")
        total += value * unit_mult[unit]
        i = k
    return total


def load_config() -> HiggsfieldConfig:
    """Read the FNF config from env vars. Raises if required fields are missing."""
    base_url = os.environ.get("FNF_BASE_URL", "").rstrip("/")
    folder_id = os.environ.get("HF_FOLDER_ID", "")
    jwt_token = os.environ.get("HF_JWT_TOKEN", "")
    dev_user_id = os.environ.get("HF_DEV_USER_ID", "")
    internal_api_key = os.environ.get("HF_INTERNAL_API_KEY", "")
    environment = os.environ.get("ENVIRONMENT", "")

    missing = []
    if not base_url:
        missing.append("FNF_BASE_URL")
    if not folder_id:
        missing.append("HF_FOLDER_ID")
    # Dev path (ENVIRONMENT=dev + HF_DEV_USER_ID) OR prod path (HF_JWT_TOKEN).
    # HF_JWT_TOKEN is optional when the dev path is used.
    is_dev = environment.lower() == "dev"
    if is_dev:
        if not dev_user_id:
            missing.append("HF_DEV_USER_ID (ENVIRONMENT=dev)")
    elif not (jwt_token or dev_user_id):
        missing.append("HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)")
    if missing:
        raise HiggsfieldConfigError(missing)

    return HiggsfieldConfig(
        base_url=base_url,
        folder_id=folder_id,
        jwt_token=jwt_token,
        dev_user_id=dev_user_id,
        internal_api_key=internal_api_key,
        timeout_seconds=_parse_timeout(os.environ.get("FNF_TIMEOUT"), 30.0),
        environment=environment,
    )


def build_headers(cfg: HiggsfieldConfig) -> dict[str, str]:
    headers: dict[str, str] = {"Accept": "application/json"}
    if cfg.dev_user_id:
        headers["hf-dev-user-id"] = cfg.dev_user_id
    if cfg.folder_id:
        headers["hf-dev-folder-id"] = cfg.folder_id
    if cfg.jwt_token:
        headers["X-Claudesfield-Token"] = cfg.jwt_token
    if cfg.internal_api_key:
        headers["X-Higgsfield-Internal-Key"] = cfg.internal_api_key
    return headers


def config_is_available() -> bool:
    """True when the env is complete enough to construct a client."""
    try:
        load_config()
    except HiggsfieldConfigError:
        return False
    return True


def missing_env_vars() -> list[str]:
    try:
        load_config()
    except HiggsfieldConfigError as exc:
        return list(exc.missing)
    return []
