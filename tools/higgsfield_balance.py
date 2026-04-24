"""higgsfield_balance — read workspace credit balance.

Port of ``higgsfieldcli balance``. Returns ``{balance: {credits_balance,
subscription_balance}, pricing: {...}}``. Doubles as a lightweight
end-to-end auth probe — if this returns 200 the env vars + token are good.
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
)
from tools.registry import registry, tool_error, tool_result

logger = logging.getLogger(__name__)


def higgsfield_balance(args: dict, **_kw) -> str:
    del args  # no parameters
    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    try:
        with HiggsfieldClient(cfg) as client:
            response = client.get_balance()
    except HiggsfieldAPIError as exc:
        return tool_error(str(exc), status_code=exc.status_code, body=exc.body)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_balance failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")

    if not isinstance(response, dict):
        return tool_result({"response": response})
    return tool_result(response)


HIGGSFIELD_BALANCE_SCHEMA: dict = {
    "name": "higgsfield_balance",
    "description": (
        "Read the current Higgsfield workspace balance. Returns "
        "{balance: {credits_balance, subscription_balance}, pricing: {...}}. "
        "No parameters. Also useful as a quick connectivity / auth sanity "
        "check before kicking off a batch of generations."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


def _check_available() -> bool:
    if not config_is_available():
        logger.debug("higgsfield toolset unavailable: %s", missing_env_vars())
        return False
    return True


registry.register(
    name="higgsfield_balance",
    toolset="higgsfield",
    schema=HIGGSFIELD_BALANCE_SCHEMA,
    handler=higgsfield_balance,
    check_fn=_check_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="Show Higgsfield workspace balance + pricing.",
    emoji="💳",
)
