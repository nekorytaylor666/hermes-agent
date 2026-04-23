# Variants Prompt Template

Secondary image type showing all available variants of a product (colors, flavors, sizes, styles) arranged uniformly in a single frame. Helps customers understand the full option range and pick the variant that fits them.

## Placeholders

- `[PRODUCT_DESCRIPTION]` — base product description
- `[VARIANTS_LIST]` — list of specific variants with a distinguishing name. Examples:
  - Beverages: "Peach & Verbena, Raspberry & Mint, Lemon & Basil"
  - Skincare: "Travel 30ml, Standard 100ml, Family 250ml"
  - Apparel: "Black, Cream, Sage Green, Navy"
- `[VARIANT_COUNT]` — number of variants, typically 3 to 6

## Template

```
Amazon secondary image — product variants showcase for [PRODUCT_DESCRIPTION].

Layout:
- 1:1 square composition
- [VARIANT_COUNT] variants of the same product arranged in a clean horizontal row or grid
- Uniform spacing between variants
- All variants shown at the same angle, same size, same positioning
- Small labels below or beside each variant with its name

Variants to display:
[VARIANTS_LIST]

Consistency rules (critical):
- Every variant shown from the SAME angle
- Every variant at the SAME scale
- Every variant lit with the SAME lighting direction and intensity
- ONLY the variant attribute (color/flavor/size) differs between them
- Identical background for all variants
- All variants photographed as if from the same session

Variant labels (write EACH in this exact format):
- Variant 1 Label: "[VARIANT_1_NAME]" (30pt, sans-serif)
- Variant 2 Label: "[VARIANT_2_NAME]" (30pt, sans-serif)
- Variant 3 Label: "[VARIANT_3_NAME]" (30pt, sans-serif)
(add more variants as needed)

Typography for labels:
- **CRITICAL TEXT FORMAT RULE:** Every text element written as `Label: "exact text" (Xpt)`.
- Small, clean, sans-serif labels under each variant
- Same font, same 30pt size, same color for all labels
- Dark text on light background

Background:
- Pure white or very soft off-white gradient
- Minimal shadow under each variant
- Clean and minimal — variants are the focus

Quality:
- Hyperrealistic product photography
- Sharp focus on every variant
- Color accuracy is critical — each variant's true color must be rendered faithfully

Consistency with main image:
- Product shape, proportions, packaging design match the reference exactly
- Only the variant-distinguishing element changes

Strict exclusions:
- NO "Amazon's Choice" or other badges on any variant
- NO price tags, NO currency symbols
- NO promotional text like "NEW!", "Bestseller"
- NO props or decorative elements around the variants
- NO hands, NO people
- NO different angles between variants (consistency rule)
```

## Example (filled) — for the peach-verbena lemonade line

```
Amazon secondary image — product variants showcase for the 'lapochka' natural lemonade line, 330ml aluminum cans.

Layout:
- 1:1 square composition
- 3 variants arranged in a clean horizontal row
- Uniform spacing, all cans the same scale
- Small label below each can with its flavor name

Variants to display:
1. Peach & Verbena (peach-colored label with soft green accents)
2. Raspberry & Mint (soft pink label with green mint accents)
3. Lemon & Basil (pale yellow label with deep green basil accents)

Consistency rules:
- All 3 cans shown at the exact same 45-degree angle
- All 3 cans the same size in frame
- Same soft diffused lighting from upper left
- Same pure white background
- Only label colors and flavor artwork differ

Typography for labels:
- Variant 1 Label: "Peach & Verbena" (30pt, sans-serif, dark green, small caps)
- Variant 2 Label: "Raspberry & Mint" (30pt, sans-serif, dark green, small caps)
- Variant 3 Label: "Lemon & Basil" (30pt, sans-serif, dark green, small caps)
- All labels centered below each can

Background:
- Pure white seamless background
- Minimal soft shadow under each can

Quality:
- Hyperrealistic photography
- Color-accurate rendering of each flavor's label

Consistency with main image:
- Same can design, same typography layout, same proportions as the reference
- Only the label flavor and accent colors differ

Strict exclusions:
- NO badges on any can
- NO price tags
- NO promotional text
- NO fruit props or garnishes
- NO hands
```

## higgsfieldcli call

```bash
CREATED=$(export $(cat .env | grep -v '^#' | xargs) && bin/higgsfieldcli generate --json '[{
  "model":"nano_banana_2",
  "prompt":"[FILLED_PROMPT]",
  "aspect_ratio":"1:1",
  "resolution":"2k",
  "images":[{"id":"'$MAIN_JOB_ID'","type":"nano_banana_2_job"}]
}]')
VARIANTS_JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d[0]['job_ids'][0])")

export $(cat .env | grep -v '^#' | xargs) && bin/higgsfieldcli status --job-id "$VARIANTS_JOB_ID" --poll
```

## Key reminders

- Consistency between variants is the #1 quality signal — any difference in angle/lighting/size looks amateur
- Limit to 6 variants max in one image — more than 6 makes each one too small to see clearly
- Arrange in logical order (by color family, flavor intensity, size)
- Labels should be short — flavor/color name only, not descriptions
- If the product only has 1 variant, skip this image and substitute with a different secondary type (e.g., additional lifestyle or size reference)
