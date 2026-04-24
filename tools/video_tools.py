#!/usr/bin/env python3
"""
Video Tools Module

Analyze videos with Google Gemini. Accepts either a local file path or a URL.
For URLs, downloads the video via ``yt-dlp`` when needed (TikTok, Instagram,
generic pages) or fetches direct MP4 CDN links directly. YouTube URLs are
forwarded to Gemini natively (no download).

Environment:
    GOOGLE_GENERATIVE_AI_API_KEY   Gemini API key. Optional if a proxy at
                                   GOOGLE_GENERATIVE_AI_BASE_URL injects it.
    GOOGLE_GENERATIVE_AI_BASE_URL  Overrides the Gemini base URL (proxy).
                                   Default: https://generativelanguage.googleapis.com
    HERMES_VIDEO_MODEL             Default Gemini model. Default: gemini-2.5-pro.
    HERMES_VIDEO_MAX_SIZE_MB       Max download size cap (default 500).

Registered tool: ``video_analyze`` (toolset ``vision``).
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any, Awaitable, Dict, Optional, Tuple
from urllib.parse import urlparse

import httpx

from tools.debug_helpers import DebugSession
from tools.url_safety import is_safe_url
from tools.website_policy import check_website_access

logger = logging.getLogger(__name__)
_debug = DebugSession("video_tools", env_var="VIDEO_TOOLS_DEBUG")


# ---------------------------------------------------------------------------
# Constants & env resolution (resolved per call so tests can monkeypatch)
# ---------------------------------------------------------------------------

_DEFAULT_MODEL = "gemini-2.5-pro"
_DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com"
_DEFAULT_MAX_SIZE_MB = 500
_UPLOAD_TIMEOUT = 300.0
_GENERATE_TIMEOUT = 300.0
_PROCESS_POLL_INTERVAL = 3.0
_PROCESS_MAX_WAIT = 180.0
_GENERATE_RETRIES = 3
_YTDLP_TIMEOUT = 180

_YOUTUBE_DOMAINS = ("youtube.com", "youtu.be")
_PAGE_DOMAINS = (
    "tiktok.com", "instagram.com", "facebook.com", "fb.watch",
    "twitter.com", "x.com", "vimeo.com", "reddit.com",
)
_MIME_BY_EXT = {
    ".mp4": "video/mp4",
    ".m4v": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".mkv": "video/x-matroska",
    ".avi": "video/x-msvideo",
    ".3gp": "video/3gpp",
}


def _base_url() -> str:
    return os.environ.get("GOOGLE_GENERATIVE_AI_BASE_URL", _DEFAULT_BASE_URL).rstrip("/")


def _api_key() -> str:
    key = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY", "")
    return "" if key == "placeholder" else key


def _default_model() -> str:
    return os.environ.get("HERMES_VIDEO_MODEL", "").strip() or _DEFAULT_MODEL


def _max_size_bytes() -> int:
    raw = os.environ.get("HERMES_VIDEO_MAX_SIZE_MB", "").strip()
    try:
        mb = int(raw) if raw else _DEFAULT_MAX_SIZE_MB
    except ValueError:
        mb = _DEFAULT_MAX_SIZE_MB
    return mb * 1024 * 1024


def _with_key(url: str, key: str) -> str:
    if not key:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}key={key}"


# ---------------------------------------------------------------------------
# URL classification
# ---------------------------------------------------------------------------


def _classify_url(url: str) -> str:
    """Return 'youtube', 'page', or 'direct'."""
    host = (urlparse(url).hostname or "").lower()
    if any(host == d or host.endswith("." + d) for d in _YOUTUBE_DOMAINS):
        return "youtube"
    if any(host == d or host.endswith("." + d) for d in _PAGE_DOMAINS):
        return "page"
    return "direct"


def _mime_for_path(path: Path) -> str:
    return _MIME_BY_EXT.get(path.suffix.lower(), "video/mp4")


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------


async def _download_direct(url: str, dest: Path) -> Tuple[Path, str]:
    """Download a direct video URL to ``dest``. Returns (path, content_type)."""
    blocked = check_website_access(url)
    if blocked:
        raise PermissionError(blocked["message"])
    if not is_safe_url(url):
        raise PermissionError(f"Refusing to download from unsafe URL: {url}")

    max_bytes = _max_size_bytes()
    content_type = "video/mp4"
    downloaded = 0
    async with httpx.AsyncClient(follow_redirects=True, timeout=_UPLOAD_TIMEOUT) as client:
        async with client.stream("GET", url) as resp:
            resp.raise_for_status()
            ct = resp.headers.get("Content-Type", "")
            if ct:
                content_type = ct.split(";")[0].strip() or content_type
            with dest.open("wb") as fh:
                async for chunk in resp.aiter_bytes(chunk_size=65536):
                    downloaded += len(chunk)
                    if downloaded > max_bytes:
                        raise ValueError(
                            f"Video exceeds size cap "
                            f"({max_bytes // (1024*1024)} MB)"
                        )
                    fh.write(chunk)
    logger.info("Downloaded %.1f MB (direct)", downloaded / 1024 / 1024)
    return dest, content_type


def _run_ytdlp(url: str, out_dir: Path) -> Path:
    """Blocking yt-dlp invocation. Returns path to downloaded file."""
    if shutil.which("yt-dlp") is None:
        raise RuntimeError("yt-dlp is not installed or not on PATH")

    template = str(out_dir / "video.%(ext)s")
    max_bytes = _max_size_bytes()
    max_size_arg = f"{max_bytes}"

    base_cmd = [
        "yt-dlp",
        "--no-playlist",
        "--max-filesize", max_size_arg,
        "-o", template,
    ]

    attempts = [
        base_cmd + ["-f", "best[ext=mp4]/best", url],
        base_cmd + [url],
    ]
    last_err = ""
    for cmd in attempts:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=_YTDLP_TIMEOUT)
        if result.returncode == 0:
            for child in sorted(out_dir.iterdir()):
                if child.is_file() and child.stem == "video":
                    return child
            last_err = "yt-dlp reported success but no output file found"
            continue
        last_err = (result.stderr or result.stdout or "").strip()[:500]

    raise RuntimeError(f"yt-dlp failed: {last_err}")


async def _download_ytdlp(url: str, out_dir: Path) -> Tuple[Path, str]:
    path = await asyncio.to_thread(_run_ytdlp, url, out_dir)
    size = path.stat().st_size
    if size > _max_size_bytes():
        raise ValueError(
            f"Downloaded video exceeds size cap ({_max_size_bytes() // (1024*1024)} MB)"
        )
    logger.info("Downloaded %.1f MB via yt-dlp", size / 1024 / 1024)
    return path, _mime_for_path(path)


# ---------------------------------------------------------------------------
# Gemini File API
# ---------------------------------------------------------------------------


async def _upload_to_gemini(path: Path, content_type: str) -> Dict[str, str]:
    """Upload ``path`` to Gemini using the resumable upload protocol.

    Returns dict with ``uri``, ``mimeType``, ``name``.
    """
    size = path.stat().st_size
    logger.info("Uploading %s (%.1f MB) to Gemini", path.name, size / 1024 / 1024)

    start_url = _with_key(f"{_base_url()}/upload/v1beta/files", _api_key())
    start_body = json.dumps({"file": {"display_name": path.name}}).encode()

    async with httpx.AsyncClient(timeout=_UPLOAD_TIMEOUT) as client:
        start_resp = await client.post(
            start_url,
            content=start_body,
            headers={
                "Content-Type": "application/json",
                "X-Goog-Upload-Protocol": "resumable",
                "X-Goog-Upload-Command": "start",
                "X-Goog-Upload-Header-Content-Length": str(size),
                "X-Goog-Upload-Header-Content-Type": content_type,
            },
        )
        start_resp.raise_for_status()
        upload_url = start_resp.headers.get("x-goog-upload-url")
        if not upload_url:
            raise RuntimeError("Gemini resumable-start response missing x-goog-upload-url header")

        # PUT raw bytes directly to upload_url (usually a signed Google URL,
        # bypasses any proxy body-size limits).
        with path.open("rb") as fh:
            data = fh.read()
        put_resp = await client.put(
            upload_url,
            content=data,
            headers={
                "Content-Type": content_type,
                "X-Goog-Upload-Command": "upload, finalize",
                "X-Goog-Upload-Offset": "0",
                "Content-Length": str(size),
            },
        )
        put_resp.raise_for_status()
        body = put_resp.json()

    file_info = body["file"]
    return {
        "uri": file_info["uri"],
        "mimeType": file_info.get("mimeType", content_type),
        "name": file_info["name"],
    }


async def _wait_for_active(file_name: str) -> None:
    """Poll the Gemini Files endpoint until the file is ACTIVE."""
    url = f"{_base_url()}/v1beta/{file_name}"
    deadline = time.monotonic() + _PROCESS_MAX_WAIT
    async with httpx.AsyncClient(timeout=60.0) as client:
        while time.monotonic() < deadline:
            try:
                resp = await client.get(_with_key(url, _api_key()))
                if resp.status_code == 200:
                    state = resp.json().get("state", "")
                    if state == "ACTIVE":
                        return
                    if state == "FAILED":
                        raise RuntimeError("Gemini reported file processing FAILED")
            except httpx.HTTPError as e:
                logger.debug("Polling error (will retry): %s", e)
            await asyncio.sleep(_PROCESS_POLL_INTERVAL)
    raise TimeoutError(
        f"Uploaded video did not become ACTIVE within {_PROCESS_MAX_WAIT:.0f}s"
    )


async def _delete_gemini_file(file_name: str) -> None:
    """Best-effort cleanup of an uploaded Gemini file."""
    url = _with_key(f"{_base_url()}/v1beta/{file_name}", _api_key())
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            await client.delete(url)
    except Exception as e:
        logger.debug("Could not delete Gemini file %s: %s", file_name, e)


# ---------------------------------------------------------------------------
# generateContent
# ---------------------------------------------------------------------------


async def _generate(model: str, file_uri: str, mime_type: str, prompt: str) -> str:
    """Call Gemini generateContent with a fileData part + text prompt."""
    url = f"{_base_url()}/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"fileData": {"fileUri": file_uri, "mimeType": mime_type}},
                {"text": prompt},
            ],
        }],
    }

    last_err: Optional[Exception] = None
    async with httpx.AsyncClient(timeout=_GENERATE_TIMEOUT) as client:
        for attempt in range(_GENERATE_RETRIES):
            try:
                resp = await client.post(
                    _with_key(url, _api_key()),
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                resp.raise_for_status()
                data = resp.json()
                candidates = data.get("candidates") or []
                if not candidates:
                    raise RuntimeError(f"Gemini returned no candidates: {data}")
                parts = candidates[0].get("content", {}).get("parts", []) or []
                text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
                return text
            except httpx.HTTPStatusError as e:
                last_err = e
                body = ""
                try:
                    body = e.response.text[:300]
                except Exception:
                    pass
                logger.warning(
                    "Gemini generate attempt %d failed: %s %s",
                    attempt + 1, e.response.status_code, body,
                )
                if attempt < _GENERATE_RETRIES - 1:
                    await asyncio.sleep(2 * (attempt + 1))
            except httpx.HTTPError as e:
                last_err = e
                logger.warning("Gemini generate transport error: %s", e)
                if attempt < _GENERATE_RETRIES - 1:
                    await asyncio.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Gemini generateContent failed: {last_err}")


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


async def video_analyze_tool(
    video_source: str,
    prompt: str,
    model: Optional[str] = None,
) -> str:
    """Analyze a video with Gemini.

    Args:
        video_source: HTTP/HTTPS URL or absolute/relative local file path.
        prompt: Analysis instructions for the model.
        model: Gemini model id. Defaults to ``HERMES_VIDEO_MODEL`` or
            ``gemini-2.5-pro``.

    Returns:
        JSON string with ``success``, ``analysis``, and metadata.
    """
    chosen_model = (model or "").strip() or _default_model()
    debug_info: Dict[str, Any] = {
        "video_source": video_source[:200],
        "prompt": prompt[:200] + ("..." if len(prompt) > 200 else ""),
        "model": chosen_model,
        "success": False,
        "error": None,
    }

    tmp_dir: Optional[tempfile.TemporaryDirectory] = None
    uploaded_file: Optional[str] = None

    try:
        if not video_source or not video_source.strip():
            raise ValueError("video_source is required")
        if not prompt or not prompt.strip():
            raise ValueError("prompt is required")

        resolved = video_source.strip()
        if resolved.startswith("file://"):
            resolved = resolved[len("file://"):]

        local = Path(os.path.expanduser(resolved))
        is_url = resolved.startswith(("http://", "https://"))

        # Case A: local file — upload directly
        if local.is_file() and not is_url:
            size = local.stat().st_size
            if size > _max_size_bytes():
                raise ValueError(
                    f"Local video exceeds size cap "
                    f"({_max_size_bytes() // (1024*1024)} MB)"
                )
            content_type = _mime_for_path(local)
            file_info = await _upload_to_gemini(local, content_type)
            uploaded_file = file_info["name"]
            await _wait_for_active(uploaded_file)
            text = await _generate(chosen_model, file_info["uri"], file_info["mimeType"], prompt)

        elif is_url:
            kind = _classify_url(resolved)
            debug_info["url_kind"] = kind

            # Case B: YouTube — send URL natively, no download
            if kind == "youtube":
                text = await _generate(chosen_model, resolved, "video/mp4", prompt)

            # Case C/D: download then upload
            else:
                tmp_dir = tempfile.TemporaryDirectory(prefix="hermes_video_")
                out_dir = Path(tmp_dir.name)
                if kind == "page":
                    path, content_type = await _download_ytdlp(resolved, out_dir)
                else:
                    path = out_dir / f"video_{uuid.uuid4().hex[:8]}.mp4"
                    try:
                        path, content_type = await _download_direct(resolved, path)
                    except httpx.HTTPStatusError as e:
                        if e.response.status_code in (401, 403, 404):
                            logger.info(
                                "Direct download returned %s; falling back to yt-dlp",
                                e.response.status_code,
                            )
                            path, content_type = await _download_ytdlp(resolved, out_dir)
                        else:
                            raise

                file_info = await _upload_to_gemini(path, content_type)
                uploaded_file = file_info["name"]
                await _wait_for_active(uploaded_file)
                text = await _generate(chosen_model, file_info["uri"], file_info["mimeType"], prompt)

        else:
            raise ValueError(
                f"video_source is neither an existing local file nor an "
                f"http(s) URL: {video_source!r}"
            )

        result = {
            "success": True,
            "model": chosen_model,
            "analysis": text or "",
        }
        debug_info["success"] = True
        debug_info["analysis_length"] = len(text or "")
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        logger.error("video_analyze failed: %s", e, exc_info=True)
        debug_info["error"] = f"{type(e).__name__}: {e}"
        return json.dumps(
            {"success": False, "model": chosen_model, "error": str(e), "analysis": ""},
            ensure_ascii=False,
        )
    finally:
        if uploaded_file:
            await _delete_gemini_file(uploaded_file)
        if tmp_dir is not None:
            try:
                tmp_dir.cleanup()
            except Exception:
                pass
        _debug.log_call("video_analyze_tool", debug_info)
        _debug.save()


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


def check_video_requirements() -> bool:
    """Tool is usable when we have a Gemini API key or a proxy base URL configured."""
    if _api_key():
        return True
    custom_base = os.environ.get("GOOGLE_GENERATIVE_AI_BASE_URL", "").strip()
    return bool(custom_base)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
from tools.registry import registry, tool_error  # noqa: E402

VIDEO_ANALYZE_SCHEMA = {
    "name": "video_analyze",
    "description": (
        "Analyze a video with Google Gemini. Accepts a local file path or a URL "
        "(YouTube is handled natively; TikTok/Instagram/etc. are downloaded via "
        "yt-dlp; direct MP4 URLs are streamed). Returns the model's text response "
        "to your prompt."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "video_source": {
                "type": "string",
                "description": (
                    "URL (http/https) or local file path to the video. "
                    "YouTube URLs are analyzed natively without download."
                ),
            },
            "prompt": {
                "type": "string",
                "description": "Instructions for Gemini (what to extract, describe, or answer).",
            },
            "model": {
                "type": "string",
                "description": (
                    "Gemini model id (e.g. gemini-2.5-pro, gemini-2.5-flash). "
                    "Defaults to HERMES_VIDEO_MODEL or gemini-2.5-pro."
                ),
            },
        },
        "required": ["video_source", "prompt"],
    },
}


def _handle_video_analyze(args: Dict[str, Any], **_kw: Any) -> Awaitable[str]:
    video_source = args.get("video_source", "")
    prompt = args.get("prompt", "")
    model = args.get("model") or None
    if not video_source:
        async def _err():
            return tool_error("video_source is required", success=False)
        return _err()
    if not prompt:
        async def _err():
            return tool_error("prompt is required", success=False)
        return _err()
    return video_analyze_tool(video_source, prompt, model)


registry.register(
    name="video_analyze",
    toolset="vision",
    schema=VIDEO_ANALYZE_SCHEMA,
    handler=_handle_video_analyze,
    check_fn=check_video_requirements,
    requires_env=["GOOGLE_GENERATIVE_AI_API_KEY"],
    is_async=True,
    emoji="🎬",
    max_result_size_chars=200_000,
)
