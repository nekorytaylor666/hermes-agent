"""Tests for tools/video_tools.py — URL classification, arg validation, registry wiring."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.video_tools import (
    _base_url,
    _classify_url,
    _default_model,
    _max_size_bytes,
    _mime_for_path,
    _with_key,
    check_video_requirements,
    video_analyze_tool,
    VIDEO_ANALYZE_SCHEMA,
)


# ---------------------------------------------------------------------------
# _classify_url
# ---------------------------------------------------------------------------


class TestClassifyUrl:
    def test_youtube_long(self):
        assert _classify_url("https://www.youtube.com/watch?v=abc") == "youtube"

    def test_youtube_short(self):
        assert _classify_url("https://youtu.be/abc") == "youtube"

    def test_tiktok(self):
        assert _classify_url("https://www.tiktok.com/@u/video/123") == "page"

    def test_instagram_reel(self):
        assert _classify_url("https://www.instagram.com/reel/abc/") == "page"

    def test_vimeo(self):
        assert _classify_url("https://vimeo.com/12345") == "page"

    def test_x_com(self):
        assert _classify_url("https://x.com/user/status/1") == "page"

    def test_direct_mp4(self):
        assert _classify_url("https://cdn.example.com/video.mp4") == "direct"

    def test_empty_host_falls_through_to_direct(self):
        assert _classify_url("not-a-url") == "direct"


# ---------------------------------------------------------------------------
# _mime_for_path
# ---------------------------------------------------------------------------


class TestMimeForPath:
    def test_mp4(self):
        assert _mime_for_path(Path("clip.mp4")) == "video/mp4"

    def test_webm(self):
        assert _mime_for_path(Path("clip.webm")) == "video/webm"

    def test_mov(self):
        assert _mime_for_path(Path("clip.MOV")) == "video/quicktime"

    def test_unknown_defaults_to_mp4(self):
        assert _mime_for_path(Path("clip.xyz")) == "video/mp4"


# ---------------------------------------------------------------------------
# env resolution
# ---------------------------------------------------------------------------


class TestEnvResolution:
    def test_default_base_url(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_GENERATIVE_AI_BASE_URL", raising=False)
        assert _base_url() == "https://generativelanguage.googleapis.com"

    def test_proxied_base_url_strips_trailing_slash(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_GENERATIVE_AI_BASE_URL", "https://proxy.example.com/")
        assert _base_url() == "https://proxy.example.com"

    def test_default_model(self, monkeypatch):
        monkeypatch.delenv("HERMES_VIDEO_MODEL", raising=False)
        assert _default_model() == "gemini-2.5-pro"

    def test_override_model(self, monkeypatch):
        monkeypatch.setenv("HERMES_VIDEO_MODEL", "gemini-2.5-flash")
        assert _default_model() == "gemini-2.5-flash"

    def test_max_size_default(self, monkeypatch):
        monkeypatch.delenv("HERMES_VIDEO_MAX_SIZE_MB", raising=False)
        assert _max_size_bytes() == 500 * 1024 * 1024

    def test_max_size_override(self, monkeypatch):
        monkeypatch.setenv("HERMES_VIDEO_MAX_SIZE_MB", "100")
        assert _max_size_bytes() == 100 * 1024 * 1024

    def test_max_size_bad_value_falls_back(self, monkeypatch):
        monkeypatch.setenv("HERMES_VIDEO_MAX_SIZE_MB", "abc")
        assert _max_size_bytes() == 500 * 1024 * 1024


# ---------------------------------------------------------------------------
# _with_key
# ---------------------------------------------------------------------------


class TestWithKey:
    def test_no_key(self):
        assert _with_key("https://api.example.com/foo", "") == "https://api.example.com/foo"

    def test_appends_with_question_mark(self):
        assert _with_key("https://api.example.com/foo", "SECRET") == \
            "https://api.example.com/foo?key=SECRET"

    def test_appends_with_ampersand_when_query_present(self):
        assert _with_key("https://api.example.com/foo?x=1", "SECRET") == \
            "https://api.example.com/foo?x=1&key=SECRET"


# ---------------------------------------------------------------------------
# check_video_requirements
# ---------------------------------------------------------------------------


class TestAvailability:
    def test_available_with_api_key(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_GENERATIVE_AI_API_KEY", "real-key")
        monkeypatch.delenv("GOOGLE_GENERATIVE_AI_BASE_URL", raising=False)
        assert check_video_requirements() is True

    def test_available_with_proxy_url_only(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_GENERATIVE_AI_API_KEY", raising=False)
        monkeypatch.setenv("GOOGLE_GENERATIVE_AI_BASE_URL", "https://proxy.example.com")
        assert check_video_requirements() is True

    def test_placeholder_key_treated_as_missing(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_GENERATIVE_AI_API_KEY", "placeholder")
        monkeypatch.delenv("GOOGLE_GENERATIVE_AI_BASE_URL", raising=False)
        assert check_video_requirements() is False

    def test_unavailable_when_both_missing(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_GENERATIVE_AI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_GENERATIVE_AI_BASE_URL", raising=False)
        assert check_video_requirements() is False


# ---------------------------------------------------------------------------
# video_analyze_tool — input validation paths (no network)
# ---------------------------------------------------------------------------


class TestVideoAnalyzeInputValidation:
    @pytest.mark.asyncio
    async def test_rejects_empty_source(self):
        result = json.loads(await video_analyze_tool("", "describe"))
        assert result["success"] is False
        assert "video_source" in result["error"]

    @pytest.mark.asyncio
    async def test_rejects_empty_prompt(self):
        result = json.loads(await video_analyze_tool("https://ex.com/a.mp4", ""))
        assert result["success"] is False
        assert "prompt" in result["error"]

    @pytest.mark.asyncio
    async def test_rejects_non_url_non_file(self, tmp_path):
        missing = tmp_path / "does_not_exist.mp4"
        result = json.loads(await video_analyze_tool(str(missing), "describe"))
        assert result["success"] is False
        assert "neither" in result["error"]

    @pytest.mark.asyncio
    async def test_model_override_reported_even_on_error(self):
        result = json.loads(await video_analyze_tool("", "prompt", model="gemini-2.5-flash"))
        assert result["model"] == "gemini-2.5-flash"


# ---------------------------------------------------------------------------
# Registry wiring
# ---------------------------------------------------------------------------


class TestRegistration:
    def test_schema_required_fields(self):
        props = VIDEO_ANALYZE_SCHEMA["parameters"]["properties"]
        assert set(VIDEO_ANALYZE_SCHEMA["parameters"]["required"]) == {"video_source", "prompt"}
        assert "model" in props  # optional

    def test_tool_is_registered_in_vision_toolset(self):
        from tools.registry import registry
        entry = registry.get_entry("video_analyze")
        assert entry is not None
        assert entry.toolset == "vision"
        assert entry.is_async is True

    def test_tool_listed_in_vision_toolset(self):
        from toolsets import resolve_toolset
        assert "video_analyze" in resolve_toolset("vision")

    def test_tool_listed_in_hermes_cli_core(self):
        from toolsets import resolve_toolset
        assert "video_analyze" in resolve_toolset("hermes-cli")
