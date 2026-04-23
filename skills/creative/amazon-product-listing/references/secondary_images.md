# Secondary Images

Secondary images appear on the product detail page after the main image. Unlike the main image, Amazon's rules here are lenient — this is where selling happens. Use the creative freedom to communicate benefits, build trust, and drive conversion.

Amazon allows up to 8 secondary slots. The product page typically displays 6 + video. This skill generates 6 as the default.

## Default 6-image carousel recipe (use this when user doesn't specify)

| # | Type | Purpose | Conversion impact |
|---|------|---------|------------------|
| 1 | Infographic — key benefits | 4–6 selling points with icons and annotation lines | +8% |
| 2 | Size reference / dimensions | Show physical size with a common-object reference | Reduces returns |
| 3 | Lifestyle (in use) | Product being used by target customer in a realistic scene | +18% |
| 4 | Lifestyle (in context) | Product placed in its intended environment | +18% |
| 5 | Detail / material close-up | Macro shot of texture, craftsmanship, quality | +6% |
| 6 | What's in the box / variants | Full package contents OR color/flavor variants | Reduces returns |

**Overall impact:** 7 images vs 4 images = +32% conversion rate. Optimized image sets can lift interaction rate by up to +30%.

## The 7 secondary image types

### 1. Infographic (benefits callout)

**Purpose:** Highlight 4–6 core selling points with visual annotations.

**Key principles:**
- Maximum 4–6 selling points — more creates clutter
- Annotation lines or arrows pointing directly to product features
- Icons alongside text to reinforce each point visually
- Clear visual hierarchy — most important benefit gets more space
- Phrase-based copy ("100% Organic", "BPA-Free"), NOT full sentences
- Text ≥30pt minimum for mobile readability
- Text color must contrast strongly with background

**Template:** `assets/prompt_templates/infographic.md`

### 2. Multi-angle shots

**Purpose:** Show the product from different perspectives so customers understand its 3D form.

**Key principles:**
- Typically 1 image showing 2–4 angles (front, back, side, top)
- Consistent lighting across all angles
- Clean neutral background (light gray, gradient, or white)
- All views should feel like the same photo session
- Product occupies dominant space in each angle

**Template:** `assets/prompt_templates/multi_angle.md`

### 3. Detail shot (macro / close-up)

**Purpose:** Show material quality, craftsmanship, texture, or a key unique feature up close.

**Key principles:**
- Extreme close-up / macro photography aesthetic
- Shallow depth of field emphasizes the featured detail
- Focus on what makes the product quality-worthy: stitching, material weave, surface finish, engraved details, food texture
- No text required — the image itself tells the story
- If text is added, limit to 1 short phrase (e.g., "Premium Leather")

**Template:** `assets/prompt_templates/detail_shot.md`

### 4. Lifestyle image

**Purpose:** Show the product being used by the target customer in a realistic scene. This is the highest-converting secondary type (+18%).

**Key principles:**
- Realistic scene matching the target demographic and use case
- Product must remain the focal point — not swallowed by the scene
- Background should support the story but not distract
- Natural lighting is almost always best (soft daylight from a window, morning/afternoon, not golden hour)
- Show emotion — happy, focused, satisfied user
- For products used at home: bathroom (skincare), kitchen (food/beverages), bedroom (apparel/accessories), home gym (fitness)
- For outdoor products: matching natural environment

**Template:** `assets/prompt_templates/lifestyle.md`

### 5. Variants

**Purpose:** Display available colors, flavors, sizes, or styles in one image.

**Key principles:**
- All variants arranged uniformly — same angle, same lighting, same spacing
- Only the variant attribute changes (color/flavor/size), everything else is identical
- Neutral background (pure white or very soft gradient)
- Label each variant with its name in small text below or beside it
- Arrange in logical order (by color family, by flavor intensity, by size)

**Template:** `assets/prompt_templates/variants.md`

### 6. What's in the box

**Purpose:** Show everything the customer receives in the package. Dramatically reduces returns caused by "missing items" confusion.

**Key principles:**
- All components clearly visible and spread out (not stacked)
- Flat lay composition (top-down view) usually works best
- Neutral background (white, off-white, or wood texture)
- Optional: small label next to each item naming it
- Include quantity indicators if there are multiples ("x2")

**Template:** `assets/prompt_templates/whats_in_box.md`

### 7. Size reference

**Purpose:** Give customers a real-world sense of physical size.

**Key principles:**
- Use a universally recognized reference object:
  - Credit card (84mm × 54mm)
  - Coin (varies — specify dime, quarter)
  - Smartphone (iPhone-sized)
  - Hand (palm or fingers holding the product)
  - Standard water bottle
- Clear visible scale/measurement lines can be added with dimension labels
- Keep the product as primary subject, reference object as clearly secondary
- Neutral background

**Template:** `assets/prompt_templates/size_reference.md`

## General secondary image principles

### Composition
- **One core message per image** — if you need to say two things, make two images
- Clean composition, no clutter
- High contrast between subject and background
- Product always primary, everything else supports it

### Typography (for infographics and any image with text)
- Minimum 30pt font size (Amazon compresses images — smaller text becomes unreadable)
- Maximum 2–3 font families across the whole set
- Use font weights (bold, regular, light) to create hierarchy
- Sans-serif fonts work best for mobile readability

### Mobile-first design
- Over 70% of Amazon traffic is mobile
- Critical information must NOT be in the outer 5% of the frame (mobile crops edges)
- Text that looks fine on desktop may be unreadable on phone — always check at small size
- High contrast matters more on mobile (varied lighting conditions)

### Consistency across the set
- Same color palette across all 6 secondary images
- Same font family and weights
- Same icon style (if icons are used)
- Product appearance identical (guaranteed by using main image as reference)
- Similar lighting temperature (cool vs warm) across all images

## Absolutely prohibited on secondary images

- Fake badges ("Amazon's Choice", "Bestseller", "Prime", "Sale", etc.)
- Review screenshots or star ratings pulled from other listings
- Competitor product photos or copied imagery
- Seller contact info (email, phone, website, social handles)
- Price tags or currency symbols (pricing happens in the listing, not the image)
- Disparaging language about competitors
- Unverifiable claims ("#1 best", "FDA approved" without documentation)
- Nudity, violence, or inappropriate content

## Conversion data reference

| Image type | Lift vs. no image of this type |
|------------|-------------------------------|
| Lifestyle images | +18% conversion |
| Infographics | +8% conversion |
| Detail close-ups | +6% conversion |
| 7 images total vs 4 images total | +32% conversion |
| Fully optimized image set | Up to +30% interaction rate |

Use this data to justify image selection when the user asks "do I really need all 6?"
