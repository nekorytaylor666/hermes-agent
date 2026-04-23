# Stage 0: Requirements Capture

Capture and lock 100% of the user's vision before any creative work begins.

## Intake Protocol

Ask the user these questions. If any answer is unclear or missing, ask for clarification — **never assume or fill in blanks**.

### Required Questions

1. **What is the video about?** (core idea — record verbatim or close paraphrase)
2. **How long should it be?** (target duration in seconds — minimum 16s)
3. **What aspect ratio?** (default: `16:9` for horizontal, `9:16` for vertical/mobile, `1:1` for square)
4. **What visual style?** (cinematic, documentary, music video, dreamy, gritty, minimalist, etc. — if user describes freely, translate to filmmaking terms later)

### Content Questions

5. **Who or what appears in the video?** (characters, subjects, objects — for each: name, role, appearance description)
6. **Where does it take place?** (locations — for each: name, description)
7. **Are there specific moments that MUST be included?** (key scenes, beats, events)
8. **Any dialogue?** (record verbatim, assign to characters)
9. **Music direction?** (genre, mood, tempo — or specific track if user provides)
10. **Subtitles?** (language, or none)

### Boundary Questions

11. **Anything you explicitly do NOT want?** (prohibitions — record as-is)
12. **Any reference material?** (photos, videos, mood boards — handle via upload)

## Handling Vague Requests

- If user says "make me a 60-second video about coffee" with no further detail → ask questions 4–11.
- If user provides a detailed brief covering all points → skip redundant questions, confirm understanding.
- If user says "surprise me" or "you decide" for a specific aspect → explain that this pipeline requires user direction for all creative decisions. Ask them to provide at least a rough direction.
- If a character has no specified appearance → ask the user to describe them, or propose a description and get explicit approval before proceeding.

## Handling Reference Material

When user provides photos, videos, or mood boards:
- Upload via `higgsfieldcli upload --file <path>` and record the media_id.
- Note in requirements.json what each reference is for (character appearance, location mood, style reference, etc.).
- Reference material informs — it does not override — the user's verbal requirements.

## Confirmation Protocol

After capturing all answers:

1. Present requirements back to the user in clean format:
   ```
   Project: [title]
   Duration: ~[X] seconds | Aspect ratio: [ratio]
   Style: [description]

   Content:
   [summary of what happens]

   Characters:
   — [name] | [role] | [appearance]

   Locations:
   — [name] | [description]

   Key moments:
   — [moment 1]
   — [moment 2]

   Dialogue:
   — [character]: "[line]"

   Music: [direction or "none specified"]
   Subtitles: [language or "none"]

   Will NOT include:
   — [prohibition 1]
   ```

2. Ask: "Is anything missing or wrong? I'll build the storyboard based on exactly this."
3. User confirms → set `confirmed: true` → proceed to Stage 1.
4. User corrects → update requirements → re-present → confirm again.

## Requirements Lock

After `confirmed: true`:
- `requirements.json` is **immutable** unless the user explicitly requests a change.
- If the user requests a change after confirmation → update the specific field → re-confirm → proceed.
- Changes to requirements after storyboard approval may require re-storyboarding — warn the user.

## Output: requirements.json

```json
{
  "project_title": "string",
  "target_duration_sec": 60,
  "aspect_ratio": "16:9",
  "style": {
    "user_description": "string (verbatim user words about style)",
    "visual_style_tag": "string (translated to filmmaking terms: lens, lighting, color, texture — used as style prefix for all video prompts)"
  },
  "content": {
    "summary": "string (user's core idea, verbatim or close paraphrase)",
    "characters": [
      {
        "name": "string",
        "role": "string (user's description of who this person/entity is)",
        "appearance": "string (user's description of how they look)",
        "image_prompt": "string (gender, build, age range, hair, face feature, clothing, signature detail — NO character names)"
      }
    ],
    "locations": [
      {
        "location_id": "loc_01",
        "name": "string",
        "description": "string (user's description)",
        "location_prompt": "string (under 60 words, NO PEOPLE, empty set, include lighting/time-of-day)"
      }
    ],
    "props": [
      {
        "prop_id": "prop_01",
        "name": "string",
        "description": "string"
      }
    ],
    "key_moments": [
      "string (user-specified moments that MUST appear in the video)"
    ],
    "dialogue": [
      {
        "character": "string (character name)",
        "line": "string (verbatim dialogue)",
        "context": "string (when/where this line is spoken, if specified)"
      }
    ],
    "music_direction": "string or null",
    "subtitle_language": "string or null"
  },
  "prohibitions": [
    "string (anything the user explicitly said they do NOT want)"
  ],
  "reference_material": [
    {
      "media_id": "string",
      "purpose": "string (what this reference is for)"
    }
  ],
  "confirmed": false
}
```

## image_prompt Construction

When building the `image_prompt` field from user's appearance description:

- Include: gender, approximate build/stature, hair style + color, defining face feature, primary clothing, one signature detail.
- Exclude: character names, abstract personality traits, backstory.
- Keep under 30 words.
- If user described the character vaguely ("a mysterious man") → ask for visual specifics before writing the prompt.

## location_prompt Construction

When building the `location_prompt` field from user's location description:

- Include: space type, key objects/furniture, lighting, time of day, color palette, atmosphere.
- Exclude: people, characters, action, narrative.
- Keep under 60 words.
- Always end with empty-set implication — the location is shown without inhabitants.
