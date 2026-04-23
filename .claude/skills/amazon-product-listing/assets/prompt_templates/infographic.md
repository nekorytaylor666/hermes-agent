# Infographic Prompt Template

Secondary image type that highlights 4–6 key selling points with annotations, icons, and short phrases. Highest-density image in the set — use it to communicate benefits that would take too long to notice visually.

## Placeholders

- `[PRODUCT_DESCRIPTION]` — brief product description
- `[SELLING_POINT_1]` through `[SELLING_POINT_N]` — 4 to 6 short phrases (2–4 words each). Examples: "100% Organic", "BPA-Free", "12-Hour Battery", "Hypoallergenic", "Dishwasher Safe"
- `[COLOR_PALETTE]` — brand color scheme, e.g. "white and soft green accents", "black and gold", "pastel pink and cream"

## Template

```
Amazon secondary image — benefits infographic for [PRODUCT_DESCRIPTION].

Layout:
- 1:1 square composition
- Product displayed prominently in the center or on one side
- 4 to 6 selling point callouts arranged around the product
- Each callout: simple icon + short text phrase
- Thin clean annotation lines connecting each callout to the relevant product feature (where visually appropriate)
- Clear visual hierarchy — most important selling point gets larger or most prominent placement

Selling points to display (write EACH one in this exact format):
1. Callout 1: "[SELLING_POINT_1]" (32pt)
2. Callout 2: "[SELLING_POINT_2]" (32pt)
3. Callout 3: "[SELLING_POINT_3]" (32pt)
4. Callout 4: "[SELLING_POINT_4]" (32pt)
(add Callout 5 and 6 if applicable)

Typography:
- **CRITICAL TEXT FORMAT RULE:** Every text element in the image must be specified in this exact format: `Label: "exact text content" (Xpt)`. Always include the actual quoted text and the point size in parentheses.
- Sans-serif font, clean and modern
- Maximum 2 font weights (bold for callout names, regular for any supporting text)
- High contrast between text and background — dark text on light background preferred
- Text is CRISP and PERFECTLY LEGIBLE, no blurring, no warping
- Minimum size for any readable text is 30pt

Icons:
- Simple line icons or solid icons, consistent style across all callouts
- Icons support the text, do not replace it
- Matching stroke weight and visual weight across all 4-6 icons

Background and colors:
- Clean, minimalist background — soft off-white, subtle gradient, or brand-aligned
- Color palette: [COLOR_PALETTE]
- NOT pure white (reserved for main image)
- High contrast between product and background

Product:
- Photorealistic, matches the reference main image exactly
- Product is the visual anchor of the composition
- Product lighting matches the callout area lighting

Mobile safety:
- Keep all text and icons within the inner 90% of the frame
- Nothing critical in the outer 5% (mobile cropping)

Strict exclusions:
- NO "Amazon's Choice", "Prime", "Bestseller", "Sale", "New", "Free Shipping" badges
- NO review screenshots, NO star ratings from other listings
- NO competitor brand names or logos
- NO seller contact information (email, phone, URL, social handles)
- NO price tags or currency symbols
- NO unverifiable claims like "#1 best" without proof
- NO cartoon or comic style — clean modern commercial design
```

## Example (filled) — for the peach-verbena lemonade

```
Amazon secondary image — benefits infographic for aluminum can of natural lemonade with peach and verbena flavor, brand 'lapochka'.

Layout:
- 1:1 square composition
- Product can displayed prominently in the center
- 4 selling point callouts arranged around the can
- Each callout: simple icon + short text phrase
- Thin clean annotation lines connecting callouts to the can

Selling points to display:
Callout 1: "Zero Sugar" (32pt)
Callout 2: "100% Natural" (32pt)
Callout 3: "Real Fruit Juice" (32pt)
Callout 4: "No Preservatives" (32pt)

Typography:
- Sans-serif font, clean and modern
- Callouts written as: Label: "exact text" (Xpt)
- Bold for selling point names (32pt), regular for any supporting text
- Dark green text on soft cream background
- Text is crisp and perfectly legible

Icons:
- Simple line icons with consistent stroke weight
- Zero Sugar → crossed-out sugar cube icon
- 100% Natural → leaf icon
- Real Fruit Juice → peach icon
- No Preservatives → shield or checkmark icon

Background and colors:
- Soft cream background with a subtle gradient
- Color palette: cream, soft green, peach accents
- NOT pure white
- High contrast between the can and the background

Product:
- Photorealistic can, matches the main image exactly
- Sharp focus on the label

Mobile safety:
- All text and icons within the inner 90% of the frame

Strict exclusions:
- NO "Amazon's Choice", "Prime", "Bestseller", "Sale" badges
- NO review screenshots
- NO competitor brand names
- NO seller contact information
- NO price tags
- NO cartoon style
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
INFOGRAPHIC_JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d[0]['job_ids'][0])")

export $(cat .env | grep -v '^#' | xargs) && bin/higgsfieldcli status --job-id "$INFOGRAPHIC_JOB_ID" --poll
```

## Key reminders

- Max 6 selling points — more creates clutter
- Short phrases (2–4 words) — full sentences become unreadable at mobile size
- Selling points must be factual and verifiable
- Icons and typography should match across the whole 6-image set (consistency)
- Product reference from main image is MANDATORY in `"images"` array
