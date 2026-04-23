# Continuity Rules

Cross-cutting rules for maintaining visual and narrative consistency across all shots. Read this file from Stage 1 onward.

## Character Description Registry

### Purpose

Video prompts must describe characters by physical appearance, NEVER by name. This registry ensures the same character is described consistently across every shot.

### Building the Registry

After Stage 0 (requirements capture), build the registry from `requirements.json.content.characters`:

For each character, derive two description forms:

| Form | Length | When to use | Example |
|---|---|---|---|
| Full description | 8–10 words | First mention in a shot's prompt | "a tall woman in a dark coat with cropped silver hair" |
| Shorthand | 3–4 words | Subsequent mentions in same prompt | "the silver-haired woman" |

### Rules

- The **full description** is based on `image_prompt` but written as natural prose, not a keyword list.
- The **shorthand** picks the most visually distinctive trait (hair color, clothing, build).
- The SAME full description and SAME shorthand are used across ALL shots for that character.
- If a character changes clothing or appearance mid-video (per storyboard), create a new full description for shots after the change. Note the change point.
- Never use character names. Not in any prompt. Not even as part of a longer phrase.

### Registry Format

```
Character Registry:
  [CharacterName]:
    full: "a tall woman in a dark coat with cropped silver hair"
    short: "the silver-haired woman"
    media_id: abc123
    masked: true

  [CharacterName2]:
    full: "a young man in a wrinkled linen shirt with dark curly hair and glasses"
    short: "the curly-haired man"
    media_id: def456
    masked: true
```

## Style Tag Consistency

A single `style_tag` is defined in `storyboard.json`, derived from `requirements.json.style.visual_style_tag`.

- This tag is prepended to EVERY shot's video prompt as the `Style & Mood:` section.
- It ensures visual coherence across all shots: same color palette, same lighting feel, same lens aesthetic.
- The style tag should contain filmmaking terms: lens type, lighting quality, color grading, film stock, atmosphere.
- Example: `"Style & Mood: Anamorphic 35mm, warm golden hour tones, soft naturalistic lighting, shallow depth of field, gentle film grain."`

**Never change the style tag between shots unless the storyboard explicitly calls for a style shift (e.g., flashback sequence).**

## Cross-Shot Overlap

### Visual Continuity Between Consecutive Shots

Shot N+1 must begin from the exact visual state where shot N ends:

- **Character positions:** If shot N ends with a character standing at a window, shot N+1 opens with them at the window.
- **Clothing state:** If a character's jacket is off in shot N, it's off in shot N+1 (unless the storyboard says they put it back on).
- **Facial state / emotion:** If shot N ends with a character smiling, shot N+1 opens with the same expression (unless the cut implies time passage).
- **Lighting:** If shot N is dusk, shot N+1 at the same location is also dusk (unless time jump).
- **Props:** If a character is holding an object at the end of shot N, they're holding it at the start of shot N+1.

### How to Encode Overlap in Prompts

When writing the Dynamic Description for shot N+1:

1. Open with 1–2 sentences that describe the visual state matching shot N's ending.
2. Then proceed with the new action.

Example:
- Shot 3 ends: "...she turns toward the window, coat draped over one arm, golden light on her face."
- Shot 4 opens: "The silver-haired woman stands at the tall window, coat draped over her arm, warm golden light on her face. She reaches for the handle and pushes the window open..."

### Location Transitions

When changing location between shots:

- The storyboard's `transition_to_next` field guides the transition type.
- If transition is `cut` to a new location: shot N+1 establishes the new space in its opening.
- If transition is `match cut`: shot N's ending composition echoes in shot N+1's opening.
- A character's **face or body** can be the bridge: end on close-up of face in location A → open on same face in location B.

## Location Consistency

- The same `location_prompt` is used every time a location appears across different shots.
- If a location's lighting/time-of-day changes between shots (e.g., morning → evening), note this explicitly in the Static Description: "Same café interior, now lit by amber evening light through the windows."
- Never introduce new furniture, objects, or architectural changes to a location unless the storyboard specifies it.

## Prop Tracking

- Props mentioned in `props_present` for a shot MUST be visually present in the prompt.
- Track prop state changes explicitly:
  - "An open book on the table" → later shot: "The book lies closed on the table"
  - "A lit candle" → later shot: "The candle, burned lower, still flickering"
- If a character picks up or puts down a prop, describe the action explicitly OR start the shot with the prop already in the new state.
- One object interaction per beat — don't describe picking up AND using in one sentence.

## Engine Constraint Reminders

These constraints from `/video-skill` affect continuity planning:

- **≤ 3 characters rendered on screen simultaneously.** This is a rendering quality limit — the engine loses tracking above 3 visible people. If a scene has 4+ characters, split into internal shots that show subsets. **This does NOT limit `--media` attachment count.** You can attach up to 9 image refs via `--media` flags (location + characters + props).
- **Character exits frame = gone for rest of shot.** Don't have a character leave and return in the same shot.
- **No reflection shots.** Avoid mirrors, puddles, glass reflections.
- **Micro-expressions as physics.** Write "jaw clenches, nostrils flare" not "looks angry."
- **Never describe age.** Use role labels or physical descriptions instead.
