# Video Imitation / Reference Rules

## When This Applies

Triggered by user requests containing: "referencing this video", "imitating this video", "similar to this video", "derivative of", "in the style of this video", etc.

---

## Core Rules

### 1. Reference Boundary

Only reference **creative techniques** from the source video:
- Camera movement
- Action rhythm
- Transition effects
- Style and color tone
- Editing rhythm

The core theme, content, and plot must come entirely from the user's requirements. Never use the reference video's content, characters, or materials directly.

### 2. Material Citation

Reference videos must be clearly scoped in the prompt:
- `"Completely refer to the camera movement effects of @Video1"`
- `"Refer to the editing rhythm of @Video1"`

If the user provides new main materials (characters, scenes), label their purpose explicitly to ensure the core content is the user's new content — not the reference.

### 3. Originality Requirement

The generated video must be original. It may only reference technique — never be substantially similar to the reference video's content.

If the reference video contains copyrighted content, remind the user to ensure their creation does not infringe on original rights.

### 4. Requirement Matching

All referenced techniques must serve the user's creative needs. Never alter the user's subject, scene, or plot requirements because of the reference.

---

## Prohibited Behaviors

- Do not copy content, characters, or plot from the reference video
- Do not modify the user's core themes or content — only reference creative techniques
- Do not use copyrighted material (background music, dialogue) from the reference unless the user explicitly authorizes it

---

## Example

| User Request | Optimized Prompt | Rationale |
|-------------|-----------------|-----------|
| "Using the camerawork of this food video, create a coffee-making video." | "Referring to the camerawork and editing rhythm of @Video1, showcase the pour-over coffee making process: 0-3 seconds close-up of grinding coffee beans, 3-7 seconds hot water poured over the coffee grounds, 7-10 seconds coffee dripping into the cup, warm color tone, food photography style, 4K high definition." | Only camerawork and rhythm referenced; core content is entirely the user's coffee-making request. |
