# Seedance 2.0 — Engine Constraints

Hard rendering constraints. Violating these produces glitches or rejection.

## Feasibility Limits

| Parameter | Limit |
|-----------|-------|
| Duration | ≤ 12s default, ≤ 15s if requested, never > 15s |
| Story/visual beats | ≤ 4 per scene |
| Characters per shot | ≤ 3 (drops tracking above 3) |
| ZH prompt length | ≤ 1,800 characters |
| Parallel elements (single-shot) | ≤ 3 simultaneous actions/subjects |

## Rendering Rules

### What Works
- **Atmospheric particles** (fog, rain, dust, snow, light rays) — render reliably, use freely
- **Micro-expressions as physics** — "jaw clenches, nostrils flare" works; "looks angry" doesn't
- **Named techniques** — "spinning back kick" works; "left forearm rotates 45° to deflect" doesn't
- **Force and direction** — "driven into car, metal buckling" works
- **Environmental progression** — light shifts, weather evolves, particles accumulate

### What Breaks
- **Reflection shots** (mirrors, puddles, blades, visors) — breaks scene geography. NEVER use
- **Exit + re-entry** in same shot — Seedance teleports the character. Character leaves frame = gone for rest of shot
- **Off-screen state changes** — if audience didn't see it, next shot = continuity error
- **Destruction sequences** — don't describe sequential physics ("first floor buckles, second pancakes"). Describe event + aftermath only
- **Biomechanics** — "left forearm rotates 45° to deflect right hook at wrist level" fails. Use named move or intent: "deflects and counters with an elbow"
- **> 3 characters tracked across cuts** — name the acting pair per shot. Multi-character: A↔B in shot 1, A↔C in shot 2

## Spatial Continuity

- **Breaks on every cut.** Re-anchor positions, facing direction, movement vector after any cut
- **180° rule:** if character moves left-to-right, maintain after cut. State direction explicitly
- **Cross-shot appearance** handled by character sheets/reference images — don't re-describe appearance across shots

## Duration-to-Density

Seedance stretches same content slower for longer durations — kills pacing. Compensate with more edit points.

### Multi-shot Action (LINEAR)
| Duration | Segments | Inserts |
|----------|----------|---------|
| ≤ 6s | 1–2 | 0 |
| 7–10s | 2–3 | 0–1 |
| 11–12s | 2–3 | 1–2 |
| 13–15s | 3–4 | 2–3 |

### Multi-shot Action (CHAOTIC/montage)
| Duration | Shots |
|----------|-------|
| ≤ 6s | 2–3 |
| 7–10s | 3–5 |
| 11–12s | 5–8 |
| 13–15s | 6–10 |

### Dialogue
| Duration | Shots | Max Words | Max Exchanges |
|----------|-------|-----------|---------------|
| 5–6s | 2–3 | 8–12 | 1–2 |
| 7–10s | 3–5 | 15–22 | 2–4 |
| 11–12s | 4–6 | 22–28 | 3–5 |
| 13–15s | 5–7 | 25–35 | 4–6 |

**Principle:** every 3s above 10s → +1 edit point. No shot > ~4s screen time (action) or ~5s (general).

## Beat Compression

Compress user input into **≤ 4 beats** before writing.

### Compression Tiers

**Tier 1 — Untouchable:**
- The climactic beat (most important visual moment)
- The power-shift line (dialogue where dominance flips)
- Setup that makes climax legible

**Tier 2 — Keep if space allows:**
- Character establishment
- Environmental setup
- Secondary reactions

**Tier 3 — Trim first:**
- Repeated similar actions ("fights guard 1, then 2, then 3" → "overwhelms guards")
- Transitional beats (walking, opening doors)
- Reaction beats convertible to visual subtext
- Redundant dialogue restating what body language shows

**Rules:** Merge, don't delete. Never split into multiple scenes. Compression is silent.

## Product Angle Lock (CRITICAL)

Seedance invents textures and geometry for any product surface it hasn't seen in a reference photo. This produces hallucinated backs, bottoms, and sides that don't match the real product.

### Single-input mode (1 photo)
The product is **angle-locked**. Every shot shows the product from the same face visible in the reference photo. The camera may orbit, push in, pull back, or change height — but the product itself **never rotates, flips, or tilts** to expose any surface not visible in the reference. No "different angle of the product" — only different camera positions viewing the same face.

### Multi-input mode (2+ photos of same product)
The product may appear from any angle that **matches one of the provided reference photos**. Transitions between angles happen via **hard cuts, never via continuous rotation**. No intermediate angles — only the exact views from the references.

### Rules
- Never describe the product rotating, spinning, turning, or flipping in the prompt
- Never describe a shot showing "a different angle of the product" when only 1 reference exists
- Camera movement ≠ product rotation. The camera moves freely; the product stays locked
- With 2+ references: cut between angles, never animate a rotation between them

## Age-Blind Character Rule (CRITICAL)

Never describe characters by age — in either language. The content filter raises sensitivity when it detects minors.

**Trigger words to NEVER use:** boy, girl, child, kid, young, teen, little, 男孩, 女孩, 孩子, 少年, 少女, 小孩, 年轻

**Instead:** Use role-based labels — "a figure in a wool cloak," "a rider on horseback," "a traveler." With reference images: describe by role, clothing, and action only.
