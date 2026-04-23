# Scene Type: General (CS3.5)

For scenes without combat or dialogue: landscapes, journeys, atmospheric shots, transformations, montages, scale. Characters present only as subjects within environment (walking, observing — not fighting, not speaking).

---

## Scene Classification

**CONTINUOUS** (default): Single location or continuous journey, smooth spatial flow.
**MONTAGE**: Multiple locations, time jumps, thematic collage.
**Ambiguous → CONTINUOUS.**

### CONTINUOUS Mode
- Long tracking/crane/aerial segments
- Max 1–2 strategic cuts. Camera IS the narrator
- Environmental progression: light shifts, weather evolves, particles accumulate
- Camera relationship to character = emotional distance

### MONTAGE Mode
- Cuts = primary tool. Contrast and rhythm between shots IS the content
- Visual rhyming: match shapes, colors, movement directions across cuts
- No spatial re-anchoring between shots (different locations/times)

### Sub-Classification
- **CHARACTER-DRIVEN**: camera distance = emotional tone. Close = intimacy, far = isolation.
- **CAMERA-TECHNICAL**: camera itself IS the intent (drone shot, crane reveal). Camera direction is SACRED.
- **ENVIRONMENT-DRIVEN**: space IS the subject. Character secondary or absent.

---

## Archetypes (6 Types)

| Archetype | What Changes | Camera Signature | Time Dynamic |
|-----------|-------------|-----------------|-------------|
| **Reveal** | Hidden → visible | Pan, crane, dolly reveal. Camera controls WHEN viewer sees | Slow build → disclosure |
| **Journey** | Position in space | Tracking, aerial, traveling alongside | Steady momentum, gradual shifts |
| **Atmosphere** | Nothing — mood IS content | Minimal movement, slow push-in or static. Micro-changes carry drama | Near-still |
| **Transformation** | State change (day→night, season) | Match cuts between states, or slow continuous change | Time compressed |
| **Montage** | Theme through variety | Rapid cuts, visual rhyming (shape/color/movement match) | Rhythmic, cuts = music |
| **Scale** | Size perception | Extreme wide, vertical crane, macro-to-wide, drone ascending | Expansion or contraction |

### Decision Tree
1. Hidden → visible? → **Reveal**
2. Subject moves through space? → **Journey**
3. State changes over time? → **Transformation**
4. Multiple locations/times? → **Montage**
5. About scale/vastness? → **Scale**
6. Nothing changes, mood IS content? → **Atmosphere**
7. Default → **Atmosphere**

### LOCKED Camera Style Override
When Camera Style is LOCKED, it overrides archetype camera behavior. Archetype defines spatial logic (what changes, where subjects are), but movement/angle/rig come ONLY from LOCKED style.

---

## Beat Compression

Compress to ≤ 4 visual beats. A "beat" = one visual unit with one clear subject or transformation.

Default: peak moment. "A forest" → dramatic light with depth, not empty establishing shot. Override for Atmosphere (peaks through subtlety).

User-described specific beats are LOCKED — merge if > 4, never drop.

---

## Environmental Progression (CRITICAL)

Primary tool for visual interest. For ≥ 3 beats: at least one progressive change per beat.

- **Light:** sun angle, cloud shadow, golden hour, artificial on/off
- **Weather:** rain intensifying, fog lifting, wind, snow beginning
- **Atmosphere:** dust thickening, smoke drifting, mist settling, haze clearing
- **Activity:** traffic increasing, birds scattering, water rising, tide changing

For ≤ 2 beats or Atmosphere archetype: micro-changes sufficient (flame flicker, light drift).

---

## Cut Rules (Multi-Shot)

### Double Contrast (mandatory)
Every cut changes BOTH shot size AND camera mode.
Shot-size scale: extreme wide → wide → medium → medium close-up → close-up → ECU.
Camera modes: Static | Tracking | Crane | Aerial | Dolly — never repeat across a cut.

### Re-anchoring
After cuts: re-anchor spatial relationships, positions, lighting direction.

### Inserts
0.3–0.5s, beat-free, distinct subject. Max one per beat.

### Shot Timing
| Duration | Type | Max |
|----------|------|-----|
| < 1s | Insert | punctuation |
| 1–2s | Compressed | energy |
| 2–4s | Normal | development |
| 4–6s | Peak | absorption |
| 6+s | Extended | contemplation |

Never three same-duration shots in a row.

---

## Shot Density (Multi-Shot)

### MONTAGE
| Duration | Shots |
|----------|-------|
| ≤6s | 2–3 |
| 7–10s | 3–5 |
| 11–12s | 4–6 |
| 13–15s | 5–8 |

### CONTINUOUS
| Duration | Segments | Inserts |
|----------|----------|---------|
| ≤6s | 1 | 0 |
| 7–10s | 1–2 | 0–1 |
| 11–12s | 2–3 | 1 |
| 13–15s | 2–3 | 1–2 |

---

## Single-Shot Mode

Triggered by: shot_count=1, "one-take"/"single shot"/"no cuts"/"oner" in prompt, or One Take camera preset.

**Conversion strategies (priority order):**
1. **Spatial layering** — beats at different depths, camera reveals each
2. **Temporal chaining** — sequential in one take
3. **Camera as edit** — motion changes as transitions (whip-pan, speed change)
4. **Light/atmosphere as beat** — environmental progression marks phases

**Limits:** ≤ 4 beats, ≤ 4 parallel elements, ≤ 3 characters. Temporal markers only — no scene labels. Density: ≤ 6 sentences for ≤10s, ≤ 8 for 11–15s.

---

## Sound Design (Mandatory)

Every prompt includes ambient + detail sounds + intensity guidance. Exception: user requests "no sound."

Structure: primary ambient layer + secondary detail sounds + rhythm/intensity note.

Examples:
- "Ambient: wind across rock faces, gravel under boots. Detail: distant hawk cry. Intensity: builds as light fades."
- "Ambient: rain on leaves, thunder distant. Detail: drip from eave, branch creak. Intensity: steady, enveloping."

---

## Depth Layering

Every wide shot must have at least 3 depth layers:
1. **Foreground** — frame element, texture, blur
2. **Midground** — subject
3. **Background** — context, environment

---

## Rules

- **Only describe what's visible/audible.** ❌ "The air smells of pine." ✅ "Pine needles on ground, wind through branches."
- **Timelapse = explicit visual transition.** "Day → night" must be continuous light change or match cuts — not abstract skip
- **Characters described as user specifies** — wardrobe + appearance + action. ≤ 5 named per scene, ≤ 3 per shot
- **Character sheets** (multi-angle/neutral BG): extract character only. Sheet background is NOT a location reference
- **Reference images showing motion** = mid-scene snapshot, not starting pose (unless user says "start from this image")
- **Particles** (fog, rain, dust, snow, light rays) render reliably — use freely

---

## Genre Modifiers

| Genre | Tempo | Camera | Palette | Sound |
|-------|-------|--------|---------|-------|
| Epic | Slow, ceremonial | Crane, aerial, extreme wides, volumetric light | God rays, golden hour, rich saturated | Orchestral, wind, reverb |
| Horror | Slow, restricted | Static wide + empty space, slow creep | Practical only, half-shadow, flicker | Ambient hum, creak, silence |
| Drama | Contemplative, minimal cuts | Close, shallow DOF, gentle dolly | Naturalistic soft, single source | Room tone, silence, solo instrument |
| Comedy | Observational stillness | Busy backgrounds, static wide holds | Bright, flat, even | Detail foley, music cue |
| Noir | Medium, deliberate | Low angles, hard shadow geometry | Chiaroscuro, wet surfaces, neon | Jazz, rain, urban night |
| Action | Kinetic, rapid cuts, particles | Dynamic tracking, wide establishing | High contrast, harsh side-light | Impact SFX, drone |

If no genre (AUTO): infer from content.

---

## Overflow Compression

**Tier 1 — UNTOUCHABLE:** climactic beat + setup that makes climax legible.
**Tier 2 — Keep if space:** character establishment, environmental setup, secondary reactions.
**Tier 3 — Trim first:** repeated similar images, transitional beats, redundant angles.

Rules: merge, don't delete. Always compress into one scene, never split. Compression is silent. Single-shot overflow: beats → spatial layers or temporal phases. Parallel elements cap ≤ 4.
