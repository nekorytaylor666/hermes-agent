# Scene Type: Action (CS3.5)

For scenes with physical conflict, pursuit, combat, stunts, kinetic spectacle.

**Dialogue in action scenes:** secondary to physical action. Compress to ≤ 15 words (multi-shot) or ≤ 8 words (single-shot). Keep only the line that triggers/escalates action — convert rest to physical behavior. Full dialogue scenes route to Dialogue Director.

---

## Scene Classification

**LINEAR** (default): Single location, cause→effect chain, chase with directional movement.
**CHAOTIC**: Multiple locations, intercut, tonal contrast between beats.
**Ambiguous → default LINEAR** (fewer spatial artifacts).

### LINEAR Mode
- Long one-take segments (Steadicam/tracking/handheld)
- Max 1–2 strategic cuts per scene (sub-second inserts don't count)
- Keep active characters in frame within segments. Character exits frame = gone for rest of segment
- Cause→effect must be explicit — never skip a link
- Scenes > 10s: **sandwich structure** — alternate one-take segments with short inserts

### CHAOTIC Mode
- Each shot = independent vignette with own angle, location, energy
- Cuts ARE the primary tool — contrast between shots IS the spectacle
- No spatial re-anchoring between shots (different locations). **Exception:** re-anchor if returning to previously shown location
- Don't re-describe character appearance across shots (character sheets handle this)
- **Rhythm:** alternate short-long (1–2s punch → 3–4s develop → 1–2s punch). Never three same-length shots in a row. End on longest or shortest — not medium
- **Energy arc:** open high → dip briefly mid-scene (breath beat — insert or wide flash) → peak higher for final

---

## Action Archetypes (10 Types)

| Archetype | Camera Focus | Space Dynamic |
|-----------|-------------|---------------|
| **Pursuit** | The GAP is the drama — every beat must visually change the distance between pursuer and pursued | Environment shapes the path, not the other way around |
| **Duel** | Lower angle on dominant side; dominance MUST alternate | Fighters trade position |
| **Standoff** | Micro-movements; camera does the work | Static space; push-in for pressure |
| **Impact** | Build-up slow → hit fast → aftermath slow | Point of contact = center |
| **Overwhelm** | Hero center, threats periphery | Hero advances through space |
| **Catastrophe** | Scale grows each beat | Space deforms |
| **Reveal** | Camera controls what viewer sees when | Hidden → exposed |
| **Escape** | Constriction → effort → release | Space tightens then opens |
| **Transformation** | Single subject, body changes | Camera orbits/pushes in |
| **Parallel** | Switching rhythm = tension | Two spaces intercut |

### Archetype Details

**Pursuit** — **the GAP is the drama.** Every beat must visually change the distance between pursuer and pursued. Describe gap with physical markers: car-lengths, strides, visible objects between them. Never use abstract "ahead in frame" alone. Pursuer visibility rule: every pursuit scene must include pursuer with physical distance marker + at least one visible detail.

**Tension source depends on environment** — four models:
- **Open space** (highway, field, rooftop): tension = exposure + endurance. Nowhere to hide, gap dynamics dominate. Camera emphasizes the shrinking/growing distance.
- **Narrow space** (alley, corridor, stairwell): tension = proximity + sound. Pursuer is close, every footstep audible. Camera tightens, walls compress the frame.
- **Vertical** (scaffolding, fire escape, cliff): tension = height + grip. One slip = fall. Camera tilts to emphasize vertical distance and precariousness.
- **Crowded** (market, station, street festival): tension = inability to sprint. Pursued weaves, pursuer loses line-of-sight. Camera tracks through bodies and obstacles.

**Space dynamic:** environment shapes the path, not the other way around — the pursued runs the shortest route, obstacles exist only where the environment naturally places them. **Max 1 physical obstacle interaction per scene** — remaining tension comes from gap dynamics, line-of-sight breaks, and near-catches.

Mandatory obstacle before reversal: previous scene must show the obstacle that forces direction change. U-turn/overtake protocol: show obstacle → show braking/reaction → show reversal on camera. First scene after reversal must re-anchor new direction, new gap, and who is closer to what landmark.

**Duel** — neither side dominates more than one consecutive beat. Every dominance shift marked by visible physical consequence on the losing fighter: stagger backward, drop to knee, lose weapon grip, get slammed into obstacle, lose ground (≥2 steps retreat). "B counterattacks" alone insufficient — describe what happens to A's body. If one side dominates throughout → it's Overwhelm, not Duel.

**Overwhelm** — each takedown must name the strike AND the impact point on opponent's body. ✅ "drives elbow into his ribs, he doubles over" ✅ "catches his arm, wrenches behind his back, drives knee into spine" ❌ "disarms and drops him" ❌ "takes him down." Hero advances THROUGH opponents — contact is the throughline.

**Reveal** — camera controls information release. Hidden → exposed progression.

**Parallel** — two separate spaces intercut. Switching rhythm builds tension.

### Archetype Decision Tree
1. Chasing / being chased? → **Pursuit** (escape focus → **Escape**)
2. Two opponents, alternating advantage? → **Duel**
3. One side dominates throughout? → **Overwhelm**
4. Tension before action, no movement? → **Standoff**
5. Single decisive contact moment? → **Impact**
6. Environment deforms / scale grows? → **Catastrophe**
7. Subject's body/state changes? → **Transformation**
8. Two separate spaces intercut? → **Parallel**
9. Hidden → exposed? → **Reveal**
10. Default → **Duel** (most versatile camera logic)

Complex scenes chain 2–3 archetypes: "clears room then standoff" = Overwhelm → Standoff.

### Archetype Deference Rule
If user prompt contains ≥3 specific action beats with described camera/spatial directions, archetype serves as FALLBACK only — fill gaps, never override what user described. Archetype fully drives scene only when user input is vague (≤2 specific beats, no camera/spatial directions).

### LOCKED Camera Style Override
When Camera Style axis is LOCKED, it overrides archetype camera behavior entirely. Archetype still defines spatial logic (distance, obstacles, position swaps, dominance shifts) but camera movement, angle vocabulary, and rig type come ONLY from the LOCKED Camera Style.

Examples: Pursuit + Classic Static = subjects run through static frame, camera stays planted on tripod with slow dolly. Distance and obstacle logic still apply, but camera never tracks. Duel + Classic Static = fighters exchange blows in master shot with slow dolly, no handheld coverage.

---

## Beat Rules

### Beat Compression
Compress to ≤ 4 beats before writing. A "beat" = one dramatic unit with one clear outcome. 1-line and 20-line inputs produce prompts of comparable structural density.

**User-beat preservation:** If user described specific beats, they are LOCKED — the skeleton. Director adds texture between them. If user beats > 4, compress by MERGING adjacent beats into dramatic units — never by DROPPING.

**Default: in medias res.** Scene already in progress. No setup, no resolution unless user explicitly requests it.

### Beat Variety Rule
Every consecutive beat must differ **qualitatively** — in obstacle type, action type, or scale. Repeating the same action collapses into a single beat.

Archetype-specific variety:
- **Pursuit/Escape** — tension source must shift between beats (gap dynamics, line-of-sight, environment change, near-catch). Max 1 physical obstacle interaction per scene — do not chain obstacle after obstacle.
- **Duel** — each exchange must differ in method and distance (not a fixed progression). Method of dominance shift must also change.
- **Overwhelm** — each opponent = different threat/dispatch method; identical opponents compress into one beat
- **Catastrophe** — each beat = qualitatively larger scale

### Action Motivation Rule
Every action must be motivated by the character's goal. Before writing any beat, ask: "Why does the character do this?" If the answer is "to fill screen time" or "it looks cool" — replace it. Obstacles must physically block the character's path. ✅ "Cargo cart rolls into his path — he vaults over it." ❌ "He collides with a cart at the pier edge" (cart wasn't blocking path).

**Test:** does removing this action break the cause→effect chain? If scene reads fine without it → it's filler.

### Obstacle Tourism Anti-Pattern (PROHIBITED)

A character never changes direction **toward** an obstacle. The pursued runs the shortest escape route; obstacles are encountered only because the environment places them in that path.

**Red flags:**
- A chain of 2+ obstacle interactions in one scene (jump fence → dodge cart → slide under barrier). This reads as a theme-park obstacle course, not a pursuit.
- Character detours toward a hazard that wasn't blocking the path.
- Obstacles appear conveniently at dramatic moments without environmental justification.

**Replace obstacle chains with gap dynamics:**
- Pursuer's hand almost reaching collar → pursued ducks at last second
- Line-of-sight breaks behind a pillar or vehicle — pursuer overshoots
- Near-miss with traffic or crowd — no physical contact, just proximity threat
- Environment naturally narrows (alley mouth, doorway) — gap compresses without obstacle interaction

**Limit:** max 1 physical obstacle interaction per scene. All remaining tension comes from distance changes, near-catches, and line-of-sight dynamics.

---

## Action Description Rules

- **Action = intent + named technique + contact point.** ✅ "spinning back kick connects with jaw" ✅ "drives elbow into ribs" ❌ "disarms and drops him" ❌ "left forearm rotates 45° to deflect" (biomechanics). If user names a specific move — preserve it and add contact point. If user gives vague action — invent named technique with contact point.
- **Force and direction, not destruction sequence.** ✅ "driven into car, metal buckling" ❌ "first floor buckles, second pancakes." For environment events: describe event + visible aftermath, not sequential physics.
- **Dominance shifts require visible physical consequence.** The losing side must visibly lose ground, balance, or control. ✅ "A staggers back two steps, sword arm dropping" ❌ "B now dominates" (no visible change on A).
- **Environmental progression:** world reacts. Dust thickens, glass cracks, smoke drifts. At least one progressive change per beat.
- **Reference images showing action = mid-action.** Not a starting pose (unless user says "start from this image").

---

## Cut Rules

### 1. Double Contrast (mandatory)
Every cut changes BOTH shot size AND camera character.
Shot-size scale: extreme wide → wide → medium → medium close-up → close-up → ECU.
Camera modes: Handheld | Static/locked-off | Stabilized tracking | Crane/vertical — never repeat across a cut.

### 2. Re-anchoring and 180° Rule
After every cut (not inserts), first sentence must contain three spatial markers:
1. **Who-where:** which character at which landmark/side
2. **Facing direction:** which way each moves/faces
3. **Relative position:** who ahead/behind, closer/farther

180° rule: left-to-right before cut → same after. State movement direction explicitly.

### 3. Inserts
Sub-second (0.3–0.5s) dramatic punctuation. Any shot size.

**Conflict-motivated (mandatory).** Every insert must: (a) show visible consequence of conflict, (b) show reaction to action, or (c) reveal new information. If none → cut it.

**Anti-patterns (never use):**
- Generic body-part closeups without conflict context: boots on ground, hands gripping straps, fists clenching in air, feet in puddles — in ANY variation
- Isolated object details not participating in conflict
- **Test:** remove insert mentally. If scene reads identically → no function.

**Good examples by archetype:**
- Pursuit: bystander hitting ground while hero sprints past (consequence). Wide flash showing distance to goal (information).
- Duel: opponent's face at impact — pain, loss of control (reaction). Weapon skittering across floor (consequence).
- Overwhelm: bystander reacting to violence (reaction). Last opponent's hesitation seeing allies down (information).
- Standoff: finger tightening on trigger (escalation). Sweat on active conflict element (tension).

### 4. Shot Timing
Scene labels: `Scene N (Xs–Ys):`. Timestamps cover full duration without gaps/overlaps. Shorter scenes = tighter prose, longer = more detail.

### 5. Position Swap Protocol
When characters trade spatial roles (who leads/follows, who is left/right):
- **Show cause on camera.** The action causing swap must be visible. Seedance cannot infer.
- **One swap per segment.** Multiple → separate across segments.
- **Re-anchor immediately.** First sentence after cut names new positions using landmarks. ✅ "A now at far door, B at entrance." ❌ "They've switched places."
- **Single-shot swap:** camera tracks the character who initiates through the transition.

---

## Vehicle Rules
Vehicle U-turns cannot be rendered as continuous motion — Seedance teleports. **Workaround:** Scene N ends with braking at obstacle. Scene N+1 opens with vehicle already facing new direction, stated in re-anchor. Never describe the rotation itself. Preferred alternatives: reverse in straight line, swerve around obstacle, take side street.

---

## Single-Shot Mode

Entire scene = one continuous camera move, zero cuts.

**Conversion strategies (priority order):**
1. **Spatial layering** — action at different depths (foreground, midground, background). Camera reveals each layer progressively.
2. **Temporal chaining** — beats happen sequentially as camera follows character through space (plan-séquence).
3. **Camera as edit** — camera speed/direction changes replace cuts. Whip-pan, push-in→hold→pan = multiple beats, zero cuts.
4. **Environmental progression** — visible changes mark transitions (dust, fire, weather, light).

**Limits:** ≤ 4 beats, ≤ 4 parallel elements, ≤ 3 characters, ≤ 8 dialogue words. Density: ≤ 6 sentences for ≤10s, ≤ 8 for 11–15s. Temporal markers only — no scene labels.

---

## Shot Density (Multi-Shot)

**CHAOTIC:** ≤6s: 2–3 shots | 7–10s: 3–5 | 11–12s: 5–8 | 13–15s: 6–10
**LINEAR:** ≤6s: 1–2 seg, 0 inserts | 7–10s: 2–3 seg, 0–1 ins | 11–12s: 2–3 seg, 1–2 ins | 13–15s: 3–4 seg, 2–3 ins

Principle: every 3s above 10s → +1 edit point. No shot > ~4s screen time.

---

## Genre Modifiers

| Genre | Tempo & Cuts | Camera | Palette & Light | Sound |
|-------|-------------|--------|-----------------|-------|
| Action | Fast, whip-pans on transfers | Handheld, dynamic tracking | High contrast, harsh side-light | Impact SFX, low-end drone, silence before hit |
| Horror | Slow, rare significant cuts | Static wide, empty space, slow push-in | Practical only, half-shadow, flicker | Ambient unease, atonal drone |
| Comedy | Follows timing: setup normal, payoff hold | Wider, static holds, cut for reaction | Bright, flat, even, faces readable | Exaggerated foley, silence before punchline |
| Noir | Medium, cuts on power shifts | Low-angle dominant, Dutch on compromise | Chiaroscuro, hard through blinds, neon | Jazz, rain, urban night |
| Epic | Slow, ceremonial | Crane, aerial, extreme wides, low-angle authority | Volumetric God rays, firelight, saturated | Orchestral, room reverb, distant weather |
| Drama | Deliberate, each cut has weight | Close, shallow DOF, subtle dolly, eye-level | Naturalistic soft light, single source | Room tone, breathing, solo instrument |

If no genre (AUTO): do not apply genre table — camera, tempo, palette determined by archetype alone.

---

## Overflow Compression

**Tier 1 — UNTOUCHABLE (never cut):**
- The climactic beat (most important visual moment)
- The power-shift line (dialogue where dominance flips)
- Setup that makes climax legible

**Tier 2 — Keep if space allows:**
- Character establishment
- Environmental setup
- Secondary reactions

**Tier 3 — Trim first:**
- Repeated similar actions → merge ("overwhelms guards")
- Transitional beats (walking, opening doors)
- Reaction beats convertible to visual subtext
- Redundant dialogue restating what body language shows

Rules: merge, don't delete. Never split into multiple scenes. Final: ≤ 4 beats, ≤ 15s, ≤ 3 chars/shot. Compression is silent.

---

## Hidden Objects
Seedance cannot render "hidden" objects. If object is narratively hidden: dedicate one ECU scene to showing it explicitly (hand gripping pistol under table edge). In subsequent scenes, reference ONLY through body language (white knuckles, rigid forearm). If no room for reveal scene, describe physical effect on character's posture.

---

## Speed Ramps
Optional artistic tool — director may use slow motion, speed ramp, or freeze frame at emotional peak (not physical peak). Maximum one per scene. Weave into Dynamic Description as temporal directive in prose, not metadata. Must not conflict with LOCKED Camera Style.
