---
name: video-skill
description: |
  Video generation skill (Seedance 2.0). Loaded by Mr Higgs for simple text-to-video, or by video-agent for complex generation (references, scene routing, imitation).
---

## Model Capabilities

| Dimension   | Spec                       |
| ----------- | -------------------------- |
| Image input | ≤ 9 images                 |
| Video input | ≤ 3 videos, 2–15s total    |
| Text input  | English only               |
| Max files   | 12 combined                |
| Duration    | 4–15s (< 4s auto-padded)   |
| Audio       | Generated automatically    |

---

## PROMPT CONSTRUCTION — MANDATORY RULES

**Apply ALL rules below to EVERY video generation. No exceptions.**

### Prompt Section Format

Every prompt is a **single JSON object** `{"prompt":"..."}` containing a single continuous string with inline section labels. Prompt hard cap: **4000 characters.**

```
Camera: [body + lens + rendering + focal + aperture]
Camera Style: [movement axis — preset or custom]
Light: [lighting axis — preset or custom]
Style & Mood: [color axis + genre texture + atmosphere — NEVER skip]
Narrative Summary: [1-sentence scene description]
Starting Composition: [first frame lock — positions, distances, facing, camera angle]
Dynamic Description: [scene-by-scene with timestamps — Scene N (Xs–Ys): ... → Transition.]
Static Description: [location, props, ambient — establish everything referenced in Dynamic]
Negative: [all "no X" constraints, deduplicated]
```

For full section details, injection rules, and examples see `.claude/skills/video-skill/references/prompt-structure.md`.
For style axis presets and custom style guidance see `.claude/skills/video-skill/references/style-system.md`.
For camera body/lens/focal/aperture presets see `.claude/skills/video-skill/references/camera-type.md`.

### 8-Point Pre-Generation Checklist

**Verify EVERY prompt passes ALL 8 checks before running `higgsfieldcli generate`.**

**CHECK 0 — Audio is mandatory (HARD RULE):** Every `seedance_2_0` generation MUST include BOTH of these, together, or it is invalid and must not be submitted:

1. `"generate_audio": true` in the JSON payload (the parameter that actually renders audio).
2. An `Audio:` section in the prompt describing spoken lines, ambient sound, or music direction (what to render).

Only skip if the user explicitly asks for silence ("no sound", "silent", "mute", "без звука"). In every other case — including UGC, marketing, ads, talking-heads, ASMR, product demos, dialogue scenes, b-roll, montage pieces, cinematic-long-video shots — audio is non-negotiable.

- FAIL: prompt has `Audio:` copy but payload missing `"generate_audio": true` → silent output, audio description ignored
- FAIL: payload has `"generate_audio": true` but prompt has no `Audio:` section → arbitrary/undirected audio
- FAIL: both omitted on any non-silent-intent video (default case)
- PASS: both present, Audio section describes the desired soundscape

**CHECK 1 — Material References:** If using elements via `<<<element_id>>>` — no additional flags needed, backend resolves automatically. If using `medias` instead → prompt MUST contain `@Image1` with a purpose label.

- ELEMENT: `"<<<abc123>>> walks down the street..."` (no medias needed)
- MEDIA FAIL: `"medias":[{"role":"start_image","data":{"id":"abc","type":"media_input"}}]` + `"A cat running"` (no @Image1)
- MEDIA PASS: `"medias":[{"role":"start_image","data":{"id":"abc","type":"media_input"}}]` + `"@Image1 is the character reference. The cat leaps..."`

**CHECK 2 — Camera Movement:** Prompt MUST contain a specific camera term from Camera Style axis or explicit movement in Dynamic Description: `pan, tilt, zoom, dolly, push in, pull out, truck, crane, pedestal, orbit, arc, tracking, static, handheld, aerial, Steadicam, whip-pan`

- FAIL: `"cinematic"`, `"smooth motion"`, `"dynamic angle"` — NOT camera movements
- PASS: Camera Style preset (contains movement vocabulary), or explicit `"slow dolly push in"`, `"static wide shot"`, `"crane lift + pan"`

**CHECK 3 — Starting Composition:** Prompt MUST contain a Starting Composition section locking the first frame: character positions in frame, facing direction, camera position/angle, key props.

- FAIL: Dynamic Description starts with action but no spatial setup
- PASS: `"Starting Composition: Camera 10 feet from desk, eye-level, wide shot. Figure in dark suit frame-left facing figure in white shirt frame-right."`

**CHECK 4 — Style & Mood (never skip):** Must contain Style & Mood section with color/atmosphere. Camera Settings, Camera Style, and Light sections must be present (from presets or custom).

- FAIL: Jumping straight to Narrative Summary with no style sections
- PASS: All four style-related sections present (Camera, Camera Style, Light, Style & Mood)

**CHECK 5 — Engine Limits:** ≤ 4 beats, ≤ 3 characters per shot, ≤ 15s, ≤ 4000 chars total prompt.

**CHECK 6 — Negative Block:** Prompt ends with Negative section collecting all "no X" from Camera Style, Light, Color, camera_settings, and user constraints. Deduplicated.

**CHECK 8 — No Antislop:** Remove: breathtaking, stunning, captivating, mesmerizing, masterfully, visual feast, seamlessly, effortlessly, a symphony of, speaks volumes, resonates deeply. See `.claude/skills/video-skill/references/prompt-structure.md` for full list.

### Constraint System — SACRED / RESPECT

Extract constraints from user input before building the prompt. Two tiers:

**SACRED (never override, never omit — output is invalid without them):**
- Negations — all "no X" items ("no people", "no camera movement", "no music")
- Style locks — any user-provided camera/light/color axis string is LOCKED, director cannot override
- Content restrictions — "no violence", "family-safe", "realistic"
- Numeric parameters — aperture f-stop, focal length, duration_seconds
- Dialogue integrity — user-provided dialogue is UNTOUCHABLE (never rewrite, soften, or translate)
- Product accuracy — exact visual details from reference images (colors, logos, shape, material)

**RESPECT (preserve unless conflicts with engine limits):**
- Camera direction suggestions (not locked, but strong preference)
- Lighting mood requests
- Pacing keywords (slow, snappy, building)
- Character physicality notes

**Priority chain:** SACRED > RESPECT > LOCKED style.axes > user prompt direction > archetype > genre > feasibility limits.

**Verification before output:**
1. Confirm every SACRED item appears in final prompt unchanged
2. All SACRED negations collected into Negative block
3. Flag conflicts (e.g. "no cuts" + multi-shot) — resolve per priority chain
4. User dialogue present in Dynamic Description verbatim

### Density by Duration

| Duration | Sentences in Dynamic Description |
| -------- | -------------------------------- |
| ≤ 10s    | 4–8                              |
| 11–12s   | 6–10                             |
| 13–15s   | 8–14, consider time segmentation |

**Single-shot:** ≤ 6 sentences for ≤10s, ≤ 8 for 11–15s.

### Camera & Style

Camera movement is determined by the **Camera Style axis** — either a preset (10 options from Hitchcock to Doyle) or a custom string. See `.claude/skills/video-skill/references/style-system.md` for full presets and custom style templates.

When Camera Style is LOCKED (preset or custom string), movement vocabulary comes ONLY from that axis. When null, the director selects based on scene content and archetype.

**Cut rules:** Every cut changes BOTH shot size AND camera mode. Re-anchor positions after cuts. Maintain 180° rule. See `.claude/skills/video-skill/references/camera-system.md` for full cut rules.

**Scene labels:** Multi-shot uses `Scene N (Xs–Ys):` with `→ Transition.` markers. Single-shot uses temporal markers `(0–3s)` only.

### Engine Hard Constraints

- ≤ 3 characters per shot (drops tracking above 3)
- ≤ 5 named characters per scene total
- Character exits frame = gone for rest of shot (no re-entry)
- NEVER use reflection shots (mirrors, puddles, blades)
- Off-screen = nonexistent — show state changes on camera before referencing
- Action = named technique or intent, NOT biomechanics
- Micro-expressions as physics: "jaw clenches" not "looks angry"
- Describe characters as user specifies — use wardrobe + appearance + action
- Prompt hard cap: 4000 characters

### Audio is ON by default

Every `seedance_2_0` generation payload must include `"generate_audio": true`. The only exception is when the user explicitly asks for a silent clip ("no sound", "silent", "mute", "без звука").

**Important distinction — two separate controls:**

- **`"generate_audio": true`** — JSON parameter. This is what actually renders audio in the output video.
- **`Audio:` prompt section** — describes the intended sound design (ambient, diegetic, sfx cues). Descriptive only — does not by itself trigger audio rendering.

Both are needed together when audio is wanted. A prompt with `Audio:` copy but `"generate_audio": false` produces a silent video with no sound matching the description.

---

## SCENE TYPE ROUTING

Classify the scene, then apply the right rules:

| Scene Contains                                 | Type          | Key Rules                                                                         |
| ---------------------------------------------- | ------------- | --------------------------------------------------------------------------------- |
| Combat, stunts, pursuit, physical conflict     | **Action**    | Read `.claude/skills/video-skill/references/scene-action.md` — archetypes, LINEAR/CHAOTIC, beat compression  |
| Spoken dialogue driving drama                  | **Dialogue**  | Read `.claude/skills/video-skill/references/scene-dialogue.md` — power dynamics, shot patterns, word budgets |
| Landscape, journey, atmosphere, transformation | **General**   | Read `.claude/skills/video-skill/references/scene-general.md` — archetypes, environmental progression        |
| Imitating another video's style                | **Imitation** | Read `.claude/skills/video-skill/references/imitation-rules.md` — reference only technique, never content    |

---

## COMPLETE PROMPT EXAMPLES

### Action Scene (12s, MMA fight)

```json
{"prompt":"Camera: ARRI Alexa 35 digital cinema camera, clean sensor, 8K. ARRI Signature Prime lens, large format | ARRI Signature Prime rendering — high resolution, soft micro-contrast, ultra-creamy round bokeh | 35, f/4. Camera Style: Cinematographic style of Paul Greengrass, aggressive handheld in crowd, focus hunting losing and locking, low aggressive angles, no stability, no dolly, no crane, no composed framing. Light: Lighting: single large soft diffused source above and behind the subject angled downward, light falling onto top of head and shoulders, eyes in soft shadow under brow ridge, no frontal light, no flat even illumination. Style & Mood: Flat naturalistic color, no stylization, true reds, true whites. High-octane athletic realism, sweat and muscle definition, gritty arena intensity. Narrative Summary: In a fierce MMA exchange, Fighter A launches strikes but gets intercepted by Fighter B's devastating counter and takedown. Starting Composition: Camera at cage-side level, 35mm medium shot. Fighter A (black shorts, shaved head) frame-left in orthodox stance. Fighter B (red shorts, cornrowed hair) frame-right in southpaw. Both circling clockwise, three feet apart. Canvas scuffed, overhead spots casting hard pools. Scene 1 (0–4s): 35mm, eye-level, aggressive handheld. Fighter A frame-left fires a jab-cross combination, Fighter B (frame-right) absorbs behind a high guard, sweat spraying on impact. Camera shudders with each strike. → Smash cut. Scene 2 (4–7s): 24mm, low-angle, handheld from canvas level. Fighter B steps offline and drives a heavy leg kick into A's lead thigh — A's weight buckles, knee dipping. Camera tilts up as B closes distance. → Hard cut. Scene 3 (7–12s): 50mm, wide stabilized tracking. Fighter B (now frame-left) shoots a double-leg takedown, hooks both legs and drives forward. Fighter A carried backward across the octagon, slammed spine-first into the chain-link fence, metal rattling from the collision. B pins A against the cage, forearm across chest. Static Description: Enclosed octagon cage, black wire mesh, padded posts, scuffed canvas floor. Bright hazy spotlights overhead, flying sweat droplets catching light. Ambient: crowd roar, body impacts, heavy breathing, cage rattle. Negative: no stability, no dolly, no crane, no composed framing, no slow motion, no music."}
```

### Atmosphere Scene (10s, forest at dawn)

```json
{"prompt":"Camera: ARRI Alexa 35, Cooke S7/i Full Frame | Cooke S7/i rendering — warm organic tone, gentle halation on highlights, smooth bokeh | 35, f/2.8. Camera Style: Cinematographic style of Roger Deakins — measured stillness, single slow reframe pan ≤5°, tripod-locked, no handheld, no crane, no snap movement. Light: Only natural daylight, pre-dawn transitioning to first light, no artificial sources, no fill light. Style & Mood: Kodak Vision3 250D daylight stock, warm amber in highlights, muted sage in shadows. Epic naturalism, volumetric mist, God rays through treeline gaps. Narrative Summary: A solitary traveler moves through primordial forest as dawn light transforms the landscape. Starting Composition: Camera at eye level on tripod, 35mm wide shot. A cloaked figure enters frame-right at midground depth on a narrow path. Foreground: fern fronds and moss-covered roots. Midground: the path winding between massive trunks. Background: pale gold light shafts piercing mist between trees. Scene 1 (0–4s): 35mm, eye-level, static tripod. The cloaked figure moves left-to-right along the path, ferns brushing legs, mist curling with each step. Pale gold shafts pierce through canopy gaps, particles drifting in beams. Wind sways upper branches. Ambient: birdsong, soft footfall on damp earth, wind through canopy. → Hard cut. Scene 2 (4–7s): 24mm, low-angle, static locked. Camera at root level. ECU of dewdrop on spider web, light refracting through it. Behind: the figure passes in soft focus, scale of trunks visible above. → Hard cut. Scene 3 (7–10s): 85mm, telephoto, slow reframe pan 3° right. Compressed perspective — figure small against cathedral-scale trees. Warm dawn beam breaks through directly ahead, mist glowing gold. Figure pauses, turns head toward the light, holds gaze. Static Description: Ancient temperate forest, massive moss-covered trunks, fern-covered floor, low-hanging mist. Pre-dawn transitioning to first light. Dew on every surface. No structures, no other people. Negative: no handheld, no crane, no snap movement, no people other than the traveler, no music, no dialogue, no text overlay."}
```

---

## VIDEO IMITATION / REFERENCE MODE

When user references another video's style/camera/rhythm — read `.claude/skills/video-skill/references/imitation-rules.md`.

**Key principle:** Reference ONLY creative techniques. Content, characters, story = user's own.

```
Camera: [settings]. Camera Style: [axis]. Light: [axis].
Style & Mood: Referring to the [camera movement / editing rhythm] of @Video1, [color + atmosphere].
Narrative Summary: [user's scene]. Starting Composition: [first frame].
Dynamic Description: [user's content with referenced technique applied]. Static Description: [location].
Negative: [constraints].
```

---

## CLI COMMANDS

### `generate` — Generate (Seedance 2.0)

**Single video:**

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"Camera: [settings]. Camera Style: [axis]. Light: [axis]. Style & Mood: [color + atmosphere]. Narrative Summary: [scene]. Starting Composition: [first frame]. [Scene labels with timestamps]. Static Description: [location]. Negative: [constraints].","duration":8,"aspect_ratio":"9:16"}]'
```

**Multiple independent videos (parallel):**

The CLI accepts a JSON array for concurrent generation. Use this when generating multiple independent scenes/shots that don't depend on each other's results:

```bash
higgsfieldcli generate --json '[
  {"model":"seedance_2_0","prompt":"Camera: ... [scene 1]","duration":8,"aspect_ratio":"9:16"},
  {"model":"seedance_2_0","prompt":"Camera: ... [scene 2]","duration":10,"aspect_ratio":"9:16"}
]'
```

All items run concurrently. Each prints its own result JSON line as it completes. Errors are reported per-item (`request[N]: ...`).

**When to use parallel:** Multiple independent scenes, variant takes of the same scene, batch generation of unrelated clips.
**When NOT to use parallel:** Scene B requires Scene A's output as a reference input.

| JSON field       | Type   | Default    | Description                                                                                                                                   |
| ---------------- | ------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`          | string | _required_ | Always `"seedance_2_0"`                                                                                                                       |
| `prompt`         | string | _required_ | Must pass all 7 checks. CS3.5 format: Camera→Camera Style→Light→Style & Mood→Narrative→Starting Comp→Dynamic→Static→Negative                  |
| `medias`         | array  | —          | Input media. Each entry: `{"role":"start_image","data":{"id":"ID","type":"TYPE"}}` (roles: image, video, audio, file, start_image, end_image) |
| `duration`       | int    | `8`        | 4–15 seconds                                                                                                                                  |
| `width`          | int    | `720`      | Width px                                                                                                                                      |
| `height`         | int    | `720`      | Height px                                                                                                                                     |
| `aspect_ratio`   | string | `"1:1"`    | `"1:1"`, `"3:4"`, `"9:16"`, `"16:9"`                                                                                                          |
| `resolution`     | string | `"720p"`   | `"720p"`                                                                                                                                      |
| `generate_audio` | bool   | `true`     | Audio is ON by default. Set to `false` ONLY when the user explicitly asks for a silent clip, or when the clip is b-roll / loop material intended to be paired with external audio in post (montage, marketing ad with custom voiceover, etc.).  |

### `upload` — Upload Reference Media

```bash
higgsfieldcli upload --file /path/to/image.png
```

Returns `{"id": "media_abc", "url": "https://..."}` — only `id` is needed in the `medias` array.

#### IP Check for Seedance 2 Inputs

**All uploaded images, videos, and elements used as Seedance 2 inputs MUST pass IP check before generation.** Use `--force-ip-check` to upload and wait for the check to complete:

```bash
higgsfieldcli upload --file /path/to/image.png --force-ip-check
```

Returns `{"id": "media_abc", "url": "https://...", "status": "...", "ip_check_finished": true}`.

| Flag               | Description                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| `--force-ip-check` | Triggers IP check on the uploaded media and waits until it completes (retries up to 5 times on timeout) |

**IP check result:** If `ip_check_finished` is `true` and `status` is not `"ip_detected"`, the media is safe to use. If `status` is `"ip_detected"`, choose different media.

If IP check fails, do NOT use the media for video generation — it will be rejected. Choose different source media instead.

### Polling — Fire-and-Forget

`higgsfieldcli generate` no longer blocks. It prints a `created` line with `job_set_id`, `job_set_type`, `job_ids` immediately and returns. Capture that and move on — do NOT use long timeouts or `run_in_background`.

**Poll only when the video result is referenced downstream** (montage input, image/video chain, or user asks for the URL):

```bash
higgsfieldcli status --job-id JOB_ID --poll
```

Returns `{"job_id","status","job_set_type","ip_check_finished","ip_detected","job_set_id","result":{"url","type"}}`. `result.url` is the CDN URL of the finished video; `result.type` is `"video"`. Reference the job in a subsequent generate with `id=JOB_ID`, `type=seedance_2_0_job` (no url needed). If the downstream generation is also `seedance_2_0` and references a prior job, run `higgsfieldcli job-ip-check --job-id <id> --poll` before submitting.

**Terminal statuses:** `completed`, `canceled`, `failed`, `nsfw`, `ip_detected`

---

## WORKFLOWS

### Text-to-Video

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"Camera: ARRI Alexa 35, clean sensor, 8K. ARRI Signature Prime | high resolution, soft micro-contrast, creamy bokeh | 35, f/2.8. Camera Style: Cinematographic style of David Fincher, imperceptible dolly forward, mechanically perfect stabilization, no handheld, no snap movement. Light: Only natural daylight from window, soft directional gradient, no artificial sources, no fill light. Style & Mood: Kodak Vision3 250D, warm amber highlights, neutral shadows. Morning warmth, golden hour volumetric light, coffee steam catching sun rays. Narrative Summary: Morning light fills a cozy coffee shop as steam curls from ceramic cups. Starting Composition: Camera in doorway, eye-level, 35mm wide shot. Wooden counter midground, ceramic cups aligned, tall windows frame-right casting long shadows across surfaces. No people visible. Scene 1 (0–4s): 35mm, eye-level, imperceptible dolly push in from doorway toward counter. Steam curls from cups, morning light streams through windows, long shadows shift across wooden surfaces. Ambient: distant street sounds, ceramic clink, coffee machine hum. Scene 2 (4–8s): 50mm, medium shot, micro push-in. Camera arrives at counter level. Steam rises through a shaft of window light, particles suspended. A hand enters frame-right, lifts a cup. Static Description: Coffee shop interior, wooden counter, ceramic cups, tall windows, morning light, exposed brick wall. Negative: no handheld, no snap movement, no fast cuts, no music.","duration":8,"aspect_ratio":"9:16"}]'
```

Returns a `created` line immediately with `job_set_id`, `job_set_type: "seedance_2_0"`, `job_ids`. Do not wait. Poll only if the video is referenced downstream.

### Element-to-Video (Preferred for Characters/Locations)

Use reference elements for consistent characters and locations across multiple videos. No upload or masking needed.

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"Camera: Arriflex 16SR, 16mm film, heavy grain. ARRI Signature Prime | high resolution, creamy bokeh | 35, f/2.8. Camera Style: Cinematographic style of Sean Baker, subtle handheld with operator breathing, near-static micro-sway, no aggressive handheld, no crane, no dolly. Light: Only practical light sources — neon signs, street lamps, no fill light, no flat illumination. Style & Mood: Fuji Eterna 500, desaturated blue-grey wash, steel-blue midtones, cold and metallic. Gritty documentary intimacy, rain-soaked urban night. Narrative Summary: <<<CHAR_ELEMENT_ID>>> walks through <<<LOC_ELEMENT_ID>>> on a rain-soaked night. Starting Composition: Camera at shoulder height, 35mm medium shot. The figure (<<<CHAR_ELEMENT_ID>>>) enters frame-left, walking right-to-left along the sidewalk. Neon signs reflect in wet asphalt. Scattered pedestrians in background. Scene 1 (0–4s): 35mm, shoulder-height, subtle handheld tracking from the side. The figure walks right-to-left, coat swaying, rain catching streetlight glare. Neon reflections slide across wet pavement. → Hard cut. Scene 2 (4–8s): 50mm, medium close-up, micro push-in. The figure pauses, turns head and looks back over shoulder. Rain beads on coat fabric. Breath visible in cold air. Static Description: Rain-soaked urban street at night, neon signs, wet asphalt, scattered pedestrians, puddles reflecting colored light. Negative: no aggressive handheld, no crane, no dolly, no choreographed camera path, no music.","duration":8,"aspect_ratio":"9:16"}]'
```

The backend automatically resolves `<<<element_id>>>` and injects the element's media as reference. Multiple elements can be used in a single prompt.

### Image-to-Video (Legacy — use elements when possible)

```bash
# 1. Upload reference
UPLOAD=$(higgsfieldcli upload --file output/images/character.png)
IMAGE_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Generate with reference
higgsfieldcli generate --json "[{\"model\":\"seedance_2_0\",\"prompt\":\"@Image1 is the character reference. Camera: Arriflex 16SR, 16mm film, heavy grain. ARRI Signature Prime | creamy bokeh | 35, f/2.8. Camera Style: Cinematographic style of Sean Baker, subtle handheld, near-static micro-sway, no aggressive handheld, no crane, no dolly. Light: Only practical sources — neon signs, street lamps, no fill light. Style & Mood: Desaturated blue-grey wash, gritty documentary aesthetic. Narrative Summary: A figure walks through a rain-soaked city street at night. Starting Composition: Camera at shoulder height, 35mm medium shot. The figure (@Image1) enters frame-left on wet sidewalk, neon reflections on asphalt. Scene 1 (0–4s): 35mm, handheld tracking from the side. The figure walks right-to-left, coat swaying, rain catching streetlight glare. → Hard cut. Scene 2 (4–8s): 50mm, push-in. The figure pauses and looks back over shoulder. Rain beads on fabric. Static Description: Rain-soaked urban street at night, neon signs, wet asphalt, scattered pedestrians. Negative: no aggressive handheld, no crane, no dolly, no music.\",\"medias\":[{\"role\":\"start_image\",\"data\":{\"id\":\"$IMAGE_ID\",\"type\":\"media_input\"}}],\"duration\":8,\"aspect_ratio\":\"9:16\"}]"
```

---

## DEFAULTS

| Use Case          | Aspect Ratio | Width | Height |
| ----------------- | ------------ | ----- | ------ |
| Vertical (mobile) | `9:16`       | 720   | 1280   |
| Portrait          | `3:4`        | 540   | 720    |
| Horizontal        | `16:9`       | 1280  | 720    |
| Square            | `1:1`        | 720   | 720    |

## ERROR HANDLING

| Error         | Fix                                          |
| ------------- | -------------------------------------------- |
| `status 401`  | Proxy auth error                             |
| `status 429`  | Rate limited — wait and retry                |
| `failed`      | Retry with different prompt                  |
| `nsfw`        | Content flagged — modify prompt              |
| `ip_detected` | IP content — modify prompt or choose new ref |

---

## DEEP-DIVE REFERENCES

| File                               | When to Read                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------- |
| `.claude/skills/video-skill/references/prompt-structure.md`   | Full CS3.5 section format, image reference system, density caps, antislop, examples   |
| `.claude/skills/video-skill/references/style-system.md`       | Three-axis style system (Camera/Light/Color presets), DP Combos, custom styles, Session Lock |
| `.claude/skills/video-skill/references/camera-type.md`        | Camera Body, Lens, Focal Length, Aperture presets and injection rules                 |
| `.claude/skills/video-skill/references/camera-system.md`      | Camera terms, cut rules, speed ramp integration, depth layering                       |
| `.claude/skills/video-skill/references/engine-constraints.md` | Rendering limits, duration-to-density tables, beat compression, product angle lock    |
| `.claude/skills/video-skill/references/scene-action.md`       | 10 action archetypes, LINEAR/CHAOTIC, beat variety, position swaps, single-shot, overflow tiers |
| `.claude/skills/video-skill/references/scene-dialogue.md`     | 6 dialogue archetypes, shot patterns, word budgets, compression, single-shot mode, overflow tiers |
| `.claude/skills/video-skill/references/scene-general.md`      | 6 general archetypes, sub-classification, shot density, single-shot, sound design, overflow tiers |
| `.claude/skills/video-skill/references/producer-guide.md`     | Session Lock, prompt writing guidelines, visual review, multi-clip planning            |
| `.claude/skills/video-skill/references/style-vocabulary.md`   | Genre modifier system, style keywords, aspect ratio guide                             |
| `.claude/skills/video-skill/references/imitation-rules.md`    | Video reference/imitation rules                                                       |
