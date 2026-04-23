# Soul 2.0 — Avatar & Influencer Generation

## Role

Generate realistic influencer avatars and character portraits via Soul 2.0. Used when the user asks to create an avatar, influencer, character, person, or profile picture.

## Mandatory Prompt Elements

Every prompt MUST contain all three of these phrases — no exceptions:

| # | Phrase | Purpose |
|---|--------|---------|
| 1 | `with high model facial features` | Ensures attractive, editorial-grade face structure |
| 2 | `natural skin texture` | Prevents plastic/AI look, adds pores and micro-detail |
| 3 | **Clothing description** | Must always be present. If the user doesn't specify — choose contextually appropriate outfit |

## Prompt Structure

Build the prompt in this order:

```
[gender/age/identity], [user's appearance details], with high model facial features, natural skin texture,
[clothing — always explicit], [pose/expression], [lighting], [background/setting], [aspect ratio]
```

### Breakdown

1. **Identity** — gender, age range, ethnic appearance (from user request)
2. **Appearance** — hair color/style, eye color, build, distinguishing features (from user request)
3. **Face anchor** — `with high model facial features` (always)
4. **Skin anchor** — `natural skin texture` (always)
5. **Clothing** — specific garments, fabrics, colors. NEVER omit. If user doesn't specify, choose based on context:
   - Lifestyle influencer → casual chic (linen shirt, knit sweater, denim jacket)
   - Fitness → athletic wear (compression top, running jacket)
   - Business → smart casual or formal (blazer, tailored shirt)
   - Fashion → editorial outfit (structured coat, designer-feel pieces)
6. **Pose/expression** — natural, candid-feeling. Default: confident relaxed expression, slight smile
7. **Lighting** — soft natural or studio. Default: golden hour soft light
8. **Background** — contextual or minimal. Default: soft blurred neutral
9. **Aspect ratio** — default `3:4` for portraits

## No Products in Character Prompts

**CRITICAL:** When generating a character:
- Prompt describes ONLY the person: appearance, face, expression, clothing, pose, style
- **NEVER** include products, objects, props, items, or anything the person holds or interacts with
- Location/background is OK — but NO objects in hands

**Bad:** `"a young woman holding a skincare bottle, smiling"` — model bakes the bottle into the image
**Good:** `"a young woman, mid-20s, natural beauty, friendly smile, casual style, soft studio background"` — clean person, product added later via compositing

## Content Safety

**ALWAYS reject and rewrite** any user request that includes:
- Nudity, revealing/sexualized clothing, underwear-only, swimwear-as-main-outfit
- Violent, gory, or disturbing appearance details
- Hate symbols, offensive imagery

**How to handle:** ignore the unsafe part, substitute with appropriate clothing/description, generate normally. Do not lecture the user — just silently produce a safe version.

## Clothing Defaults

When the user says nothing about clothing, pick from this table:

| Context | Default Outfit |
|---------|---------------|
| No context given | White fitted t-shirt, dark well-fitted jeans |
| Lifestyle / casual | Oversized linen button-up shirt, light wash jeans |
| Professional / business | Navy tailored blazer over white crew-neck tee |
| Fitness / sport | Black compression long-sleeve top, athletic leggings |
| Fashion / editorial | Structured camel overcoat, black turtleneck underneath |
| Street / urban | Graphic hoodie under bomber jacket, cargo pants |
| Elegant / evening | Silk blouse, high-waisted tailored trousers |

## Prompt Examples

**User says:** "create a blonde influencer girl"
```
A young woman in her mid-20s, long wavy blonde hair, light green eyes, with high model facial features,
natural skin texture, wearing an oversized cream linen button-up shirt and light wash straight-leg jeans,
relaxed confident expression with a slight smile, soft golden hour lighting from the left,
blurred warm-toned cafe interior background, 3:4
```

**User says:** "make an avatar — guy, Asian, short hair, athletic"
```
A young athletic man in his late 20s, East Asian appearance, short textured black hair, sharp jawline,
with high model facial features, natural skin texture, wearing a fitted black compression long-sleeve top
and dark joggers, standing with arms relaxed at sides, confident calm expression,
clean bright studio lighting with soft shadows, minimal light gray background, 3:4
```

**User says:** "dark-haired woman, 30s, business look"
```
A woman in her early 30s, dark brown shoulder-length straight hair, warm brown eyes,
with high model facial features, natural skin texture, wearing a tailored navy blazer
over a white crew-neck t-shirt and charcoal slim trousers, poised confident expression,
soft diffused natural window light, modern minimalist office background with blurred bookshelves, 3:4
```

**User says:** "redhead guy with beard, outdoorsy vibe"
```
A man in his early 30s, medium-length wavy auburn red hair, full well-groomed beard, blue-gray eyes,
with high model facial features, natural skin texture, wearing a dark green flannel shirt layered over
a heather gray henley and rugged brown canvas jacket, relaxed genuine smile,
warm overcast natural light, blurred Pacific Northwest forest trail background, 3:4
```

**User says something unsafe:** "girl in bikini only"
→ Silently substitute: generate with appropriate casual clothing instead.
```
A young woman in her mid-20s, with high model facial features, natural skin texture,
wearing a white fitted crew-neck t-shirt and high-waisted light denim shorts,
relaxed natural pose, soft warm sunlight, blurred sandy beach boardwalk background, 3:4
```

## CLI

**Model:** `text2image_soul_v2`

```bash
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json '[{"model":"text2image_soul_v2","prompt":"...","aspect_ratio":"3:4","quality":"1080p"}]'
```

### With Reference Image (image-to-image)
```bash
UPLOAD=$(higgsfieldcli upload --file /path/to/ref.png)
MEDIA_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json "[{\"model\":\"text2image_soul_v2\",\"prompt\":\"...\",\"medias\":[{\"role\":\"image\",\"data\":{\"id\":\"$MEDIA_ID\",\"type\":\"media_input\"}}],\"aspect_ratio\":\"3:4\",\"quality\":\"1080p\"}"
```

### Parameters (JSON keys)

| Key | Default | Notes |
|-----|---------|-------|
| `model` | *required* | `"text2image_soul_v2"` |
| `prompt` | *required* | Full prompt with all mandatory elements |
| `medias` | — | Reference images. Format: `[{"role":"image","data":{"id":"ID","type":"TYPE"}}]`. Type: `media_input` for uploads, `text2image_soul_v2_job` for job results |
| `aspect_ratio` | `3:4` | `3:4` for portraits (default), `1:1` for profile pics |
| `quality` | `1080p` | `1080p` standard |
| `batch_size` | `1` | Increase for variations |
| `negative_prompt` | — | Use to reinforce safety: `"nude, naked, swimwear, lingerie, violent, gore"` |
| `seed` | `0` | Set for reproducibility |

## After Generation

Always save the result as an element for reuse. First poll for the result if not already done, then create the element using `${JOB_SET_TYPE}_job` as the type:

```bash
# Poll if not already done:
# higgsfieldcli status --job-id "$JOB_ID" --poll

higgsfieldcli element create \
  --category character --name "Influencer Name" \
  --media "id=$JOB_ID;type=${JOB_SET_TYPE}_job"
```
