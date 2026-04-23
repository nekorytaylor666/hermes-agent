#!/usr/bin/env python3
"""DEPRECATED — use `contentcli analyze` or `youtubecli analyze video` instead.

Download a video, upload to Google Gemini, and analyze it.

Supports three URL types:
- Direct MP4 URLs (Instagram CDN) — downloads directly
- YouTube URLs — sends to Gemini API natively (no download needed)
- Page URLs (TikTok, Instagram post) — downloads via yt-dlp, then uploads

Returns the structured analysis text.

Usage:
    python3 analyze_video.py <video_url> --prompt-file references/analysis-templates.md
    python3 analyze_video.py <video_url> --prompt "Your custom analysis prompt"

Model: Hardcoded to gemini-2.5-pro. No override, no fallback.

Environment:
    GOOGLE_GENERATIVE_AI_API_KEY — optional (appends ?key= if set)
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError


GEMINI_BASE_URL = os.environ.get("GOOGLE_GENERATIVE_AI_BASE_URL", "https://generativelanguage.googleapis.com")
GEMINI_UPLOAD_URL = f"{GEMINI_BASE_URL}/upload/v1beta/files"
GEMINI_FILE_URL = f"{GEMINI_BASE_URL}/v1beta"
GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_GENERATE_URL = f"{GEMINI_BASE_URL}/v1beta/models/{GEMINI_MODEL}:generateContent"


YOUTUBE_DOMAINS = ("youtube.com", "youtu.be", "www.youtube.com")
PAGE_DOMAINS = ("tiktok.com", "instagram.com", "www.tiktok.com", "www.instagram.com")


def classify_url(url: str) -> str:
    """Classify URL type: 'youtube', 'page' (needs yt-dlp), or 'direct' (MP4 CDN)."""
    from urllib.parse import urlparse
    host = urlparse(url).hostname or ""
    if any(d in host for d in YOUTUBE_DOMAINS):
        return "youtube"
    if any(d in host for d in PAGE_DOMAINS):
        return "page"
    return "direct"

MAX_WAIT_SECONDS = 120
POLL_INTERVAL = 3
MAX_RETRIES = 3


def get_api_key():
    key = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY", "")
    return "" if key == "placeholder" else key


def url_with_key(base_url: str, api_key: str) -> str:
    """Append ?key=api_key if key is non-empty, otherwise return base_url as-is."""
    if api_key:
        return f"{base_url}?key={api_key}"
    return base_url


def download_video_direct(url: str) -> tuple[bytes, str]:
    """Download video from direct CDN URL and return (data, content_type)."""
    print(f"Downloading video (direct)...", file=sys.stderr)
    req = Request(url)
    with urlopen(req, timeout=120) as resp:
        content_type = resp.headers.get("Content-Type", "video/mp4")
        data = resp.read()
    print(f"Downloaded {len(data) / 1024 / 1024:.1f} MB", file=sys.stderr)
    return data, content_type


def download_video_ytdlp(url: str) -> tuple[bytes, str]:
    """Download video using yt-dlp and return (data, content_type)."""
    print(f"Downloading video via yt-dlp...", file=sys.stderr)

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "video.mp4")

        result = subprocess.run(
            ["yt-dlp", "-f", "best[ext=mp4]/best", "-o", output_path, "--no-playlist", url],
            capture_output=True, text=True, timeout=120,
        )

        if result.returncode != 0:
            print(f"yt-dlp error: {result.stderr[:300]}", file=sys.stderr)
            # Try without format filter
            result = subprocess.run(
                ["yt-dlp", "-o", output_path, "--no-playlist", url],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode != 0:
                raise RuntimeError(f"yt-dlp failed: {result.stderr[:300]}")

        # Find the downloaded file (yt-dlp may change extension)
        downloaded = None
        for f in os.listdir(tmpdir):
            if f.startswith("video"):
                downloaded = os.path.join(tmpdir, f)
                break

        if not downloaded or not os.path.exists(downloaded):
            raise RuntimeError("yt-dlp produced no output file")

        with open(downloaded, "rb") as f:
            data = f.read()

        ext = os.path.splitext(downloaded)[1].lower()
        mime_map = {".mp4": "video/mp4", ".webm": "video/webm", ".mkv": "video/x-matroska"}
        content_type = mime_map.get(ext, "video/mp4")

        print(f"Downloaded {len(data) / 1024 / 1024:.1f} MB via yt-dlp", file=sys.stderr)
        return data, content_type


def upload_to_gemini(video_data: bytes, content_type: str, api_key: str) -> dict:
    """Upload video to Gemini using resumable two-step protocol.

    Step 1: POST a small JSON body to start a resumable upload (through proxy).
    Step 2: PUT raw bytes directly to the returned upload URL (bypasses proxy).
    This avoids the proxy's body-size limit for large videos.
    """
    print("Uploading to Gemini (resumable)...", file=sys.stderr)
    size = len(video_data)

    # Step 1 — start resumable upload
    start_body = json.dumps({"file": {"display_name": "video"}}).encode()
    req = Request(
        url_with_key(GEMINI_UPLOAD_URL, api_key),
        data=start_body,
        headers={
            "Content-Type": "application/json",
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(size),
            "X-Goog-Upload-Header-Content-Type": content_type,
        },
        method="POST",
    )

    with urlopen(req, timeout=60) as resp:
        upload_url = resp.headers.get("x-goog-upload-url")
        if not upload_url:
            raise RuntimeError("Missing x-goog-upload-url header in resumable start response")

    print(f"Upload URL obtained, sending {size / 1024 / 1024:.1f} MB...", file=sys.stderr)

    # Step 2 — PUT raw bytes directly to the upload URL (bypasses proxy)
    req = Request(
        upload_url,
        data=video_data,
        headers={
            "Content-Type": content_type,
            "X-Goog-Upload-Command": "upload, finalize",
            "X-Goog-Upload-Offset": "0",
            "Content-Length": str(size),
        },
        method="PUT",
    )

    with urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())

    file_info = data["file"]
    print(f"Uploaded: {file_info['name']}", file=sys.stderr)
    return {
        "uri": file_info["uri"],
        "mimeType": file_info["mimeType"],
        "name": file_info["name"],
    }


def wait_for_active(file_name: str, api_key: str):
    """Poll until the uploaded file is ACTIVE."""
    print("Waiting for Gemini to process video...", file=sys.stderr)
    start = time.time()

    while time.time() - start < MAX_WAIT_SECONDS:
        try:
            req = Request(url_with_key(f"{GEMINI_FILE_URL}/{file_name}", api_key))
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                state = data.get("state", "")

                if state == "ACTIVE":
                    print("File is ACTIVE", file=sys.stderr)
                    return
                if state == "FAILED":
                    print(f"Error: Gemini file processing failed", file=sys.stderr)
                    sys.exit(1)

                print(f"  State: {state}, waiting...", file=sys.stderr)
        except HTTPError:
            pass

        time.sleep(POLL_INTERVAL)

    print(f"Error: File did not become ACTIVE within {MAX_WAIT_SECONDS}s", file=sys.stderr)
    sys.exit(1)


def analyze_video(file_uri: str, mime_type: str, prompt: str, api_key: str) -> str:
    """Send the video + prompt to Gemini and return analysis text."""
    payload = json.dumps({
        "contents": [{
            "role": "user",
            "parts": [
                {"fileData": {"fileUri": file_uri, "mimeType": mime_type}},
                {"text": prompt},
            ],
        }],
    }).encode()

    for attempt in range(MAX_RETRIES):
        try:
            url = url_with_key(GEMINI_GENERATE_URL, api_key)
            req = Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())

            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

            # Strip everything before first # (clean output)
            hash_idx = text.find("#")
            if hash_idx >= 0:
                text = text[hash_idx:]

            return text

        except HTTPError as e:
            if attempt < MAX_RETRIES - 1:
                print(f"  Gemini error {e.code}, retrying in 5s...", file=sys.stderr)
                time.sleep(5)
            else:
                body = e.read().decode() if e.fp else ""
                print(f"Error: Gemini analysis failed after {MAX_RETRIES} retries: {e.code} {body}", file=sys.stderr)
                sys.exit(1)

    return ""


def load_prompt(prompt_file: str = None, prompt_text: str = None) -> str:
    """Load analysis prompt from file or direct text."""
    if prompt_text:
        return prompt_text

    if prompt_file:
        # Resolve path: try as-is first, then relative to CWD, then relative to skill dir
        if not os.path.isabs(prompt_file) and not os.path.exists(prompt_file):
            skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate = os.path.join(skill_dir, prompt_file)
            if os.path.exists(candidate):
                prompt_file = candidate

        with open(prompt_file, "r") as f:
            content = f.read()

        # Strip YAML frontmatter if present
        if content.startswith("---"):
            end = content.find("---", 3)
            if end != -1:
                content = content[end + 3:].strip()

        return content

    print("Error: provide --prompt-file or --prompt", file=sys.stderr)
    sys.exit(1)


def analyze_youtube(url: str, prompt: str, api_key: str) -> str:
    """Analyze YouTube video natively — Gemini accepts YouTube URLs directly."""
    print(f"Analyzing YouTube video natively (no download)...", file=sys.stderr)

    payload = json.dumps({
        "contents": [{
            "role": "user",
            "parts": [
                {"fileData": {"fileUri": url, "mimeType": "video/mp4"}},
                {"text": prompt},
            ],
        }],
    }).encode()

    for attempt in range(MAX_RETRIES):
        try:
            url = url_with_key(GEMINI_GENERATE_URL, api_key)
            req = Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())

            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            hash_idx = text.find("#")
            return text[hash_idx:] if hash_idx >= 0 else text

        except HTTPError as e:
            if attempt < MAX_RETRIES - 1:
                print(f"  Gemini error {e.code}, retrying in 5s...", file=sys.stderr)
                time.sleep(5)
            else:
                body = e.read().decode() if e.fp else ""
                print(f"Error: Gemini failed: {e.code} {body[:200]}", file=sys.stderr)
                return ""
    return ""


def main():
    parser = argparse.ArgumentParser(description="Analyze a video with Google Gemini")
    parser.add_argument("video_url", help="URL of the video to analyze (YouTube, TikTok, Instagram, or direct MP4)")
    parser.add_argument("--prompt-file", help="Path to prompt template file")
    parser.add_argument("--prompt", help="Direct prompt text")
    args = parser.parse_args()

    api_key = get_api_key()
    prompt = load_prompt(args.prompt_file, args.prompt)
    url_type = classify_url(args.video_url)

    print(f"Gemini model: {GEMINI_MODEL}", file=sys.stderr)
    print(f"URL type: {url_type}", file=sys.stderr)

    # YouTube — send URL directly to Gemini (no download)
    if url_type == "youtube":
        analysis = analyze_youtube(args.video_url, prompt, api_key)
        print(analysis)
        print(f"\n# Analysis complete (YouTube native)", file=sys.stderr)
        return

    # TikTok/Instagram page — download via yt-dlp
    if url_type == "page":
        try:
            video_data, content_type = download_video_ytdlp(args.video_url)
        except Exception as e:
            print(f"Error downloading via yt-dlp: {e}", file=sys.stderr)
            sys.exit(1)
    # Direct CDN URL — download directly
    else:
        try:
            video_data, content_type = download_video_direct(args.video_url)
        except HTTPError as e:
            if e.code == 403:
                print(f"Direct URL expired (403). Trying yt-dlp fallback...", file=sys.stderr)
                try:
                    video_data, content_type = download_video_ytdlp(args.video_url)
                except Exception as e2:
                    print(f"Error: both direct and yt-dlp failed: {e2}", file=sys.stderr)
                    sys.exit(1)
            else:
                raise

    # Upload to Gemini
    file_info = upload_to_gemini(video_data, content_type, api_key)

    # Wait for processing
    wait_for_active(file_info["name"], api_key)

    # Analyze
    print("Analyzing with Gemini...", file=sys.stderr)
    analysis = analyze_video(file_info["uri"], file_info["mimeType"], prompt, api_key)

    # Output to stdout
    print(analysis)
    print(f"\n# Analysis complete", file=sys.stderr)


if __name__ == "__main__":
    main()
