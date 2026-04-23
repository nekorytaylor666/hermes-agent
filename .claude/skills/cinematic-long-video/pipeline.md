# Long Video Production Pipeline

General-purpose pipeline for videos longer than 15 seconds. Genre-agnostic, style-agnostic. This pipeline serves the user's vision — it adds only technical filmmaking execution.

## Core Principle

**Never add characters, plots, scenes, dialogue, or stylistic choices the user did not request.** When in doubt, ask.

## Pipeline

```
User: idea + duration + style preferences
  → Stage 0: Requirements Capture (lock all requirements)
  → Stage 1: Storyboard Design (shot-level plan + JSON) → user approval gate
  → Stage 1+: Generate reference images → create elements (soul-cast for characters, soul-location for environments)
  → Stage 2 loop:
      Shot generation (one shot at a time, with <<<element_id>>> in prompts)
      User: "continue" → next shot / revision request → revise current shot
  → Stage 3: Assembly instructions (shot order, transitions, BGM/subtitle notes)
```

## References

Read these BEFORE executing any step:

| File                                               | When to read                   | What's inside                                                                  |
| -------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------ |
| [requirements-capture.md](requirements-capture.md) | **Stage 0**                    | Intake questions, confirmation protocol, requirements.json schema              |
| [storyboard-design.md](storyboard-design.md)       | **Stage 1**                    | Duration budgeting, shot decomposition, storyboard.json schema, approval gate  |
| [visual-references.md](visual-references.md)       | **Stage 1+**                   | Character/location/prop image generation, eye mask workaround, upload registry |
| [shot-generation.md](shot-generation.md)           | **Stage 2 + Stage 3**          | Pre-shot checklist, prompt construction, execution protocol, assembly          |
| [continuity.md](continuity.md)                     | **Always from Stage 1 onward** | Character description registry, cross-shot overlap, style consistency          |

## State Detection

| What exists                                             | State               | Action                                 |
| ------------------------------------------------------- | ------------------- | -------------------------------------- |
| No files                                                | Fresh start         | Stage 0 → read requirements-capture.md |
| requirements.json (confirmed: false)                    | Requirements draft  | Present to user, get confirmation      |
| requirements.json (confirmed: true), no storyboard.json | Requirements locked | Stage 1 → storyboard                   |
| storyboard.json, no approved.flag                       | Storyboard pending  | Show user_display → wait               |
| approved.flag, no images                                | Approved, no images | Stage 1+ → generate images             |
| Images exist, no shots/                                 | Images done         | Stage 2 → shot generation              |
| Some shots exist                                        | In progress         | Continue from last incomplete shot     |
| All shots done                                          | Assembly            | Stage 3 → assembly.json                |

## Output Structure

```
output/
├── requirements.json
├── storyboard.json
├── approved.flag
├── images/
├── shots/
├── videos/
└── assembly.json
```

## Delegation Rules

- **Images:** Always invoke `/image-skill`. Never call `higgsfieldcli generate --json '[{"model":"nano_banana_2",...}]'` directly.
- **Videos:** Always invoke `/video-skill`. Never call `higgsfieldcli generate --json '[{"model":"seedance_2_0",...}]'` directly.
- **Upload & Element:** `higgsfieldcli upload` and `higgsfieldcli element` may be called directly.
- **Fire-and-forget:** The CLI returns a `created` line immediately with `job_set_id`, `job_set_type`, `job_ids`. Do not wait — no special timeout needed. Poll via `higgsfieldcli status --job-id <id> --poll` when the result is needed downstream (element creation, showing result to user for approval). Still never use `run_in_background: true` — you must capture the `created` line.

## Prohibited Behaviors

- Never add characters, plots, or elements the user did not mention
- Never modify the storyboard after approval unless user explicitly requests
- Never impose a genre, aesthetic, or narrative structure the user did not choose
- Never skip requirements confirmation (Stage 0) or storyboard approval gate
- Never auto-advance to the next shot without user approval

## Prompt Language

- **Default:** English prompts.
- **ZH mode:** When user's content is Chinese or characters speak Mandarin, use ZH prompts with EN dialogue in Audio section.
