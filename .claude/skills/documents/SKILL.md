---
name: documents
description: |
  Extract text from documents, analyze videos, and convert file formats.
  Use contentcli for document extraction, video analysis, and format conversion.
---

# Document Extraction, Video Analysis & Format Conversion

Unified content processing via `contentcli`.

## Document Extraction

```bash
contentcli extract --url "https://example.com/report.pdf"
contentcli extract --url "https://example.com/report.pdf" --pdf-mode ocr    # scanned PDFs
contentcli extract --url "https://example.com/data.xlsx" --format json
contentcli extract --url "https://example.com/contract.docx"
```

PDF modes: `auto` (default — text first, OCR fallback), `fast` (text only), `ocr` (force OCR for scanned docs).

### Decision Tree

1. **CSV / TXT / MD** → can just `Read` directly (they're text)
2. **PDF / DOCX / XLSX URL** → `contentcli extract --url <url>` (Firecrawl parses server-side)
3. **Scanned PDF** → `contentcli extract --url <url> --pdf-mode ocr`
4. **User-uploaded documents** → arrive as S3 URLs in media attachments, use `contentcli extract --url <s3_url>`
5. **Never** `Read` binary files (.pdf, .docx, .xlsx) directly

### Output Formats

- `--format markdown` (default) — clean markdown to stdout
- `--format json` — structured `{"content": "...", "metadata": {...}, "source": "..."}`

## Video Analysis

```bash
contentcli analyze --url "https://youtube.com/watch?v=VIDEO_ID" --prompt "Summarize this video"
contentcli analyze --url "https://tiktok.com/@user/video/123" --prompt-file analysis-template.md
contentcli analyze --url "https://instagram.com/reel/ABC123" --prompt "What products are shown?" --raw
contentcli analyze --file /tmp/video.mp4 --prompt "Describe this video" --raw
```

- YouTube → Gemini native (no download)
- TikTok / Instagram → yt-dlp download → Gemini upload → analysis
- Direct MP4 URL → download → Gemini upload → analysis
- Local file (`--file`) → upload directly to Gemini (no download step)
- Default model: `gemini-2.5-pro`, override with `--model`
- `--raw` for plain text output (no JSON wrapper)
- `--url` and `--file` are mutually exclusive

### Instagram Reels (preferred workflow)

yt-dlp often fails on Instagram (login required). Use `instagramcli` to get the direct CDN URL, download locally, then analyze with `--file`:

```bash
# 1. Get video_url from media info
instagramcli media info --code <SHORTCODE> 2>&1 | python3 -c "import json,sys; print(json.load(sys.stdin)['video_url'])"

# 2. Download with curl (CDN URLs are time-limited, download immediately)
curl -L -o /tmp/reel.mp4 "<video_url>"

# 3. Analyze the local file
contentcli analyze --file /tmp/reel.mp4 --prompt "..." --raw
```

### YouTube-Specific Features

For YouTube metadata, transcripts, comments, trends, and channel analysis, use `youtubecli`:

```bash
youtubecli transcript --id "VIDEO_ID"                    # captions
youtubecli video --id "VIDEO_ID"                         # metadata
youtubecli comments --id "VIDEO_ID"                      # comments
youtubecli search --query "topic"                        # search
youtubecli trends                                        # trending
youtubecli analyze channel --id "@handle"                # channel analysis
```

## Format Conversion

### Video → MP4

```bash
contentcli convert video --input clip.webm
contentcli convert video --input clip.mov --output result.mp4
```

Uses `ffmpeg` (H.264 + AAC). Input can be any format ffmpeg supports (WebM, MOV, AVI, MKV, etc.).

### Image → PNG (HEIC, WebP, etc.)

```bash
contentcli convert image --input photo.heic
contentcli convert image --input photo.webp --output result.png
```

Uses ImageMagick (preferred) or ffmpeg as fallback.

### XLSX → CSV

```bash
contentcli convert xlsx --input data.xlsx
contentcli convert xlsx --input data.xlsx --output result.csv
```

Multi-sheet XLSX produces one CSV per sheet: `data_Sheet1.csv`, `data_Sheet2.csv`, etc.

