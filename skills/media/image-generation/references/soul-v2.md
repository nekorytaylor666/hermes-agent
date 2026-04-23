# Soul 2.0

## Inputs

**Text-to-image:** prompt only. Optimized for high-quality, visually rich aesthetic images — portraits, landscapes, abstract art, product shots, editorial, fashion, stylized illustrations.
**Image-to-image:** reference image via `medias` array. Prompt is **ignored** when medias is provided — the model transforms the reference image directly.

## Prompt Structure

Write as a **single dense paragraph** in this order:

1. **Opening** — subject + shot type: "A high-angle close-up of...", "A wide aerial shot capturing...".
2. **Details and textures** — objects, clothing, materials: "glossy", "weathered", "rough-hewn", "knitted". Transcribe desired text verbatim.
3. **Setting** — background, flooring, walls, object arrangement, negative space.
4. **Lighting** — sources (natural, flash, ambient, neon) and quality: "specular highlights", "diffuse shadows", "volumetric rays".
5. **Color palette** — dominant and accent colors: "muted olive and slate gray", "warm amber tones".
6. **Composition and camera** — angle, framing, depth of field, lens characteristics (wide-angle distortion, bokeh).
7. **Medium** — capture medium: "35mm film", "digital editorial", "flash photography". Mention grain/noise if relevant.
8. **Mood** — emotional tone: "nostalgic and melancholic", "cozy and intimate".

## Key Rules

- **Objective, technical tone.** Photographic terminology: "subsurface scattering", "leading lines", "dynamic range". Material reality, not abstract concepts.
- No poetry — dense, grounded visual description.
- Broader style range than Soul Cinematic — editorial, fashion, nature, product, abstract.
- Model enforces minimum age 20 for human subjects. Age up minors to "young woman/man, 20 years old".
- Model adds opaque clothing internally. "Transparent", "sheer", "see-through" get replaced with opaque alternatives.
- Describe clothing to match scene aesthetic.
- **No text/lettering** — this model doesn't render readable text well.
- **Use Soul 2.0 for all aesthetic images that don't need cinematic framing.** For cinematic frames, film-like shots, and people with original cinematic appearance — use Soul Cinematic instead.

## Output Format

One clean prompt paragraph. No analysis, JSON, or labels unless the user asks.

## CLI

**Binary:** `higgsfieldcli` (project root)
**Model:** `text2image_soul_v2`
### Generate

```bash
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json '[{"model":"text2image_soul_v2","prompt":"A high-angle close-up of a weathered ceramic mug on a rough oak table, steam curling upward, diffuse morning light from a frosted window, muted earth tones with warm amber highlights, shallow depth of field, 35mm film grain, cozy and intimate","aspect_ratio":"3:4","quality":"1080p"}]'
```

### Generate with Reference Image (Image-to-Image)

Prompt is **ignored** when `medias` is provided — the model transforms the reference directly.

```bash
# 1. Upload reference image
UPLOAD=$(higgsfieldcli upload --file /path/to/image.png)
IMAGE_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Generate image-to-image (prompt ignored, model transforms the reference)
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json "[{\"model\":\"text2image_soul_v2\",\"medias\":[{\"role\":\"image\",\"data\":{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}}],\"aspect_ratio\":\"3:4\",\"quality\":\"1080p\"}"
```

### Parameters (JSON keys)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `model` | string | *required* | `"text2image_soul_v2"` |
| `prompt` | string | — | Text prompt (required for text-to-image, ignored with medias) |
| `medias` | array | — | Reference images. Format: `[{"role":"image","data":{"id":"ID","type":"TYPE"}}]`. Type: `media_input` for uploads, `text2image_soul_v2_job` for job results |
| `width` | int | `1536` | Image width |
| `height` | int | `2048` | Image height |
| `aspect_ratio` | string | `3:4` | `9:16`, `3:4`, `2:3`, `1:1`, `4:3`, `16:9`, `3:2` |
| `quality` | string | `1080p` | `1080p` or `basic` |
| `batch_size` | int | `1` | Number of images to generate |
| `seed` | int | random | Random seed (auto-generated 1–999999 if omitted) |
| `style_id` | string | `3db34ab5-...` | Style ID (default: General) |
| `enhance_prompt` | bool | `true` | Enable prompt enhancement |
| `negative_prompt` | string | — | Negative prompt |

### Recommended Sizes

| Use Case | Aspect Ratio | Quality |
|----------|-------------|---------|
| Aesthetic portrait | `3:4` | `1080p` |
| Tall portrait | `2:3` | `1080p` |
| Landscape / nature | `16:9` | `1080p` |
| Standard landscape | `4:3` | `1080p` |
| Wide landscape | `3:2` | `1080p` |
| Product shot | `1:1` | `1080p` |
| Editorial / fashion | `9:16` | `1080p` |
