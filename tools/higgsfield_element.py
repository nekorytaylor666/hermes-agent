"""higgsfield_element — manage persistent reference elements.

Port of ``higgsfieldcli element list/get/create``. Elements are reusable
character / environment / prop references keyed by UUID; once created they
can be injected into any generation via ``<<<element_id>>>`` in the prompt
and the backend resolves the underlying media automatically.

Single tool, ``action`` discriminator, matches the Go subcommand layout.
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

_ALLOWED_ACTIONS = {"list", "get", "create"}
_ALLOWED_CATEGORIES = {
    # Canonical category tags accepted by the backend. Not all are valid at
    # once — the API will reject unknown ones, but this list is accurate as
    # of the Go CLI.
    "image", "video", "auto", "face", "outfit", "product", "location",
    "object", "style", "character", "environment", "prop",
}
_ALLOWED_FILTERS = {"image", "video"}


def _normalize_media(raw: Any, field: str, idx: int) -> dict:
    """Validate and return an element media entry ``{id, url, type}``."""
    if not isinstance(raw, dict):
        raise ValueError(f"{field}[{idx}]: expected object, got {type(raw).__name__}")
    mid = str(raw.get("id") or "").strip()
    url = str(raw.get("url") or "").strip()
    mtype = str(raw.get("type") or "media_input").strip()
    if not mid:
        raise ValueError(f"{field}[{idx}]: id is required")
    if not url:
        raise ValueError(f"{field}[{idx}]: url is required")
    return {"id": mid, "url": url, "type": mtype}


def _normalize_media_list(raw: Any, field: str) -> list[dict]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError(f"{field} must be an array")
    return [_normalize_media(item, field, i) for i, item in enumerate(raw)]


def _do_list(client: HiggsfieldClient, args: dict) -> dict:
    params: dict[str, Any] = {}

    category = args.get("category")
    if category:
        params["category"] = str(category)

    categories = args.get("categories")
    if isinstance(categories, list) and categories:
        params["categories"] = ",".join(str(c) for c in categories if c)
    elif isinstance(categories, str) and categories:
        params["categories"] = categories

    filt = args.get("filter")
    if filt:
        if filt not in _ALLOWED_FILTERS:
            raise ValueError(
                f"filter: invalid value {filt!r} (allowed: {', '.join(sorted(_ALLOWED_FILTERS))})"
            )
        params["filter"] = filt

    if "pinned" in args and args["pinned"] is not None:
        params["pinned"] = bool(args["pinned"])
    if "ip_detected" in args and args["ip_detected"] is not None:
        params["ip_detected"] = bool(args["ip_detected"])

    size_raw = args.get("size", 20)
    try:
        size = int(size_raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("size must be an integer") from exc
    size = max(1, min(size, 1000))
    params["size"] = size

    cursor = args.get("cursor")
    if cursor:
        params["cursor"] = str(cursor)

    return client.list_elements(params)


def _do_get(client: HiggsfieldClient, args: dict) -> dict:
    element_id = args.get("element_id") or args.get("id")
    if not element_id or not isinstance(element_id, str):
        raise ValueError("element_id is required for action=get")
    return client.get_element(element_id.strip())


def _do_create(client: HiggsfieldClient, args: dict) -> dict:
    category = str(args.get("category") or "auto").strip()
    # Backend validates the category authoritatively; we warn but don't block
    # on unknown values so new categories don't require a code update.
    if category not in _ALLOWED_CATEGORIES:
        logger.debug("unknown element category %s — passing through to backend", category)

    medias = _normalize_media_list(args.get("medias"), "medias")
    video_medias = _normalize_media_list(args.get("video_medias"), "video_medias")

    if not medias and not video_medias:
        raise ValueError(
            "create requires at least one entry in 'medias' or 'video_medias'"
        )

    body: dict[str, Any] = {"category": category}
    if args.get("name"):
        body["name"] = str(args["name"])
    if args.get("description"):
        body["description"] = str(args["description"])
    if medias:
        body["medias"] = medias
    if video_medias:
        body["video_medias"] = video_medias
    if args.get("audio_input_id"):
        body["audio_input_id"] = str(args["audio_input_id"])

    return client.create_element(body)


def higgsfield_element(args: dict, **_kw) -> str:
    action = args.get("action")
    if action not in _ALLOWED_ACTIONS:
        return tool_error(
            "\"action\" must be one of: " + ", ".join(sorted(_ALLOWED_ACTIONS))
        )

    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    try:
        with HiggsfieldClient(cfg) as client:
            if action == "list":
                return tool_result(_do_list(client, args))
            if action == "get":
                return tool_result(_do_get(client, args))
            if action == "create":
                return tool_result(_do_create(client, args))
    except ValueError as exc:
        return tool_error(str(exc))
    except HiggsfieldAPIError as exc:
        return tool_error(str(exc), status_code=exc.status_code, body=exc.body)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_element failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")

    return tool_error("unreachable")  # pragma: no cover


HIGGSFIELD_ELEMENT_SCHEMA: dict[str, Any] = {
    "name": "higgsfield_element",
    "description": (
        "Manage persistent reference elements (characters, environments, "
        "props). Action discriminator selects the operation: "
        "list (browse elements with filters), "
        "get (fetch one by element_id), "
        "create (register a new element from existing media/video IDs). "
        "Once created, reference an element in any generation prompt via "
        "`<<<element_id>>>` and the backend resolves the underlying media "
        "automatically. For create: supply at least one entry in 'medias' "
        "or 'video_medias', each shaped like {id, url, type}. Each entry's "
        "id+url must already exist — upload is not yet wired up, so media "
        "IDs must come from prior generations (via job_set_type_job type) "
        "or from user-supplied uploads."
    ),
    "parameters": {
        "type": "object",
        "required": ["action"],
        "properties": {
            "action": {
                "type": "string",
                "enum": sorted(_ALLOWED_ACTIONS),
                "description": "Operation to perform.",
            },

            # --- list ---
            "category": {
                "type": "string",
                "description": "list/create: single category (e.g. character, environment, prop, face, outfit, product, location, object, style, image, video, auto).",
            },
            "categories": {
                "type": "array",
                "items": {"type": "string"},
                "description": "list: multiple categories (joined as comma-separated on the wire).",
            },
            "filter": {
                "type": "string",
                "enum": sorted(_ALLOWED_FILTERS),
                "description": "list: restrict to 'image' or 'video' elements.",
            },
            "pinned": {"type": "boolean", "description": "list: filter by pinned status."},
            "ip_detected": {"type": "boolean", "description": "list: filter by IP-detected status."},
            "size": {"type": "integer", "description": "list: page size (default 20, cap 1000)."},
            "cursor": {"type": "string", "description": "list: pagination cursor from a previous response."},

            # --- get ---
            "element_id": {"type": "string", "description": "get: the element UUID."},

            # --- create ---
            "name": {"type": "string", "description": "create: optional display name."},
            "description": {"type": "string", "description": "create: optional free-text description."},
            "medias": {
                "type": "array",
                "description": "create: image medias [{id, url, type?}]. type defaults to 'media_input'; use '<job_set_type>_job' to reference a prior generation (e.g. 'nano_banana_2_job').",
                "items": {
                    "type": "object",
                    "required": ["id", "url"],
                    "properties": {
                        "id": {"type": "string"},
                        "url": {"type": "string"},
                        "type": {"type": "string"},
                    },
                },
            },
            "video_medias": {
                "type": "array",
                "description": "create: video medias (same shape as medias).",
                "items": {
                    "type": "object",
                    "required": ["id", "url"],
                    "properties": {
                        "id": {"type": "string"},
                        "url": {"type": "string"},
                        "type": {"type": "string"},
                    },
                },
            },
            "audio_input_id": {
                "type": "string",
                "description": "create: optional audio input media ID.",
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
    name="higgsfield_element",
    toolset="higgsfield",
    schema=HIGGSFIELD_ELEMENT_SCHEMA,
    handler=higgsfield_element,
    check_fn=_check_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="CRUD for Higgsfield reference elements.",
    emoji="🧩",
)
