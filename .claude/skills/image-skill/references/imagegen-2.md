# GPT Image 2.0

## Inputs

Text prompts with optional reference images (up to 16). Four sub-models give distinct analog/retro aesthetics — select via `sub_model`.

## Sub-models (texture / look)

Set the aesthetic via the `sub_model` field:

| `sub_model`            | Look                                |
| ---------------------- | ----------------------------------- |
| `videotape-alpha`      | **Default.** VHS / videotape look   |
| `cassettetape-alpha`   | Cassette / tape-style aesthetic     |
| `electricaltape-alpha` | Electrical-tape / raw analog look   |
| `tidepool-alpha`       | Soft, washed-out pool aesthetic     |

## Key Rules

- **Default resolution: `1k`.** Raise to `2k` or `4k` only when higher detail is needed.
- **Default quality: `low`.** Pass `"quality":"high"` for best fidelity; costs more.
- `aspect_ratio: "auto"` requires at least one media in `medias`; with no medias it falls back to `1:1`.
- Up to 16 reference images allowed in `medias`.
- `batch_size` accepts `1`–`4` images per call.

## CLI

**Binary:** `higgsfieldcli` (project root)
**Model:** `imagegen_2_0`
**job_set_type (for referencing results):** `imagegen_2_0_job`

### Generate (text-to-image)

```bash
# Fire-and-forget — returns created line immediately
higgsfieldcli generate --json '[{"model":"imagegen_2_0","prompt":"a cat in space","aspect_ratio":"1:1","quality":"high","sub_model":"videotape-alpha"}]'
```

### Generate with reference image(s)

```bash
# 1. Upload reference
UPLOAD=$(higgsfieldcli upload --file /path/to/image.png)
IMAGE_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Generate with reference — imagegen_2_0 uses "medias" (role + data form)
higgsfieldcli generate --json "[{\"model\":\"imagegen_2_0\",\"prompt\":\"...\",\"medias\":[{\"role\":\"image\",\"data\":{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}}],\"aspect_ratio\":\"auto\",\"sub_model\":\"videotape-alpha\"}]"
```

### Parameters (JSON keys)

| Key            | Type    | Default           | Description                                                                                                                                       |
| -------------- | ------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`        | string  | *required*        | `"imagegen_2_0"`                                                                                                                                  |
| `prompt`       | string  | *required*        | Text prompt                                                                                                                                       |
| `sub_model`    | string  | `videotape-alpha` | One of `videotape-alpha`, `cassettetape-alpha`, `electricaltape-alpha`, `tidepool-alpha`                                                           |
| `quality`      | string  | `low`             | `low` (default), `medium`, `high`                                                                                                                  |
| `resolution`   | string  | `1k`              | `1k`, `2k`, `4k`                                                                                                                                  |
| `aspect_ratio` | string  | `1:1`             | `1:1`, `3:2`, `2:3`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9`, `27:16`, `16:27`, `9:8`, `8:9`, `auto` (auto requires medias, else falls back to 1:1) |
| `width`        | int     | —                 | Image width in pixels (resolved from `aspect_ratio` + `resolution` when omitted)                                                                  |
| `height`       | int     | —                 | Image height in pixels                                                                                                                            |
| `medias`       | array   | `[]`              | Up to 16 reference images. Each: `{"role":"image","data":{"id":"ID","type":"media_input"}}`                                                       |
| `batch_size`   | int     | `1`               | `1`–`4` images per call                                                                                                                           |
| `folder_id`    | UUID    | —                 | Optional folder to save results into                                                                                                              |

### Referencing a previous GPT Image 2.0 result

Build the reference with `id=<job_id>` and `type=imagegen_2_0_job` (poll the upstream job to completion first):

```bash
higgsfieldcli generate --json "[{\"model\":\"imagegen_2_0\",\"prompt\":\"...\",\"medias\":[{\"role\":\"image\",\"data\":{\"id\":\"$JOB_ID\",\"type\":\"imagegen_2_0_job\"}}],\"sub_model\":\"tidepool-alpha\"}]"
```
