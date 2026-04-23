# Seedream V5 Lite

## Inputs

Text prompts + optional reference images. Excels at **face identity preservation** from reference photos, compositing from multiple references, product placement, text transfer between images. Prompt is always required, even with reference images (edit mode).

Reference images in the prompt as **"Image0"**, **"Image1"**, **"Image2"** — matching their order in the `medias` array. Up to 10 images.

## Prompt Structure

Instruction-based — tell the model what to do with the inputs:

1. **Action** — what to do with figures: "Replace the product in Image1 with that from Image2", "Place the person from Image1 into the scene from Image2".
2. **Subject** — for face preservation: which figure has the face, how the person should appear.
3. **Typography** — for text transfer: "Copy the text from Image3 to the top", specify contrast and placement.
4. **Style** — visual direction, lighting, atmosphere, palette.
5. **Constraints** — negative/conditional: "do not change the background", "keep original lighting", "without changing...".

## Key Rules

- Reference as **Image N** (1-indexed), matching `medias` array order.
- Multi-image composition: reference elements from different images freely.
- Prompt always required — even in edit mode with `medias`, you must describe what to do.
- Face preservation: instruct to use that person's likeness from a specific Image N.
- Negative and conditional instructions work well: "but not overly...", "without changing...".
- **Best model for face identity** — use when a non-famous person's face from a reference photo must be preserved in output.

## Output Format

One clean instruction prompt. No wrapping or JSON needed.

## CLI

**Binary:** `higgsfieldcli` (project root)
**Model:** `seedream_v5_lite`
### Generate

```bash
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json '[{"model":"seedream_v5_lite","prompt":"A futuristic city skyline at sunset","aspect_ratio":"16:9","quality":"high"}]'
```

### Generate with Reference Image

```bash
# 1. Upload reference image
UPLOAD=$(higgsfieldcli upload --file /path/to/face.png)
IMAGE_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Generate with reference (prompt describes the edit)
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json "[{\"model\":\"seedream_v5_lite\",\"prompt\":\"Place this person on a tropical beach at golden hour, preserve face identity\",\"medias\":[{\"role\":\"image\",\"data\":{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}}],\"aspect_ratio\":\"3:4\",\"quality\":\"high\"}"
```

### Parameters (JSON keys)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `model` | string | *required* | `"seedream_v5_lite"` |
| `prompt` | string | *required* | Text prompt (always required, even with medias) |
| `medias` | array | — | Reference images. Format: `[{"role":"image","data":{"id":"ID","type":"TYPE"}}]`. Type: `media_input` for uploads, `seedream_v5_job` for job results (note: not `seedream_v5_lite_job`) |
| `aspect_ratio` | string | `3:4` | `1:1`, `3:4`, `4:3`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9` |
| `quality` | string | `basic` | `basic` (2K) or `high` (3K) |
| `batch_size` | int | `4` | Number of images to generate |
| `seed` | int | random | Random seed (auto-generated 1–999999 if omitted) |

Width/height are auto-resolved from quality + aspect_ratio — no need to specify manually.

### Recommended Sizes

| Use Case | Aspect Ratio | Quality |
|----------|-------------|---------|
| Face portrait | `3:4` | `high` |
| Full body | `2:3` | `high` |
| Scene composite | `16:9` | `high` |
| Square headshot | `1:1` | `high` |
| Ultra-wide cinematic | `21:9` | `high` |
