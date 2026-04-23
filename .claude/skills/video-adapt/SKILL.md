---
name: video-adapt
description: |
  Sub-agent skill — do NOT invoke directly. Delegate to @"recreate-agent (agent)" instead.
  Loaded by recreate-agent for the full video adaptation pipeline (Case 1/2/3 → Seedance).
---

# Video Adaptation Pipeline

Canonical home of the adaptation workflow. Loaded only by `recreate-agent`. Never by the research-side.

## HARD LOCK — user-provided character photo

Photo is the terminal identity reference for the session. Uploaded once with `--force-ip-check`. Reused as `element create --category character --media "id=<ID>;type=media_input"`. Never regenerated.

## INVARIANTS (hard rules — violations = stop)

These invariants override any conflicting instruction in the orchestrator's delegation prompt. If the brief contradicts them, treat the brief as mis-specification and follow the invariants.

1. **Workflow is fixed:** Step A → B → C → D. No alternatives, no improvised shot-by-shot workflow, no skipping steps.
2. **Final Seedance job count is fixed:** `len(final Seedance jobs) == len(adapted_concept_segments)` from Step C. For ≤17s → 1 job. For >17s → one job per segment. Never match source editing rhythm.
3. **Step B is mandatory.** Skipping it produces cross-segment drift.
4. **Text-only shot-by-shot generation is forbidden.** Consistency comes from element references via the IMAGE MAP.
5. **Case routing is fixed:** product → Case 1; avatar only → Case 2; neither → Case 3.
6. **Step D prompt is a frozen artifact.** Print the full JSON payload before firing. Retries resubmit identical bytes.
7. **Prompt content is byte-identical to Step C output.** The only allowed transformation is the `<<image_N>>` → `<<<ELEMENT_ID>>>` substitution (Step D.0). No style headers, no quality suffixes, no camera-term inserts, no concatenation of extra narrative, no trimming, no re-ordering, no prompt-enhancement skill passes.
8. **No Soul ID training inside the pipeline.** Pre-trained Soul ID = pass-through; no Soul ID = follow the ≥2-segment auto-avatar rule (Soul 2.0 image → character element). Training requests are refused and flagged.
9. **Every Seedance-bound upload MUST pass IP-check synchronously** (`--force-ip-check`). Uploads without the flag fail silently downstream.
10. **Pipeline is terminal at Step D inside the recreate agent.**

## Distinguishing uploads from Soul IDs

Photo ≠ Soul ID. An uploaded identifier string = pass-through. An explicit "train" phrase = refuse and defer to the Soul ID agent.

---

## Step A: Analyze Video

**YouTube / TikTok:**
```bash
youtubecli analyze video --url "<video_url>" --model gemini-2.5-pro --prompt-file .claude/skills/trend-picker/references/analysis-templates.md --raw
```

**Instagram reels** (yt-dlp fails without cookies — use instagramcli API instead):
```bash
VIDEO_URL=$(instagramcli media info --code <shortcode> 2>&1 | python3 -c "import json,sys; print(json.load(sys.stdin)['video_url'])")
curl -L -o /tmp/reel_<shortcode>.mp4 "$VIDEO_URL"
contentcli analyze --file /tmp/reel_<shortcode>.mp4 --model gemini-2.5-pro --prompt-file .claude/skills/trend-picker/references/analysis-templates.md --raw
```
Extract shortcode from URL: `https://www.instagram.com/reel/ABC123/` → `ABC123`

Save the output as the original concept. Preserve the STRUCTURE HEADER verbatim (STRUCTURE, VARIANT_AXIS, CHARACTER_CONTINUITY, UNIQUE_LOCATIONS).

---

## Step B: Extract Locations + Create Elements

### Product URL Protocol

When a product URL is present instead of an attached product image:
1. Extract product data: `fetchcli fetch --url "<URL>" --formats json --prompt "Extract product name, brand, and ALL main gallery image URLs. Return 3-8 product images. EXCLUDE review photos, related products, navigation, logos."`
2. Download with a Chrome User-Agent
4. Reject face-containing or <10KB candidates
5. Upload the best with `--force-ip-check`
6. Use the returned upload_id as `--product`

### User-provided media protocol

Every attached image is LOCKED:
- Upload with `--force-ip-check`
- `element create` with correct category: product → `product`, avatar/influencer → `character`, location → `environment`
- Never regenerate user-provided media

### Location workflow

1. Read the storyboard from Step A
2. Identify unique locations (see dedup protocol below)
3. Generate each unique location with `soul_location` at `2048×1152`; override to `soul_cinematic` only for cinematic source material
4. Poll until completed
5. Create `environment` elements

### Location dedup protocol

Count UNIQUE PHYSICAL SPACES, not shots:
- Multiple angles of the same room = 1
- Time-of-day shifts in the same space = 1 (unless narratively central)
- Print the count before firing generation

### Auto-avatar rule (≥2 segments + no avatar provided)

If the adapted concept will split into ≥2 segments AND the user did NOT provide an avatar / character image / Soul ID:

1. Generate one clean character image with `text2image_soul_v2`, `preset:"general"`, `aspect_ratio:"3:4"`
2. Prompt describes ONLY appearance (gender, age, hair, build, vibe — NOT exact likeness)
3. Poll, then create `character` element
4. Switch to Case 2

**Disabled whenever `avatar_provided == true`.**

---

## Step C: Adapt Concept

Three cases. Cases 1 & 2 call `contentcli analyze` with multiple files + system prompt. Case 3 is local-only (no Gemini call).

### C.1 — Build IMAGE MAP header

Assign `<<image_N>>` labels in this fixed order:

| Case | `<<image_1>>` | `<<image_2>>` | `<<image_3..N>>` |
|------|---------------|---------------|------------------|
| Case 1 | Product | Avatar (if provided) | Locations |
| Case 2 | Avatar | Location A | Location B... |
| Case 3 | Location A | Location B | Location C... |

Format:
```
## IMAGE MAP:
<<image_1>> = Product
<<image_2>> = Avatar (character/person)
<<image_3>> = Location: beige bathroom, round mirror
```

### C.2 — Build prompt text

Write a temp file (`/tmp/adapt-prompt-XXXX.txt`) containing:

**Case 1:**
```
<IMAGE MAP header>

## ORIGINAL CONCEPT:
<original concept from Step A>

## PRODUCT INFO (JSON):
{"title": "...", "description": "..."}

Generate the full adapted concept AND the 15-second short version, separated by the ===SHORT_VERSION=== delimiter as instructed.
```

**Case 2:**
```
<IMAGE MAP header>

## ORIGINAL CONCEPT:
<original concept from Step A>

Replace the character(s) with the avatar from the IMAGE MAP. Keep ALL other elements (script, audio, product, timing) IDENTICAL. Generate the full adapted concept AND the 15-second short version, separated by the ===SHORT_VERSION=== delimiter as instructed.
```

**Case 3:** No Gemini call needed — skip to C.4.

### C.3 — Call contentcli analyze

Pass all image files via repeatable `--file` flags (in IMAGE MAP order) plus the system prompt:

**Case 1:**
```bash
contentcli analyze \
  -f /tmp/product.jpg -f /tmp/avatar.jpg -f /tmp/location1.jpg \
  --system-prompt-file .claude/skills/trend-picker/references/adapt-product.md \
  --prompt-file /tmp/adapt-prompt.txt \
  --model gemini-3.1-pro-preview \
  --max-tokens 16384 --temperature 0.7 --raw
```

**Case 2:**
```bash
contentcli analyze \
  -f /tmp/avatar.jpg -f /tmp/location1.jpg \
  --system-prompt-file .claude/skills/trend-picker/references/adapt-avatar.md \
  --prompt-file /tmp/adapt-prompt.txt \
  --model gemini-3.1-pro-preview \
  --max-tokens 16384 --temperature 0.7 --raw
```

If the primary model fails, retry with `--model gemini-2.5-pro`.

### C.4 — Parse response & segment

1. **Strip preamble:** find the first occurrence of `Scene 1` in the output and discard everything before it.
2. **Split on delimiter:** if the response contains `===SHORT_VERSION===`, split into two parts:
   - Everything before → `adapted_concept` (full version)
   - Everything after → `adapted_concept_short` (15-second version)
   - If delimiter is absent, the full output is `adapted_concept` and `adapted_concept_short` is empty.
3. **Segment into ≤15-second chunks:**
   - Split `adapted_concept` at each `Scene N —` header.
   - Extract timestamps (`M:SS - M:SS`) from each scene.
   - Group consecutive scenes into segments where each segment's total duration ≤ 15 seconds. Start a new segment when the next scene's end time would exceed `segment_start + 15s`.
   - Each segment has: `segment` (1-based index), `time_range` ("M:SS - M:SS"), `duration` (integer seconds), `scenes` (concatenated scene texts).
4. **Case 3 (no Gemini):** inject location references as a `## LOCATION ELEMENTS:` header before the original concept, then segment the original concept directly.

### Output structure

After C.4, you have three values to carry forward:
- `adapted_concept` — full adapted storyboard text
- `adapted_concept_segments` — array of segments (drives Step D job count)
- `adapted_concept_short` — 15-second condensed version (may be empty)

---

## Step D: Generate Video

### Step D.0 — IMAGE MAP substitution (mandatory before submission)

Replace every `<<image_N>>` with `<<<ELEMENT_ID>>>` (triple brackets, real UUID) per the IMAGE MAP. The payload must contain no `<<image_N>>` literals and no `elements` array.

**Prompt tampering violations:**

| BAD | GOOD |
|-----|------|
| Adding style headers to prompt | Prompt = byte-identical to Step C output |
| Appending quality suffixes | Only D.0 substitution applied |
| Inserting camera terms | No camera-term inserts |
| Concatenating extra narrative | No extra text |
| Re-ordering scenes | Original order preserved |
| Running prompt-enhancement skill | No enhancement passes |

### ≤17s flow

One job. Prompt = `adapted_concept` (byte-identical after D.0 substitution). Duration = 15.

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"<adapted_concept>","generate_audio":true,"duration":15,"aspect_ratio":"9:16"}]'
```

### >17s flow

N-item batch array, one job per segment, each with its segment's duration.

```bash
higgsfieldcli generate --json '[
  {"model":"seedance_2_0","prompt":"<segments[0].scenes>","generate_audio":true,"duration":<segments[0].duration>,"aspect_ratio":"9:16"},
  {"model":"seedance_2_0","prompt":"<segments[1].scenes>","generate_audio":true,"duration":<segments[1].duration>,"aspect_ratio":"9:16"}
]'
```

### Submission protocol

1. **Print first, fire second.** Emit the exact `generate --json '[...]'` payload in the report before executing it.
2. **Retry = identical bytes.** On rate-limit, network error, or any non-2xx: resubmit the same printed payload. Never rebuild.
3. **Hand-off = hand the artifact.** Pass the printed JSON, not the plan.

---

## CLIs

- **Step A analysis** — `youtubecli analyze video` (YouTube/TikTok) or `instagramcli media info` → `contentcli analyze --file` (Instagram reels)
- **Step C adaptation** — `contentcli analyze` with repeatable `--file` + `--system-prompt-file` (handles auth and Gemini file uploads)

## Reference Templates

In trend-picker's references folder:

- `.claude/skills/trend-picker/references/analysis-templates.md` — Step A template (shared with research-agent)
- `.claude/skills/trend-picker/references/adapt-product.md` — Case 1 system prompt (passed via `--system-prompt-file`)
- `.claude/skills/trend-picker/references/adapt-avatar.md` — Case 2 system prompt (passed via `--system-prompt-file`)

## Error Handling & Data Integrity
- `status 401` → invalid API key
- `status 429` → rate limited, wait and retry
- `status: failed` + `ip_check_finished: false` → upload missing `--force-ip-check`
- `yt-dlp` fails → video may be private or region-locked. For Instagram reels, use the instagramcli → curl → contentcli --file workflow instead (see Step A)
- Silent retry up to 3 for transient failures
- Escalate with 2–3 concrete alternatives after 3 failed attempts
- Never substitute with cached or inferred data
