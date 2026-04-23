# Seedance 2.0 — Prompt Structure (CS3.5)

## Output Format

The final prompt is a **single continuous string** with inline section labels. No markdown, no line-break formatting. Output as a JSON object: `{"prompt":"..."}`.

Prompt hard cap: **4000 characters.** If over budget, trim in order: Narrative Summary → Static Description → Style & Mood (1 sentence min) → Dynamic Description (never cut entirely).

---

## Section Order

```
1. Camera Settings
2. Camera Style
3. Light
4. Style & Mood
5. Narrative Summary
6. Starting Composition
7. Dynamic Description
8. Static Description
9. Negative
```

All sections are inline labels within one continuous string. Example skeleton:

```
Camera: [body + lens + rendering + focal + aperture]. Camera Style: [axis]. Light: [axis]. Style & Mood: [color + genre texture + atmosphere]. Narrative Summary: [1 sentence]. Starting Composition: [first frame lock]. Scene 1 (0–4s): [description]. → Hard cut. Scene 2 (4–8s): [description]. Static Description: [location, props, ambient]. Negative: [all constraints].
```

---

## Section Details

### 1. Camera Settings

Raw `camera_settings` string copied as-is when provided. When null — director generates: `"Camera: [Body], [Lens] | [Rendering] | [focal_length], f/[aperture]"`.

See `.claude/skills/video-skill/references/camera-type.md` for preset strings, parsing rules, and injection details.

### 2. Camera Style

Inject full Camera Style axis string. When LOCKED (string) — as-is. When null — director selects from Auto Fallback and states the choice.

Format: `Camera Style: [full preset or custom string]`

See `.claude/skills/video-skill/references/style-system.md` for presets, custom style templates, and fallback tables.

### 3. Light

Inject full Light Style axis string. When LOCKED — as-is. When null — director selects.

Format: `Light: [full preset or custom string]`

See `.claude/skills/video-skill/references/style-system.md` for presets and rules. Key rule: **describe sources, not effects** — name what emits light and where, never describe light effects on surfaces.

### 4. Style & Mood

Color axis integrated here + genre texture + atmosphere. **Never skip.** Even when genre is AUTO, provide at least 1 sentence of visual atmosphere.

Format: `Style & Mood: [color grade + atmosphere + texture]`

2–3 sentences. Color Style preset string (or custom) goes here. Film stock references belong here.

### 5. Narrative Summary

One sentence: who, what conflict, what stakes. Safe terms only.

Format: `Narrative Summary: [sentence]`

### 6. Starting Composition (MANDATORY)

First frame lock — exactly what Seedance renders in frame 0, before any action or dialogue begins. Without this, Seedance invents random positions that conflict with Scene 1.

Format: `Starting Composition: [camera position, distance, angle, character positions with wardrobe, facing direction, prop positions, lighting on faces]`

**Must contain:**
- Camera position and angle (distance in feet, eye-level/low/high)
- Each character's position in frame (frame-left/right/center, foreground/midground/background)
- Each character's wardrobe and visual anchor (on first appearance)
- Facing direction and spatial relationship between characters
- Key props and their positions

Example: `Starting Composition: Camera 10 feet from desk, eye-level, wide shot. A figure in a dark suit (Detective) frame-left in wooden chair facing a figure in a wrinkled shirt (Suspect) frame-right. Mahogany desk between them. Single desk lamp illuminates the suspect's face from above-left. Detective's face half-shadowed.`

### 7. Dynamic Description

Scene-by-scene action with dialogue woven in. Present tense, active voice.

#### Multi-shot format

Numbered scene labels with timestamps and transition markers:

```
Scene 1 (0–4s): [shot size + camera mode]. [Spatial anchor: who-where + facing]. [Action]. → Hard cut.
Scene 2 (4–8s): [shot size + camera mode]. [Spatial anchor]. [Action]. → Smash cut.
Scene 3 (8–12s): [shot size + camera mode]. [Spatial anchor]. [Action + resolution].
```

**Scene 1 Grounding Rule (MANDATORY):** The first 1–2 sentences of Scene 1 must mention at least 2 key environmental elements from Starting Composition, integrated into the action — not listed, but woven into the character's movement or camera behavior.

✅ "Fugitive sprints between parked cars lining the narrow street, neon signs streaking pink reflections across rain-hammered asphalt" — environment (parked cars, neon signs, rain on asphalt) is part of the action.

❌ "Fugitive sprints toward camera, arms pumping, rain spraying off shoulders" — generic running with no environment anchoring. Starting Composition elements are absent.

This ensures visual continuity between the static first frame (Starting Composition) and the first moment of motion.

**Scene label rules:**
- Timestamps cover full duration without gaps or overlaps
- Last scene has NO transition marker
- Transition types: `Hard cut`, `Smash cut`, `Match cut`, `Whip-pan transition`, `Cut on [action]`

**Spatial anchor (mandatory):** first sentence of each scene states character positions and facing/movement direction. After cuts: re-anchor who is where, which direction they face, relative positions.

#### Single-shot format

Temporal markers only — no scene labels, no `→` transitions:

```
(0–3s) Camera tracks left as... (3–6s) The figure pauses, turns... (6–10s) Slow push-in reveals...
```

Density cap: ≤ 6 sentences for ≤10s, ≤ 8 sentences for 11–15s.

#### Dialogue integration (when scene contains dialogue)

Dialogue is woven directly into Dynamic Description with voice descriptors:

```
A leans forward, jaw tight, voice low and controlled: 'The money never reached the account.' — B steps back, breath catching, hands raised...
```

Rules:
- Voice descriptor before quoted line: "voice low:", "barely audible:", "sharp, cutting:"
- Physical action wraps around dialogue: action before line, reaction after
- User-provided dialogue is UNTOUCHABLE — never rewrite, soften, or translate
- Preserve original language of dialogue lines verbatim

#### Sound design integration

**General / Action scenes:** sound design is mandatory — include ambient + detail sounds + intensity guidance within or after Dynamic Description. Exception: user requests "no sound."

**Dialogue scenes:** sound design only if user explicitly requests it. Default: SFX only (foley, ambient). No music unless specified.

### 8. Static Description

Location, props, ambient details. Establish everything referenced in Dynamic Description. One sentence on how the space reinforces the scene's mood.

Format: `Static Description: [location geometry, surfaces, props, light sources, atmosphere]`

### 9. Negative

All "no X" constraints collected and deduplicated from: Camera Style axis, Light axis, Color axis, camera_settings, and user prompt. Mandatory — always present.

Format: `Negative: [comma-separated list of negations].`

Assembly order:
1. Extract "no X" from Camera Style
2. Extract "no X" from Light
3. Extract "no X" from Color
4. Extract "no X" from camera_settings
5. Add user's SACRED negation constraints
6. Deduplicate
7. Single comma-separated block

---

## Density Caps

### Per-scene limits

- Multi-shot: ≤ 4 sentences per scene (1 spatial anchor + 1–2 action + 1 camera/transition)
- Insert: 1 sentence
- Single-shot temporal block: ≤ 3 sentences

### Total Dynamic Description by duration

| Duration | Total Sentences |
|----------|----------------|
| ≤ 10s | 4–8 |
| 11–12s | 6–10 |
| 13–15s | 8–14 |

Single-shot: ≤ 6 sentences for ≤10s, ≤ 8 for 11–15s.

---

## Image Reference System

When user provides reference images, prepend a legend before the first section label:

```
<<<image_1>>> — a figure in tactical armor. <<<image_2>>> — an industrial warehouse.
Camera: ...
```

In body, use descriptive label with `(<<<image_n>>>)` on first mention, then descriptive label only:

```
The armored figure (<<<image_1>>>) charges through the warehouse (<<<image_2>>>)...
```

### Material Reference System (higgsfieldcli)

| Syntax | Range |
|--------|-------|
| `@Image1` – `@Image9` | Up to 9 reference images |
| `@Video1` – `@Video3` | Up to 3 reference videos (2–15s total) |

- Label every `@` reference's purpose in the prompt
- Arrange ImageList/VideoList in same order as `@` references
- When modifying existing video, pass it in VideoList
- Map `<<<image_1>>>` to `@Image1`, `<<<image_2>>>` to `@Image2`, etc.

---

## Antislop — Never Use These Words

These waste Seedance's attention budget. Remove without replacement:

breathtaking, stunning, captivating, mesmerizing, awe-inspiring, masterfully, meticulously, exquisitely, beautifully crafted, cinematic masterpiece, visual feast, a symphony of, seamlessly, effortlessly, flawlessly, cutting-edge, state-of-the-art, next-level, rich tapestry, vibrant tapestry, kaleidoscope of, elevate, unlock, unleash, harness, groundbreaking, a testament to, speaks volumes, resonates deeply

---

## Language Rules

- **Prompts are always in English.** All section content in English regardless of user's language.
- **Dialogue defaults to English.** Other language only on explicit user request — write dialogue lines in that language, everything else stays English.
- Present tense, active voice.
- Vivid but economical. No poetic padding.
- Consistent character names. Unnamed → functional labels ("a figure in dark clothing").
- No emotion labels — describe physical manifestation ("jaw clenches" not "looks angry").
- No metadata headers in prose (no "[Camera Movement]" labels).
- Direct output — full creative intensity, no euphemisms.

---

## Complete Prompt Example (General scene, Journey archetype, 12s, multi-shot)

```json
{"prompt":"Camera: ARRI Alexa 35, Cooke S7/i Full Frame | Cooke S7/i rendering — warm organic tone, gentle halation on highlights, smooth bokeh with swirling edges | 35, f/2.8. Camera Style: Cinematographic style of Roger Deakins — measured stillness, gravity in every frame, single slow reframe pan ≤5°, tripod-locked with imperceptible weight shifts, no handheld, no crane, no snap movement. Light: Only natural daylight, golden hour side-light from frame-left, long shadows stretching across terrain, warm rim on elevated surfaces, cool fill in valleys, no fill light, no bounce, no artificial sources. Style & Mood: Kodak Vision3 250D daylight stock, warm amber in highlights, muted sage in shadows, grain visible in sky gradients. Solitary journey through geological time. Dust and distance. Narrative Summary: A lone traveler crosses a vast canyon at golden hour, dwarfed by layered rock formations. Starting Composition: Camera at eye level on tripod, 35mm wide shot. A figure in a dark coat and wide-brimmed hat enters frame-right at midground depth, walking left-to-right along a narrow ridge trail. Foreground: dry scrub brush and cracked red earth. Midground: the ridge trail curving along canyon wall. Background: layered sandstone formations glowing amber, deep canyon below filled with blue shadow. Scene 1 (0–4s): 35mm, eye-level, static tripod. The traveler moves steadily left-to-right along the ridge, coat catching wind. Dust lifts from each footfall, suspended in side-light. Shadow stretches three body-lengths across red earth. Canyon depth visible below — blue haze softening the far wall. Ambient: wind across rock faces, gravel under boots. → Hard cut. Scene 2 (4–8s): 24mm, low-angle, static locked. Camera planted at trail level. Boots cross frame in foreground, each step grinding loose gravel. Behind and below: canyon opens into full depth — horizontal strata of ochre, rust, pale cream catching last direct light. A hawk circles in middle distance, wings fixed. → Hard cut. Scene 3 (8–12s): 85mm, telephoto, slow reframe pan 3° right. Compressed perspective flattens the traveler against canyon wall behind. Figure small — quarter of frame height. Layered rock fills the rest: warm light on upper strata fading to cool shadow below. Wind moves coat hem. Traveler pauses, turns head toward canyon, holds gaze two seconds. Light drops as sun touches horizon. Distant hawk cry. Static Description: Desert canyon system, layered sandstone walls 200 meters deep, narrow ridge trail along western rim, dry scrub vegetation, no structures, no other people. Wind steady 15mph carrying fine red dust. Golden hour transitioning to dusk. Negative: no handheld, no crane, no snap movement, no people other than the traveler, no music, no dialogue, no text overlay."}
```
