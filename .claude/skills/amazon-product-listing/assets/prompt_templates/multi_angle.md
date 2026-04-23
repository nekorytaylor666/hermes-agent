# Multi-Angle Shots Prompt Template

Secondary image type showing the product from 2–4 different angles in a single frame, so customers understand its full 3D form without clicking through multiple photos.

## Placeholders

- `[PRODUCT_DESCRIPTION]` — brief product description
- `[ANGLES]` — specify angles to show. Typical sets:
  - Beverages: "front label, back label, top of can"
  - Electronics: "front, back, left side, top"
  - Apparel: "front, back, side profile"
  - Footwear: "side profile, top down, sole, heel"
  - Skincare: "front, back with ingredient list, top with cap closed, bottom"

## Template

```
Amazon secondary image — multi-angle product showcase for [PRODUCT_DESCRIPTION].

Layout:
- 1:1 square composition
- 3 to 4 views of the same product arranged in a clean grid or row
- Views to include: [ANGLES]
- Each angle is clearly distinct and shows a different side of the product
- Uniform spacing between each view
Typography for optional angle labels (only if helpful):
- **CRITICAL TEXT FORMAT RULE:** If any labels are used, write in format: `Label: "exact text" (Xpt)`.
- Example: Angle Label 1: "Front" (24pt, sans-serif)
- Small, minimal labels under each view — one word each
- Usually no labels needed — angles should be visually obvious

Lighting and color:
- Identical lighting across ALL angles — same temperature, same direction, same intensity
- Same soft diffused studio lighting
- Consistent color rendering across all views
- All products look like they're from the same photo session

Background:
- Clean light gray, subtle gradient, or soft off-white
- NOT pure white (reserved for main image)
- Minimal, non-distracting
- Subtle natural shadow under each view

Quality:
- Hyperrealistic photography for each angle
- Sharp focus on every view
- Product fills most of each grid cell but leaves breathing room

Consistency with main image:
- Same product design, label, colors, and materials as the reference
- Product must look identical — only the viewing angle changes

Strict exclusions:
- NO text overlays describing what each angle is (small single-word labels are OK if helpful)
- NO arrows, NO decorative graphics
- NO watermarks, NO badges
- NO props, NO accessories
- NO people, NO hands
- Different angles should NOT look like different products
```

## Example (filled) — for the peach-verbena lemonade

```
Amazon secondary image — multi-angle product showcase for aluminum can of natural lemonade with peach and verbena flavor, brand 'lapochka'.

Layout:
- 1:1 square composition
- 3 views of the same can arranged in a horizontal row
- Views to include: front label view, back label view with nutrition facts, top-down view showing the can opening
- Uniform spacing between views
- No labels needed — angles are visually obvious

Lighting and color:
- Identical soft diffused studio lighting across all 3 views
- Consistent color rendering
- Same lighting direction (slightly from above, slightly from left)

Background:
- Clean light gray background, subtle gradient
- Minimal shadow under each can

Quality:
- Hyperrealistic photography
- Sharp focus on every view
- Each can fills most of its section

Consistency with main image:
- Same can design, label typography, colors, and proportions as the reference
- Product identical across all 3 angles

Strict exclusions:
- NO text overlays
- NO arrows or decorative graphics
- NO watermarks, NO badges
- NO props like fruit or garnishes
- NO people, NO hands
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
MULTIANGLE_JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d[0]['job_ids'][0])")

export $(cat .env | grep -v '^#' | xargs) && bin/higgsfieldcli status --job-id "$MULTIANGLE_JOB_ID" --poll
```

## Key reminders

- Choose angles that reveal genuinely different information (e.g., back label with ingredients, not just another front view)
- Lighting consistency is the #1 sign of professional quality
- Keep labels minimal or absent — the image should read at a glance
