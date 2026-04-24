"""Input media / image resolution.

Mirrors ``generation/json_media.go`` and ``generation/media_flag.go``.
"""

from __future__ import annotations

from typing import Any, Iterable

from .client import HiggsfieldClient

# Roles that are image-like and for which we auto-resolve type/url via
# GET /input-images/{id} when the caller didn't supply them.
IMAGE_ROLES = {"image", "start_image", "end_image"}

# Per-model role allow-lists. Models not present here accept any role
# (validation is skipped) — mirrors Go behavior.
MODEL_ALLOWED_ROLES: dict[str, set[str]] = {
    "claudesfield_video": {"image"},
    "text2image_soul_v2": {"image"},
    "soul_cinematic": {"image"},
    "seedream_v5_lite": {"image"},
    "seedream_v4_5": {"image"},
    "imagegen_2_0": {"image"},
    "kling3_0": {"image", "video", "start_image", "end_image"},
    "image_auto": {"image"},
    "grok_image": {"image"},
    "seedance1_5": {"start_image", "end_image"},
    "cinematic_studio_2_5": {"image"},
    "cinematic_studio_3_0": {"image", "start_image"},
    "wan2_7": {"image", "start_image"},
    "veo3_1_lite": {"start_image", "end_image"},
    "grok_video": {"start_image"},
}


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("expected a list")
    return value


def _resolve_image_type_url(client: HiggsfieldClient, image_id: str) -> tuple[str, str]:
    info = client.get_input_image(image_id)
    return info.get("type", ""), info.get("url", "")


def resolve_media_inputs(
    client: HiggsfieldClient,
    model: str,
    raw_inputs: Iterable[dict] | None,
) -> list[dict]:
    """Convert JSON ``medias`` entries into FNF ``{role, data: {id, type, url}}`` items.

    Matches ``resolveMediaInputs`` in ``generation/json_media.go``.
    """
    items = _as_list(raw_inputs)
    if not items:
        return []

    allowed = MODEL_ALLOWED_ROLES.get(model)

    out: list[dict] = []
    for idx, entry in enumerate(items):
        if not isinstance(entry, dict):
            raise ValueError(f"medias[{idx}]: expected object, got {type(entry).__name__}")
        role = entry.get("role") or "image"
        data = entry.get("data") or {}
        if not isinstance(data, dict):
            raise ValueError(f"medias[{idx}]: data must be an object")
        image_id = data.get("id") or ""
        if not image_id:
            raise ValueError(f"medias[{idx}]: id is required")

        if allowed is not None and role not in allowed:
            raise ValueError(
                f"medias[{idx}]: role {role!r} is not supported by model {model} "
                f"(allowed: {', '.join(sorted(allowed))})"
            )

        mtype = data.get("type") or ""
        murl = data.get("url") or ""

        if not mtype:
            if role not in IMAGE_ROLES:
                raise ValueError(
                    f"medias[{idx}]: type is required for role {role!r}"
                )
            mtype, resolved_url = _resolve_image_type_url(client, image_id)
            if not murl:
                murl = resolved_url

        out.append({"role": role, "data": {"id": image_id, "type": mtype, "url": murl}})
    return out


def resolve_image_inputs(
    client: HiggsfieldClient,
    raw_inputs: Iterable[dict] | None,
) -> list[dict]:
    """Convert JSON ``images`` entries into FNF ``{id, type, url}`` items.

    Matches ``resolveImageInputs`` in ``generation/json_media.go``.
    """
    items = _as_list(raw_inputs)
    if not items:
        return []

    out: list[dict] = []
    for idx, entry in enumerate(items):
        if not isinstance(entry, dict):
            raise ValueError(f"images[{idx}]: expected object, got {type(entry).__name__}")
        image_id = entry.get("id") or ""
        if not image_id:
            raise ValueError(f"images[{idx}]: id is required")
        itype = entry.get("type") or ""
        iurl = entry.get("url") or ""
        if not itype:
            itype, resolved_url = _resolve_image_type_url(client, image_id)
            if not iurl:
                iurl = resolved_url
        out.append({"id": image_id, "type": itype, "url": iurl})
    return out


def resolve_optional_image(
    client: HiggsfieldClient,
    raw: dict | None,
) -> dict | None:
    """Match ``resolveOptionalImage`` — returns None if ``raw`` is None."""
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError("expected an object")
    image_id = raw.get("id") or ""
    if not image_id:
        raise ValueError("image id is required")
    itype = raw.get("type") or ""
    iurl = raw.get("url") or ""
    if not itype:
        itype, resolved_url = _resolve_image_type_url(client, image_id)
        if not iurl:
            iurl = resolved_url
    return {"id": image_id, "type": itype, "url": iurl}
