# Stage 2: Shot-by-Shot Video Generation + Stage 3: Assembly

Generate video for each shot sequentially, one at a time. Always invoke `/video-skill` — never call `higgsfieldcli generate --json '[{"model":"seedance_2_0",...}]'` directly.

## Input

- `storyboard.json` → shots array
- Element registry (character → element_id, location → element_id, prop → element_id)
- Read `continuity.md` alongside this file

## Pre-Shot Checklist — VERIFY BEFORE EVERY SHOT

- [ ] **Location ref:** `location_id` for this shot → has element ID in registry? Embed `<<<element_id>>>` in prompt.
- [ ] **Character refs:** EVERY character in `characters_present` → has element ID? Embed ALL as `<<<element_id>>>` in prompt.
- [ ] **Prop refs:** Any prop in `props_present` → has element ID? Embed `<<<element_id>>>` in prompt.
- [ ] **Missing entity?** If any character/location has no element ID → **STOP**. Generate image (soul-cast/soul-location), create element, THEN proceed.
- [ ] **Count verification:** Count `<<<...>>>` references in prompt. Expected = 1 (location) + len(characters_present) + len(props_present). If count ≠ expected → STOP, find missing ref.
- [ ] **Duration:** matches shot's `duration_sec` (4–15s).
- [ ] **Aspect ratio:** matches `storyboard.json.aspect_ratio`.
- [ ] **Audio:** `"generate_audio":true` always set in JSON. Audio is mandatory for every shot.
- [ ] **Scene type reference read:** Which scene type? (Action / Dialogue / General). Which reference file was read? Which archetype or pattern applied? If you cannot answer these three questions → STOP, go back to Step 2.
- [ ] **Prompt:** passes ALL 7 `/video-skill` checks (see below).
- [ ] **Continuity:** if this is shot 2+, prompt begins from ending visual state of previous shot (see continuity.md).

**DO NOT send a shot with missing element refs. Every character in characters_present = a `<<<element_id>>>` in the prompt. Location = a `<<<element_id>>>`. Every prop = a `<<<element_id>>>`.**

**NOTE:** The "≤ 3 characters per shot" engine rule limits how many people are rendered on screen simultaneously — it does NOT limit how many elements you can reference.

## Prompt Construction Flow

For each shot, construct the video prompt following this exact sequence:

### Step 1: Start with Style Tag

Prepend `storyboard.json.style_tag` as the Style & Mood section:

```
Style & Mood: [style_tag from storyboard.json]
```

### Step 2: Route Scene Type — MANDATORY READ

**Before writing ANY prompt, classify the shot and READ the matching reference file.** This is not optional. The reference contains archetypes, camera patterns, density rules, and word budgets specific to the scene type. Prompts built without consulting the reference will be generic and flat.

| Shot content                                 | Scene type   | Reference to read                               | What it gives you                                                                                                                      |
| -------------------------------------------- | ------------ | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Combat, stunts, pursuit, physical conflict   | **Action**   | `.claude/skills/video-skill/references/scene-action.md`       | Archetypes (Pursuit/Duel/Standoff/Impact), LINEAR vs CHAOTIC modes, action-specific density tables, beat compression                   |
| Spoken dialogue driving the scene            | **Dialogue** | `.claude/skills/video-skill/references/scene-dialogue.md`     | Archetypes (Confrontation/Interrogation/Confession), power dynamics, OTS/dirty-single shot patterns, word budgets per duration, L-cuts |
| Landscape, atmosphere, journey, establishing | **General**  | `.claude/skills/video-skill/references/scene-general.md`      | Archetypes (Reveal/Journey/Atmosphere/Transformation), environmental progression, landscape rules                                      |
| Mixed (dialogue + action in same shot)       | **Both**     | Read BOTH `.claude/skills/video-skill/references/scene-dialogue.md` AND `.claude/skills/video-skill/references/scene-action.md` | Dialogue word budget constrains the action density; action camera rules override dialogue framing during physical beats                |

**Verification:** After reading the reference, note which archetype or pattern you are applying. Examples:

- Shot 2 (Novak confronts Kira): Scene type = Dialogue. Archetype = Confrontation. Applied: tight OTS, axis cross on power shift, quick ping-pong cuts on attack words.
- Shot 5 (hand-to-hand fight): Scene type = Action. Archetype = Duel. Applied: lower angle on dominant side, dominance alternates, LINEAR mode with 2–3 segments for 7s.
- Shot 8 (running through rain): Scene type = General. Archetype = Journey. Applied: tracking alongside, steady momentum, gradual shift.

### Step 3: Determine Internal Shot Structure (Multi-Shot vs. Single-Shot)

Each storyboard "shot" (= one seedance clip, 4–15s) can contain **multiple internal camera setups** separated by cuts. This is critical for visual interest — a single unbroken camera move gets monotonous, especially for clips 7s+.

**Decision table:**

| Clip duration | Storyboard content                                     | Internal structure                                | Cuts |
| ------------- | ------------------------------------------------------ | ------------------------------------------------- | ---- |
| 4–6s          | Single action, single emotion, establishing            | **Single-shot** — one continuous camera move      | 0    |
| 4–6s          | Two distinct beats (e.g., action + reaction)           | **2 internal shots**                              | 1    |
| 7–10s         | Single slow action (walk, gaze, atmosphere)            | **Single-shot** — one continuous move, OK         | 0    |
| 7–10s         | Multiple beats (discover + react, approach + confront) | **2–3 internal shots**                            | 1–2  |
| 11–15s        | Any content                                            | **2–4 internal shots** — almost always multi-shot | 1–3  |

**Multi-shot prompt pattern:**

Write the Dynamic Description with explicit cut markers. Every cut MUST change BOTH shot size AND camera style (per `/video-skill` cut rules):

```
Dynamic Description: Medium handheld tracking shot follows the dark-haired woman
through the corridor, fluorescent lights flickering overhead. Hard cut to a close-up
of her hand pushing open a metal door. Cut to a wide static shot — she steps into the
rain-soaked parking garage, puddles reflecting the cold fluorescent glow.
```

**Cut vocabulary:** `Hard cut to`, `Cut to`, `Immediate cut to`, `Smash cut to`, `Quick cut to`

**Single-shot prompt pattern:**

For clips that work as one continuous take, use flowing camera movement language without cut markers:

```
Dynamic Description: Slow crane descent revealing the apartment rooftop at dusk —
camera settles into a wide stabilized shot as the figure walks to the railing,
warm light catching the edges of the cityscape beyond.
```

**Rule of thumb:** If the storyboard `camera_intent` mentions alternating angles, reactions, or multiple framings — use multi-shot. If it describes one continuous movement — use single-shot.

### Step 4: Build 4-Section Prompt

```
Style & Mood: [style_tag — already set in Step 1]
Narrative Summary: [1-sentence safe description of what happens in this clip]
Dynamic Description: [camera movement + action prose with explicit cuts if multi-shot — PURE PHYSICS, no emotion labels, no dialogue text]
Static Description: [location, props, ambient — establish everything referenced in Dynamic]
Audio: [dialogue lines ONLY here — verbatim, original language — plus SFX/music notes]
```

### Step 5: Apply Density by Duration

**Multi-shot clips** (with cuts):

| Clip duration | Internal shots | Sentences in Dynamic Description |
| ------------- | -------------- | -------------------------------- |
| 4–6s          | 2              | 3–5                              |
| 7–10s         | 2–3            | 5–8                              |
| 11–12s        | 3–4            | 7–10                             |
| 13–15s        | 3–4            | 9–14                             |

**Single-shot clips** (one continuous take):

| Clip duration | Sentences in Dynamic Description |
| ------------- | -------------------------------- |
| 4–6s          | 2–4                              |
| 7–10s         | 4–6                              |
| 11–15s        | 5–8                              |

### Step 6: Insert Character Descriptions

From the continuity registry (see continuity.md):

- First mention in this shot: 8–10 word physical description
- Subsequent mentions in same prompt: 3–4 word shorthand
- **NEVER use character names** in video prompts

### Step 6: Insert Camera Movement

Translate the shot's `camera_intent` into specific camera terms from `/video-skill`:

- Level 1 (movement): Pan, Tilt, Zoom, Dolly, Push In, Pull Out, Truck, Crane, Orbit, Tracking, Static, Handheld, Aerial
- Level 2 (modifier): Slow, Smooth, Rapid, Subtle, Cinematic
- Level 3 (combine ≤ 2–3): `Orbit + Push In`, `Crane Lift + Pan`

### Step 7: Append Quality Suffix

- EN: `Facial features clear and undistorted, consistent clothing, 4K Ultra HD, stable and blur-free.`
- ZH: `面部特征清晰无变形，服装一致，4K超高清，画面稳定无模糊。`

### Step 8: Run 7-Point Checklist

From `/video-skill`:

1.
2. **Material References:** Elements via `<<<element_id>>>` are resolved automatically — no `@Image` labels needed. If using legacy `"medias"` array instead → prompt MUST contain `@Image1` labels.
3. **Camera Movement:** Prompt MUST contain a specific camera term (not just "cinematic" or "dynamic").
4. **Style & Mood:** ≥ 2 specific keywords, first 50 chars = filmmaking.
5. **Quality Suffix:** Appended at end.
6. **Engine Limits:** ≤ 4 beats, ≤ 3 characters per shot, ≤ 15s, ZH ≤ 1,800 chars.
7. **ZH Safety:** If any Chinese text, verify no hard-block words.
8. **No Antislop:** Remove: breathtaking, stunning, captivating, mesmerizing, masterfully, visual feast, seamlessly, effortlessly.

**If any check fails → fix before submitting.**

## CLI Command

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"<<<location_element_id>>> <<<character_1_element_id>>> <<<character_2_element_id>>> <full prompt following all rules above>","generate_audio":true,"duration":<shot_duration_sec>,"aspect_ratio":"<aspect_ratio>","width":<width>,"height":<height>}]'
```

No `"medias"` array needed when using elements — the backend resolves `<<<element_id>>>` automatically.

### Aspect Ratio Dimensions

| Aspect ratio | Width | Height |
| ------------ | ----- | ------ |
| 16:9         | 1280  | 720    |
| 9:16         | 720   | 1280   |
| 1:1          | 720   | 720    |

## Execution Protocol — STRICT

1. Construct prompt for shot N.
2. Submit generation command — CLI returns `created` line immediately. Poll via `higgsfieldcli status --job-id <id> --poll` to get the result.
3. Show result to user.
4. Save `shot_NNN.json` with prompt, job_id, status, output_path.
5. Wait for user: "continue" / "ok" / "next" → proceed to shot N+1.
6. If user requests revision → revise prompt → resubmit → wait again.

**Do NOT send the next shot until the previous one is completed AND the user approves.**

## Output: shot_NNN.json

```json
{
  "shot_number": 1,
  "duration_sec": 8,
  "location_id": "loc_01",
  "characters_present": ["CharacterName"],
  "elements": {
    "characters": [
      { "name": "CharacterName", "element_id": "<<<abc123-...>>>" }
    ],
    "location": { "location_id": "loc_01", "element_id": "<<<def456-...>>>" },
    "props": []
  },
  "video_prompt": "string (full prompt that was sent, with <<<element_id>>> references)",
  "job_id": "string",
  "status": "completed",
  "output_url": "string (URL from job result)",
  "output_path": "output/videos/shot_001.mp4"
}
```

## Handling Failures

| Status        | Action                                                          |
| ------------- | --------------------------------------------------------------- |
| `completed`   | Save video, show to user, wait for approval                     |
| `failed`      | Retry with different prompt or check element references         |
| `nsfw`        | Content flagged. Modify prompt, check ZH safety rules, resubmit |
| `ip_detected` | IP content detected. Modify prompt, resubmit                    |
| `canceled`    | Investigate, resubmit if appropriate                            |

---

# Stage 3: Assembly

After ALL shots are generated and approved.

## Output: assembly.json

```json
{
  "project_title": "string",
  "total_duration_sec": 62,
  "aspect_ratio": "16:9",
  "shot_order": [
    {
      "shot_number": 1,
      "file": "output/videos/shot_001.mp4",
      "duration_sec": 8,
      "transition_to_next": "cut"
    },
    {
      "shot_number": 2,
      "file": "output/videos/shot_002.mp4",
      "duration_sec": 10,
      "transition_to_next": "dissolve"
    }
  ],
  "bgm": "string or null (user's music direction)",
  "subtitle_language": "string or null",
  "subtitle_content": [
    {
      "shot_number": 1,
      "timestamp": "0:00-0:08",
      "text": "string (dialogue or narration)"
    }
  ],
  "assembly_notes": "string (any additional notes for post-production)"
}
```

## Presenting Assembly to User

```
All [N] shots generated! Here's the assembly plan:

1. shot_001.mp4 (8s) — [brief description] → [cut]
2. shot_002.mp4 (10s) — [brief description] → [dissolve]
3. shot_003.mp4 (6s) — [brief description] → [cut]
...

Total: ~[X] seconds
Music: [direction or "none"]
Subtitles: [language or "none"]

To assemble the final video, you can use ffmpeg or a video editor.
Shot files are in output/videos/ in order.
```

## ffmpeg Assembly Reference

If the user wants command-line assembly, provide:

### Simple concatenation (all cuts, no transitions):

```bash
# Create file list
for f in output/videos/shot_*.mp4; do echo "file '$f'"; done > output/filelist.txt

# Concatenate
ffmpeg -f concat -safe 0 -i output/filelist.txt -c copy output/final.mp4
```

### With crossfade transitions:

```bash
# Example: 0.5s crossfade between shot 1 and shot 2
ffmpeg -i output/videos/shot_001.mp4 -i output/videos/shot_002.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=7.5[v]" \
  -map "[v]" output/final_partial.mp4
```

### Adding background music:

```bash
ffmpeg -i output/final.mp4 -i bgm.mp3 \
  -filter_complex "[1:a]volume=0.3[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -shortest output/final_with_bgm.mp4
```

**Note:** Assembly is external to the pipeline. The CLI does not support video concatenation. These are reference commands — the user may prefer a video editing application.
