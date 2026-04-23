#!/usr/bin/env python3
"""Generate new video concepts using Gemini 3.1 Pro.

Takes video analyses + client profile via stdin, generates 3 adapted concepts.

Usage:
    echo '{"analyses": [...], "client": {...}}' | python3 generate_concepts.py
    echo '{"analyses": [...], "client": {...}}' | python3 generate_concepts.py --model gemini-2.5-pro

Input JSON format (stdin):
    {
        "analyses": [
            {
                "creator": "@username",
                "platform": "tiktok",
                "views": 3100000,
                "engagementRate": 12.25,
                "analysis": "# CONCEPT\\n...",
                "musicName": "New Sun",
                "musicAuthor": "Chihei Hatakeyama"
            }
        ],
        "client": {
            "name": "Kokotini Hotel",
            "niche": "boutique hotel Italy",
            "audience": "travelers 25-45, couples",
            "style": "warm Mediterranean, la dolce vita",
            "description": "Boutique hotel in Italy with ocean views"
        }
    }

Environment:
    GOOGLE_GENERATIVE_AI_API_KEY — required
    GEMINI_CONCEPTS_MODEL — optional (default: gemini-3.1-pro-preview)
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError


DEFAULT_MODEL = "gemini-3.1-pro-preview"
FALLBACK_MODEL = "gemini-2.5-pro"
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
MAX_OUTPUT_TOKENS = 8192


def get_api_key():
    key = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
    if not key:
        print("Error: GOOGLE_GENERATIVE_AI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    return key


def call_gemini(prompt: str, model: str, api_key: str) -> str:
    """Send prompt to Gemini and return text response."""
    url = f"{GEMINI_BASE}/{model}:generateContent?key={api_key}"

    payload = json.dumps({
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}],
        }],
        "generationConfig": {
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
            "temperature": 1.0,
        },
    }).encode()

    req = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Error: Gemini {model} returned {e.code}: {body[:300]}", file=sys.stderr)
        return ""

    text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    return text


def build_prompt(analyses: list, client: dict) -> str:
    """Build the concept generation prompt from analyses and client profile."""

    # Compile all analyses into one reference block
    references = ""

    for i, a in enumerate(analyses, 1):
        creator = a.get("creator", "unknown")
        platform = a.get("platform", "?")
        views = a.get("views", 0)
        eng = a.get("engagementRate", 0)
        url = a.get("url", "")
        analysis_text = a.get("analysis", "")

        references += f"\n### Reference [{i}]: @{creator} ({platform}, {views:,} views, {eng}% engagement)\n"
        if url:
            references += f"Source URL: {url}\n"
        references += f"{analysis_text}\n"

    music_section = ""

    client_name = client.get("name", "the brand")
    client_niche = client.get("niche", "")
    client_audience = client.get("audience", "")
    client_style = client.get("style", "")
    client_desc = client.get("description", "")

    return f"""# ROLE
You are an elite creative director specializing in viral short-form video content (Instagram Reels, TikTok).

# OBJECTIVE
Based on the reference video analyses below, generate exactly 3 NEW video concepts for **{client_name}**.

# CLIENT PROFILE
- **Brand:** {client_name}
- **Niche:** {client_niche}
- **Description:** {client_desc}
- **Target audience:** {client_audience}
- **Style:** {client_style}

# REFERENCE VIDEOS (analyzed by AI)
{references}
{music_section}
# RULES
- Generate exactly 3 concepts — no more, no less
- Do NOT copy the originals — translate the core idea into {client_niche} context
- Each concept must have a unique angle/format
- HOOKS are the most important part — the first 3 seconds must stop scrolling
- Transfer RETENTION MECHANISMS from references into new concepts — don't just adapt the topic, adapt the engagement architecture (open loops, delayed payoff, micro-escalations, pattern interrupts)
- Include specific scene descriptions, not vague directions
- Do NOT include per-second timestamps like [0:00-0:03] in the script — describe the flow as a sequence of scenes without timing markers
- For AUDIO: describe the style, genre, tempo, and mood of the music — NEVER name specific artists, songs, or tracks even if recognizable from the references
- Look for PATTERNS across references — what formats/techniques appear in multiple videos?
- Each concept MUST include a SOURCES section citing which reference(s) inspired it using GFM footnote syntax [^1], [^2], etc.

# OUTPUT FORMAT

For each concept, use this exact structure:

# CONCEPT 1
Text description of the concept (1-3 sentences)

## HOOK
Detailed hook description (1-3 sentences)
- VISUAL: what is seen in the first 1-2 seconds
- AUDIO: first spoken words (confident, direct, no intro)
- TEXT: on-screen statement if any (max 6-8 words)
- The hook must create either fear of loss, strong curiosity, or identity relevance
- Why this hook works for {client_audience}

## RETENTION
How this concept keeps viewers watching (1-3 sentences)
- Open loops, delayed payoff, micro-escalations every 3-5s, pattern interrupts
- Clear forward momentum — the viewer feels the video is going somewhere

## REWARD
What the viewer gets by watching (1-2 sentences)
- Education (clarity), Entertainment (emotional release), or Inspiration (action)

## AUDIO
Describe the audio style, genre, tempo, and mood (never name specific artists or tracks)

## SCRIPT
Detailed script (1-20 sentences, as many as needed)
- 1. Immediate hook (no greeting) 2. Problem framing / tension 3. Why this matters 4. Main insight 5. Clean close
- Scenes, actions, voiceover, exact wording
- Tone matching {client_name}'s style

## SOURCES
- Inspired by: [^N] @creator — what specific element was adapted (hook technique, format, retention mechanism, visual style)

# CONCEPT 2
...

# CONCEPT 3
...

After all concepts, add footnote definitions:

[^1]: @creator — platform — Source URL
[^2]: @creator — platform — Source URL
...

# BEGIN YOUR WORK"""


def main():
    parser = argparse.ArgumentParser(description="Generate video concepts using Gemini 3.1 Pro")
    parser.add_argument("--model", default=None, help=f"Gemini model (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    model = args.model or os.environ.get("GEMINI_CONCEPTS_MODEL", DEFAULT_MODEL)
    api_key = get_api_key()

    # Read input from stdin
    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: no data on stdin", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    analyses = data.get("analyses", [])
    client = data.get("client", {})

    if not analyses:
        print("Error: no analyses provided", file=sys.stderr)
        sys.exit(1)

    prompt = build_prompt(analyses, client)

    print(f"Generating concepts with {model}...", file=sys.stderr)
    print(f"  References: {len(analyses)} videos", file=sys.stderr)
    print(f"  Client: {client.get('name', '?')}", file=sys.stderr)

    result = call_gemini(prompt, model, api_key)

    if not result:
        print(f"  Primary model failed, trying fallback: {FALLBACK_MODEL}", file=sys.stderr)
        result = call_gemini(prompt, FALLBACK_MODEL, api_key)

    if not result:
        print("Error: both models failed to generate concepts", file=sys.stderr)
        sys.exit(1)

    # Clean output — strip before first #
    hash_idx = result.find("#")
    if hash_idx >= 0:
        result = result[hash_idx:]

    print(result)
    print(f"\n# Concepts generated with {model}", file=sys.stderr)


if __name__ == "__main__":
    main()
