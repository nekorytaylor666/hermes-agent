"""higgsfield_soul_id — manage Soul IDs (custom face references).

Port of ``higgsfieldcli soul-id create/status/list/delete``. Soul IDs are
trained face identity models for ``text2image_soul_v2`` — supply a directory
of portraits and the backend produces a ``reference_id`` that preserves the
exact person's likeness across generations.

Actions:
- ``create``  — upload images from a local directory, submit for training,
  return the reference. Blocks for the upload phase (~1 s per image);
  training itself is async by default — pass ``poll=true`` to wait up to
  30 min for it to finish.
- ``status``  — fetch one reference; poll until terminal if requested.
- ``list``    — list references with filters.
- ``delete``  — delete by id.
"""

from __future__ import annotations

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
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
from tools.higgsfield.polling import (
    SOUL_ID_FAIL_STATUSES,
    SOUL_ID_SUCCESS_STATUSES,
    wait_for_soul_id,
)
from tools.registry import registry, tool_error, tool_result

logger = logging.getLogger(__name__)

_ALLOWED_ACTIONS = {"create", "status", "list", "delete"}
_ALLOWED_REF_TYPES = {"soul", "soul_2", "soul_cinematic", "soul_v2_preset"}
_ALLOWED_LIST_STATUSES = {"not_ready", "queued", "in_progress", "completed", "failed"}

# Image extensions supported by the FNF backend (mirrors MimeTypeForExt in Go).
_MIME_BY_EXT: dict[str, str] = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".heic": "image/heic",
    ".heif": "image/heif",
}

MAX_IMAGES = 100
UPLOAD_WORKERS = 4  # parallel upload-confirm lanes per training run


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _discover_images(directory: Path) -> tuple[list[Path], list[str]]:
    """Return (files, mimetypes) for supported images directly under ``directory``."""
    if not directory.exists():
        raise ValueError(f"dir does not exist: {directory}")
    if not directory.is_dir():
        raise ValueError(f"dir is not a directory: {directory}")

    files: list[Path] = []
    mimetypes: list[str] = []
    for entry in sorted(directory.iterdir()):
        if not entry.is_file():
            continue
        mt = _MIME_BY_EXT.get(entry.suffix.lower())
        if not mt:
            continue
        files.append(entry)
        mimetypes.append(mt)
    return files, mimetypes


def _files_from_explicit_list(paths: list[str]) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    mimetypes: list[str] = []
    for raw in paths:
        p = Path(raw).expanduser()
        if not p.exists() or not p.is_file():
            raise ValueError(f"file not found: {raw}")
        mt = _MIME_BY_EXT.get(p.suffix.lower())
        if not mt:
            raise ValueError(
                f"unsupported extension {p.suffix!r} (allowed: {', '.join(sorted(_MIME_BY_EXT))})"
            )
        files.append(p)
        mimetypes.append(mt)
    return files, mimetypes


def _upload_one(
    client: HiggsfieldClient,
    path: Path,
    batch_item: dict,
) -> dict:
    """Single upload + confirm. Returns ``{file, media_id, size}``."""
    filename = path.name
    content = path.read_bytes()
    client.upload_to_presigned(
        batch_item["upload_url"],
        content,
        batch_item.get("content_type", "application/octet-stream"),
    )
    client.confirm_upload(batch_item["id"], filename, force_ip_check=False)
    return {"file": filename, "media_id": batch_item["id"], "size": len(content)}


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


def _do_create(client: HiggsfieldClient, args: dict) -> dict:
    directory = args.get("dir")
    explicit_files = args.get("files")

    if directory and explicit_files:
        raise ValueError("pass either 'dir' or 'files', not both")
    if not directory and not explicit_files:
        raise ValueError("'dir' (directory path) or 'files' (list of paths) is required")

    if directory:
        dir_path = Path(str(directory)).expanduser()
        files, mimetypes = _discover_images(dir_path)
        source_label = str(dir_path)
    else:
        if not isinstance(explicit_files, list) or not explicit_files:
            raise ValueError("'files' must be a non-empty array of paths")
        files, mimetypes = _files_from_explicit_list([str(f) for f in explicit_files])
        source_label = f"{len(files)} files"

    if not files:
        raise ValueError(f"no supported image files found under {source_label}")
    if len(files) > MAX_IMAGES:
        raise ValueError(f"too many images ({len(files)}), maximum is {MAX_IMAGES}")

    name = str(args.get("name") or "Soul ID")
    poll = bool(args.get("poll", False))
    timeout = float(args.get("timeout_seconds") or 1800.0)

    logger.debug("soul_id create: discovered %d images from %s", len(files), source_label)

    # Step 1: pre-register the media slots (one POST).
    batch = client.create_media_batch(mimetypes, source="user_upload")
    if len(batch) != len(files):
        raise HiggsfieldError(
            f"media batch size mismatch: expected {len(files)}, got {len(batch)}"
        )

    # Step 2: upload+confirm each image, in parallel.
    workers = max(1, min(UPLOAD_WORKERS, len(files)))
    uploads: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        uploads = list(
            pool.map(
                lambda pair: _upload_one(client, pair[0], pair[1]),
                zip(files, batch),
            )
        )

    # Step 3: kick off soul-v2 training.
    input_images = [{"id": u["media_id"], "type": "media_input"} for u in uploads]
    ref = client.create_soul_v2_reference(name, input_images)

    # Step 4: optional poll.
    if poll:
        try:
            ref = wait_for_soul_id(
                client, ref.get("id", ""), interval=5.0, timeout=timeout,
            )
        except HiggsfieldTimeout as exc:
            return {
                "reference_id": ref.get("id", ""),
                "name": ref.get("name", name),
                "status": ref.get("status", "timeout"),
                "images_used": len(files),
                "error": str(exc),
                "uploads": uploads,
            }

    return {
        "reference_id": ref.get("id", ""),
        "name": ref.get("name", name),
        "status": ref.get("status", ""),
        "images_used": len(files),
        "uploads": uploads,
    }


def _do_status(client: HiggsfieldClient, args: dict) -> dict:
    reference_id = args.get("reference_id") or args.get("id")
    if not reference_id or not isinstance(reference_id, str):
        raise ValueError("reference_id is required for action=status")
    reference_id = reference_id.strip()

    poll = bool(args.get("poll", False))
    timeout = float(args.get("timeout_seconds") or 1800.0)

    ref = client.get_custom_reference(reference_id)

    if poll:
        status = ref.get("status", "")
        if status not in SOUL_ID_SUCCESS_STATUSES and status not in SOUL_ID_FAIL_STATUSES:
            try:
                ref = wait_for_soul_id(
                    client, reference_id, interval=5.0, timeout=timeout,
                )
            except HiggsfieldTimeout as exc:
                return {**ref, "error": str(exc), "status": "timeout"}
    return ref


def _do_list(client: HiggsfieldClient, args: dict) -> dict:
    ref_type = str(args.get("type") or "soul_2")
    if ref_type not in _ALLOWED_REF_TYPES:
        raise ValueError(
            f"type: invalid value {ref_type!r} (allowed: {', '.join(sorted(_ALLOWED_REF_TYPES))})"
        )

    statuses_raw = args.get("status") or args.get("statuses")
    statuses: list[str] = []
    if isinstance(statuses_raw, str) and statuses_raw:
        statuses = [statuses_raw]
    elif isinstance(statuses_raw, list):
        statuses = [str(s) for s in statuses_raw if s]
    for s in statuses:
        if s not in _ALLOWED_LIST_STATUSES:
            raise ValueError(
                f"status: invalid value {s!r} "
                f"(allowed: {', '.join(sorted(_ALLOWED_LIST_STATUSES))})"
            )

    size_raw = args.get("size", 10)
    try:
        size = int(size_raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("size must be an integer") from exc
    size = max(1, min(size, 100))

    params: dict[str, Any] = {
        "type": ref_type,
        "statuses": statuses,
        "size": size,
    }
    if args.get("search"):
        params["search"] = str(args["search"])
    if args.get("cursor"):
        params["cursor"] = str(args["cursor"])

    return client.list_custom_references(params)


def _do_delete(client: HiggsfieldClient, args: dict) -> dict:
    reference_id = args.get("reference_id") or args.get("id")
    if not reference_id or not isinstance(reference_id, str):
        raise ValueError("reference_id is required for action=delete")
    reference_id = reference_id.strip()
    client.delete_custom_reference(reference_id)
    return {"status": "deleted", "reference_id": reference_id}


# ---------------------------------------------------------------------------
# Tool handler
# ---------------------------------------------------------------------------


def higgsfield_soul_id(args: dict, **_kw) -> str:
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
            if action == "create":
                return tool_result(_do_create(client, args))
            if action == "status":
                return tool_result(_do_status(client, args))
            if action == "list":
                return tool_result(_do_list(client, args))
            if action == "delete":
                return tool_result(_do_delete(client, args))
    except ValueError as exc:
        return tool_error(str(exc))
    except HiggsfieldAPIError as exc:
        return tool_error(str(exc), status_code=exc.status_code, body=exc.body)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_soul_id failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")

    return tool_error("unreachable")  # pragma: no cover


HIGGSFIELD_SOUL_ID_SCHEMA: dict[str, Any] = {
    "name": "higgsfield_soul_id",
    "description": (
        "Manage Soul IDs — trained face identity references for "
        "text2image_soul_v2. Action discriminator selects the operation: "
        "create (upload a directory of portraits and submit for training; "
        "training takes up to 30 min — async by default, pass poll=true to "
        "wait), "
        "status (check / wait on one reference), "
        "list (browse references with filters), "
        "delete (remove by reference_id). "
        "Once created, use the reference_id in higgsfield_generate via "
        "`{\"model\": \"text2image_soul_v2\", \"soul_id\": \"<REFERENCE_ID>\", ...}` "
        "to generate images preserving the trained face."
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

            # --- create ---
            "dir": {
                "type": "string",
                "description": "create: path to a local directory containing portrait images (jpg, jpeg, png, webp, heic, heif). Subdirectories are ignored. Max 100 images.",
            },
            "files": {
                "type": "array",
                "items": {"type": "string"},
                "description": "create: explicit list of local file paths (alternative to 'dir'). Mutually exclusive with 'dir'.",
            },
            "name": {
                "type": "string",
                "description": "create: optional display name (default 'Soul ID').",
            },
            "poll": {
                "type": "boolean",
                "description": "create/status: wait for training to reach a terminal status (completed, showcase_completed, or failed). Default false — training takes up to 30 min, so usually submit async and check back with action=status later.",
            },
            "timeout_seconds": {
                "type": "number",
                "description": "create/status: max seconds to wait when poll=true (default 1800 = 30 min).",
            },

            # --- status / delete ---
            "reference_id": {
                "type": "string",
                "description": "status/delete: the Soul ID (custom reference) UUID.",
            },

            # --- list ---
            "type": {
                "type": "string",
                "enum": sorted(_ALLOWED_REF_TYPES),
                "description": "list: reference type filter (default 'soul_2').",
            },
            "status": {
                "type": "string",
                "enum": sorted(_ALLOWED_LIST_STATUSES),
                "description": "list: filter by training status.",
            },
            "search": {"type": "string", "description": "list: substring search by name."},
            "size": {
                "type": "integer",
                "description": "list: page size (default 10, cap 100).",
            },
            "cursor": {
                "type": "string",
                "description": "list: pagination cursor from a previous response.",
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
    name="higgsfield_soul_id",
    toolset="higgsfield",
    schema=HIGGSFIELD_SOUL_ID_SCHEMA,
    handler=higgsfield_soul_id,
    check_fn=_check_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="Manage Soul IDs — trained face identity references.",
    emoji="🧬",
    max_result_size_chars=32000,
)

# Silence unused imports that only appear inside helpers.
_ = os
