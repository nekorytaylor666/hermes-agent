---
name: trend-picker
description: |
  Sub-agent skill — do NOT invoke directly. Delegate to @"research-agent (agent)" instead.
  Loaded by research-agent sub-agent for social media research and trend discovery.
---

# Trend Picker

Unified social media research, ad intelligence, and trend discovery. Fetches data from all platforms, ranks by engagement, analyzes with AI, generates content concepts.

## CLIs

| CLI | Platform | Binary |
|-----|----------|--------|
| **instagramcli** | Instagram | `instagramcli` |
| **tiktokcli** | TikTok | `tiktokcli` |
| **youtubecli** | YouTube | `youtubecli` |
| **trendscli** | YouTube Shorts (external service) | `trendscli` |
| **adscli** | Meta, TikTok ads | `adscli` |
| **fetchcli** | Web (any URL) | `fetchcli` |
| **contentcli** | Documents + video analysis | `contentcli` |

---

## Instagram (instagramcli)

API: EnsembleData. All user commands accept `--username` / `-u` directly — the CLI resolves username→ID automatically. Pass `--user-id` only if you already have the numeric pk.

### User Research
```bash
instagramcli user info -u "alexmitch6"                            # profile (pk, username, full_name, is_verified)
instagramcli user details -u "alexmitch6"                         # detailed profile (bio, links, recent posts)
instagramcli user basic-stats -u "alexmitch6"                     # followers, following, profile pic
instagramcli user posts -u "alexmitch6" --depth 2                 # recent posts (depth 1 = ~10 posts)
instagramcli user reels -u "alexmitch6" --depth 3 --sort views    # reels sorted by play_count (flat output)
instagramcli user tagged -u "alexmitch6"                          # posts where user is tagged
instagramcli user followers -u "alexmitch6"                       # follower count
```

**Reels are always flat.** `user reels` returns `{"items": [{code, play_count, like_count, comment_count, caption, video_duration, taken_at, clips_metadata, ...}], "count": N}`. Use `--sort views` to rank by play_count descending, `--sort likes` for like_count, `--sort date` for taken_at.

### Download Assets (profile pic + media thumbnails)
```bash
instagramcli user download -u "alexmitch6" -o /tmp/alexmitch6
```
Downloads profile picture and up to 12 recent media thumbnails to the output directory, automatically resized to 2K (max 2048px). Returns JSON with `{username, output_dir, files: [...]}`. Use this when you need actual image files (e.g. for face references, content generation).

### Content Discovery
```bash
instagramcli search -q "keyword"                    # search users, hashtags, places
instagramcli music --id <music_id>                   # posts using a specific audio
```

### Post Analysis
```bash
instagramcli media info --code <shortcode>           # post details by shortcode
instagramcli media info --code <shortcode> --comments 50  # include up to 50 comments
instagramcli media comments --code <shortcode>       # paginated comments (resolves code→media_id)
instagramcli media comments --media-id <numeric_id>  # paginated comments by media ID
```

### Pagination
All paginated endpoints use `--cursor` for the next page token. Each response includes a cursor for the next page when more results are available.

### Response Shapes
- `user info` → `{"pk": "123", "username": "...", "full_name": "...", "is_verified": true, ...}`
- `user basic-stats` → `{"id": "123", "username": "...", "full_name": "...", "followers": 2482958, "following": 350, "profile_pic_url": "..."}`
- `user reels` → `{"items": [{code, play_count, like_count, comment_count, video_duration, taken_at, caption: {text: "..."}, clips_metadata: {music_info: ...}, ...}], "count": N}`
  - ER = (like_count + comment_count) / play_count
  - `clips_metadata.music_info.music_asset_info` has `title` and `display_artist`
- `media info` → GraphQL response: `{"__typename": "GraphVideo", "shortcode": "X", "id": "...", "is_video": true, ...}`
  - Engagement is in `edge_media_preview_like.count` and `edge_media_to_comment.count`
  - For reels analysis, prefer `user reels --sort views` instead — it has flat engagement data
- `download` → `{"username": "...", "output_dir": "/tmp/...", "files": ["/tmp/.../profile_pic.jpg", ...]}`

---

## TikTok (tiktokcli)

API: EnsembleData. All endpoints return JSON; paginated endpoints include `nextCursor`.

### User Research
```bash
tiktokcli user info -u "charlidamelio"                          # profile (id, secUid, stats)
tiktokcli user posts -u "charlidamelio" --depth 2               # user posts (depth 1 = ~30 posts)
tiktokcli user posts-from-secuid --sec-uid <secUid> --depth 1   # posts by secUid
tiktokcli user search -q "brand"                                # search users by keyword
tiktokcli user followers --id <id> --sec-uid <secUid>           # followers (requires both id + secUid from user info)
tiktokcli user followings --id <id> --sec-uid <secUid>          # followings
tiktokcli user likes --sec-uid <secUid>                         # liked posts
```

**Important:** Call `user info` first to get `id` and `secUid` (returned in response).

### Content Discovery (keyword + hashtag)
```bash
tiktokcli keyword search -q "skincare" --period 7              # search posts by keyword (~20/page, period in days: 1,7,30,90,180)
tiktokcli keyword search -q "skincare" --period 7 --sort 1     # sort: 0=relevance, 1=most liked, 2=most recent
tiktokcli keyword search -q "skincare" --country US            # geo-targeted results
tiktokcli keyword full-search -q "skincare" --period 7         # full search (all pages, single call)
tiktokcli hashtag search -n "skincare"                         # hashtag posts (~20/page)
tiktokcli hashtag full-search -n "skincare" --days 7           # all hashtag posts within N days (single call)
```

### Built-in Ranking (--rank flag)
All keyword and hashtag commands support `--rank` to return viral-scored results directly (no piping needed):
```bash
tiktokcli keyword search -q "skincare" --period 7 --rank --top-k 3                    # top 3 by viral score
tiktokcli keyword search -q "skincare" --period 7 --rank --top-k 10 --min-views 0     # trend discovery preset
tiktokcli hashtag search -n "skincare" --rank --top-k 5                                # top 5 hashtag videos
tiktokcli hashtag full-search -n "skincare" --days 7 --rank --top-k 3 --min-views 50000  # brand/competitor preset
```
Ranking flags: `--rank` (enable), `--top-k N` (default 3), `--min-views N` (default 50000), `--max-age N` days (default 7).
Viral score = velocity (views/day) × engagement rate ((likes+comments)/views×100). Falls back to raw views if no videos pass filters.

### Music / Sounds
```bash
tiktokcli music search -q "viral"                              # search sounds by name
tiktokcli music search -q "viral" --sort 1                     # sort: 0=relevance, 1=most used, 2=most recent, 3=shortest, 4=longest
tiktokcli music posts --id <music_id>                          # posts using a sound
tiktokcli music details --id <music_id>                        # sound details
```

### Post Analysis
```bash
tiktokcli post info --url "https://www.tiktok.com/@user/video/123"  # post details by URL
tiktokcli post multi --ids "123;456;789"                            # multiple posts by ID
tiktokcli post comments --id <aweme_id>                             # comments
tiktokcli post comment-replies --id <aweme_id> --comment-id <cid>   # comment replies
```

### Live Search
```bash
tiktokcli live search -q "keyword"                             # search live streams
tiktokcli live search -q "keyword" --country US                # geo-targeted live search
```

All paginated commands support `--cursor` for pagination.

---

## YouTube (youtubecli)

### Data Retrieval
```bash
youtubecli search -q "query"                    # search
youtubecli video --id "VIDEO_ID"                # video details
youtubecli transcript --id "VIDEO_ID"           # transcript
youtubecli comments --id "VIDEO_ID"             # comments
youtubecli channel --id "@handle"               # channel info (default: popular sort)
youtubecli channel --id "@handle" --sort recently_uploaded  # latest videos first
youtubecli trends --category now                # trending
```

### Response Shapes

- `channel` → `{about, channel, videos_sections: [{videos: [{video_id, id, title, link, views, length, published_time, thumbnail}]}], shorts_sections}`
  - `videos_sections` default sort is **popular** (by views). Use `--sort recently_uploaded` for chronological.
  - `video_id` and `id` are both the YouTube video ID (e.g. `"oA85M9JHsW0"`)
  - `published_time` is relative: `"2 months ago"`, `"1 year ago"`
  - `length` is duration string: `"14:18"`
- `search` → `{channels, videos: [{video_id, id, title, link, views, length, published_time, channel: {id, title}, thumbnail}], shorts, pagination}`
  - Same field names as channel videos. `video_id` = `id`.
  - `channel.id` is the uploader's channel ID — use to filter results to a specific creator
- `video --id "ID"` → `{video: {video_id, id, title, views, likes, length_seconds, published_time, description, thumbnail, ...}, channel, comment}`
  - Data is nested under the `video` key (NOT top-level)
  - `published_time` is an absolute date here: `"Feb 13, 2026"`
  - `length_seconds` is duration in seconds (integer)
  - `video_id` = `id` = the YouTube video ID

### Gemini-Powered Analysis
```bash
youtubecli analyze video --url "URL"                    # video analysis (default model)
youtubecli analyze video --url "URL" --model gemini-2.5-pro  # video analysis (custom model)
youtubecli analyze video --url "URL" --prompt-file analysis.md --raw  # raw text output
youtubecli analyze trends                               # trend analysis
youtubecli analyze channel --id "@handle"               # channel analysis
```

YouTube and TikTok videos are downloaded via yt-dlp and uploaded to Gemini. **For Instagram reels, use the instagramcli → curl → `contentcli analyze --file` workflow** (see Step 3 below) — yt-dlp requires Instagram cookies not available in the agent container. Flags: `--model`/`-m` (override model), `--prompt-file` (read prompt from file), `--system-prompt`/`-s`, `--raw`/`-r` (plain text, no JSON).

---

## YouTube Shorts Trends (trendscli)

Read-only CLI over the internal FNF Data Ingestion API. Returns breakout shorts and growing channels already discovered and enriched by our trending pipeline (VidIQ breakout_score, views-per-hour, channel growth month-over-month). No external API quota cost — all data is from our own DB.

### Discovery (preset commands)
```bash
trendscli viral-now --hours 6 --limit 20                  # videos breaking out right now
trendscli growth-leaders --days 30 --min-subs-growth 10000 --limit 20   # fastest-growing channels
trendscli competitor <channel_id> --limit 20              # all tracked videos of a channel
```

### Raw queries (full filter control)
```bash
trendscli videos --min-breakout 70 --min-vph 1000 --limit 50
trendscli channels --country US --min-subs 100000 --format-contains animation
trendscli run <run_id>                                    # trending-shorts discovery run status
trendscli trending <query_id>                             # trending analysis status
```

### When to use trendscli vs youtubecli
- **trendscli** — you want *our* pre-ranked, pre-enriched YouTube Shorts trending data (breakout scores, VPH, monthly growth). Fast, no external quota.
- **youtubecli** — you need live search/fetch of arbitrary YouTube content (any video by ID, transcripts, comments, public trending).

All IDs (`channel_id`, `video_id`, `run_id`) must come from a prior `trendscli` response — this CLI does not support external YouTube IDs.

---

## Ad Libraries (adscli)

### Meta (Facebook/Instagram)
```bash
adscli meta search -q "keyword" --active-status active --sort-by impressions_high_to_low
adscli meta search --page-id <id> --active-status active
adscli meta page --page-id <id>
```

### TikTok Ads
```bash
adscli tiktok search -q "keyword" --sort-by unique_users_seen_high_to_low
adscli tiktok advertiser --id <advertiser_id>
```

### Finding Winners (default filters)

1. **Active ads only:** `--active-status active`
2. **Sort by reach:** `--sort-by impressions_high_to_low` (Meta) / `unique_users_seen_high_to_low` (TikTok)
3. **Longevity filter:** After fetching, only present ads running 3+ days
   - 3-7 days: testing phase
   - 7-14 days: likely profitable
   - 14-30 days: proven winner
   - 30+ days: evergreen creative

---

## Web Content (fetchcli)

```bash
fetchcli fetch --url "https://example.com"                                              # read URL → markdown
fetchcli fetch --url "https://example.com" --formats json --prompt "Extract key data"   # structured JSON extraction (compact ~2-3KB)
fetchcli search --query "latest news"                                                    # web search
fetchcli walk --url "https://example.com" --limit 10                                   # crawl site
fetchcli map --url "https://example.com"                                                 # map site URLs
```

`--prompt` and `--schema` run LLM extraction server-side and return structured JSON. **Do NOT add `markdown` to formats for large pages** (Amazon, e-commerce) — they produce 100KB+ that truncates the output. Use `--formats json` alone for product pages. Use `--include-tags`/`--exclude-tags` to filter HTML content and reduce output size.

---

## Viral Content Analysis Pipeline

Full workflow for analyzing competitor content and generating adapted concepts.

### Step 0: Identify Product
From the user's input (image, text, URL, brand name) determine:
- **Brand** — exact brand name (e.g. "CeraVe", "Dyson", "Nike")
- **Product** — specific product (e.g. "moisturizing cream", "airwrap", "air max")
- **Category** — broad niche (1 word: "skincare", "haircare", "sneakers", "fitness")

Do NOT invent creative search phrases. Just extract what the product IS.

### Step 1: Discover Content
Run ALL of these in parallel. Never skip any group.

**Emit all Bash calls from groups 1a, 1b (initial hashtag/sound fetch), 1c, and 1d in a SINGLE response turn — do not wait for one group to finish before issuing the next. Multiple Bash tool calls in one turn execute concurrently.**

**1a. Brand/product search on platforms** (exact brand name):
```bash
tiktokcli keyword search -q "<brand>" --period 7
instagramcli search -q "<brand>"
tiktokcli keyword search -q "<brand> <product>" --period 7
instagramcli search -q "<brand> <product>"
```

**1b. Trending hashtags + sounds in category** (platform tells you what's trending, not Claude):
```bash
tiktokcli hashtag search -n "<category>"
tiktokcli music search -q "<category>"
```
Then use top 3 returned hashtags to search — emit these follow-up calls together in a single turn:
```bash
tiktokcli hashtag search -n "<trending_hashtag>"
instagramcli search -q "<trending_hashtag>"
```

**1c. Ad library — proven winners** (brands spending money = working creatives):
```bash
adscli meta search -q "<category>" --active-status active --sort-by impressions_high_to_low
adscli tiktok search -q "<category>" --sort-by unique_users_seen_high_to_low
```

**1d. Web context** (what's trending in the niche right now):
```bash
fetchcli search --query "<category> trending tiktok 2026"
```

### Step 2: Rank Videos
Use tiktokcli's built-in `--rank` flag (no piping needed). For Instagram, pipe through rank_videos.py:
```bash
tiktokcli keyword search -q "<brand>" --period 7 --rank --top-k 3
tiktokcli hashtag search -n "<trending_hashtag>" --rank --top-k 3
instagramcli search -q "<brand>" | python3 .claude/skills/trend-picker/scripts/rank_videos.py --top-k 3
instagramcli search -q "<trending_hashtag>" | python3 .claude/skills/trend-picker/scripts/rank_videos.py --top-k 3
```

Viral score = velocity × engagement_rate. Default: 7-day window, 50K min views, top 3.

**Freshness defaults by intent (tiktokcli --rank presets):**
- Trend discovery → `--rank --max-age 3 --min-views 0 --top-k 10`
- Brand/product research → `--rank --max-age 7 --min-views 50000 --top-k 3` (default)
- Deep historical → `--rank --max-age 30 --min-views 10000 --top-k 10`

**Fallback:** ranking auto-falls back to sorting by raw views if no videos pass filters.

Collect all top-ranked videos across sources, deduplicate, take overall top 5.

### Step 3: Analyze with Gemini (scene-by-scene storyboard)

**Run ALL video analyses in parallel — emit every `youtubecli analyze video` / `contentcli analyze` Bash call for all top-ranked videos in a SINGLE response turn. Never analyze one video and wait for results before starting the next. Gemini calls are the slowest step; parallelizing them is critical.**

**YouTube / TikTok** — use youtubecli directly (yt-dlp handles download):
```bash
youtubecli analyze video --url "<video_url>" --model gemini-2.5-pro --prompt-file .claude/skills/trend-picker/references/analysis-templates.md --raw
```

**Instagram reels** — yt-dlp fails without cookies. Use instagramcli → curl → contentcli --file:
```bash
# 1. Get direct video URL from Instagram API
VIDEO_URL=$(instagramcli media info --code <shortcode> 2>&1 | python3 -c "import json,sys; print(json.load(sys.stdin)['video_url'])")

# 2. Download locally (CDN URLs expire quickly)
curl -L -o /tmp/reel_<shortcode>.mp4 "$VIDEO_URL"

# 3. Analyze local file with Gemini
contentcli analyze --file /tmp/reel_<shortcode>.mp4 --model gemini-2.5-pro --prompt-file .claude/skills/trend-picker/references/analysis-templates.md --raw
```

For multiple Instagram reels: emit all 3 instagramcli info fetches together, then all 3 curl downloads together, then all 3 contentcli analyze calls together — each group in its own single turn.

Extract the shortcode from the reel URL: `https://www.instagram.com/reel/DGONU8bvIZJ/` → shortcode is `DGONU8bvIZJ`.

Outputs a hyper-detailed scene-by-scene production blueprint: Scene Label, Shot Type, Visual Description, Audio Script, timestamps. Uses Gemini 2.5 Pro.

### Step 4: Generate Concepts
```bash
echo '{"analyses": [...], "client": {...}}' | python3 .claude/skills/trend-picker/scripts/generate_concepts.py
```

Generates 3 NEW video concepts based on the analyzed references + client profile. Concepts include HOOK, RETENTION, REWARD, AUDIO, SCRIPT.

### Step 5: Visual Preview (optional)
Delegate to `/image-skill` or `/video-skill` for previews. Never call CLI directly.

---

## Video Adaptation — NOT IN THIS SKILL

Full video adaptation (Case 1/2/3 → Seedance) lives in a separate skill and agent:

- **Skill:** `video-adapt` — canonical Step A → D, INVARIANTS, IMAGE MAP, auto-avatar rule.
- **Agent:** `@recreate-agent` — the only agent that loads `video-adapt` and runs the adapt pipeline.

This skill covers research and Mode A video analysis (classify + storyboard + STOP). If a brief arriving at research-agent includes a source video URL with an explicit adapt signal (recreate / reproduce / "сделай как это" / `mode=adapt` + product/brand context), research-agent refuses and flags the orchestrator to re-route to `@recreate-agent`. Adaptation is never run from here.

Video analysis (Step A) uses `youtubecli analyze video` — a compiled Go binary shared across agents. Video adaptation (Step C) uses `contentcli analyze` with `--system-prompt-file` pointing to this skill's reference templates (`adapt-product.md`, `adapt-avatar.md`).

---

## Viral Analysis (on-demand)

When user explicitly asks "why is this video viral" / "analyze why this works" — use the strategic template instead.

**YouTube / TikTok:**
```bash
youtubecli analyze video --url "<video_url>" --model gemini-2.5-pro --prompt-file .claude/skills/trend-picker/references/viral-analysis.md --raw
```

**Instagram reels** (same instagramcli → curl → contentcli --file pattern as Step 3):
```bash
VIDEO_URL=$(instagramcli media info --code <shortcode> 2>&1 | python3 -c "import json,sys; print(json.load(sys.stdin)['video_url'])")
curl -L -o /tmp/reel_<shortcode>.mp4 "$VIDEO_URL"
contentcli analyze --file /tmp/reel_<shortcode>.mp4 --model gemini-2.5-pro --prompt-file .claude/skills/trend-picker/references/viral-analysis.md --raw
```

Returns: CONCEPT, HOOK, RETENTION MECHANISMS, REWARD, AUDIO & MUSIC, SCRIPT. This is a strategy analysis, not a production blueprint.

---

## Mode C — Creator DNA (persona-clone preflight)

**Trigger:** orchestrator passes `mode=creator_dna` explicitly in the delegation prompt. Never auto-activated. Used only when orchestrator is building a new persona that should hit the same audience as a reference creator.

**Purpose:** extract cross-reel behavioral + kinetic + audio DNA from a reference creator so downstream stages (soul-id, image generation, recreate-agent Case 2) can transplant that DNA onto a new persona. This is DIFFERENT from Step A (per-reel production storyboard) and from Mode G (metadata-level visual summary).

**Workflow:**

1. **Pull top reels** — use platform CLI to get the creator's highest-viewed reels, ranked:
   ```bash
   instagramcli user clips-gql --user-id <id> --sort-by-views   # Instagram
   tiktokcli user posts --sec-uid <secUid>                       # TikTok
   ```
   Take top 3 by default, top 5 only when orchestrator requests deep mode.

2. **Analyze each reel with Gemini + creator-dna template** — emit all N Bash calls in a **single response turn** (parallel):
   ```bash
   youtubecli analyze video --url "<reel_url>" --model gemini-2.5-pro \
     --prompt-file .claude/skills/trend-picker/references/creator-dna.md --raw
   ```
   Each call returns one JSON doc matching the `creator-dna.md` contract. Do not issue them one at a time.

3. **Aggregate into cross-reel DNA** — compute the signatures that repeat across ≥2 reels. Retain per-reel JSONs (they will be consumed individually by recreate-agent Case 2). Produce one aggregate report:
   ```json
   {
     "creator": "@handle",
     "reels_analyzed": 3,
     "per_reel": [{"url": "...", "dna": {...}}, ...],
     "aggregate_dna": {
       "stable_visual": [...],
       "stable_kinetic": [...],
       "stable_audio": [...],
       "stable_narrative": [...],
       "replicable_signatures": [...],
       "non_replicable_signatures": [...]
     }
   }
   ```

4. **Upload the aggregate report** via `higgsfieldcli upload-file --file /tmp/creator-dna-<handle>.json` and return only the public `url` plus reel URL list to the orchestrator.

**Output contract (what research-agent returns to orchestrator):**

```json
{
  "mode": "creator_dna",
  "creator": "@handle",
  "reels_analyzed": 3,
  "reel_urls": ["url1", "url2", "url3"],
  "dna_report_url": "https://...",
  "aggregate_summary": {
    "stable_visual": ["3-5 bullets"],
    "stable_kinetic": ["3-5 bullets"],
    "replicable_signatures": ["top 3 traits to transplant"]
  }
}
```

**Failure policy:** yt-dlp fails on 1–2 reels → continue with remaining ≥1. All fail → escalate to orchestrator with alternatives. Never fabricate DNA from metadata alone.

**What Mode C does NOT do:**
- Does not train Soul IDs (soul-id-agent owns that)
- Does not generate images or videos (image-agent / recreate-agent own that)
- Does not run Step A per-reel storyboard adaptation (recreate-agent Step A owns that; Mode C and Step A use different templates for different outputs)

---

## Scripts

```
scripts/
├── rank_videos.py         # Viral score ranking (velocity x ER) — only needed for instagramcli piping; tiktokcli has --rank built-in
├── generate_concepts.py   # Gemini 3.1 Pro — 3 new concepts from analyses — research-only

└── analyze_video.py       # DEPRECATED — use `contentcli analyze` or `youtubecli analyze video` instead
```

## Reference Templates

```
references/
├── analysis-templates.md  # Scene-by-scene storyboard analysis (default) — shared with recreate-agent
├── viral-analysis.md      # Strategic viral analysis (on-demand only) — research-only
├── creator-dna.md         # Mode C: cross-reel creator DNA extraction — research-only
├── adapt-product.md       # Case 1: product adaptation prompt — used ONLY by @recreate-agent via video-adapt
├── adapt-avatar.md        # Case 2: avatar replacement prompt — used ONLY by @recreate-agent via video-adapt
└── concept-generation.md  # Concept generation guidelines — research-only
```

## Error Handling

All CLIs output JSON to stdout, errors to stderr. Common:
- CLI not configured → check shell environment
- `status 401` → invalid API key
- `status 429` → rate limited, wait and retry
- yt-dlp fails → video may be private or region-locked

## Data Integrity

Rules for handling source material (URLs, uploads, analysis outputs). Apply to every tool in this skill, especially `youtubecli analyze video`.

- **Work only with user-provided inputs.** Do not pull from cache, prior sessions, `/tmp/*` artifacts, or adjacent files unless the user explicitly asks for it. The URL or file the user handed you is the only valid source.
- **Retry transient tool failures silently up to 3 times.** Download/upload/API errors (HTTP 4xx/5xx, timeouts, `yt-dlp` fails, Gemini upload 403) get 3 attempts without commentary.
- **URL fetching fallback chain.** For web content retrieval specifically: (1) `fetchcli fetch` (up to 3 retries), (2) `fetchcli search` with the URL or domain as query, (3) `WebFetch` built-in tool as final fallback. Only proceed to the next tier after the previous one is exhausted.
- **After all tiers are exhausted, escalate with alternatives.** Surface the blocker + 2–3 concrete alternatives the user can choose from (different endpoint, different tool, direct file upload, skip step). Never silently substitute with cached or inferred data.
