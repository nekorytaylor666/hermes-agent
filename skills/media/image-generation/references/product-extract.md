# Product URL Extraction Pipeline

When a user pastes a product page URL (Amazon, Shopify, AliExpress, Google Store, etc.), run this pipeline automatically. No user approval needed.

## Step 1: Extract Product Data + Images

Use `fetchcli fetch` with **`--formats json` only** and `--prompt` to extract structured product data and gallery image URLs in a single call. The LLM extraction reads the page and returns a compact JSON object with curated product images.

**CRITICAL: Do NOT add `markdown` to the formats.** Marketplace pages produce 100KB+ of markdown that will truncate the output and bury the extracted data. The `json` format alone is sufficient — it returns product info AND image URLs in ~2-3KB.

```bash
fetchcli fetch \
  --url "USER_URL" \
  --formats json \
  --prompt "Extract product name, brand, price, currency, selected color/variant, full description, all feature bullet points, technical specifications, and ALL product image URLs from the main gallery (front, side, back, close-up, packaging). Classify each image by section: main_gallery, description, review, other. Return 3-8 unique product gallery images. EXCLUDE user review photos, related products, navigation, banners, color swatch icons, size charts, logos."
```

The response `json` field contains the structured product data including curated image URLs.

## Step 2: Filter Images (extraction side)

From the extracted `images` array:

1. **DISCARD immediately**: `section: "review"` — user-submitted review photos are low quality and unusable
2. **DISCARD immediately**: `section: "other"` — navigation, banners, ads, unrelated images
3. **KEEP only**: `section: "main_gallery"` (priority) and `section: "description"`
4. Prefer `main_gallery` images first. Only use `description` images if fewer than 5 from gallery.

## Step 3: Visual Filter (Claude)

The extraction tool cannot analyze image content — it only reads page HTML. So Claude must visually verify each image:

1. Download kept images: `curl -sL -o /tmp/product_N.jpg "IMAGE_URL"`
2. View each image using the Read tool
3. **DISCARD** images where a human face is clearly visible
4. **DISCARD** images showing a different color/variant/design of the product than the one on the product page. The images must show the EXACT same product — same color, same design, same variant as listed on the page.
5. **KEEP** images that show the exact product only (hands holding a product are OK, faces are not)
6. Take up to **5** best product images

If after filtering there are 0 usable images, tell the user: "All product images on this page contain people. Here are the best product shots available:" and show the 2-3 where the product is most prominent.

## Step 4: Write Description (Claude)

Using the raw extracted data (features, specifications, description), write a rich product description. Rules:

- **Language**: Match the user's conversation language
- **Length**: 150-300 words, detailed but scannable
- **Structure**: Product name + brand → what it is (1 sentence) → key selling points (3-5) → technical highlights → who it's for
- **Tone**: Informative, not salesy. Focus on facts and real benefits
- **Include**: All meaningful specs (dimensions, weight, materials, compatibility)
- **Exclude**: Generic marketing fluff, unverifiable claims

## Step 5: Deliver to User

Present to the user:
1. Product images (up to 5, filtered and verified)
2. Detailed description
3. Price and key specs

No questions, no approval prompts. Just deliver.

## When to Also Generate Marketing Images

Only if the user **explicitly asks** for generation ("make an ad", "create a creative", "generate marketing images"). In that case, after delivering the product data, proceed to `/image-skill` Workflow B with the extracted product images as references.
