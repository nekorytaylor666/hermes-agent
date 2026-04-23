# Orchestration Rules

## Persona-Clone Trigger (Audience-Parity)

Fires only after Rule 0 is confirmed NOT applicable (no user-supplied source video URL with adapt intent). Activate when ALL four conditions hold: (a) brief references an existing creator (`@username` or platform URL to a profile, not a single video), (b) intent is to create a **new** persona/influencer, (c) phrasing implies audience parity ("hit the same audience", "like @X but not a copy", "such as @X", "under the same audience as @X"), (d) output is multi-post / multi-reel / content plan (not a single one-shot).

When triggered, do NOT proceed to soul-id-agent or generation until the user picks depth via `AskUserQuestion`: **Deep** (video-DNA pipeline: reel-level Gemini analysis + adaptation per reel, ~5-10 min, higher cost) or **Quick** (metadata-only research, fast and cheap).

### Deep Path

1. `@"research-agent (agent)"` with explicit `mode=creator_dna` — returns aggregate DNA report URL + top-3 reel URLs.
2. Orchestrator generates ONE base portrait of the persona via direct t2i call (`text2image_soul_v2`, neutral pose, clean outfit, face-forward, no props — `nano_banana_2` is FORBIDDEN on this path, it produces a non-editorial look that poisons LoRA training).
3. This single base kadr forks into TWO ASYNC BRANCHES that never block each other:
   - **Branch V (video, starts immediately):** `higgsfieldcli upload --force-ip-check` -> `higgsfieldcli element create --category character` -> pass the resulting `character_element_id` to every reel `@"recreate-agent (agent)"` in parallel (Case 2, source = reel URL from step 1). Recreate-agent does NOT build its own element — it uses the shared one via `<<<element_id>>>` in the Seedance prompt.
   - **Branch I (image, runs in parallel):** same base kadr -> `nano_banana_2` produces 4 pose/outfit variations with the base kadr wired in as the reference image via the correct reference field per the model schema (NOT a generic `image_urls` guess — verify the field name before the call) -> `@"soul-id-agent (agent)"` trains LoRA on the 5-kadr dataset -> once Soul ID completes, `@"image-agent (agent)"` generates carousel/stills via Soul 2.0 with `soul_id`.
4. Reels NEVER wait for Soul ID training — only the carousel waits on Branch I.
5. The orchestrator never writes video prompts on this path.

### Quick Path

Current behaviour (metadata research -> soul-id -> direct image/video generation).

Cache the DNA report URL in the session artifact list so follow-up requests in the same chat reuse it instead of re-analyzing.

---

## Shared-First Fan-Out

Default behavior when spawning >=3 parallel sub-agents where an asset is IDENTICAL across every output (not similar, not "kind of the same" — identical). Most common cases: one product across N videos, one brand kit across N posts, one source video for N recreate branches, one location for N shots, one persona across N reels.

Before the fan-out, the orchestrator pre-builds each identical asset ONCE and passes the resulting artifact IDs to every fan-out delegation prompt as givens (same standing as a user-provided URL or file path). The orchestrator does NOT instruct sub-agents on how to use the IDs — it just provides them. Sub-agents handle them as first-class inputs.

### Canonical shared artifacts to consider

`product_element_id` (upload + IP-check + element create) + extracted facts; `brand_kit` (brief + logo element + color palette); `character_element_id` / `soul_id` (when a single persona spans multiple outputs); `source_video_dna` (research/analysis result for recreate fan-outs); `location_element_id` / `prop_element_id`.

### How to build

If the asset is simple (clean user-provided image, plain facts), direct CLI is fine (`upload --force-ip-check` + `element create`). If the asset requires multi-step discovery (product URL fetch with image filtering, brand style extraction, viral video DNA analysis), delegate ONE exploratory sub-agent call to produce the artifact, then reuse its output across the fan-out. Never attempt fragile discovery (e.g. Amazon image filtering, JS-rendered SPAs) directly in the orchestrator when a dedicated skill exists.

### Why

Without this, every parallel sub-agent re-runs the same shared-asset build (fetch -> download -> upload -> IP-check -> element). On N=10 that is ~200+ duplicate tool calls, per-agent turn-limit exhaustion, and partial output where some videos land with the shared asset and some without.

### When NOT to apply

- N <= 2 outputs (overhead >= savings)
- Assets are similar but not identical across outputs (e.g. 5 different products in a campaign — products are per-instance, but brand/location may still be shared)
- A single terminal agent produces N outputs internally (e.g. amazon-listing-agent, image-agent batch, cinematic-long-video) — the agent handles sharing inside its own skill
- Uncertain whether the asset is truly identical — fall back to default (each fan-out agent discovers its own), which is always safe

Scope of pre-built artifacts is the CURRENT request — do not cache across user turns or sessions.

---

## Delegation Pre-Flight

### Read User-Provided Media First

If the user's message includes any media URL or attached image, view and understand it BEFORE delegating. Download URLs to local files first (`curl -sL -o /tmp/<name>.jpg "<url>"`, then Read). Pass BOTH the content description AND the original path/URL in the delegation prompt — sub-agents need the actual asset, not just a text description.

### Attachment Path Resolution

When an inline attachment (`[Image: source: <filename>]`) is not at the expected path, ask the user to re-share. Do NOT fall back to text-description delegation.

### Identity Continuity Preflight

Before delegating persona/character content, check: (a) named/implied persona with a face? (b) appears across ≥2 generations? (c) no existing identity source (photo, Soul ID, element)? If (a)+(b) yes and (c) no → Soul ID bootstrap via `@"soul-id-agent (agent)"` first.

Does not apply to: single one-offs, product shots with incidental humans, content where identity source already exists.

### Minimal Delegation — Pass WHAT, Not HOW

Pass only: (1) user's goal in one sentence, (2) assets with paths/URLs, (3) user constraints (length, format, platform). Do NOT prescribe workflow steps, model names, CLI flags, or pipeline stages. Sub-agents own their method via their skill's invariants.

### Marketing Video >15s

Each marketing clip is limited to 15s. Offer to split into multiple connected clips. Wait for user confirmation, then include the split plan in the delegation prompt.
