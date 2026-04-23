# Stage 1: Storyboard Design

Transform locked requirements into a shot-level production plan.

## Input

- `requirements.json` with `confirmed: true`
- Read `continuity.md` alongside this file

## Duration Budgeting

### Shot Duration Ranges by Content Type

| Content type | Duration per shot | Notes |
|---|---|---|
| Action / fast-paced | 4–7s | Quick cuts, high energy |
| Dialogue / conversation | 6–10s | Time for speech + reactions |
| Atmosphere / establishing | 8–15s | Slow, immersive |
| Montage / quick cuts | 4–6s per segment | Rhythmic assembly |
| Default (mixed content) | 8–10s | Best seedance-2.0 quality sweet spot |

### Decomposition Algorithm

1. Read `target_duration_sec` from requirements.json.
2. Classify the overall video tempo based on style and content:
   - Fast (action, music video, montage): average 5–6s per shot
   - Medium (narrative, brand story, documentary): average 8–9s per shot
   - Slow (atmospheric, artistic, contemplative): average 10–12s per shot
3. Calculate initial shot count: `ceil(target_duration_sec / average_shot_duration)`.
4. Assign individual shot durations (each 4–15s) to sum to target.
5. Adjust: if any shot exceeds 15s, split it. If any shot is under 4s, merge with adjacent.

### Example

User requests 60s narrative video, medium tempo:
- Average shot = 8s → initial count = 8 shots
- Budget: [8, 10, 6, 8, 8, 6, 8, 6] = 60s ✓

## Shot Decomposition Rules

### Mandatory Coverage

Every element from requirements.json MUST be accounted for:

- [ ] Every `key_moments[]` entry → mapped to at least 1 shot
- [ ] Every `characters[]` entry → appears in at least 1 shot
- [ ] Every `dialogue[]` entry → assigned to exactly 1 shot's `audio_notes`
- [ ] Every `locations[]` entry → used in at least 1 shot (if user mentioned it, it must appear)

### Prohibition

- [ ] **Nothing outside requirements.json may be added.** No extra characters, no invented plot points, no surprise locations.
- [ ] If the requirements feel thin and the video needs more content → go back to the user: "Your requirements cover about [X] seconds of content. Would you like to add more scenes, or should I extend the existing ones with longer atmospheric shots?"

### Narrative Flow

- Default structure: beginning → middle → end.
- If user specified a non-linear structure (flashback, circular, etc.) → follow their structure.
- If user gave no structure preference → use simple chronological flow.

## Camera Intent + Internal Shot Structure

Each storyboard "shot" = one seedance clip (4–15s). But a clip can contain **multiple internal camera setups** with cuts inside it. This is essential for visual variety — a single unbroken camera move for 8+ seconds gets monotonous.

### When to plan multi-shot clips

| Clip duration | Content has multiple beats? | Recommended structure |
|---|---|---|
| 4–6s | No — single action | Single continuous take |
| 4–6s | Yes — action + reaction | 2 internal camera setups |
| 7–10s | No — one slow action | Single take is OK |
| 7–10s | Yes — discover + react, approach + confront | 2–3 internal setups |
| 11–15s | Any | Almost always 2–4 internal setups |

### Camera intent format

Write the `camera_intent` field to explicitly indicate the internal structure:

**Multi-shot example:**
```
"camera_intent": "Medium tracking shot following her through corridor → hard cut to close-up of hand on door handle → cut to wide static as she enters the garage"
```

**Single-shot example:**
```
"camera_intent": "Slow dolly push-in from wide to medium, one continuous take"
```

### Camera vocabulary by content type

| Shot content | Camera intent examples |
|---|---|
| Character introduction | Medium tracking → cut to close-up on face (multi-shot) |
| Dialogue scene | OTS alternating with cuts between speakers (multi-shot) |
| Action/movement | Tracking shot → cut to impact close-up → cut to wide aftermath (multi-shot) |
| Establishing location | Wide crane or aerial, slow pan (single-shot) |
| Emotional moment | Slow push in to close-up, shallow DOF (single-shot) |
| Montage segment | Quick cuts between varied angles (multi-shot, 3–4 setups) |
| Discovery / reveal | Wide establishing → cut to close-up of discovered object → cut to face reaction (multi-shot) |
| Confrontation | Medium two-shot → alternating close-ups as tension builds (multi-shot) |

Camera intent is a direction — the exact camera terms and cut markers are finalized in Stage 2 when constructing the video prompt.

## Transition Planning

Plan how consecutive shots connect:

| Transition type | When to use |
|---|---|
| Hard cut | Default. Scene continues or cuts to new angle |
| Match cut | Visual or motion similarity between end of shot N and start of shot N+1 |
| Dissolve | Time passage, dream/memory sequences |
| Whip-pan transition | Fast energy shift, montage |
| L-cut / J-cut | Dialogue carries across shot boundary |

## Output: storyboard.json

```json
{
  "project_title": "string",
  "target_duration_sec": 60,
  "actual_duration_sec": 62,
  "aspect_ratio": "16:9",
  "style_tag": "string (filmmaking terms from requirements.style.visual_style_tag — prepended to EVERY video prompt)",
  "shot_count": 7,
  "shots": [
    {
      "shot_number": 1,
      "timestamp": "0:00-0:08",
      "duration_sec": 8,
      "location_id": "loc_01",
      "characters_present": ["CharacterName"],
      "props_present": ["prop_01"],
      "scenario": "string (user-facing description: what happens, plain language, includes dialogue if any)",
      "camera_intent": "string (camera movement + framing direction for this shot)",
      "audio_notes": "string (dialogue lines verbatim, SFX notes, music cues)",
      "transition_to_next": "string (cut / match cut / dissolve / whip-pan / etc.)"
    }
  ],
  "user_display": {
    "title": "string",
    "duration": "string (e.g., '~60 seconds, 7 shots')",
    "style": "string",
    "shot_list": [
      {
        "number": 1,
        "time": "0:00-0:08",
        "description": "string (scenario in plain language)"
      }
    ]
  }
}
```

## Presenting to User

Show ONLY `user_display` — clean text, no JSON, no technical details:

```
Title: [title]
Duration: ~60 seconds, 7 shots
Style: [style description]

Shot list:
1. [0:00-0:08] — [description]
2. [0:08-0:18] — [description]
3. [0:18-0:24] — [description]
...

Does this match your vision? I can adjust shots, reorder, or change durations before we start generating.
```

Do NOT show: camera_intent, transition_to_next, location_id, props_present, audio_notes.
The user sees the story — not the production plan.

## Approval Gate

- User approves → create `approved.flag` file → proceed to Stage 1+.
- User requests changes → revise storyboard → re-present → wait for approval.
- **Never proceed past this gate without explicit user approval.**

## Revision Protocol

| User requests | Action |
|---|---|
| Change a shot's content | Update that shot's scenario + dependent fields |
| Add a new shot | Insert, re-number, adjust timestamps and durations |
| Remove a shot | Delete, re-number, redistribute duration if needed |
| Reorder shots | Rearrange, update timestamps and transitions |
| Change overall duration | Recalculate shot durations proportionally |
| Change style | Update style_tag, note that all shots will use new style |
| Add a character/location | Update requirements.json first, then revise storyboard |

After any revision: re-present `user_display` and wait for approval again.
