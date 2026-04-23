---
name: amazon-product-listing
description: |
  Creates professional Amazon marketplace product images (main image, secondary images, A+ content) from a product photo or product URL. Use this skill whenever the user mentions Amazon listings, Amazon product images, main image + secondary images, A+ content, A+ page, product infographics for e-commerce, lifestyle shots for Amazon, Amazon compliance, or wants to generate any set of product images that must follow Amazon marketplace requirements. Always use this skill when the user provides a product image or product URL and asks for Amazon-ready visuals — even if they don't explicitly say "Amazon skill" or "listing skill". The skill handles product analysis, compliance-safe generation via higgsfieldcli (nano_banana_2 model), and produces images that pass Amazon's Suppressed Listing checks.
---

# Amazon Product Listing Designer

Turns a single product photo or product URL into a full set of Amazon-compliant marketplace images: main image, secondary images (infographics, multi-angle, detail shots, lifestyle, variants, what's in box, size reference), and A+ Brand Content modules. All generation happens through `higgsfieldcli` using the `nano_banana_2` model.

## When to use this skill

- User provides a product image or a product URL and asks for Amazon images
- User mentions "main image", "secondary images", "A+ content", "A+ page", "Amazon listing"
- User wants product infographics, lifestyle shots, or feature callouts for e-commerce
- User asks to improve an existing Amazon listing's visuals

## When NOT to use this skill

- Generic product photography requests with no Amazon context
- Social media content (Instagram, TikTok posts) — use a different skill
- Video generation — this skill is image-only
- Logo or brand identity design

---

## Workflow (4 steps)

### Step 1 — Autonomous product analysis

Analyze the input without asking questions first.

**If input is an image:** Examine it visually. Identify product name, brand, category, packaging type (bottle/can/box/pouch), colors, flavor/variant, key visible features, and materials.

**If input is a URL:** Use `fetchcli fetch` with **`--formats json` only** and `--prompt` to extract structured product data in a single call. Do NOT add `markdown` — marketplace pages produce 100KB+ of markdown that truncates the output.

```bash
fetchcli fetch --url "<PRODUCT_URL>" --formats json \
  --prompt "Extract product name, brand, price, full description, all feature bullet points, available variants/colors, and ALL product image URLs from the main gallery. Return 3-8 unique product images. EXCLUDE review photos, related products, navigation, banners, logos."
```

If `fetchcli` returns empty or incomplete content, fall back to `searchcli read`:

```bash
searchcli read --url "<PRODUCT_URL>" --with-alt --wait-for-selector "#productTitle"
```

If both tools fail (geo-restricted, blocked), ask the user to share the product image directly.

**Extract these data points:**
- Product name
- Brand
- Category (beverage, skincare, electronics, apparel, food, etc.)
- Packaging (aluminum can, glass bottle, plastic pouch, box, etc.)
- Visual characteristics (colors, shape, size)
- Flavor / variant / model
- Key selling points (if visible on packaging or in URL content)
- Target user hypothesis (based on product type)

### Step 2 — Present the plan (single confirmation question)

Use this exact structure (adapt to the user's language — Russian or English):

```
What I see: [1-2 sentence product description with brand, category, key details]

Amazon image plan:
Per Amazon standards, I can create:

1. Main Image (1) — product on pure white background, compliant with Amazon's mandatory rules
2. Secondary Images (6):
   • Infographic with key benefits
   • Multi-angle shots
   • Lifestyle images (product in use)
   • Detail shots
   • Variants (if applicable)
   • What's in the box
3. A+ Content (8 modules) — for the extended brand page

What would you like me to create?
• Complete set (main + 6 secondary + A+ page)?
• Product images only (main + 6 secondary)?
• A+ page only?
• Or start with the main image and continue from there?
```

### Step 3 — Handle corrections and scope confirmation

If the user corrects the product analysis ("it's not peach, it's passion fruit" / "the brand is spelled differently") — update the internal understanding and apply the correction to ALL subsequent prompts.

If the user picks a scope — proceed to Step 4.

If the user's request is vague — default to generating the main image first, then ask which secondary they want next.

### Step 4 — Generation (in the correct order)

**Critical order:** Main image ALWAYS first. It establishes the visual baseline and is used as a reference in every subsequent image for product consistency.

**Execution flow:**

1. **Upload product reference** — single upload call → capture `$PRODUCT_UPLOAD_ID`
2. **Generate main image** — single generation call with the product upload as reference
3. **Poll main image** until `completed` — MANDATORY before any downstream generation, because every other image references `$MAIN_JOB_ID`
4. **Generate ALL remaining images AS ONE BATCH** — whatever the user asked for (secondary only, A+ only, full set, or custom subset) goes in a SINGLE `generate --json` array call. If user wants 14 images → 14 entries. If 8 → 8 entries. If 3 → 3 entries. All run concurrently on the backend. Every entry references `$MAIN_JOB_ID` in its `"images"` array.
5. **Poll each job** as they complete. As each one finishes, download it and call `present_files` immediately — do NOT wait for the entire batch before showing the first result. User sees images stream in one by one as they become ready.

**One batch means exactly one `generate` call for everything after main.** No splitting into secondary batch + A+ batch. One array, all items at once, maximum parallelism.

**Timing expectation:** With one batch of parallel generation, a full 15-image set completes in ~1 minute of wall-clock time (dominated by main image + slowest item in the batch), versus ~8 minutes if done one-by-one.

---

## higgsfieldcli Integration

### Model

**Only `nano_banana_2` is used in this skill.** Do NOT use `text2image_soul_v2`, `soul_cast`, or any other model — even for lifestyle images with people. Nano Banana Pro handles product + person composition well enough, and using one model guarantees visual consistency across the whole set.

### Aspect ratios and resolution

| Image type | `aspect_ratio` |
|------------|----------------|
| Main image | `1:1` |
| All secondary images | `1:1` |
| A+ Hero Banner (Module 1) | `21:9` |
| A+ Modules 2–7 | `3:2` |
| A+ Brand Endorsement (Module 8) | `21:9` |

**Resolution:** all images generated at `"resolution":"2k"`. Never specify `width` / `height` in pixels — always use `aspect_ratio` + `resolution`. The backend sizes the image correctly for the chosen ratio at 2k quality.

### Upload product reference

```bash
higgsfieldcli upload --file /path/to/product.png
```

Returns `{"id": "media_abc", ...}`. Save the `id` as `$PRODUCT_UPLOAD_ID`.

**Note:** No `--force-ip-check` flag needed — that's only for video generation. Images don't require it.

### Generate main image

```bash
CREATED=$(higgsfieldcli generate --json '[{
  "model":"nano_banana_2",
  "prompt":"[MAIN_IMAGE_PROMPT]",
  "aspect_ratio":"1:1",
  "resolution":"2k",
  "images":[{"id":"'$PRODUCT_UPLOAD_ID'","type":"media_input"}]
}]')
MAIN_JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d[0]['job_ids'][0])")
```

### Poll main image to completion

```bash
higgsfieldcli status --job-id "$MAIN_JOB_ID" --poll
```

Wait for `"status":"completed"`. If `"status":"ip_detected"` or `"status":"nsfw"` — modify the prompt (remove trademarked language or ambiguous content) and retry.

### Generate ALL remaining images as ONE batch

After main image is polled to completion, submit everything the user asked for in a SINGLE `generate --json` array call. The array length = exactly the number of images the user requested. All items run concurrently on the backend.

For `nano_banana_2`, references go in `"images"` array (NOT `"medias"`). Every entry references `$MAIN_JOB_ID` with `"type":"nano_banana_2_job"`.

**Example — full set (14 images: 6 secondary + 8 A+):**

```bash
CREATED=$(higgsfieldcli generate --json '[
  {"model":"nano_banana_2","prompt":"[INFOGRAPHIC_PROMPT]","aspect_ratio":"1:1","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[MULTI_ANGLE_PROMPT]","aspect_ratio":"1:1","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[DETAIL_SHOT_PROMPT]","aspect_ratio":"1:1","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[LIFESTYLE_1_PROMPT]","aspect_ratio":"1:1","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[LIFESTYLE_2_PROMPT]","aspect_ratio":"1:1","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[VARIANTS_OR_WHATS_IN_BOX_PROMPT]","aspect_ratio":"1:1","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_1_HERO_BANNER]","aspect_ratio":"21:9","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_2_PAIN_POINTS]","aspect_ratio":"3:2","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_3_FEATURES]","aspect_ratio":"3:2","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_4_INGREDIENTS]","aspect_ratio":"3:2","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_5_EFFICACY]","aspect_ratio":"3:2","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_6_HOW_TO_USE]","aspect_ratio":"3:2","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_7_VARIANTS]","aspect_ratio":"3:2","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]},
  {"model":"nano_banana_2","prompt":"[APLUS_MODULE_8_ENDORSEMENT]","aspect_ratio":"21:9","resolution":"2k","images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]}
]')

# Parse ALL job_ids — CREATED is a JSON array with one entry per submitted image
# Each entry has "index" (0-based) matching input position
ALL_JOBS=$(echo "$CREATED" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(' '.join([item['job_ids'][0] for item in d]))")
```

Then poll each one as it finishes and present to user:

```bash
# Poll each in turn — as each completes, download and present immediately
for JOB_ID in $ALL_JOBS; do
  higgsfieldcli status --job-id "$JOB_ID" --poll
  # status --poll blocks until terminal — download result URL and call present_files here
done
```

The backend runs all items concurrently regardless of polling order — the bottleneck is the slowest single image, not the sum.

**Example — "A+ page only" (8 images):** just 8 entries in the array, no secondary.

**Example — "3 different infographics" (3 images after main):** 3 entries in the array, each infographic with different angle/layout, all `aspect_ratio:"1:1"`.

**Key reference rules:**
- `"type":"nano_banana_2_job"` when referencing the main image (a previous Nano Banana result)
- `"type":"media_input"` only when referencing a freshly uploaded file (main image generation only)
- Batch array order is preserved — `d[0]` is the first prompt submitted, `d[N-1]` is the last

### Partial scope handling

**Core principle:** batch size = exactly what the user asked for. Don't pad with extras, don't drop requested items. If they ask for N images, submit N entries in a single batch.

Examples:
- "Full set" → 1 main + batch of 14 (6 secondary + 8 A+) = 15 images total
- "Product images only" → 1 main + batch of 6 = 7 total
- "A+ page only" → 1 main + batch of 8 = 9 total (main still needed as reference anchor for product consistency)
- "Only infographic and lifestyle" → 1 main + batch of 2 = 3 total
- "3 different infographic variations" → 1 main + batch of 3 infographics (different layouts) = 4 total
- "Main + A+ modules 1, 3, 6" → 1 main + batch of 3 A+ modules = 4 total
- "Give me 15 images" (no breakdown specified) → default carousel recipe: 1 main + 14 (6 secondary + 8 A+)

**Single batch for everything after main.** Whatever mix of secondary and A+ the user wants, all items go in ONE `generate --json` call. Different `aspect_ratio` values per item are fine — the array can mix `1:1`, `3:2`, `21:9` in the same call. The CLI runs everything concurrently regardless of batch size or ratio mix.

### Downloading and presenting the results

After each poll returns `completed`, extract the result URL from the status response, download the file to `/mnt/user-data/outputs/` with a descriptive kebab-case filename (e.g. `lapochka-peach-lemonade-infographic.jpg`), and call `present_files` to show the user. Present each image AS IT COMPLETES inside the batch loop — do not accumulate all 6 and dump them at once.

---

## Multi-image consistency (critical rules)

1. **Main image first** — always. It's the visual anchor for the whole set.
2. **Reference main image** — every secondary and every A+ module prompt must include `"images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]`.
3. **Consistent product appearance** — product color, material, shape, label design must be identical across all images. The reference enforces this; do not over-describe the product in the prompt (let the reference do the work).
4. **Unified visual style** — pick a color palette, font style, and icon style for the whole set. State these constraints in every prompt.

---

## Compliance Checklist (run before EVERY generation)

**Before generating the MAIN IMAGE**, verify the prompt includes ALL of the following:
- [ ] Background: pure white RGB 255,255,255
- [ ] Product fills ≥85% of the frame
- [ ] Shot at 45-degree angle (shows volume)
- [ ] Soft even lighting, no harsh shadows
- [ ] 1:1 square composition, product centered
- [ ] Photorealistic, looks like a real photograph
- [ ] Explicit negatives: no text, no logos (except those physically on the product), no watermarks, no badges, no props, no packaging boxes, no decorative graphics, no borders, no color blocks
- [ ] For apparel only: live model or invisible mannequin, model standing, not sitting/lying

**Suppressed Listing triggers** — these MUST be in the negative section of every main image prompt:
- "Amazon's Choice", "Prime", "Bestseller", "Sale", "New", "Free Shipping" badges
- Review screenshots
- Seller contact info (email, phone, website, URLs)
- Price tags
- Collage of multiple product angles in one frame

**Before generating SECONDARY IMAGES**, verify:
- [ ] Text is ≥30pt (readable on mobile after Amazon's image compression)
- [ ] One core message per image — no clutter
- [ ] Product reference (main image JOB_ID) is included in the `"images"` array
- [ ] Critical content is NOT in the outer 5% of the frame (mobile cropping)
- [ ] High contrast between text and background
- [ ] Max 2-3 font families, max 4-6 selling points per infographic

**Before generating A+ MODULES**, additionally verify:
- [ ] Correct ratio per module (21:9 for Hero/Endorsement, 3:2 for middle modules)
- [ ] Text size ≥30pt (Amazon compresses A+ images aggressively)
- [ ] Narrative flows from module to module (problem → solution → proof → use → variants → brand)
- [ ] Consistent brand visual identity across all 8 modules

**Absolutely prohibited across ALL images (main, secondary, A+):**
- Nudity, sexual content, or suggestive imagery
- Violence, blood, or cruelty
- Copyrighted third-party imagery (no copying competitor photos)
- Unverifiable claims ("#1 best", "FDA approved" without proof)

---

## Iteration guidance

When the user is not satisfied with a generated image, ask guiding questions instead of regenerating blindly:

- "Is the product itself wrong, or is it the background / scene?"
- "Does the selling point text need different wording?"
- "Does the lifestyle scene match your target customer?"
- "Can you share a competitor's image you like as a reference?"

For text changes on infographics — regenerate only the problem image, not the whole set.
For product appearance changes — regenerate main image first, then all downstream images that reference it.

---

## Reference Files

Load the relevant reference file(s) BEFORE building prompts:

- **`references/main_image_rules.md`** — Read before generating the main image. Contains mandatory Amazon rules, Suppressed Listing triggers, apparel-specific rules, and the 45° angle guidance.

- **`references/secondary_images.md`** — Read when generating any secondary image. Contains the 7 secondary types, the default 6-image carousel recipe, and per-type key principles.

- **`references/aplus_modules.md`** — Read when generating A+ content. Contains the 8 modules with exact specs, narrative structure, and mobile cropping rules.

- **`references/technical_specs.md`** — Read when the user asks about file formats, sizes, or delivery. Contains JPEG/PNG/TIFF rules, sRGB color profile, DPI requirements.

- **`references/category_conventions.md`** — Read when you identify the product category. Contains category-specific conventions for beverages, food, skincare, electronics, apparel, pet products, etc.

## Prompt Templates

Load the relevant template file BEFORE each generation. These files contain the actual prompt structures to send to `nano_banana_2`:

- `assets/prompt_templates/main_image.md`
- `assets/prompt_templates/infographic.md`
- `assets/prompt_templates/multi_angle.md`
- `assets/prompt_templates/detail_shot.md`
- `assets/prompt_templates/lifestyle.md`
- `assets/prompt_templates/variants.md`
- `assets/prompt_templates/whats_in_box.md`
- `assets/prompt_templates/size_reference.md`
- `assets/prompt_templates/aplus_modules.md`

Each template uses `[PLACEHOLDER]` syntax. Fill placeholders with data from Step 1 (product analysis). Never send a prompt with unfilled placeholders.
