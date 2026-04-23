# Size Reference Prompt Template

Secondary image type showing the physical size of the product using a universally recognized reference object. Reduces returns caused by "smaller/larger than I expected" complaints.

## Placeholders

- `[PRODUCT_DESCRIPTION]` — base product description
- `[REFERENCE_OBJECT]` — a universally known-size object to compare against. Options:
  - Credit card (85mm × 54mm) — great for small electronics, cosmetics, wallets
  - Smartphone (≈150mm tall) — great for gadgets, bottles, mid-size items
  - Coin (US quarter = 24mm, €1 = 23mm) — great for very small items, jewelry
  - Hand (palm ≈180mm) — great for handheld tools, grips
  - Standard water bottle (500ml = 220mm tall) — great for beverages, tall items
- `[DIMENSION_LABELS]` — optional specific measurements to display. Examples: "Height: 158mm, Width: 66mm, Diameter: 52mm"

## Template

```
Amazon secondary image — size reference for [PRODUCT_DESCRIPTION].

Layout:
- 1:1 square composition
- Product placed next to [REFERENCE_OBJECT] at the SAME scale
- Both objects at the same viewing angle
- Both objects positioned so their relative size is immediately clear
- Optional: clean dimension lines with measurements ([DIMENSION_LABELS])

Reference object presentation:
- [REFERENCE_OBJECT] is universally recognizable, standard size
- Positioned clearly but visually subordinate to the product
- The product remains the primary subject
- Reference object is intact, upright, and clearly identifiable

Dimension indicators (optional — write EACH label in this exact format):
- Height Label: "Height: [VALUE] mm" (30pt, sans-serif)
- Width Label: "Width: [VALUE] mm" (30pt, sans-serif)
- Diameter Label: "Diameter: [VALUE] mm" (30pt, sans-serif)
- (use the units the user requests — mm, cm, or inches)
- **CRITICAL TEXT FORMAT RULE:** Every text element written as `Label: "exact text" (Xpt)`.
- Clean thin dimension lines in a subtle color
- Labels positioned clearly along the dimension lines

Background:
- Clean light gray or soft off-white
- Minimal, non-distracting
- Subtle natural shadow under both objects

Lighting:
- Soft, even, diffused lighting
- Same lighting on both the product and the reference object

Quality:
- Hyperrealistic product photography
- Sharp focus on both objects and any dimension lines
- Accurate scale representation — no visual tricks

Consistency with main image:
- Product matches the reference exactly — same design, colors, proportions

Strict exclusions:
- NO exaggerated scaling that misrepresents true size
- NO branded reference objects (use a generic smartphone, not a specific brand)
- NO promotional text or badges
- NO price tags
- NO multiple reference objects — ONE clean size anchor
- NO hands that aren't needed for scale (unless hand IS the reference)
```

## Example (filled) — for the peach-verbena lemonade can

```
Amazon secondary image — size reference for the 'lapochka' 330ml aluminum can of peach-verbena natural lemonade.

Layout:
- 1:1 square composition
- The can placed next to a standard smartphone at the same scale
- Both objects upright, side by side
- Dimension lines to the left of the can showing height

Reference object presentation:
- Generic modern smartphone, approximately 150mm tall
- Screen off / neutral dark screen
- Brand markings avoided or blurred
- Positioned clearly but visually subordinate to the can

Dimension indicators:
- Height Label: "Height: 115mm" (30pt, sans-serif) — positioned at midpoint of vertical line to left of can
- Diameter Label: "Diameter: 66mm" (30pt, sans-serif) — positioned below the can
- Thin vertical and horizontal dimension lines in dark gray

Background:
- Soft light gray, clean and minimal
- Subtle shadow under both objects

Lighting:
- Soft diffused studio lighting from upper left
- Same lighting on the can and the phone

Quality:
- Hyperrealistic product photography
- Sharp focus on both objects

Consistency with main image:
- Can design, label, colors match the reference exactly

Strict exclusions:
- NO branded phone (no Apple logo, no specific brand markers)
- NO promotional text
- NO other objects in the frame
- NO exaggerated scale
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
SIZEREF_JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d[0]['job_ids'][0])")

export $(cat .env | grep -v '^#' | xargs) && bin/higgsfieldcli status --job-id "$SIZEREF_JOB_ID" --poll
```

## Key reminders

- Pick a reference object that CUSTOMERS KNOW the size of (credit card, coin, phone, hand) — obscure objects don't help
- Keep scale ACCURATE — exaggerating size loses customer trust and causes returns
- Choose the reference based on product size:
  - Tiny items (earrings, USB drives) → coin
  - Small items (cosmetics, pocket tools) → credit card
  - Medium items (bottles, gadgets) → smartphone or hand
  - Large items (kitchen appliances) → person silhouette or common furniture
- Generic, unbranded reference objects only — Amazon doesn't want third-party branding in your images
