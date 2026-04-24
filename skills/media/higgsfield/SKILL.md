---
name: higgsfield
description: |
  READ-ONLY platform reference — not an action skill, never invoke directly for user requests.
  Read this when you need: Soul 2.0 character prompt rules (location matching by product type,
  lighting, real prompt examples), media JSON format, --force-ip-check upload requirement
  for video, element system commands, Soul Cast/Location workflows, Soul ID decision table.
  Referenced by /video-marketing-skill and /image-skill internally.
---

## Image Model Selection

First match wins. If the user explicitly names a model — use that model and skip the table.

| Model                | When to use                                                                                                                                                                                                                                                                       | JSON model name      |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| **Seedream V5 Lite** | Editing a REAL PHOTOGRAPH where face identity must be preserved. Only for photographic face edits from real photos. NEVER for cartoon, stylized, or AI-generated characters                                                                                                       | `seedream_v5_lite`   |
| **Seedream V4.5**    | High-quality generation with input image support. Similar to V5 Lite but different model version                                                                                                                                                                                  | `seedream_v4_5`      |
| **Soul Cinematic**   | Cinematic stills, moodboards, film-reference frames with **no named actor** or specific person's face. For a cinematic still that needs a specific actor's face → use Nano Banana Pro                                                                                               | `soul_cinematic`     |
| **Soul 2.0**          | Default for person/character generation: UGC, influencer, editorial, fashion, y2k, streetwear, Kodak/film aesthetics. Use when **vibe > strict feature accuracy** and no IP/exotic trigger (no named characters, no real actor likeness, no exotic features like vitiligo/heterochromia). Use `"preset":"general"` by default. Follow Soul 2.0 prompt rules below | `text2image_soul_v2` |
| **Soul Cast**        | Cinematic character creation before video generation — creates characters for use in video scenes. Result should be saved as `character` element for reuse                                                                                                                        | `soul_cast`          |
| **Soul Location**    | Environment/background generation — "create a setting", "generate a location", "make a background scene". Result should always be saved as an `environment` element for reuse                                                                                                     | `soul_location`      |
| **Nano Banana Pro**    | **Default for everything else.** IP/identity precision (named characters — Spiderman, Disney, anime; real actor likeness; exotic features — vitiligo, heterochromia, specific height, rare combos); cinematic stills needing a specific actor's face; all image edits (pose, angle, outfit, background, color, small tweaks); product compositing, merging, e-commerce. All cases not matched above | `nano_banana_2`      |
| **GPT Image 2.0**      | Heavy/detail-dense only — use ONLY when: posters/cards/menus/infographics with **real quoted text** rendered accurately; fixed layouts with multiple elements in **specific positions**; UI mockups, webpage replications, screen recreations, game assets, presentation slides; heavy edits changing many small details at once / precise typography. **NOT for simple color or background swaps** — those go to Nano Banana Pro. `sub_model` = `videotape-alpha` (default), `cassettetape-alpha`, `electricaltape-alpha`, `tidepool-alpha`. Reference file: `.claude/skills/image-skill/references/imagegen-2.md` | `imagegen_2_0`       |
| **Image Auto**       | Picks the best model automatically based on prompt and medias. Use when unsure which model fits best                                                                                                                                                                              | `image_auto`         |
| **Nano Banana 2**     | Budget-friendly, fast generation. Original version with UGC, draw, product placement, and photo set modes                                                                                                                                                                        | `nano_banana`        |
| **Flux 2**           | Versatile flagship image model. Pro/Flex/Max variants via `sub_model` param. Good all-round quality                                                                                                                                                                               | `flux_2`             |
| **GPT Image 1.5**    | Powerful editing and best text rendering. Use when the image must contain readable text or typography                                                                                                                                                                              | `openai_hazel`       |
| **Kling O1**         | Versatile photorealistic generation with strong input image support                                                                                                                                                                                                               | `kling_omni_image`   |
| **Grok Image**       | Expressive, high-contrast generation and editing. Std and Pro modes                                                                                                                                                                                                               | `grok_image`         |
| **Z Image**          | Super fast, stylized text-to-image. No input image support                                                                                                                                                                                                                        | `z_image`            |

## Video Model Selection

First match wins. If the user explicitly names a model — use that model and skip the table.

| Model                    | When to use                                                                                                                    | JSON model name          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| **Seedance 2.0**         | **Default for video generation.** Reference-driven, multi-SKU, consistent identity. Also available as `claudesfield_video`     | `seedance_2_0`           |
| **Kling 3.0**            | Multi-shot, audio sync, motion transfer. Use when user explicitly requests it                                                  | `kling3_0`               |
| **Seedance 1.5 Pro**     | Reliable motion. Start/end image support. Durations: 4/8/12s                                                                   | `seedance1_5`            |
| **Cinematic Studio 2.5** | Refined cinematic camera and color. Image input support, up to 4k resolution                                                   | `cinematic_studio_2_5`   |
| **Cinematic Studio 3.0** | Most advanced cinema-grade model. Multi-shot, genre presets (action/horror/comedy/noir/drama/epic), audio generation            | `cinematic_studio_3_0`   |
| **Kling 2.6**            | Cinematic motion, advanced physics. Single input image, 5 or 10s duration                                                      | `kling2_6`               |
| **Minimax Hailuo 02**    | 1080p, natural physics, facial emotion. Multiple sub-models (minimax, minimax-fast, minimax-2.3, minimax-2.3-fast)             | `minimax_hailuo`         |
| **Wan 2.6**              | Open-weight, stylized, experimental creative. Audio and multi-video input support                                              | `wan2_6`                 |
| **Wan 2.7**              | Synchronized audio, character-consistent video                                                                                 | `wan2_7`                 |
| **Google Veo 3**         | Cinematic realism, native audio sync. 16:9 or 9:16 only. **Requires `input_image`** — no text-only. `sub_model`: `veo-3-preview` or `veo-3-fast` (default: `veo-3-fast`) | `veo3`                   |
| **Google Veo 3.1**       | Ultra-realistic, top-tier cinematic quality. Reference/style images, end image support. `sub_model`: `veo-3-1-preview` or `veo-3-1-fast` (default: `veo-3-1-fast`). `mode` auto-detected from inputs | `veo3_1`                 |
| **Google Veo 3.1 Lite**  | Fast, affordable Veo variant. 4/6/8s durations, 720p/1080p                                                                    | `veo3_1_lite`            |
| **Grok Video**           | Text and image-to-video with audio support. Single start_image input, 1-15s                                                   | `grok_video`             |

---

## Aspect Ratios

### Image models

| Ratio  | Size      | Best for                                                                     |
| ------ | --------- | ---------------------------------------------------------------------------- |
| `9:16` | 720×1280  | Vertical/stories                                                             |
| `3:4`  | 896×1200  | Portrait, mobile-first, vertical content (**default** for most image models) |
| `2:3`  | 800×1200  | Tall portrait                                                                |
| `4:5`  | 960×1200  | Instagram feed post                                                          |
| `1:1`  | 1024×1024 | Square, social feed                                                          |
| `5:4`  | 1200×960  | Instagram landscape                                                          |
| `4:3`  | 1200×896  | Standard landscape                                                           |
| `3:2`  | 1200×800  | Wide landscape                                                               |
| `16:9` | 1280×720  | Widescreen                                                                   |
| `21:9` | 1200×514  | Ultra-wide / cinematic banner                                                |

Note: `4:5` and `5:4` are supported by Nano Banana Pro only. `2:3`, `3:2`, `4:3` are supported by Soul 2.0, Soul Cinematic, Seedream models, and Nano Banana Pro. `21:9` is supported by Soul Cinematic, Seedream models, and Nano Banana Pro.

### Video (seedance-2.0)

| Ratio  | Size      | Best for                        |
| ------ | --------- | ------------------------------- |
| `21:9` | 1344×576  | Ultra-wide / cinematic          |
| `16:9` | 1280×720  | YouTube, widescreen             |
| `4:3`  | 960×720   | Standard landscape              |
| `1:1`  | 720×720   | Instagram feed, square          |
| `3:4`  | 540×720   | Portrait                        |
| `9:16` | 720×1280  | Vertical, TikTok, Reels, mobile |

### Video (kling-3.0)

| Ratio  | Size      | Best for                        |
| ------ | --------- | ------------------------------- |
| `16:9` | 1280×720  | YouTube, widescreen             |
| `1:1`  | 720×720   | Square, social feed             |
| `9:16` | 720×1280  | Vertical, TikTok, Reels, mobile |

### Video (seedance-1.5-pro)

| Ratio  | Size      |
| ------ | --------- |
| `21:9` | 1344×576  |
| `16:9` | 1280×720  |
| `4:3`  | 960×720   |
| `1:1`  | 720×720   |
| `3:4`  | 540×720   |
| `9:16` | 720×1280  |

### Video (cinematic-studio-3.0)

| Ratio  | Size      |
| ------ | --------- |
| `21:9` | 1344×576  |
| `16:9` | 1280×720  |
| `4:3`  | 960×720   |
| `1:1`  | 720×720   |
| `3:4`  | 540×720   |
| `9:16` | 720×1280  |

### Video (veo3 / veo3.1)

| Ratio  | Size      |
| ------ | --------- |
| `16:9` | 1280×720  |
| `9:16` | 720×1280  |

### Video (grok-video)

| Ratio  | Size      |
| ------ | --------- |
| `16:9` | 1280×720  |
| `9:16` | 720×1280  |
| `4:3`  | 960×720   |
| `3:4`  | 540×720   |
| `1:1`  | 720×720   |
| `3:2`  | 1080×720  |
| `2:3`  | 480×720   |

---

## Upload & Media Reference

### Upload

**Upload is not yet exposed as a tool.** When a request requires a local-file reference (product photo, custom photo, etc.), the user must supply a pre-existing `MEDIA_ID` out-of-band. If they can't, tell them the upload flow isn't wired up yet.

**For video inputs:** Seedance 2.0 still requires every input media to pass IP check. For a reference that came from a prior generated **job**, call `higgsfield_ip_check({"job_ids": ["<JOB_ID>"]})` and reject the reference if `ip_detected: true`. For media-level IP check on uploads, the tool flow isn't available yet.

When an upload ID is already available, only `id` is needed downstream in `"medias"` or `"images"` array.

### Media JSON format

Media is passed as a JSON array. Two different structures depending on model:

**`"images"` array** — for `nano_banana_2` and `seedream_v4_5` (flat objects):

| Field  | Required | Description                                              |
| ------ | -------- | -------------------------------------------------------- |
| `id`   | Yes      | Upload ID or Job ID                                      |
| `type` | Yes      | `media_input` for uploads, `<model>_job` for job results |

**`"medias"` array** — for all other models (nested `data` wrapper):

| Field       | Required | Description                                              |
| ----------- | -------- | -------------------------------------------------------- |
| `role`      | Yes      | `image`, `start_image`, `end_image`                      |
| `data.id`   | Yes      | Upload ID or Job ID                                      |
| `data.type` | Yes      | `media_input` for uploads, `<model>_job` for job results |

**`type` values:** `media_input` (uploads), `nano_banana_2_job`, `text2image_soul_v2_job`, `soul_cinematic_job`, `seedream_v5_job` (note: not `seedream_v5_lite_job`), `seedance_2_0_job`, etc.

**Examples:**

```json
"medias":[{"role":"image","data":{"id":"UPLOAD_ID","type":"media_input"}}]                     // uploaded image
"medias":[{"role":"start_image","data":{"id":"UPLOAD_ID","type":"media_input"}}]              // starting frame for video
"medias":[{"role":"image","data":{"id":"JOB_ID","type":"soul_cinematic_job"}}]                   // from a generation result
```

**Multiple inputs** — add multiple objects to the array:

```json
"medias":[{"role":"image","data":{"id":"PRODUCT_ID","type":"media_input"}},{"role":"image","data":{"id":"CREATOR_ID","type":"media_input"}}]
```

**nano_banana_2 and seedream_v4_5** — use `"images"` instead of `"medias"`:

```json
"images":[{"id":"UPLOAD_ID","type":"media_input"}]
```

---

## Generation Output & Polling Model

`higgsfield_generate` is **fire-and-forget**. It returns `{"job_ids": [...]}` immediately. Do **not** block, do not sleep, and do not hold the tool call open.

### Output — captured immediately

The tool always returns the same flat shape regardless of batch size:

```json
{
  "job_ids": ["job_...", "job_..."]
}
```

Order is preserved — `job_ids[i]` corresponds to `requests[i]`. Per-item failures appear in a sibling `errors: [{index, error}]` list only when something failed. Track the `index` → `job_id` mapping so users can refer to individual results by position (e.g., "change the third image" → index 2).

### When to poll

Only poll when the result is needed in the **same conversation** for a downstream step:

1. The result will be used as a reference in another `generate` call (image→video, character sheet, montage input, element creation).
2. The user explicitly asks for the final URL ("show me the link", "where's the image").

Otherwise — don't poll. Report the `job_id` and `job_set_type` and stop.

### How to poll

```json
higgsfield_job_status({"job_ids": ["<JOB_ID>"]})
```

Accepts one or many job IDs; polls each until terminal. Returns:

```json
{
  "job_ids": ["..."],
  "results": [
    {
      "job_id": "...",
      "status": "completed",
      "job_set_type": "<model>",
      "ip_check_finished": false,
      "ip_detected": false,
      "job_set_id": "...",
      "result": {
        "url": "https://dqv0cqkoy5oj7.cloudfront.net/.../image.png",
        "type": "image"
      }
    }
  ]
}
```

Terminal statuses: `completed`, `canceled`, `failed`, `nsfw`, `ip_detected`.

**The result URL is at `results[i].result.url`** — this is the direct download link for the generated image or video. When the user asks for the final URL or you need to show the result, extract it from there. For downstream references in other generations, use `id` + `type` (not the URL).

### Building a reference from a polled job

Once polled to `completed`, reference the job in the next `generate` call using:

- `id` = `job_id`
- `type` = `<job_set_type>_job` — derived from the `job_set_type` field plus `_job` suffix

`job_set_type` → `type` mapping:

| `job_set_type`       | Reference `type`                                |
| -------------------- | ----------------------------------------------- |
| `nano_banana_2`      | `nano_banana_2_job`                             |
| `text2image_soul_v2` | `text2image_soul_v2_job`                        |
| `soul_cinematic`     | `soul_cinematic_job`                            |
| `soul_cast`          | `soul_cast_job`                                 |
| `soul_location`      | `soul_location_job`                             |
| `seedream_v4_5`      | `seedream_v4_5_job`                             |
| `seedream_v5_lite`   | `seedream_v5_job` _(special case — no `_lite`)_ |
| `seedance_2_0`       | `seedance_2_0_job`                              |
| `kling3_0`           | `kling3_0_job`                                  |
| `imagegen_2_0`       | `imagegen_2_0_job`                              |
| `image_auto`         | `image_auto_job`                                |
| `nano_banana`        | `nano_banana_job`                               |
| `flux_2`             | `flux_2_job`                                    |
| `openai_hazel`       | `openai_hazel_job`                              |
| `kling_omni_image`   | `kling_omni_image_job`                          |
| `grok_image`         | `grok_image_job`                                |
| `z_image`            | `z_image_job`                                   |
| `seedance1_5`        | `seedance1_5_job`                               |
| `cinematic_studio_2_5` | `cinematic_studio_2_5_job`                    |
| `cinematic_studio_3_0` | `cinematic_studio_3_0_job`                    |
| `kling2_6`           | `kling2_6_job`                                  |
| `minimax_hailuo`     | `minimax_hailuo_job`                            |
| `wan2_6`             | `wan2_6_job`                                    |
| `wan2_7`             | `wan2_7_job`                                    |
| `veo3`               | `veo3_job`                                      |
| `veo3_1`             | `veo3_1_job`                                    |
| `veo3_1_lite`        | `veo3_1_lite_job`                               |
| `grok_video`         | `grok_video_job`                                |

### Pattern — generate then reference

```json
// Step 1: fire and forget — response carries job_ids[], order matches requests[]
higgsfield_generate({
  "requests": [
    {"model":"nano_banana_2","prompt":"..."}
  ]
})
// → { "job_ids": ["<JOB_ID>"] }
// The model name you used (e.g. "nano_banana_2") is the job_set_type; build
// the reference type by appending "_job" (see mapping table above).

// Step 2 — ONLY if referenced downstream: poll to completion
higgsfield_job_status({"job_ids": ["<JOB_ID>"]})

// Step 2b — If downstream model is seedance_2_0 and reference is a job (not upload):
// run IP detection before submitting the seedance_2_0 generate
higgsfield_ip_check({"job_ids": ["<JOB_ID>"]})
// Reject if results[0].ip_detected is true.

// Step 3: use as reference (type = <job_set_type>_job) — only id + type needed
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"...","medias":[{"role":"start_image","data":{"id":"<JOB_ID>","type":"nano_banana_2_job"}}]}
  ]
})
```

**Note:** Step 2b (`higgsfield_ip_check`) is required ONLY when the downstream model is `seedance_2_0` and the reference is a prior job (not an upload). For other models referencing a job, skip Step 2b — just `id` + `type` after polling to `completed`.

**Other flows not yet exposed as tools:**

- Media upload with IP check — pending (use a pre-existing `MEDIA_ID` if the user has one)
- Soul ID training (`soul-id create` / `status`) — pending

---

## Element System

Elements are persistent character/location/prop references. Once created, any generation (image or video) can reference them via `<<<element_id>>>` — the backend resolves the element automatically.

### Commands

> Element management (list / get / create) is **not yet exposed as tools.** When a task needs to list, fetch, or create an element, tell the user the element CRUD flow isn't wired up in this runtime yet. You can still **use** existing element IDs via `<<<element_id>>>` placeholders — the backend resolves them automatically at generation time.

**Categories:** `character`, `environment`, `prop`, `auto`

### Using elements in prompts

Embed `<<<element_id>>>` anywhere in any prompt:

```json
// Single element in video
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"<<<abc123>>> walks down a rainy street, noir cinematic, slow motion..."}
  ]
})

// Single element in image
higgsfield_generate({
  "requests": [
    {"model":"nano_banana_2","prompt":"<<<abc123>>> portrait, dramatic side lighting, 3:4..."}
  ]
})

// Multiple elements (in one request)
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"<<<char1_id>>> and <<<char2_id>>> face each other in <<<location_id>>>, tense standoff..."}
  ]
})
```

---

## Design Inspiration Query

Search Higgsfield's design-template index for reference images before constructing NB2 prompts, then translate the template's visual DNA (color palette, lighting, layout, typography, mood) into art-director directives.

```json
higgsfield_inspiration({"query": "fitness product energetic dark ad", "top_k": 5})
// → { query, top_k, results: [{url, keywords, ...}] }
```

- `query` — keyword string (required). Terse keywords work best.
- `top_k` — default 5, cap 50.
- `raw` — pass `true` to get the full response envelope when extra metadata is needed.

Open a returned `url` with `vision_analyze` to read the template directly (no download / local-file round-trip required).

---

## CRITICAL: Character Generation Prompt Rule

**When generating a character/creator for later use in video (soul-cast, soul-v2, soul-cinematic, any image model):**

- Prompt describes ONLY the person: appearance, face, expression, clothing, pose, style
- NEVER include products, objects, props, items, or anything the person holds or interacts with
- Location/background is OK (bedroom, studio, outdoor) — but NO objects in hands
- The product enters the video LATER via `"medias"` + `@ImageN` in the video generation step

**Bad:** `"a young woman holding a cooker in a kitchen, smiling"` — model bakes the cooker into the image
**Good:** `"a young woman, mid-20s, natural beauty, friendly smile, casual style, kitchen background"` — clean person, product added in video step

This applies to ALL image generation when the result will be used as a character in a video ad.

---

## Soul 2.0 Character Prompt Rules

When generating a person/creator via Soul 2.0, build the prompt using these rules:

### Style

- Always natural, lifestyle, UGC-feel — NOT editorial, studio, or fashion
- Natural makeup, natural hair color — unless user explicitly specifies otherwise
- Approachable, authentic — NOT cold, stylized, or heavily art-directed
- **Default light tone: neutral daylight — never golden hour, never warm sunset tones unless user explicitly requests it**

### Location / Background

**Priority order:**

1. **User specified a location** → use exactly that
2. **No location given → match to product context:**

| Product type                                             | Default location                                       |
| -------------------------------------------------------- | ------------------------------------------------------ |
| Haircare, skincare, shower gel, body care                | Bathroom / shower                                      |
| Food, beverages, kitchen appliances                      | Kitchen                                                |
| Clothing, accessories, jewelry, watches                  | Bedroom / living room                                  |
| Fitness, sports, supplements                             | Home gym / living room                                 |
| Summer clothing, sunglasses, café products, outdoor gear | Outdoor café terrace or park with people in background |
| Everything else                                          | Cozy home — bedroom or living room                     |

**Outdoor/street** only when product clearly belongs in that context (summer wear, outdoor lifestyle, café). Otherwise always indoors.

3. **No product context** → default: cozy home, bedroom or living room

### Lighting

- Always specify direction and quality — not just "natural light" but "soft natural daylight streaming in from the left window" or "cool diffused daylight from the right"
- **Default: soft neutral daylight — bright, clean, no golden or orange cast**
- Golden hour, warm sunset, or orange tones — ONLY if user explicitly requests it
- NEVER harsh studio strobes, NEVER pure white seamless background (unless user asks)
- Light should interact with the space — mention how it hits surfaces in the room

### Location detail — always be specific

A named location alone ("kitchen") produces a plain wall. Always add architectural details, materials, and color palette of the space:

- **What's in the background** — type of furniture, cabinetry, shelving, plants, textures
- **Materials** — marble, wood, tile, fabric, stainless steel etc.
- **Color palette of the space** — dominant colors that set the mood (whites + beiges, warm wood tones, soft pastels etc.)
- **Depth of field** — always add "background shows minimal depth of field, soft subtle separation" to keep the person sharp and background alive but not distracting

### Camera & atmosphere

Always end the prompt with: `Captured in UGC style with a smartphone camera, high-resolution and authentic, candid, approachable, aspirational lifestyle atmosphere.`

### No prompt rewriting

Build the prompt following these rules, then send it **as-is** to Soul 2.0 — do NOT pass `"enhance_prompt":true`. The enhancer rewrites and degrades the prompt. Never add `"enhance_prompt"` for character generation.

### Safety rules (applied BEFORE sending to CLI)

**1. Age enforcement — minimum 20 years old**
If the user requests a child, minor, teenager, or uses terms like "girl", "boy", "kid", "teen" — silently age the subject up. Change the description to ensure the person is explicitly at least 20 years old (e.g., "young woman, 20 years old"). Keep the rest of the scene intact. Do not mention this adjustment to the user.

**2. Anatomy & clothing**
If the prompt contains detailed descriptions of bare skin, specific body parts, or intimate anatomy — do NOT discard the prompt. Instead, adapt it by naturally weaving in clothing that covers sensitive areas:

- Female subjects: clothing that covers chest and lower body (pelvic area)
- Male subjects: clothing that covers lower body (pelvic area)
- Added clothing MUST match the aesthetic, setting, and style of the original prompt seamlessly

### Prompt structure

**Gender is determined by the user's request.** Default: woman. If user says "man", "guy", "male", "мужчина", "парень" — use man/he/his throughout. Never mix genders in a single prompt.

```
A [age/description] [man/woman] with [appearance], standing in a [specific location with architectural details].
[Light direction and quality], creating [lighting effect on skin/space].
[He/She] wears [casual outfit matching the context].
The background features [specific details: materials, colors, furniture].
Color palette dominated by [space colors].
Centered composition at eye-level, background shows minimal depth of field, soft subtle separation.
Captured in UGC style with a smartphone camera, high-resolution and authentic, candid, approachable, aspirational lifestyle atmosphere.
```

### Real examples (this is the quality level to target)

**Kitchen (food/beverage/kitchen product):**

```
A straight-on, mid-length portrait of a young woman in her early 20s with a warm, natural smile standing in a modern, bright kitchen. Her soft, glowing skin is illuminated by gentle, natural window light streaming in from the left, creating a flattering and even illumination across her features. She wears a casual chic outfit characterized by a fitted, long-sleeve blouse made from matte, opaque cotton and high-waisted jeans, echoing modern minimalist fashion. The kitchen background is defined by pristine white cabinetry, stainless steel hardware, and subtle recessed lighting, providing a clean and contemporary interior aesthetic. The overall composition is centered and placed at eye-level, focusing sharply on the woman while the background shows minimal depth of field, allowing for a soft, subtle separation that enhances the subject. The color palette is bright, dominated by whites, beiges, and subtle tan accents, enhancing the crisp editorial mood of the scene. Captured in a user-generated content (UGC) style with a smartphone camera, the photograph feels high-resolution and authentic, maintaining a candid, approachable, and aspirational lifestyle atmosphere.
```

**Bathroom (skincare/haircare/body care):**

```
A straight-on, mid-length portrait of a young woman in her mid-20s with a fresh, natural expression standing in a bright modern bathroom. Her glowing skin is illuminated by soft diffused light from the left, creating even, flattering tones across her face. She wears a cozy oversized cream-colored robe, casual and relaxed. The bathroom background features clean white subway tiles, matte black fixtures, a large mirror with warm vanity lighting, and a small plant on the counter. The color palette is soft and airy, dominated by whites, warm creams, and subtle sage accents. Centered composition at eye-level, background shows minimal depth of field, soft subtle separation between subject and space. Captured in UGC style with a smartphone camera, high-resolution and authentic, candid, approachable, aspirational lifestyle atmosphere.
```

**Bedroom (clothing/accessories/lifestyle):**

```
A straight-on, mid-length portrait of a young woman in her early 20s with a relaxed, warm smile sitting on the edge of a cozy bed. Soft natural daylight streams in from a window on the right, casting gentle warm light across her face and the room. She wears a casual everyday outfit — a relaxed fitted top and high-waisted trousers. The bedroom background features soft neutral bedding in warm beige tones, a wooden nightstand with a small plant, and subtly textured walls. The color palette is warm and inviting, dominated by creams, taupes, and muted warm tones. Centered composition at eye-level, background shows minimal depth of field, soft subtle separation. Captured in UGC style with a smartphone camera, high-resolution and authentic, candid, approachable, aspirational lifestyle atmosphere.
```

---

## Soul Cast — Character Creation Workflow

Use when the user needs a specific/recurring person in videos or images.

```json
// 1. Create character — non-blocking, capture job_id from the response
higgsfield_generate({
  "requests": [
    {"model":"soul_cast","prompt":"a young woman, mid-20s, natural beauty, friendly smile, casual style","width":1024,"height":1024,"batch_size":1,"character_params":{"genre":"Sitcom","budget":10}}
  ]
})
// → { "job_ids": ["<JOB_ID>"] }

// 2. Poll to completion (element creation needs the result URL)
higgsfield_job_status({"job_ids": ["<JOB_ID>"]})
```

> 3. **Create element** — element-create is **not yet exposed as a tool.** Tell the user element registration is pending a dedicated tool. In the meantime, reference the generated job directly in downstream `medias` via `{"id":"<JOB_ID>","type":"soul_cast_job"}` — no element required.

```json
// 4. Use in any generation — once an element_id exists, reference it via <<<...>>>
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"<<<elem_xyz>>> holding a skincare bottle, UGC authentic, 9:16..."}
  ]
})
```

**soul_cast JSON fields:**

- `"prompt"` — character description (required)
- `"width"` — image width (required, e.g. `1024`)
- `"height"` — image height (required, e.g. `1024`)
- `"batch_size"` — number of images (1-10)
- `"character_params"` — nested object with character details:
  - `"genre"` — one of: `"Action"`, `"Adventure"`, `"Comedy"`, `"Drama"`, `"Thriller"`, `"Horror"`, `"Detective"`, `"Romance"`, `"Sci-Fi"`, `"Fantasy"`, `"War"`, `"Western"`, `"Historical"`, `"Sitcom"`
  - `"budget"` — generation quality budget (10 = standard)
  - Optional: `"gender"`, `"build"`, `"height"`, `"race"`, `"eye_color"`, `"hair_style"`, `"hair_texture"`, `"hair_color"`, `"facial_hair"`, `"age"`, `"archetype"`, `"imperfections"`, `"outfit"`

---

## Soul Location — Environment Creation Workflow

Use when a consistent background/setting is needed across multiple shots.

```json
// 1. Generate location — non-blocking
higgsfield_generate({
  "requests": [
    {"model":"soul_location","prompt":"modern minimalist apartment, large windows, natural light, neutral tones","width":2048,"height":1152}
  ]
})
// → { "job_ids": ["<JOB_ID>"] }

// 2. Poll to completion (element creation needs the result URL)
higgsfield_job_status({"job_ids": ["<JOB_ID>"]})
```

> 3. **Create element** — not yet exposed as a tool. Reference the generated job directly via `{"id":"<JOB_ID>","type":"soul_location_job"}` in downstream `medias`.

```json
// 4. Use in generation (with an existing element_id)
higgsfield_generate({
  "requests": [
    {"model":"seedance_2_0","prompt":"<<<char_id>>> in <<<env_id>>>, morning routine, cinematic..."}
  ]
})
```

---

## When to Create Elements

- **Ideal** for `soul-cast` / `soul-location` outputs — they exist specifically for reuse
- **Reuse over recreate:** using `<<<existing_id>>>` gives better consistency than generating a new character each time
- **Current runtime:** element listing / creation is not yet exposed as a tool. When you can't create a persistent element, fall back to referencing the prior generated job directly in `medias` (`{"id":"<JOB_ID>","type":"<job_set_type>_job"}`)

---

## General Image Generation Workflow

```json
// 1. Select model (table above)
// 2. (Optional) Have a pre-existing reference IMAGE_ID if needed — upload tool not yet exposed

// 3. Generate — non-blocking, returns {job_ids}
higgsfield_generate({
  "requests": [
    {"model":"text2image_soul_v2","prompt":"<<<elem_id>>> portrait, golden hour, editorial fashion, 3:4","medias":[{"role":"image","data":{"id":"<IMAGE_ID>","type":"media_input"}}]}
  ]
})

// 4. (Optional) Only if you need to reuse this result → poll to completion
higgsfield_job_status({"job_ids": ["<JOB_ID>"]})
```

> Element creation (`element create`) is **not yet exposed as a tool.** Reference the prior job directly via `{"id":"<JOB_ID>","type":"text2image_soul_v2_job"}` in downstream `medias`.

---

## Soul ID — Trained Face Identity

Use when the user wants to train a face model from photos and generate images with that exact face. Different from Soul Cast: Soul Cast generates a random character, Soul ID trains on real photos to preserve an exact person's likeness.

### Commands

> Soul ID management (`create` / `list` / `status` / `delete`) is **not yet exposed as tools.** When the user asks to train / list / delete Soul IDs, tell them this flow isn't wired up in this runtime yet. A pre-existing `SOUL_ID` (from an earlier out-of-band training) can still be used in generation:

```json
// Generate image with trained face (requires pre-existing SOUL_ID)
higgsfield_generate({
  "requests": [
    {"model":"text2image_soul_v2","prompt":"portrait, golden hour, editorial style","soul_id":"<SOUL_ID>"}
  ]
})
```

### Full Workflow

1. **Collect face photos** — from local files, downloads, or Instagram fetch (instagramcli)
2. **Train Soul ID** — not yet exposed as a tool. Tell the user this step must be performed out-of-band; resume once a `SOUL_ID` is available.
3. **Generate with Soul ID (non-blocking):**
   ```json
   higgsfield_generate({
     "requests": [
       {"model":"text2image_soul_v2","prompt":"portrait, dramatic lighting, editorial fashion","soul_id":"<SOUL_ID>"}
     ]
   })
   ```
4. Capture `job_ids` from the response. Poll via `higgsfield_job_status({"job_ids":[...]})` only if the image is referenced downstream or the user wants the URL.

### When to use Soul ID vs Soul Cast vs Elements

| Need                                                | Use                                                                            |
| --------------------------------------------------- | ------------------------------------------------------------------------------ |
| Generate a **random** character for videos          | `text2image_soul_v2` with `"preset":"general"` → `element create` → `<<<id>>>` |
| Preserve a **real person's exact face** from photos | `soul-id create` → `text2image_soul_v2` with `"soul_id"`                       |
| Reuse any generated image across prompts            | `element create` → `<<<id>>>`                                                  |

---

## Error Handling

| Error         | Fix                                 |
| ------------- | ----------------------------------- |
| `status 401`  | Proxy auth error                    |
| `status 429`  | Rate limited — wait and retry       |
| `failed`      | Retry with different prompt         |
| `nsfw`        | Content flagged — modify prompt     |
| `ip_detected` | IP content detected — modify prompt |
