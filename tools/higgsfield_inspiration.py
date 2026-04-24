"""higgsfield_inspiration — search Higgsfield's design-template index.

Port of ``higgsfieldcli inspiration``. Hits the inspiration service with a
keyword query and returns a trimmed ``{results: [{url, keywords, ...}]}``
list so the agent can pick a template, run ``vision_analyze`` on the URL,
translate to art-director directives, and feed them into
``higgsfield_generate``.
"""

from __future__ import annotations

import logging
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
)
from tools.registry import registry, tool_error, tool_result

logger = logging.getLogger(__name__)

DEFAULT_TOP_K = 5


def _trim_result(row: dict) -> dict:
    """Extract the fields the LLM actually uses.

    Matches Go's ``extractResults``: prefer ``cloudfront_url`` over ``image_url``,
    carry forward ``keywords`` + any shallow metadata the index returns.
    """
    url = row.get("cloudfront_url") or row.get("image_url") or ""
    out: dict[str, Any] = {"url": url}
    keywords = row.get("keywords")
    if isinstance(keywords, list) and keywords:
        out["keywords"] = list(keywords)
    # Pass through a small set of optional scalar fields when present — they
    # help the agent disambiguate templates without bloating the payload.
    for passthrough in ("score", "id", "category", "designer", "mood"):
        if passthrough in row and row[passthrough] not in (None, ""):
            out[passthrough] = row[passthrough]
    return out


def higgsfield_inspiration(args: dict, **_kw) -> str:
    query = args.get("query")
    if not isinstance(query, str) or not query.strip():
        return tool_error("\"query\" is required and must be a non-empty string")
    query = query.strip()

    top_k_raw = args.get("top_k", DEFAULT_TOP_K)
    try:
        top_k = int(top_k_raw)
    except (TypeError, ValueError):
        return tool_error("\"top_k\" must be an integer")
    top_k = max(1, min(top_k, 50))

    raw = bool(args.get("raw", False))

    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    try:
        with HiggsfieldClient(cfg) as client:
            response = client.inspiration(query, top_k=top_k)
    except HiggsfieldAPIError as exc:
        return tool_error(str(exc), status_code=exc.status_code, body=exc.body)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_inspiration failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")

    if raw:
        return tool_result(response if isinstance(response, dict) else {"response": response})

    rows = response.get("results") if isinstance(response, dict) else None
    results: list[dict] = []
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            trimmed = _trim_result(row)
            if trimmed.get("url"):
                results.append(trimmed)
    return tool_result({"query": query, "top_k": top_k, "results": results})


HIGGSFIELD_INSPIRATION_SCHEMA: dict[str, Any] = {
    "name": "higgsfield_inspiration",
    "description": (
        "Search Higgsfield's design-template index for reference images "
        "matching a keyword query. Returns {query, top_k, results: [{url, "
        "keywords}]} — use vision_analyze on a promising url to read the "
        "template, translate the visual DNA (color palette, lighting, layout, "
        "typography, mood) into art-director directives, then feed them into "
        "higgsfield_generate. Pass raw=true to get the full response envelope "
        "when a downstream step needs extra metadata."
    ),
    "parameters": {
        "type": "object",
        "required": ["query"],
        "properties": {
            "query": {
                "type": "string",
                "description": "Keyword query. Terse keyword strings work best (e.g. 'fitness product energetic dark ad', 'minimalist jazz poster typography').",
            },
            "top_k": {
                "type": "integer",
                "description": "Number of results to return (default 5, cap 50).",
            },
            "raw": {
                "type": "boolean",
                "description": "Return the unmodified upstream response instead of the trimmed shape.",
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
    name="higgsfield_inspiration",
    toolset="higgsfield",
    schema=HIGGSFIELD_INSPIRATION_SCHEMA,
    handler=higgsfield_inspiration,
    check_fn=_check_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="Search Higgsfield design templates.",
    emoji="💡",
)
