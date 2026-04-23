# Nano Banana Pro

## Inputs

Text prompts with optional reference images. General-purpose model.

Reference images in the prompt as **"image_0.png"**, **"image_1.png"**, **"image_2.png"** — matching their order in `image_url`.

## Prompt Structure

Flexible, instruction-following. Combine description with directives:

1. **Subject and scene** — what to generate.
2. **Style** — medium, lighting, color, visual direction.
3. **Instructions** — direct commands: "make the background darker", "remove the text", "change jacket to red".
4. **Constraints** — negative instructions: "no text", "no watermark", "avoid oversaturation", "no people in background".

## Key Rules

- **Resolution: default is 2k.** Use 1k for speed, 2k for quality (default), 4k for ultra-high-res.
- Negative instructions are well-understood and respected.

## Output Format

One clean prompt. No wrapping or JSON needed.

## CLI

**Binary:** `higgsfieldcli` (project root)
**Model:** `nano_banana_2`
### Generate

```bash
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json '[{"model":"nano_banana_2","prompt":"Your prompt here","aspect_ratio":"3:4"}]'
```

### Generate with Reference Image

```bash
# 1. Upload reference image
UPLOAD=$(higgsfieldcli upload --file /path/to/image.png)
IMAGE_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Generate with reference (images array for nano_banana_2)
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json "[{\"model\":\"nano_banana_2\",\"prompt\":\"Transform to watercolor style, keep the composition. No text.\",\"images\":[{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}],\"aspect_ratio\":\"3:4\"}"
```

### Parameters (JSON keys)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `model` | string | *required* | `"nano_banana_2"` |
| `prompt` | string | *required* | Text prompt |
| `images` | array | — | Reference images. Format: `[{"id":"ID","type":"TYPE"}]`. Type: `media_input` for uploads, `nano_banana_2_job` for job results |
| `width` | int | `896` | Image width in pixels |
| `height` | int | `1200` | Image height in pixels |
| `aspect_ratio` | string | `3:4` | `auto`, `1:1`, `3:4`, `4:3`, `2:3`, `3:2`, `9:16`, `16:9`, `5:4`, `4:5`, `21:9` |
| `resolution` | string | `2k` | `1k` (standard), `2k` (high quality, default), `4k` (ultra high quality) |
| `batch_size` | int | `1` | Number of images to generate |

### Recommended Sizes

| Use Case | Aspect Ratio | Width | Height |
|----------|-------------|-------|--------|
| Portrait | `3:4` | 896 | 1200 |
| Landscape (standard) | `4:3` | 1200 | 896 |
| Tall portrait | `2:3` | 800 | 1200 |
| Landscape (wide) | `3:2` | 1200 | 800 |
| Square | `1:1` | 1024 | 1024 |
| Vertical (mobile) | `9:16` | 720 | 1280 |
| Widescreen | `16:9` | 1200 | 675 |
| Instagram | `4:5` | 960 | 1200 |
| Instagram landscape | `5:4` | 1200 | 960 |
| Ultra-wide | `21:9` | 1200 | 514 |
