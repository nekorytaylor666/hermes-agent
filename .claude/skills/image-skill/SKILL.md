---
name: image-skill
description: |
  Image generation skill. Loaded by Mr Higgs for simple text-to-image, or by image-agent for complex generation (references, batch, inspiration, posters).
---

# Image Generation

Pick the right model, read its reference file, craft the prompt accordingly.

## Soul ID Gate (precedes model selection)

If the brief includes a `soul_id`, use `text2image_soul_v2` with that `soul_id` parameter — skip the model selection table below entirely. Soul Cast is a different mode (random character casting) and does NOT accept `soul_id`; never route a trained Soul ID through Soul Cast.

**Payload shape:**

```json
{
  "model": "text2image_soul_v2",
  "prompt": "...",
  "soul_id": "<SOUL_ID>",
  "aspect_ratio": "3:4",
  "preset": "general"
}
```

For frames in the same batch that do NOT need the trained face (pure texture, object, or background shots), the gate does not apply — those frames use the normal model selection table.

## Model Selection

**Override rule:** If the caller explicitly specifies a model, use that model — skip the table below.

**Editing / Multiplying rule:** When the task is **editing** an existing image (pose changes, angle changes, outfit swaps, background swaps, color changes, small detail tweaks) or **multiplying** content (creating variations, alternate versions, or any derivative of an existing image), always use **Nano Banana Pro** — unless the edit is heavy/detail-dense (many simultaneous detail changes or precise typography → GPT Image 2.0). **Soul 2.0** is strictly for **creating new original content** from scratch. Soul 2.0 must never be used for edits or variations of existing images.

Otherwise, first match wins:

| Model                | When to use                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Reference                                                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Seedream V5 Lite** | Editing a REAL PHOTOGRAPH of a real person where their face identity must be preserved. Only for photographic face edits (face swaps, likeness compositing from real photos). NEVER for cartoon, stylized, 3D, illustrated, or AI-generated characters — those go to Nano Banana Pro even if a face is present                                                                                                                                                                                                      | `.claude/skills/image-skill/references/seedream.md`                                                |
| **Seedream V4.5**    | High-quality image generation with input image support. Similar to V5 Lite but different model version. Do NOT use for: product compositing, e-commerce images, Amazon listings, aesthetic/editorial content, or text rendering — use Nano Banana Pro for compositing/e-commerce/text, Soul 2.0 for aesthetic/editorial                                                                                                                                                                                              | `.claude/skills/image-skill/references/seedream.md`                                                |
| **Soul Cast**        | Cinematic character creation before video generation — "create a character for a video", "cast a character for a scene", "design a person to use in video". Creates characters that should be saved as **elements** for reuse. Text-to-image only, no image-to-image                                                                                                                                                                                                                                              | No reference file — use `higgsfieldcli generate --json '[{"model":"soul_cast",...}]'` directly     |
| **Soul Location**    | Location/environment generation — "create a setting", "generate a background", "make a scene location". Creates environments that should be saved as **elements** for reuse                                                                                                                                                                                                                                                                                                                                       | No reference file — use `higgsfieldcli generate --json '[{"model":"soul_location",...}]'` directly |
| **Soul Cinematic**   | Cinematic stills, moodboards, film-reference frames — use when there is **no named actor or specific person's face** required. For a cinematic still that needs a specific actor's face → use Nano Banana Pro instead                                                                                                                                                                                                                                                                                               | `.claude/skills/image-skill/references/soul-cinematic.md`                                          |
| **Soul 2.0**          | Default for person/character generation: UGC, influencer, editorial, fashion, y2k, streetwear, Kodak/film aesthetics. Use when **vibe > strict feature accuracy** AND **no IP/exotic trigger** (no named characters — Spiderman, Disney, anime; no real actor likeness; no hard-to-render exotic features — vitiligo, heterochromia, specific height, rare feature combos)                                                                                                                                        | `.claude/skills/image-skill/references/soul-v2-avatar.md`                                          |
| **GPT Image 2.0**      | Heavy/detail-dense only — use ONLY when the task needs super-specific control that Nano Banana Pro can't deliver: posters, cards, menus, infographics with **real quoted text rendered accurately**; fixed layouts with multiple elements in **specific positions**; UI mockups, webpage replications, screen recreations, game assets, presentation slides; heavy edits changing many small details at once / precise typography. **NOT for simple color swaps or background changes** — those go to Nano Banana Pro | `.claude/skills/image-skill/references/imagegen-2.md`                                               |
| **Nano Banana Pro**    | **DEFAULT model.** IP/identity precision (named characters — Spiderman, Disney, anime; real actor likeness; exotic features — vitiligo, heterochromia, specific height, rare combos); cinematic stills needing a specific actor's face; all image edits (pose, angle, outfit, background, color, small tweaks); product compositing, e-commerce, Amazon listings, posters, thumbnails, banners, and any task not matched above                                                                                    | `.claude/skills/image-skill/references/banana.md`                                                  |

Read the matched reference file and follow its instructions.

## Input Workflows

### Workflow A: Plain Text Prompt

User provides a text description → pick model from table → read reference → craft prompt → generate.

### Workflow B: Reference Image (attached or URL to image)

User attaches an image or provides a direct image URL →
download image (`curl -sL -o /tmp/<descriptive-name>.jpg "URL"` — name after the content, e.g. `product-sneaker.jpg`) →
upload via `higgsfieldcli upload` →
read reference → generate with reference in `images`/`medias` array.

### Workflow C: Product Page URL (Extract + Show)

User pastes a product page URL (Amazon, Shopify, AliExpress, Google Store, etc.) →
read `.claude/skills/image-skill/references/product-extract.md` for full pipeline →
extract product data and images via `fetchcli fetch --formats json --prompt "..."` →
filter and visually verify images → write product description →
deliver images + description to user. **No approval prompts.**

**Only generate marketing images if user explicitly asks** ("make an ad", "create a creative").

### Workflow C2: Product Page URL → Marketing Generation

User pastes a product URL AND asks to generate creatives →
run Workflow C first (extract + show) →
then use extracted product images as references →
read `.claude/skills/image-skill/references/banana.md` → generate marketing images with reference.

### Workflow D: Trend-Informed Generation

User asks for trend analysis + generation →
delegate research to `/trend-picker` → receive concepts →
read appropriate reference → generate images based on concepts.

## Format-Specific References

| Format                              | Reference File                                               | When                                                               |
| ----------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| Avatar, influencer, person portrait | `.claude/skills/image-skill/references/soul-v2-avatar.md`    | User says "avatar", "influencer", "profile pic", "create a person" |
| Product page URL                    | `.claude/skills/image-skill/references/product-extract.md`   | User pastes a product URL (Amazon, Shopify, etc.)                  |
| Posters, banners, launch images     | `.claude/skills/image-skill/references/poster-design.md`     | User says "poster", "banner", "promotional image"                  |
| YouTube thumbnails                  | `.claude/skills/image-skill/references/youtube-thumbnail.md` | User says "thumbnail", "preview image", "превью"                   |
| All other formats                   | `.claude/skills/image-skill/references/banana.md`            | Default for everything                                             |

Always read the matched reference file and follow its prompt structure and rules.

## Batch Generation (Parallel)

When the user requests multiple images (carousel, set, variants, A/B), **style consistency is mandatory and non-negotiable by default** — every image in the set must feel like it was designed by the same person in the same session.

**Parallel execution:** The CLI supports concurrent generation via a JSON array. Instead of running `generate --json '{...}]'` separately for each image, batch all images into a single call:

```bash
higgsfieldcli generate --json '[
  {"model":"nano_banana_2","prompt":"...image 1...","aspect_ratio":"1:1"},
  {"model":"nano_banana_2","prompt":"...image 2...","aspect_ratio":"1:1"},
  {"model":"nano_banana_2","prompt":"...image 3...","aspect_ratio":"1:1"}
]'
```

All items in the array execute concurrently. The output is a single JSON array ordered by input index:

```json
[
  {
    "index": 0,
    "job_set_id": "...",
    "job_set_type": "nano_banana_2",
    "job_ids": ["job_..."],
    "status": "created"
  },
  {
    "index": 1,
    "job_set_id": "...",
    "job_set_type": "nano_banana_2",
    "job_ids": ["job_..."],
    "status": "created"
  },
  {
    "index": 2,
    "job_set_id": "...",
    "job_set_type": "nano_banana_2",
    "job_ids": ["job_..."],
    "status": "created"
  }
]
```

Each entry's `index` matches the position in the input array (0-based). Failed items have `"status":"failed"` and an `"error"` field. Track the `index` → `job_ids` mapping so the user can reference individual results by number (e.g., "change the third image" → index 2).

**When to use parallel generation:**

- Carousel / set / campaign images — all share the same Visual DNA, only Subject varies
- A/B test variants — same style, different composition/layout
- Character + location generation (different models OK in the same array)
- Any batch where images are independent (no image depends on another's result)

**When NOT to use parallel generation:**

- Image B uses Image A's result as a reference (e.g., character sheet needs the render first)
- Sequential upload → generate workflows where the upload ID feeds into the next generation

### Step 0: Lock the Visual DNA first

Before writing any individual prompts, define and write down the shared constants for the entire batch:

```
Visual DNA:
- Designer/artist: [one name from banana.md — same for ALL images]
- Color palette: [exact hue names — same across ALL images]
- Design language: [e.g. neo-brutalist / Swiss editorial / glassmorphism — same for ALL]
- Lighting: [type, direction, temperature — same for ALL]
- Mood/energy: [e.g. bold and loud / calm and luxurious — same for ALL]
- Texture/surface: [e.g. paper grain / clean digital / concrete — same for ALL]
- Typography treatment: [weight, style — same for ALL]
```

If inspiration ran (Step 0 of Design Inspiration), the Visual DNA comes directly from the chosen template's analysis. Do not invent a new palette or designer per image — pick once, lock it.

### Per-image variation (what CAN change)

Only these elements vary across images in a batch:

| What varies                                         | What stays locked           |
| --------------------------------------------------- | --------------------------- |
| Subject (what object/scene is shown)                | Designer reference          |
| Composition layout (centered vs. diagonal vs. grid) | Color palette               |
| Angle or perspective                                | Lighting type and direction |
| Props or background elements                        | Mood and energy             |
| Text copy content                                   | Typography weight and style |
| Focal point placement                               | Design language             |

### Batch types

- **Carousel/set** (e.g., "5 Instagram cards"): Build all prompts with `"batch_size":1`, each with different Subject/Composition but identical Style/Instructions from the Visual DNA. Submit as a JSON array for parallel generation.
- **Color/edit variants**: Same reference image, change only the relevant axis (hue, background color, etc.) — all other style locked. Submit as a JSON array.
- **A/B testing**: Vary composition, angle, layout — but same designer, same palette, same mood. A/B tests designs, not brand identities. Submit as a JSON array.
- **Campaign sets**: Visual DNA is the campaign identity. Subjects and compositions vary; everything else is frozen. Submit as a JSON array.

### Prompt construction for each image in a batch

Copy the Style + Instructions block verbatim from the first image's prompt into every subsequent image's prompt. Only rewrite the Subject and Text sections per image. This is what makes the set look cohesive.

### Parallel generation command

After constructing all prompts, submit them in one call:

```bash
higgsfieldcli generate --json '[
  {"model":"nano_banana_2","prompt":"[Subject 1] [shared Style+Instructions]","aspect_ratio":"1:1"},
  {"model":"nano_banana_2","prompt":"[Subject 2] [shared Style+Instructions]","aspect_ratio":"1:1"},
  {"model":"nano_banana_2","prompt":"[Subject 3] [shared Style+Instructions]","aspect_ratio":"1:1"}
]'
```

The output is a single JSON array ordered by input index — each entry has `"index"`, `"job_ids"`, `"job_set_type"`, and `"status"`. Track the index → job_ids mapping so the user can reference individual results by number (e.g., "change the third image" → index 2). All jobs run concurrently — total wall-clock time ≈ single image time instead of N× serial.

## Aspect Ratio Guide

| Use Case                     | Aspect Ratio   | Typical Platform   |
| ---------------------------- | -------------- | ------------------ |
| Instagram feed post          | `1:1` or `3:4` | Instagram          |
| Instagram Story / Reel cover | `9:16`         | Instagram, TikTok  |
| Facebook / LinkedIn ad       | `1:1`          | Facebook, LinkedIn |
| YouTube thumbnail            | `16:9`         | YouTube            |
| Pinterest pin                | `9:16`         | Pinterest          |
| Product shot / e-commerce    | `3:4`          | Amazon, Shopify    |
| Banner / hero image          | `16:9`         | Web                |
| Infographic / poster         | `9:16`         | Print, social      |

## Step 0: Design Inspiration (inspiration — design formats only)

Query the template index to get design inspiration from real templates before constructing a designed-format NB2 prompt.

### Preflight

Before anything else, ask: **is the output a designed marketing piece with open visual-language decisions?**

Positive triggers (inspiration pays off): poster, banner, thumbnail, social ad creative, carousel card, campaign image, launch visual, promotional graphic, infographic, Facebook post, Instagram post, Instagram story, invitation, logo, graph design, photo collage, presentation slide — or semantic equivalents in any language.

- **No** → skip Step 0 entirely, go straight to prompt construction.
- **Yes** → check the skip table below; if nothing matches, run Step 0.

### When to skip

Skip Step 0 (inspiration) if **any** of the following are true:

| Condition                                            | Signal                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model is not NB2                                     | Routing to Soul Cinematic, Seedream, Soul 2.0, Soul Cast, or Soul Location                                                                                                                                                                                                                                                                                                  |
| User provided a **style/mood reference** image       | User explicitly says "inspired by this", "match this vibe", "recreate this composition" — the image is a visual brief for _how_ to generate, not _what_ to generate. inspiration competes with it and dilutes the direction.                                                                                                                                               |
| Output is fully user-specified                       | Explicit background color/style + explicit composition + explicit layout all given (e.g., "white studio background, flat lay, 1:1 recreation")                                                                                                                                                                                                                             |
| Task is single-axis mechanical                       | User specifies exactly one thing to change (color, background, angle, scale) and everything else stays locked. No open design decisions exist — the output is fully determined by the instruction + the reference image.                                                                                                                                                   |
| Subject-render, not a designed format                | Prompt asks for a scene, portrait, illustration, product shot, or realistic image with no layout/typography/marketing intent. Trigger words: "image of", "picture of", "photo of", "render of", "illustration of", "scene", "headshot", "portrait", "character concept". No format words like _poster / banner / thumbnail / ad / creative / carousel / campaign / promo_. |
| Explicit art style named in prompt                   | User named a concrete visual language: "claymation", "watercolor", "anime", "Studio Ghibli", "Van Gogh", "vector flat", "3D render", "pixel art", "line art", "cyberpunk neon", etc. Style is already locked — inspiration templates would dilute it.                                                                                                                      |
| Plain product-on-background / studio shot            | "product on white", "studio shot", "flat lay on wood", "isolated on gradient" — standard e-commerce composition, no design retrieval needed.                                                                                                                                                                                                                               |
| Person / character generation without marketing wrap | "avatar", "profile pic", "headshot", "character design", "person doing X" — the goal is the person itself, not a poster-_featuring_-a-person. If the user says "poster featuring X", inspiration still runs.                                                                                                                                                               |
| Batch continuation within same conversation          | Visual DNA has already been locked from a prior inspiration run in this session (carousel/set/campaign). Reuse it — never re-run inspiration per item.                                                                                                                                                                                                                     |

**Default is skip.** Only run Step 0 when the preflight answered _yes_ AND none of the skip rows match. inspiration is opt-in for design-heavy formats, not a blanket pre-step.

### 1. Derive a query string

3–7 English words describing visual format + mood + subject type. Not the product name.

- "make an ad for our protein shake" → `"fitness product energetic dark ad"`
- "minimalist jazz concert poster" → `"jazz concert minimalist poster typography"`
- "cozy winter skincare carousel" → `"winter skincare warm pastel lifestyle"`

### 2. Run the inspiration query with download

```bash
higgsfieldcli inspiration --query "<derived query string>" --top-k 5 --download
```

The `--download` flag automatically downloads all result files (template images) to a temporary folder. Returns JSON with:

- `directory` — path to the temp folder containing downloaded files
- `files` — list of successfully downloaded filenames

### 3. View all returned templates

Use the Read tool on each downloaded file in the temp directory. View all returned images.

### 4. Pick the most visually relevant template

Select the one whose visual content — layout, design style, subject treatment, color mood — best matches what the user wants to create. FAISS score is a starting point; your visual judgment overrides it when a lower-ranked result is a better fit.

### 5. Analyze the chosen template

Extract all of the following. Be specific — generic words ("blue", "minimal") are useless; precise descriptors ("powder blue with cobalt accent", "sparse single-object layout with 60% negative space") are what drive the generation.

**Color**

- Exact hue names for dominant, accent, and background (e.g. "dusty terracotta", "off-white cream", "deep forest green" — not "warm tones")
- Contrast level: high-contrast, mid-tone, low-contrast tonal
- Temperature: warm/cool/neutral; any color grading cast (golden, desaturated, cyan-tinted)
- Color count: monochromatic, duotone, limited palette (3–4 colors), full spectrum

**Lighting**

- Quality: hard (sharp shadows), soft (diffused, no hard edges), flat (no visible light direction)
- Direction: top-down, side (left/right), front-fill, rim/backlight, ambient
- Color temperature: warm (golden hour), cool (overcast), neutral studio
- Special: lens flare, glows, highlight bloom, gradient light wash

**Depth & dimensionality**

- Flat 2D vs. layered overlap vs. strong perspective depth
- Z-axis stacking: foreground / midground / background separation visible or absent
- Shadow treatment: sharp drop shadow, soft ambient shadow, no shadow, cast shadow on surface

**Texture & surface**

- Background surface: paper grain, concrete, fabric, clean digital, geometric pattern
- Overlay effects: film grain, halftone, noise, vignette, bokeh blur
- Finish: matte, glossy, metallic sheen, frosted glass

**Graphic elements**

- Geometric shapes: circles, rectangles, diagonal cuts, organic blobs present or absent
- Line work: thin rule lines, dividers, border frames, scan-line patterns
- Decorative: dot grids, badge/pill shapes, icons, abstract brush strokes, confetti

**Layout & composition**

- Structure: centered, rule-of-thirds, diagonal axis, grid with gutters, full-bleed
- Visual hierarchy: what the eye hits first → second → third
- Density: sparse (1–2 focal elements), balanced, dense (many elements)
- Negative space: generous / moderate / packed

**Typography** (note even if no text in template — identify the implied type treatment for the format)

- Weight: ultra-light, regular, bold, black/ultra-bold
- Style: serif, sans-serif, display, condensed, mono
- Scale contrast: large headline vs. small body, uniform scale
- Placement: centered, left-aligned, overlapping image, contained in a zone

**Design language & mood**

- Overall register: editorial, commercial, luxury, streetwear, clinical, playful, minimal
- Specific style: glassmorphism, neo-brutalism, Swiss grid, maximalist, Y2K, organic/earthy, corporate clean
- Energy: bold/loud, calm/quiet, urgent, aspirational, cozy

### 6. Translate observations to directives

Convert each analysis dimension into art-director language. Do not describe or mention the template — use it as a silent visual brief.

| Analysis                                  | Prompt directive                                                         |
| ----------------------------------------- | ------------------------------------------------------------------------ |
| "dusty terracotta + cream + forest green" | "earthy terracotta and cream color palette with deep green accent"       |
| "hard side lighting from upper left"      | "hard directional light from upper left casting sharp shadows"           |
| "flat 2D, no depth"                       | "flat graphic composition, zero depth, no cast shadows"                  |
| "strong z-axis layers"                    | "layered depth with foreground element overlapping midground subject"    |
| "paper grain overlay"                     | "subtle paper grain texture over the entire surface"                     |
| "diagonal geometric cut background"       | "diagonal color-block background split at 30° angle"                     |
| "ultra-bold condensed headline"           | "ultra-bold condensed sans-serif headline dominating upper third"        |
| "soft ambient shadow, no hard edges"      | "soft diffused ambient shadow, no hard drop shadows"                     |
| "dense layout, many elements"             | "rich layered composition with multiple overlapping elements"            |
| "glassmorphism"                           | "frosted glass panels with subtle transparency and blur"                 |
| "neo-brutalist"                           | "raw neo-brutalist layout, thick black borders, misaligned grid"         |
| "luxury editorial"                        | "luxury editorial aesthetic, generous negative space, refined restraint" |

### 7. Synthesize the full NB2 prompt (Enhancer)

After completing steps 1–6, write out the complete NB2 prompt in full before touching the CLI. Do not compose it while typing the bash command — write it here first.

**Three inputs → one prompt:**

1. **User request** — subject, intent, platform, any explicit constraints they stated
2. **Product/reference images** — if provided: object shape, exact colors, material, surface finish, key visual details that must be preserved
3. **inspiration template** — every dimension extracted in step 5, translated per step 6

**Output format** (follow `.claude/skills/image-skill/references/banana.md` for full rules):

```
[Subject]: [object, its exact visual properties from product images, positioning, surrounding elements]

[Style]: in style of [designer from banana.md], [exact inspiration color palette], [inspiration design language], [inspiration mood/energy register]

[Instructions]: [inspiration layout structure as a directive], [inspiration lighting type and direction], [inspiration shadow treatment], [inspiration depth/dimensionality], [inspiration texture/surface overlay], [inspiration graphic elements if any], [inspiration typography treatment], [any additional compositing notes from product images]

[Text]: [verbatim copy to render, font weight and style, size hierarchy, placement zone — omit entire section if no text needed]

[Constraints]: [aspect ratio], [what must NOT appear]
```

**Completeness check before submitting:** Every dimension from step 5 should appear somewhere in the prompt — color, lighting, depth, texture, graphic elements, layout, typography, mood. If a dimension is absent from the prompt, the generation will fill it randomly and likely diverge from the template's style.

**Hard constraints:**

- Never pass template URLs as `--image` to `higgsfieldcli` — template is for your analysis only
- For carousels/sets: run Step 0 once, apply the same visual DNA across all images in the set
- Do not paste keywords verbatim into the prompt — always translate to specific art-director directives
- If the inspiration returns no useful results, proceed normally without blocking

## Reference Image Source Detection (MANDATORY)

Before constructing the `images`/`medias` array, determine the source of each reference image:

### Case 1: Image is a result from a previous generation in this session

**How to detect:** You have a job ID and job_set_type from a prior `higgsfieldcli generate` command in the current conversation.

→ Do NOT upload. Use the job result directly:

- `"id"` = the job ID from the previous generation result
- `"type"` = `<model>_job` (e.g. `nano_banana_2_job`, `text2image_soul_v2_job`, `seedream_v5_job`)

### Case 2: Image is user-provided or from an external source

**How to detect:** The image URL was provided by the user, comes from an external website, or is a local file path — it was NOT generated by a previous `higgsfieldcli generate` command in this session.

→ Upload first via `higgsfieldcli upload`, then use:

- `"id"` = the upload response `id` field
- `"type"` = `media_input`

### Decision priority

Always check Case 1 first. If the image came from a generation in this conversation, you MUST use `<model>_job` type. Never re-upload generation results.

## CLI Workflow

**CRITICAL: Always use `higgsfieldcli generate --json '{...}]'` for ALL generation commands.** Never call model-specific subcommands like `higgsfieldcli image`, `higgsfieldcli video`, `higgsfieldcli nano-banana-2`, etc. — those are deprecated and will fail. The only generation interface is `generate --json`.

Every image generation follows this pattern:

1. **Select model** using the table above
2. **Read the model's reference file** for prompt rules and parameters
3. **Design Inspiration (NB2 only)**: Run Step 0 — query inspiration, view templates, analyze the best match, translate to directives, synthesize the full prompt using the Enhancer format. Skip if conditions in the "When to run" table are met.
4. **Reference elements** (if reusing characters/locations): embed `<<<element_id>>>` in the prompt
5. **Upload reference images** (if needed): `higgsfieldcli upload --file /path/to/image.png`
6. **Generate**:
   - **Single image**: `higgsfieldcli generate --json '[{"model":"<model_name>","prompt":"...","aspect_ratio":"3:4"}]'`
   - **Multiple independent images**: `higgsfieldcli generate --json '[{"model":"...","prompt":"..."},{"model":"...","prompt":"..."}]'` — all items run concurrently
   - Returns one `created` line per item immediately — capture `job_ids` and `job_set_type`. No polling unless the result is needed downstream.
7. **Create element** (if the result should be reused): poll with `higgsfieldcli status --job-id JOB_ID --poll` until completed, then `higgsfieldcli element create --category character --name "Name" --media "id=JOB_ID;type=image_job"`

### CLI Model Names (JSON format)

| Model            | JSON model name      |
| ---------------- | -------------------- |
| Nano Banana Pro    | `nano_banana_2`      |
| GPT Image 2.0      | `imagegen_2_0`       |
| Soul Cast        | `soul_cast`          |
| Soul Location    | `soul_location`      |
| Seedream V4.5    | `seedream_v4_5`      |
| Seedream V5 Lite | `seedream_v5_lite`   |
| Soul Cinematic   | `soul_cinematic`     |
| Soul 2.0          | `text2image_soul_v2` |

### Generate (text-to-image)

```bash
higgsfieldcli generate --json '[{"model":"nano_banana_2","prompt":"...","aspect_ratio":"3:4"}]'
```

Returns a `created` line immediately with `job_set_id`, `job_set_type`, `job_ids`. Do not wait. Poll only if the result is referenced downstream.

### Generate with Reference Image (image-to-image)

```bash
# 1. Upload reference image
UPLOAD=$(higgsfieldcli upload --file /path/to/image.png)
IMAGE_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2a. For nano_banana_2 / seedream_v4_5 — use "images" array
higgsfieldcli generate --json "[{\"model\":\"nano_banana_2\",\"prompt\":\"...\",\"images\":[{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}],\"aspect_ratio\":\"3:4\"}"

# 2b. For other models (soul_v2, soul_cinematic, seedream_v5_lite, seedance_2_0) — use "medias" array
higgsfieldcli generate --json "[{\"model\":\"text2image_soul_v2\",\"prompt\":\"...\",\"medias\":[{\"role\":\"image\",\"data\":{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}}],\"aspect_ratio\":\"3:4\"}"
```

### Image entry `type` values

Two sources of reference images, each with a different `type`:

| Source                                   | `type` value  | Example                      |
| ---------------------------------------- | ------------- | ---------------------------- |
| Uploaded via `higgsfieldcli upload`      | `media_input` | `"type":"media_input"`       |
| Job result (reusing a generation output) | `<model>_job` | `"type":"nano_banana_2_job"` |

**Exception:** `seedream_v5_lite` job results use `"type":"seedream_v5_job"` (not `seedream_v5_lite_job`).

### Parameters (JSON keys)

| Key               | Type   | Default    | Description                                                                                                                                                       |
| ----------------- | ------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`           | string | _required_ | Model name (e.g. `nano_banana_2`, `text2image_soul_v2`)                                                                                                           |
| `prompt`          | string | _required_ | Text prompt                                                                                                                                                       |
| `images`          | array  | —          | Reference images for `nano_banana_2`, `seedream_v4_5`. Each entry: `{"id":"ID","type":"TYPE"}`                                                                    |
| `medias`          | array  | —          | Reference images for `text2image_soul_v2`, `soul_cinematic`, `seedream_v5_lite`, `seedance_2_0`. Each entry: `{"role":"image","data":{"id":"ID","type":"TYPE"}}`  |
| `width`           | int    | `896`      | Image width in pixels                                                                                                                                             |
| `height`          | int    | `1200`     | Image height in pixels                                                                                                                                            |
| `aspect_ratio`    | string | `3:4`      | Model-dependent. Common: `1:1`, `3:4`, `4:3`, `9:16`, `16:9`. Soul 2.0/Cinematic add: `2:3`, `3:2`. Cinematic adds: `21:9`. NB2 adds: `4:5`, `5:4`, `21:9`, `auto` |
| `resolution`      | string | —          | NB2 only: `1k` (standard), `2k` (high), `4k` (ultra-high)                                                                                                         |
| `batch_size`      | int    | `1`        | Number of images to generate                                                                                                                                      |
| `quality`         | string | —          | Soul 2.0/Cinematic: `1080p` (2K) or `basic` (1.5K). Seedream V5: `basic` (2K) or `high` (3K). Seedream V4.5: `basic` (2K) or `high` (4K)                           |
| `enhance_prompt`  | bool   | —          | Enable prompt enhancement                                                                                                                                         |
| `negative_prompt` | string | —          | Negative prompt                                                                                                                                                   |
| `seed`            | int    | —          | Random seed                                                                                                                                                       |

### Recommended Sizes

| Use Case            | Aspect Ratio | Width | Height |
| ------------------- | ------------ | ----- | ------ |
| Vertical / story    | `9:16`       | 720   | 1280   |
| Portrait / product  | `3:4`        | 896   | 1200   |
| Tall portrait       | `2:3`        | 800   | 1200   |
| Instagram feed      | `4:5`        | 960   | 1200   |
| Square / social     | `1:1`        | 1024  | 1024   |
| Instagram landscape | `5:4`        | 1200  | 960    |
| Standard landscape  | `4:3`        | 1200  | 896    |
| Wide landscape      | `3:2`        | 1200  | 800    |
| Landscape / banner  | `16:9`       | 1200  | 675    |
| Ultra-wide          | `21:9`       | 1200  | 514    |

### Reference Elements

Elements are persistent references (characters, environments, props) created from generation results. Use them to maintain consistency across multiple generations.

**Creating elements:**

```bash
# Generate a character with soul_cast — fire-and-forget, capture job_id from created line
CREATED=$(higgsfieldcli generate --json '[{"model":"soul_cast","prompt":"a noir detective","width":1024,"height":1024,"batch_size":1,"character_params":{"genre":"Drama","budget":10}}]')
JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; print(json.loads(sys.stdin.read().splitlines()[0])['job_ids'][0])")

# Element creation needs the job to be completed → poll
higgsfieldcli status --job-id "$JOB_ID" --poll
higgsfieldcli element create --category character --name "Detective" \
  --media "id=$JOB_ID;type=image_job"
```

**Using elements in prompts** — embed `<<<element_uuid>>>` in the prompt. Only these models support element placeholders:

- `nano_banana_2`
- `seedream_v4_5`
- `seedream_v5_lite`
- `seedance_2_0`

Models that do **NOT** support elements: `soul_cast`, `soul_location`, `text2image_soul_v2`, `soul_cinematic`. For these, use `medias`/`images` arrays with uploaded media instead.

```bash
higgsfieldcli generate --json '[{"model":"nano_banana_2","prompt":"<<<abc123>>> portrait, dramatic lighting..."}]'
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"<<<abc123>>> walking down a rainy street..."}]'
```

**Listing existing elements:**

```bash
higgsfieldcli element list --size 20
higgsfieldcli element list --category character
```

## Polling — Fire-and-Forget

`higgsfieldcli generate` no longer blocks to completion. It prints a `created` line with `job_set_id`, `job_set_type`, and `job_ids` **immediately**, then returns. That first line is all you need for the default case — do NOT use long timeouts and do NOT run in background.

**Default: fire-and-forget.** Submit, capture `job_id` + `job_set_type`, report them, move on.

**Poll only when the result is referenced downstream:**

- Uploading the output as a reference for another generation (image→video, character sheet, compositing)
- `element create` needs the job to be completed
- User explicitly asks for the URL

Poll command:

```bash
higgsfieldcli status --job-id JOB_ID --poll
```

Returns `{"job_id","status","job_set_type","ip_check_finished","ip_detected","job_set_id","result":{"url","type"}}`. `result.url` is the CDN URL of the finished image; `result.type` is `"image"`. Build downstream references using `id=JOB_ID`, `type=<job_set_type>_job`. See `/higgsfield` skill for the full `job_set_type` → `type` mapping (note: `seedream_v5_lite` → `seedream_v5_job`).

## Error Handling

| Error        | Fix                                                                      |
| ------------ | ------------------------------------------------------------------------ |
| `status 401` | Proxy auth error                                                         |
| `status 429` | Rate limited — wait and retry                                            |
| `failed`     | Retry #1: same prompt. Retry #2: simplify prompt. Retry #3: switch model |
| `nsfw`       | Remove suggestive elements, retry once                                   |
