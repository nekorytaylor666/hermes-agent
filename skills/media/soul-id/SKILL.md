---
name: soul-id-skill
description: |
  Sub-agent skill — do NOT invoke directly. Delegate to @"soul-id-agent (agent)" instead.
  Loaded by soul-id-agent sub-agent for Soul ID creation and management.
---

## ⚠️ EXECUTION ROUTING — read this first, supersedes CLI snippets below

**Image and video generation ALWAYS go through the `higgsfield_generate` tool.**
The Go `higgsfieldcli` binary referenced later in this file is **deprecated
and unavailable at runtime** — any `higgsfieldcli generate --json '…'`
snippet is just showing the JSON body; pass that body to the tool instead.

### The tool is non-blocking by default

Do **not** wait for generation to finish. Submit, tell the user "🎨 Image
generation started (N jobs)" with the returned `job_ids`, and end the turn.
Only call `higgsfield_job_status` when the user explicitly asks for results,
or after enough time has passed that results are likely ready.

Single image:
```
higgsfield_generate({
  "model": "…",              # e.g. nano_banana_2, soul_v2, seedance_2_0
  "prompt": "…",
  "aspect_ratio": "1:1",
  # …model-specific fields (see tables below)…
})
# → returns { job_set_id, job_ids: [...], status: "created" } in ~1s
```

Parallel fan-out (dozens at once):
```
higgsfield_generate({
  "requests": [
    {"model": "nano_banana_2", "prompt": "…"},
    {"model": "nano_banana_2", "prompt": "…"},
    …
  ],
  "concurrency": 8            # 1–32
})
# → returns { submissions: [{index, job_set_id, job_ids}, …] } in ~3–5s
```

Results later (only when user asks):
```
higgsfield_job_status({"job_ids": ["…", "…"]})
```

### When to block instead

Only pass `"async": false` when the user explicitly asked for the final URL
in the same turn and is OK waiting (up to ~15 min). Default to async.

### Uploads not wired up

Media / image uploads are **not** currently exposed as a tool. Skip upload
workflows; if the user needs image-to-image with a local file, tell them
upload isn't available yet. The tool supports every model listed here
(imagegen_2_0, nano_banana_2, soul_v2 / text2image_soul_v2, soul_cinematic,
soul_cast, soul_location, seedream_v5_lite / v4_5, seedance_2_0, kling3_0,
and the full Tier-2 set).


## What is a Soul ID?

A Soul ID (internally "custom reference") is a trained identity model. You upload 1-100 face photos, the backend trains a model, and then you can generate new images that preserve that person's likeness using Soul 2.0.

## Workflow

### 0. Bootstrap from Description (fictional persona, no source photos)

Use this path when the persona does not exist in reality — a new influencer, a fictional character, a synthetic cast member — and no photos are available to collect. You generate the training set yourself from a detailed character description.

Do **not** run this path if the user provided photos, an Instagram handle, or an existing face reference. Those go to `### 1. Collect Images`.

**Steps:**

1. **Seed portrait** — generate one frontal portrait of the persona via `soul_v2` (preferred for editorial / fashion look) or `nano_banana_2` (preferred for photorealistic realism). In the prompt include: approximate age, skin tone, hair color / texture / length, eye color, face shape, build, one simple outfit, neutral background, natural light, authentic skin texture. Aspect ratio `3:4`.

   ```bash
   higgsfieldcli generate --json '{"model":"soul_v2","prompt":"<detailed portrait description>","aspect_ratio":"3:4","quality":"1080p"}'
   ```

2. **Poll the seed** until completed — the job id is needed for the next step:

   ```bash
   higgsfieldcli status --job-id <SEED_JOB_ID> --poll
   ```

2.5. **Wait for seed to complete (mandatory gate before augmentation batch)** — before firing the augmentation batch in step 3, confirm the seed job from step 2 has reached `completed`:

   ```bash
   higgsfieldcli status --job-id "$SEED_JOB_ID" --poll
   ```

   **Why this step is not optional.** Step 3 fires 4 `nano_banana_2` augmentations that each reference the seed job as input. If the batch is submitted while the seed is still `in_progress`, the reference cannot be resolved and all 4 augmentation jobs fail. Skipping this gate is the most common cause of silent bootstrap failures.

   Only after `status --poll` returns `{"status":"completed"}` proceed to step 3.

3. **Augmentation batch** — generate 4 variations of the same person using `nano_banana_2` with the seed job as reference. Use one universal prompt template, varying only `[Position]` and `[View]` across the 4 items to introduce pose / angle diversity for Soul ID training:

   ```
   Universal augmentation prompt:

   "Generate an image featuring the exact same person from the input reference,
    maintaining high facial fidelity. The context is completely changed to a new
    realistic setting with the subject wearing a new outfit. Position: [new pose].
    View: [new shot type]. Style must perfectly match the original aesthetic."
   ```

   Suggested 4-item variation axis (balances angle, distance, and pose):
   - Item 1 — Position: standing; View: medium shot, waist-up
   - Item 2 — Position: sitting or leaning forward; View: close-up portrait
   - Item 3 — Position: walking or mid-motion; View: full body shot
   - Item 4 — Position: head turn; View: side profile headshot

   Submit as a JSON array with `"images":[{"id":"<SEED_JOB_ID>","type":"text2image_soul_v2_job"}]` (or `nano_banana_2_job` if the seed was NB2) on each item. All 4 run in parallel.

4. **Poll all 4 augmentations** until completed.

5. **Download all 5 images** (seed + 4 augmentations) to a local training directory:

   ```bash
   mkdir -p /tmp/soul-bootstrap-<slug>
   curl -sL -o /tmp/soul-bootstrap-<slug>/seed.png   "<SEED_URL>"
   curl -sL -o /tmp/soul-bootstrap-<slug>/aug1.png   "<AUG1_URL>"
   curl -sL -o /tmp/soul-bootstrap-<slug>/aug2.png   "<AUG2_URL>"
   curl -sL -o /tmp/soul-bootstrap-<slug>/aug3.png   "<AUG3_URL>"
   curl -sL -o /tmp/soul-bootstrap-<slug>/aug4.png   "<AUG4_URL>"
   ```

6. **Train the Soul ID** from the local directory:

   ```bash
   higgsfieldcli soul-id create --dir /tmp/soul-bootstrap-<slug> --name "<persona-name>" --poll
   ```

   Capture the returned `reference_id` — this is the persona's Soul ID.

7. **Create a character element** (only if the persona will be used in `seedance_2_0` videos). Seedance does not consume `soul_id` directly — identity enters seedance via the `<<<element_id>>>` placeholder.

   **Reuse the seed.png from step 5.** It is a clean frontal portrait already in the training set — do not generate a separate verification/confirmation image just to upload it. Any extra generation here is wasted work.

   ```bash
   # Upload the seed portrait (already downloaded in step 5) with IP check
   UPLOAD=$(higgsfieldcli upload --file /tmp/soul-bootstrap-<slug>/seed.png --force-ip-check)
   UPLOAD_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
   UPLOAD_URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['url'])")

   # Create the element as an ip-verified character
   higgsfieldcli element create --category character_ip_verified --name "<persona-name>" \
     --description "<short visual description>" \
     --media "id=$UPLOAD_ID;url=$UPLOAD_URL;type=media_input"
   ```

   Use the returned element id in subsequent seedance prompts via `<<<ELEMENT_ID>>>`.

8. **(Optional) Verify** by generating one test image via the new Soul ID. Skip this unless you have reason to doubt the training — the seed + 4 augmentations already confirm the face. If you do verify, the test generation is for visual inspection only; do not download, upload, or reuse its output — step 7 already handled the element:

   ```bash
   higgsfieldcli generate --json '{"model":"text2image_soul_v2","prompt":"<scene matching the target style>","aspect_ratio":"3:4","quality":"1080p","soul_id":"<REFERENCE_ID>"}'
   ```

**After bootstrap completes** — downstream image generations use `soul_id` directly on `text2image_soul_v2`; downstream video generations use the element id via `<<<id>>>` in `seedance_2_0` prompts. The trained Soul ID and the element persist across sessions, so one bootstrap run covers an unlimited number of future generations of the same persona.

### 1. Collect Images

**From Instagram (using instagramcli):**

```bash
# Get user profile to find user ID
instagramcli user by-username -u "USERNAME"
# Extract user ID from response: .data.id

# Get user media posts
instagramcli user medias --user-id "USER_ID" --flat
# Extract image URLs from response — look for .image_versions2.candidates[0].url or .thumbnail_url
# For carousel posts, check .carousel_media[].image_versions2.candidates[0].url

# Paginate if needed (use cursor from response)
instagramcli user medias --user-id "USER_ID" --flat --cursor "CURSOR"
```

**From local files:**

Skip to step 2 — point `--dir` at the directory containing images.

**From URLs:**

Download images to a temp directory first:

```bash
mkdir -p /tmp/soul-id-images
curl -L -o /tmp/soul-id-images/01.jpg "IMAGE_URL_1"
curl -L -o /tmp/soul-id-images/02.jpg "IMAGE_URL_2"
# ... repeat for each image
```

### 2. Download Instagram Images

After fetching media from instagramcli, download the best image URLs:

```bash
mkdir -p /tmp/soul-id-USERNAME

# For each post, extract the highest resolution image URL and download
curl -L -o /tmp/soul-id-USERNAME/01.jpg "URL_1"
curl -L -o /tmp/soul-id-USERNAME/02.jpg "URL_2"
# ... up to 100 images (aim for 10-30 good face photos)
```

**Image selection tips for best results:**

- Prefer clear face shots (front-facing, good lighting)
- Include variety: different angles, expressions, lighting conditions
- Avoid group photos where the target face is small
- Skip heavily filtered/edited images
- 10-30 high-quality face photos is the sweet spot

### 3. Create Soul ID

```bash
higgsfieldcli soul-id create \
  --dir /tmp/soul-id-USERNAME \
  --name "Person Name" \
  --poll
```

This command:

1. Discovers all images (jpg, png, webp, heic) in the directory
2. Batch-uploads them to the Higgsfield backend
3. Creates a Soul 2.0 custom reference
4. Polls until training completes (up to 30 minutes)

Output includes `reference_id` — save this for generation.

The `--poll` flag blocks until training completes (up to 30 minutes):

```bash
higgsfieldcli soul-id create \
  --dir /tmp/soul-id-USERNAME \
  --name "Person Name" \
  --poll
```

### 4. Generate with Soul ID

Once the Soul ID status is `completed`, use it with `text2image_soul_v2`:

```bash
higgsfieldcli generate --json '[{"model":"text2image_soul_v2","prompt":"a portrait photo in a garden, soft natural lighting","soul_id":"REFERENCE_ID","soul_strength":1.0,"aspect_ratio":"3:4","batch_size":4}]'
```

The CLI returns a `created` line immediately with `job_set_id`, `job_set_type`, `job_ids`. Poll via `higgsfieldcli status --job-id <id> --poll` only if the result is needed downstream.

### 5. Management Commands

```bash
# List Soul IDs
higgsfieldcli soul-id list

# List only completed Soul IDs
higgsfieldcli soul-id list --status completed

# Check status of a specific Soul ID
higgsfieldcli soul-id status --id "REFERENCE_ID"

# Delete a Soul ID
higgsfieldcli soul-id delete --id "REFERENCE_ID"
```

## Full Example: Instagram to Soul 2.0 Generation

```bash
# 1. Get Instagram user ID
PROFILE=$(instagramcli user by-username -u "alexconsani")
USER_ID=$(echo "$PROFILE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# 2. Fetch media posts
MEDIAS=$(instagramcli user medias --user-id "$USER_ID" --flat)

# 3. Extract image URLs and download (use python3 to parse JSON)
mkdir -p /tmp/soul-id-alexconsani
# Parse and download top face images from the media response

# 4. Create Soul ID (--poll blocks until training completes)
SOUL=$(higgsfieldcli soul-id create \
  --dir /tmp/soul-id-alexconsani \
  --name "Alex Consani" \
  --poll)
REF_ID=$(echo "$SOUL" | python3 -c "import sys,json; print(json.load(sys.stdin)['reference_id'])")

# 5. Generate with Soul 2.0 — returns created line immediately (fire-and-forget)
CREATED=$(higgsfieldcli generate --json "[{\"model\":\"text2image_soul_v2\",\"prompt\":\"editorial fashion photo, studio lighting, white background\",\"soul_id\":\"$REF_ID\",\"batch_size\":4}]")
JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; print(json.loads(sys.stdin.read().splitlines()[0])['job_ids'][0])")
# Poll only if result is needed downstream:
# higgsfieldcli status --job-id "$JOB_ID" --poll
```

## Parameters Reference

### soul-id create

| Flag         | Required | Default   | Description                   |
| ------------ | -------- | --------- | ----------------------------- |
| `--dir, -d`  | Yes      | —         | Directory containing images   |
| `--name, -n` | No       | "Soul ID" | Name for the Soul ID          |
| `--poll`     | No       | false     | Poll until training completes |

### text2image_soul_v2 (with Soul ID) — via `generate --json`

| JSON field      | Required | Default     | Description                          |
| --------------- | -------- | ----------- | ------------------------------------ |
| `model`         | Yes      | —           | Always `"text2image_soul_v2"`        |
| `prompt`        | Yes      | —           | Text prompt                          |
| `soul_id`       | No       | —           | Custom reference ID                  |
| `soul_strength` | No       | 1.0         | Soul likeness strength (0.0-1.0)     |
| `aspect_ratio`  | No       | `"3:4"`     | `"3:4"`, `"1:1"`, `"9:16"`, `"16:9"` |
| `batch_size`    | No       | 1           | Number of images (1-4)               |
| `quality`       | No       | `"1080p"`   | Quality level                        |
| `style_id`      | No       | `"default"` | Style UUID                           |

### soul-id list

| Flag       | Required | Default | Description                                               |
| ---------- | -------- | ------- | --------------------------------------------------------- |
| `--type`   | No       | soul_2  | Filter: soul, soul_2, soul_cinematic, soul_v2_preset      |
| `--status` | No       | —       | Filter: not_ready, queued, in_progress, completed, failed |
| `--size`   | No       | 20      | Results per page                                          |

## Error Handling

| Error                     | Fix                                                  |
| ------------------------- | ---------------------------------------------------- |
| `no image files found`    | Directory is empty or has no supported image formats |
| `too many images (N)`     | Maximum 100 images — remove some                     |
| `soul id training failed` | Bad input images — retry with better face photos     |
| `training timed out`      | Use `soul-id status --id X --poll` to resume waiting |
| `status 422`              | Invalid request — check image formats and count      |
