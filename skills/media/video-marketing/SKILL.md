---
name: video-marketing-skill
description: |
  Sub-agent skill — do NOT invoke directly. Delegate to @"marketing-agent (agent)" instead.
  Loaded by marketing-agent sub-agent for product ad and marketing video tasks.
---

## Flow

```
User: product photo/URL + prompt
  → If URL given: extract product data via fetchcli (see Product URL Extraction below)
  → If brand style requested: run Brand Style Extraction (see below) → build Brief → apply to generation
  → Route to matching reference (see Routing table)
  → Build prompt from reference template (with Brand Brief overrides if active)
  → Obtain product photo MEDIA_ID (upload tool not yet exposed — user-supplied or out-of-band)
  → higgsfield_generate({"requests": [{model: seedance_2_0, prompt + medias, ...}]}) — returns job_ids immediately (fire-and-forget)
```

---

## Product URL Extraction

When user provides a product URL (Amazon, Shopify, AliExpress, any e-commerce), extract product data automatically before generation. **Do NOT pause for user confirmation** — if the request contains a URL + generation intent, run extraction then proceed immediately.

### Step 1: Extract structured product data + images

Use `fetchcli fetch` with **`--formats json` only** and `--prompt` to extract product data and gallery images in a single call.

**CRITICAL: Do NOT add `markdown` to the formats.** Marketplace pages produce 100KB+ of markdown that will truncate the output. The `json` format alone returns product info AND image URLs in ~2-3KB.

```bash
fetchcli fetch \
  --url "USER_URL" \
  --formats json \
  --prompt "Extract product name, brand, price, currency, selected color/variant, full description, all feature bullet points, technical specifications, and ALL product image URLs from the main gallery (front, side, back, close-up, packaging). Classify each image by section: main_gallery, description, review, other. Return 3-8 unique product gallery images. EXCLUDE user review photos, related products, navigation, banners, color swatch icons, size charts, logos."
```

The response `json` field contains the structured product data including curated image URLs.

### Step 2: Filter images

1. DISCARD: `section: "review"` (user UGC)
2. DISCARD: `section: "other"` (navigation, banners)
3. KEEP: `section: "main_gallery"` (priority) + `section: "description"`
4. Keep up to **5** best images

### Step 3: Visual filter (Claude reads each image)

**CRITICAL: Always use User-Agent when downloading images.** Without it, Amazon and other CDNs return a tiny placeholder (9 bytes) instead of the real image — causing "Could not process image" error.

```bash
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" -o /tmp/product_N.jpg "IMAGE_URL"
# Verify file is valid before reading:
ls -lh /tmp/product_N.jpg  # must be > 10KB, otherwise URL is blocked
# Then Read /tmp/product_N.jpg
```

- DISCARD: human faces visible
- DISCARD: different color/variant than page listing
- DISCARD: file smaller than 10KB (CDN placeholder, not real image)
- KEEP: product only (hands OK, faces not)

### Step 4: Build product description

- 150-300 words, informative not salesy
- Structure: Name + brand → what it is → key selling points (3-5) → specs → who it's for
- Include: dimensions, weight, materials, compatibility

### Step 5: Proceed to generation

Use extracted images in the `medias` array (upload with `--force-ip-check`). Use extracted description to inform the video prompt.

---

## Product Visual Analysis (no URL case)

**When the user provides only a product photo (no URL, no description) — MANDATORY: visually analyze the image before building any prompt.**

Read the product image and identify:

1. **Product category** — what is it exactly? (perfume, face cream, lip balm, shampoo, body lotion, foundation, mascara, sunscreen, serum, hair oil, supplement capsules, protein powder, etc.)
2. **Usage mechanic** — how is it physically used?
   - Perfume / spray bottle → **spray** (press nozzle → mist comes out)
   - Tube (cream, gel, toothpaste) → **squeeze + apply** with fingers
   - Pump bottle (serum, lotion, soap) → **press pump** → dispense onto fingers → apply
   - Lipstick / lip gloss → **swipe** directly on lips
   - Mascara → **brush** applied to lashes
   - Powder / compact → **brush or sponge** pressed on skin
   - Dropper / serum with pipette → **drop** onto fingertips → press into skin
   - Jar (cream, mask) → **scoop** with fingers → apply
   - Capsule / pill / gummy → **swallow** or **chew**
   - Powder sachet / scoop → **mix** into liquid
3. **Opening mechanic** — how does it open? (uncap, unscrew, pull tab, flip top, press pump — this must be shown BEFORE contents exit the container)
4. **Key visual details** — color, shape, material, label, any distinctive features to preserve in the prompt

**Use this analysis to write the Dynamic Description accurately.** Never default to "applies cream" or generic skincare interaction — describe the exact mechanic that matches the identified product type.

---

## Reference Index

All references are in `.claude/skills/video-marketing-skill/references/video/` (flat structure, no subfolders).

| File                                                            | Character (Soul 2.0)   | Triggers                                                                                                            |
| --------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| [tv-spot.md](.claude/skills/video-marketing-skill/references/video/tv-spot.md)                       | NO (user can provide) | tv spot, tv commercial, television ad, commercial ad                                                                |
| [ugc.md](.claude/skills/video-marketing-skill/references/video/ugc.md)                               | YES                   | ugc, talking head, creator review, person talks about product, testimonial, recommendation                          |
| [tutorial.md](.claude/skills/video-marketing-skill/references/video/tutorial.md)                     | YES                   | tutorial, how to use, step by step, guide, instructions, how-to                                                     |
| [product-review.md](.claude/skills/video-marketing-skill/references/video/product-review.md)         | NO                    | product demo, product review, show the product, demonstrate product, product in action                              |
| [unboxing.md](.claude/skills/video-marketing-skill/references/video/unboxing.md)                     | YES                   | unboxing, unbox, opening package, reveal, first reaction, unpacking                                                 |
| [ugc-virtual-try-on.md](.claude/skills/video-marketing-skill/references/video/ugc-virtual-try-on.md) | YES                   | virtual try on + ugc, try on haul, ugc try on, ugc fitting, outfit try on ugc                                       |
| [pro-virtual-try-on.md](.claude/skills/video-marketing-skill/references/video/pro-virtual-try-on.md) | NO                    | virtual try on (without ugc), fitting, studio try on, show how it looks, pro try on                                 |
| [hyper-motion.md](.claude/skills/video-marketing-skill/references/video/hyper-motion.md)             | NO                    | showcase, social short, product demo pro, professional ad, cgi ad, premium ad, product highlight, cinematic product |
| [wild-card.md](.claude/skills/video-marketing-skill/references/video/wild-card.md)                   | NO                    | wild card, crazy ad, wild, creative ad, unconventional, out of the box                                              |

**Virtual Try On routing:** if request contains "ugc" → UGC Virtual Try On. If no "ugc" or "studio"/"pro" → Pro Virtual Try On.

**Product Review vs Hyper Motion:** "demo" without "pro" → Product Review. "Demo pro" or "professional demo" → Hyper Motion.

**Character override:** User can always provide their own character/element for ANY format, regardless of the auto-generation flag above. The flag only controls whether the agent generates a character automatically when none is provided.

---

## Single-Beat vs Multi-Beat Detection

Before routing, determine if the request describes **one action** or **a sequence of different phases**.

### Single-beat (one reference)

The request describes one dominant action or all actions map to the same reference type.

Examples:

- "make a talking-head review of this product" → talking-head only
- "unboxing video" → unboxing only
- "product showcase, levitating, 3D" → product-showcase only

**Action:** Read one matching reference → build prompt → CLI.

### Multi-beat (multiple references)

The request describes a **chronological sequence** of distinct phases that map to **2+ different reference types**. Look for:

- Temporal markers: "first... then... at the end", "after that", "starts with... finishes with"
- Enumeration of distinct actions: "unpacks, then talks about it, then shows how to use, then packshot"
- Each phase matches a different reference in the routing table below

Examples:

- "she unpacks the product, talks about it, and at the end shows a packshot" → unboxing + talking-head + product-demo-pro (3 references)
- "unboxing then tutorial" → unboxing + tutorial (2 references)
- "woman presents product and then clean product showcase at the end" → talking-head + product-showcase (2 references)

**Action:** Read ALL matching references → combine their prompt patterns into one video prompt → assign chronological beats proportionally within the total duration.

**Beat allocation:** Divide total duration across beats. For a 10s video with 3 beats: ~3s + ~3s + ~4s. For 15s with 2 beats: ~7s + ~8s. Translate beat count into sentence density in the Dynamic Description (see Density by Duration in each reference).

**Prompt structure for multi-beat:** One continuous prompt with section labels. Dynamic Description flows chronologically — Beat 1 prose → Beat 2 prose → Beat 3 prose. Each beat follows the prompt rules from its reference (camera, interaction style, tone) but blended into a single coherent scene.

---

## Routing

Match the request (or each beat in multi-beat) against this table:

| User Request                                                                                     | Action                                                                                                                     |
| ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Brand-styled video — "in brand style", "brand colors", "brand identity" + URL                    | Read `.claude/skills/video-marketing-skill/references/brand-style-extraction.md` → build Brand Brief → then route to video format below → apply Brief overrides |
| TV spot, tv commercial, television ad, commercial ad                                             | Read `.claude/skills/video-marketing-skill/references/video/tv-spot.md` → build prompt → CLI                                                                    |
| UGC, talking head, creator review, person talks about product, testimonial, recommendation       | Read `.claude/skills/video-marketing-skill/references/video/ugc.md` → build prompt → CLI                                                                        |
| Tutorial, how to use, step by step, guide, instructions, how-to                                  | Read `.claude/skills/video-marketing-skill/references/video/tutorial.md` → build prompt → CLI                                                                   |
| Product demo, product review, show the product, demonstrate product, product in action           | Read `.claude/skills/video-marketing-skill/references/video/product-review.md` → build prompt → CLI                                                             |
| Unboxing, unbox, opening package, reveal, first reaction, unpacking                              | Read `.claude/skills/video-marketing-skill/references/video/unboxing.md` → build prompt → CLI                                                                   |
| Virtual try on + UGC, try on haul, ugc try on, ugc fitting                                       | Read `.claude/skills/video-marketing-skill/references/video/ugc-virtual-try-on.md` → build prompt → CLI                                                         |
| Virtual try on (without ugc), fitting, studio try on, show how it looks, pro try on              | Read `.claude/skills/video-marketing-skill/references/video/pro-virtual-try-on.md` → build prompt → CLI                                                         |
| Showcase, social short, product demo pro, professional ad, cgi ad, premium ad, cinematic product | Read `.claude/skills/video-marketing-skill/references/video/hyper-motion.md` → build prompt → CLI                                                               |
| Wild card, crazy ad, creative ad, unconventional, out of the box                                 | Read `.claude/skills/video-marketing-skill/references/video/wild-card.md` → build prompt → CLI                                                                  |
| Anything not matching above                                                                      | Read `.claude/skills/video-marketing-skill/references/video/hyper-motion.md` → build prompt → CLI (fallback)                                                    |

---

## Tools

### Upload Reference Media

**Upload is not yet exposed as a tool.** Product photos / reference images must arrive with a pre-existing `MEDIA_ID`. If the user provides a local file, tell them upload isn't wired up yet.

When referencing a prior generated job instead of an uploaded image, skip upload entirely: use `{"id": "<JOB_ID>", "type": "seedance_2_0_job"}` (or the relevant `<job_set_type>_job`) in `medias`, and call `higgsfield_ip_check({"job_ids": ["<JOB_ID>"]})` before submitting.

### Generate Video (seedance_2_0)

**Single video (still wrapped in `requests`):**

```json
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"Style & Mood: ... [full prompt from reference template]","medias":[{"role":"start_image","data":{"id":"MEDIA_ID","type":"media_input"}}],"duration":8,"aspect_ratio":"9:16"}
  ]
})
```

**Multiple independent videos (parallel):**

The `requests` array runs items concurrently. Use for multiple independent ad variants, A/B test videos, or different product angles simultaneously:

```json
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"Style & Mood: ... [variant A]","medias":[{"role":"start_image","data":{"id":"MEDIA_ID","type":"media_input"}}],"duration":8,"aspect_ratio":"9:16"},
    {"model":"seedance_2_0","prompt":"Style & Mood: ... [variant B]","medias":[{"role":"start_image","data":{"id":"MEDIA_ID","type":"media_input"}}],"duration":10,"aspect_ratio":"9:16"}
  ]
})
```

All items run concurrently (up to `concurrency`, default 8). Returns `{"job_ids": [...]}` within seconds. Per-item errors appear in `errors: [{index, error}]`.

**When to use parallel:** Multiple ad variants, A/B creative tests, same product with different angles/styles, batch of independent videos sharing the same uploaded media.
**When NOT to use parallel:** Videos that depend on each other's output (e.g., video B uses video A's result as reference).

| JSON field       | Type   | Default    | Description                                                                                                                                                                                                     |
| ---------------- | ------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`          | string | _required_ | Always `"seedance_2_0"`                                                                                                                                                                                         |
| `prompt`         | string | _required_ | Built from reference template                                                                                                                                                                                   |
| `medias`         | array  | —          | Input media. Each entry: `{"role":"start_image","data":{"id":"ID","type":"media_input"}}` (roles: image, start_image, end_image; type: `media_input` for uploads or `<job_set_type>_job` for prior job results) |
| `duration`       | int    | `8`        | 4–15 seconds                                                                                                                                                                                                    |
| `aspect_ratio`   | string | `"1:1"`    | `"1:1"`, `"3:4"`, `"9:16"`, `"16:9"`                                                                                                                                                                            |
| `generate_audio` | bool   | `true`     | Audio is ON by default. Set to `false` ONLY when the user explicitly asks for a silent clip, or when the clip is b-roll / loop material intended to be paired with external audio in post.                       |

### Fire-and-Forget Generation

`higgsfield_generate` returns `{"job_ids": [...]}` immediately. Do not wait.

Poll via `higgsfield_job_status({"job_ids": ["<id>"]})` only if the result is needed downstream (e.g., character image needed as reference for video generation, or element creation).

**Seedance 2.0 job-reference rule:** When a `seedance_2_0` generation uses a prior **job** (not upload) as input, call `higgsfield_ip_check({"job_ids": ["<UPSTREAM_JOB_ID>"]})` after the upstream job completes and before submitting the seedance generate. Reject if `ip_detected` is true.

Terminal statuses: `completed`, `canceled`, `failed`, `nsfw`, `ip_detected`

---

## Full Workflow Example

```json
// 1. Obtain product photo MEDIA_ID (upload not yet exposed as tool — user-supplied).
// 2. Generate video — returns job_ids immediately (fire-and-forget).
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"@Image1 is the product reference. Style & Mood: UGC authentic, natural window light, iPhone front-camera aesthetic, warm tones. Narrative Summary: A young woman enthusiastically reviews a skincare product in her bedroom. Dynamic Description: Medium close-up, front-facing camera at eye level — she holds the product (@Image1) up beside her face, gesturing toward it with her free hand, eyes bright, speaking directly into the lens. She tilts the bottle to show the label, then unscrews the cap and squeezes a small amount onto her fingertips. Static Description: Cozy bedroom, soft daylight from window, neutral bedding, warm ambient tones. Audio: She speaks to camera: 'Okay so this serum has completely changed my skin, like I am not exaggerating — look at this glow.' Facial features clear and undistorted, consistent clothing, 4K Ultra HD, stable and blur-free.","medias":[{"role":"start_image","data":{"id":"<MEDIA_ID>","type":"media_input"}}],"duration":10,"aspect_ratio":"9:16","generate_audio":true}
  ]
})
```

---

## Aspect Ratio Defaults

| Use Case                                | Aspect Ratio | Width | Height |
| --------------------------------------- | ------------ | ----- | ------ |
| Vertical (mobile, TikTok, Reels)        | `9:16`       | 720   | 1280   |
| Portrait (Instagram feed, mobile-first) | `3:4`        | 720   | 960    |
| Square (Instagram feed)                 | `1:1`        | 720   | 720    |
| Horizontal (YouTube, web)               | `16:9`       | 1280  | 720    |

---

## Engine Constraints

Read `.claude/skills/video-marketing-skill/references/engine-constraints.md` for full details. Key limits:

- **Duration:** ≤ 15s max
- **Beats:** ≤ 4 per scene
- **Characters:** ≤ 3 per shot (tracking drops above 3)
- **No reflections** (mirrors, puddles) — breaks scene
- **Character exits frame** = gone for rest of shot
- **Never describe age** — use role labels only

## ZH Safety

Read `.claude/skills/video-marketing-skill/references/zh-safety.md` for Chinese prompt safety rules. Required when generating Chinese-language prompts.

---

## Error Handling

| Error         | Fix                                              |
| ------------- | ------------------------------------------------ |
| `status 401`  | Proxy auth error                                 |
| `status 429`  | Rate limited — wait and retry                    |
| `failed`      | Retry with different prompt                      |
| `nsfw`        | Content flagged — modify prompt, check ZH safety |
| `ip_detected` | IP content — modify prompt                       |

---

## Character & Element Integration

**Character generation via Soul 2.0 applies ONLY when the matched reference file specifies "Character: YES".** If the reference says "Character: NO" — do NOT generate a character even if the scene includes a human. The video engine renders the person from the text description directly. User can always override by providing their own person/element reference.

**When Character: YES** — generate the character via Soul 2.0 first, then create an element, then use `<<<element_id>>>` in the video prompt. Do NOT describe the person inline in the video prompt and go directly to t2v — this produces inconsistent, low-quality characters.

Character description for Soul 2.0 is extracted from the user's prompt (appearance, outfit, style) + auto-matched location based on product type (see Soul 2.0 rules in `/higgsfield`).

**CRITICAL: Character generation prompt must NEVER mention the product.** When generating a person for a video ad, describe ONLY the person (appearance, expression, clothing, pose, style). The product enters the video via the `medias` array and `@ImageN` / `<<<element_id>>>` in the video generation step — NOT in the image generation step. Location/background is OK, objects in hands are NOT.

**MANDATORY: Before generating any character via Soul 2.0 — read `/higgsfield` and follow the Soul 2.0 Character Prompt Rules section.** It contains location matching by product type, lighting rules, architectural detail requirements, safety rules, and real prompt examples. Do NOT generate a character without reading these rules first — plain prompts produce white/neutral backgrounds.

When a video ad request involves a specific person (generated character, uploaded photo, or existing element), there are **two paths** to inject the creator into the video prompt. Choose based on what you have:

### Path 1: Element exists (from soul-v2, soul-location, or prior generation)

Use `<<<element_id>>>` directly in the prompt **instead of** `@ImageN` for the creator.

1. **Check existing elements:** `higgsfield_element({"action": "list", "category": "character", "size": 20})`. Scan the `items` array for a matching creator.
2. **If suitable element exists** — use its `id`. If not — generate via **Soul 2.0** (see Soul 2.0 Character Prompt Rules in `/higgsfield`), poll to completion, then register it: `higgsfield_element({"action":"create","category":"character","name":"…","medias":[{"id":"<JOB_ID>","url":"<RESULT_URL>","type":"text2image_soul_v2_job"}]})`.
3. **Build prompt from reference template as usual**, but replace `@ImageN is the creator reference` with `<<<element_id>>>`:
   ```
   <<<elem_xyz>>> is the creator. @Image1 is the product reference. ANGLE LOCK: ...
   Dynamic Description: <<<elem_xyz>>> holds the product up to the camera, gestures enthusiastically...
   ```
4. **Tool call** — product photo still goes in `medias` array, element is resolved from `<<<id>>>` in the prompt:
   ```json
   higgsfield_generate({
     "requests": [
       {"model":"seedance_2_0","prompt":"<<<elem_xyz>>> is the creator. @Image1 is the product reference. ...","medias":[{"role":"start_image","data":{"id":"<PRODUCT_MEDIA_ID>","type":"media_input"}}],"duration":10,"aspect_ratio":"9:16","generate_audio":true}
     ]
   })
   ```

### Path 2: Image result URL (from soul-v2, soul-cinematic, or any image generation — no element created)

Use the prior generated image as a job reference (no upload tool needed).

1. **Use the prior job ID directly** via `medias`, typed as `<job_set_type>_job` (e.g. `text2image_soul_v2_job`). No upload round-trip required. Before submitting, verify IP:
   ```json
   higgsfield_ip_check({"job_ids": ["<CREATOR_JOB_ID>"]})
   ```
2. **Build prompt from reference template** — use `@Image1` for product, `@Image2` for creator (or vice versa, just keep `medias` order matching):
   ```
   @Image1 is the product reference. @Image2 is the creator reference. ANGLE LOCK: ...
   Dynamic Description: The creator (@Image2) holds the product (@Image1) up to the camera...
   ```
3. **Tool call** — both go in the `medias` array:
   ```json
   higgsfield_generate({
     "requests": [
       {"model":"seedance_2_0","prompt":"@Image1 is the product reference. @Image2 is the creator reference. ...","medias":[{"role":"start_image","data":{"id":"<PRODUCT_MEDIA_ID>","type":"media_input"}},{"role":"start_image","data":{"id":"<CREATOR_JOB_ID>","type":"text2image_soul_v2_job"}}],"duration":10,"aspect_ratio":"9:16","generate_audio":true}
     ]
   })
   ```

### Path summary

| What you have                                 | How to inject into video prompt                                                                                      |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Element ID (from soul-v2 → element create)    | `<<<element_id>>>` in prompt, no `medias` entry needed for creator                                                   |
| Generated image file/URL (no element)         | `upload` → `{"role":"start_image","data":{"id":"...","type":"media_input"}}` in `medias` array + `@ImageN` in prompt |
| Nothing (generic person, no specific creator) | Normal flow — no creator reference, reference template defaults apply                                                |

### Environments (optional)

Same pattern with `soul-location` + `element create --category environment` for consistent backgrounds across multiple marketing videos. Use `<<<env_id>>>` in Static Description section.
