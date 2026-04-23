# Producer Guide (CS3.5)

The Producer is a creative advisor role for building and refining video generation inputs. This reference captures key concepts useful when operating in an advisory capacity.

---

## Session Lock

When working on a project (single or multi-clip), establish a Session Lock — constant parameters across all generations to prevent visual style jumping.

### LOCKED for entire session (set once):

| Parameter | What | Why |
|-----------|------|-----|
| Camera Style | Movement preset or custom | Movement vocabulary must be consistent across clips |
| Light Style | Lighting preset or custom | Light direction/quality is the visual thread |
| Color Style | Color grade preset or custom | Most noticeable discontinuity if it jumps |
| Camera Body | Body preset | Grain/sensor character must match |
| Lens | Lens preset | Optical rendering must match |

### PER-CLIP variables (change freely):

| Parameter | Rule |
|-----------|------|
| Genre | May shift within sequence (drama→action→drama) |
| Focal Length | Multi-shot: auto (Director picks). Single-shot: set specific |
| Aperture | Same as focal length: auto for multi-shot, specific for single-shot |
| global_prompt | Different content per clip |
| Duration | Clip length may vary |

### Changing the lock mid-session
Only with explicit user intent. Warn: "This breaks visual continuity with previous clips."

---

## Prompt Writing Guidelines

When writing scene descriptions (global_prompt / user_prompt):

- **Concrete visuals only** — who, where, doing what, wearing what, what changes
- **No emotion labels** — "angry" → "jaw clenches, fists tighten"
- **No metaphors** — "the city breathes" → "steam rises from grates, traffic flows"
- **≤5 named characters** — each with unique visual anchor (wardrobe color, silhouette, accessory)
- **Explicit positions** — state character positions and movement direction
- **Key dialogue lines** — include them, mark the power-shift moment
- **Account for limits** — beat count, character count, duration-complexity relationship
- **English only** — prompts always in English. Dialogue defaults English unless user requests otherwise

---

## Visual Review Framework

When analyzing generation results:

### 1. Intent Match
Characters (count, appearance, position), location (geometry, mood), action (what's happening), camera (angle, movement), mood (color, lighting).

### 2. Technical Quality
Artifacts (merged faces, extra limbs, broken hands), composition (framing, rule of thirds, depth), continuity (consistent appearance, spatial relationships), camera style registration.

### 3. Preset Effectiveness
Did Camera Style movement register? Did Light preset scheme appear? Is Color grade uniform? Are Lens optical characteristics visible?

### 4. Common Fixes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Camera moves when should be static | Missing negatives | Add "no handheld, no tracking" to Negative |
| Characters don't match refs | Improper anchoring | Use <<<image_N>>> tags, describe on first mention |
| Color grade patchy | Free-form color description | Use preset string instead |
| Scene feels slow/empty | Duration too long for content | Reduce duration or add beats |
| Characters look same | Too many, no distinct wardrobe | Reduce to ≤3/shot, unique visual anchors |
| Character teleports | Missing re-anchor | Each shot needs explicit positions + facing |

---

## Duration-Complexity Guide

| Duration | Recommended |
|----------|------------|
| 1–5s | 1–2 beats, establishing shot |
| 6–10s | 2–4 beats, one scene development |
| 11–15s | 3–4 beats, full arc, multi-shot |

Most common failure: complex multi-character scenes at 15s. Fix: fewer characters, fewer beats, or split into 2 clips.

---

## Seedance Pitfalls to Catch Before Generation

- >3 characters per shot → identity confusion
- Reflections (mirrors, water, glass) → character duplication
- Vehicle U-turns → teleportation (split across two shots)
- "Slowly orbits while zooming in" → compound camera instructions confuse engine (pick ONE move per shot)
- Film titles in prompts → may trigger content filters. Use director names only
- Abstract descriptions → ignored. Must be concrete visuals
- >4000 characters → truncated

---

## Multi-Clip Sequence Planning

When building a sequence of clips:
1. Establish Session Lock on first clip — holds for all
2. Plan narrative arc: emotional trajectory across clips
3. End-to-start continuity: each clip opens matching previous clip's ending (spatial position, emotional state, energy level)
4. Genre can shift between clips (drama→action→drama) — this controls tempo, not visual identity
5. All prompts delivered at once when possible, not drip-fed clip by clip
