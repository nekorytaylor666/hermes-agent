# Soul Cinematic

## Inputs

**Text-to-image:** prompt only. Optimized for **cinematic frames** — film-like shots, dramatic lighting, movie-quality compositions. Best for generating **people with original cinematic appearance** — characters that look like they belong in a movie.
**Image-to-image:** reference image via `medias` array. Prompt is **ignored** when medias is provided. `time_denoise_from` and `use_sultan` are set automatically for image-to-image.

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
- **Lean into cinematic language** — "anamorphic lens flare", "shallow depth of field", "film grain", "color graded in teal and orange", "rack focus", "Kodak Vision3 500T", "ARRI Alexa look".
- Model enforces minimum age 20 for human subjects. Age up minors to "young woman/man, 20 years old".
- Model adds opaque clothing internally. "Transparent", "sheer", "see-through" get replaced with opaque alternatives.
- Describe clothing to match scene aesthetic.
- **No text/lettering** — this model doesn't render readable text well.
- **Use Soul Cinematic when the shot should feel like a frame from a film** — dramatic composition, cinematic lighting (anamorphic flares, volumetric haze), natural film grain. Default 16:9 widescreen. For all other aesthetic images without cinematic framing — use Soul 2.0 instead.

## Output Format

One clean prompt paragraph. No analysis, JSON, or labels unless the user asks.

## CLI

**Binary:** `higgsfieldcli` (project root)
**Model:** `soul_cinematic`
### Generate

```bash
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json '[{"model":"soul_cinematic","prompt":"A medium shot of a woman in her late 20s standing at the edge of a rain-soaked rooftop at night, city lights bokeh behind her, wet leather jacket reflecting neon, anamorphic lens flare streaking across the frame, teal and orange color grade, shallow depth of field isolating her from the urban sprawl, 35mm Kodak Vision3 500T film stock, tension and quiet resolve","aspect_ratio":"16:9","quality":"1080p"}]'
```

### Generate with Reference Image (Image-to-Image)

Prompt is **ignored** when `medias` is provided. `time_denoise_from` and `use_sultan` are set automatically.

```bash
# 1. Upload reference image
UPLOAD=$(higgsfieldcli upload --file /path/to/image.png)
IMAGE_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Generate image-to-image (prompt ignored, model transforms the reference)
# Returns created line immediately (fire-and-forget) — poll only if result needed downstream
higgsfieldcli generate --json "[{\"model\":\"soul_cinematic\",\"medias\":[{\"role\":\"image\",\"data\":{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}}],\"aspect_ratio\":\"16:9\",\"quality\":\"1080p\"}"
```

### Parameters (JSON keys)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `model` | string | *required* | `"soul_cinematic"` |
| `prompt` | string | — | Text prompt (required for text-to-image, ignored with medias) |
| `medias` | array | — | Reference images. Format: `[{"role":"image","data":{"id":"ID","type":"TYPE"}}]`. Type: `media_input` for uploads, `soul_cinematic_job` for job results |
| `width` | int | `2048` | Image width |
| `height` | int | `1152` | Image height |
| `aspect_ratio` | string | `16:9` | `9:16`, `3:4`, `2:3`, `1:1`, `4:3`, `16:9`, `3:2`, `21:9` |
| `quality` | string | `1080p` | `1080p` or `basic` |
| `batch_size` | int | `1` | Number of images to generate |
| `seed` | int | random | Random seed (auto-generated 1–999999 if omitted) |
| `style_id` | string | `5fbabfac-...` | Cinematic style ID (default: General) |
| `enhance_prompt` | bool | `true` | Enable prompt enhancement |
| `negative_prompt` | string | — | Negative prompt |

### Recommended Sizes

| Use Case | Aspect Ratio | Quality |
|----------|-------------|---------|
| Ultra-wide cinematic | `21:9` | `1080p` |
| Cinematic frame (widescreen) | `16:9` | `1080p` |
| Standard landscape | `4:3` | `1080p` |
| Wide landscape | `3:2` | `1080p` |
| Square cinematic | `1:1` | `1080p` |
| Cinematic portrait | `3:4` | `1080p` |
| Tall portrait | `2:3` | `1080p` |
| Film still (vertical) | `9:16` | `1080p` |
