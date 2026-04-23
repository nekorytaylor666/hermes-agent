# Product Review

Faceless UGC product demonstration — person actively uses the product on camera. Focus is on the product in action, not the person. Voiceover narration over the footage. iPhone aesthetic, real rooms, natural daylight, casual clothing, imperfect framing. The product is real, the person is real, the setting is real. Always.

**Character:** NO (auto-generated). User can provide their own person reference.

## Core Principle

Every video looks like it was filmed on an iPhone by a real person in their real home or street. Never cinematic, never studio, never TV-commercial quality. Handheld iPhone footage, real rooms, natural daylight, casual clothing, imperfect framing.

---

## Product Understanding

### Mode A: Product image(s) + product description provided

Use the provided description directly. Extract: product name, brand, category, key features, specs. The product image is used for @Image references and Angle Lock — not for analysis.

### Mode B: Product image(s) provided, no description

**MANDATORY: Visually analyze the product image before writing any prompt.**

Identify:
1. **Product category** — what is it exactly?
2. **Usage mechanic** — how is it physically used?
   - Perfume / spray bottle → **spray** (press nozzle → mist)
   - Tube → **squeeze + apply** with fingers
   - Pump bottle → **press pump** → dispense onto fingers → apply
   - Lipstick / lip gloss → **swipe** directly on lips
   - Mascara → **brush** applied to lashes
   - Dropper / serum with pipette → **drop** onto fingertips → press into skin
   - Jar → **scoop** with fingers → apply
   - Capsule / pill → **swallow** or **chew**
   - Clothing / shoes → **wear**
   - Tech / electronics → **hold and present** only
   - General → **hold and present** by default
   This mechanic is the ONLY way the product may be interacted with in the Dynamic Description.
3. **Opening mechanic** — how does it open? (uncap, unscrew, pull tab, flip top, press pump, tear wrapper, lift lid). This MUST be shown before any contents exit the container.
4. **Key visual details** — color, shape, material, label text, distinctive features

### Mode C: No product image (text-only)

Extract product information entirely from the text request. No @Image references, no Angle Lock. Product is described in words within the Dynamic Description.

---

## Style & Mood

UGC authentic, natural lighting, real-life environment, iPhone/handheld aesthetic, warm ambient tones. Never studio, never professional lighting setup, never polished.

## Framing

- Mostly close-ups and medium shots of the product in use — hands, feet, body parts interacting with the product
- Full-body or face shots are rare and brief, only when necessary for context
- Describe the action naturally (e.g. "she dries her hair in front of the bathroom mirror" NOT "camera from behind shows her drying hair")

## Audio

Audio runs continuously — NO silent frames, NO gaps. Every shot is covered by speech.

- **Faceless shots** (hands/product close-up): warm voiceover narration over footage. Format: `A warm, natural female voice narrates casually over the footage: "..."` (for male: `A deep, warm male voice narrates casually over the footage: "..."`)
- **Face visible shots** (person in frame, interacting with product): person speaks on camera while performing the action — talks and does simultaneously, like a real TikTok creator. Format: `She speaks while applying: "..."` 
- Mode can switch between shots — voiceover on a close-up, then on-camera speech when face appears. Transitions are natural.
- If user provides specific text: use exactly that
- If no text: auto-generate casual UGC-style narration describing what's shown, highlighting benefits

## Shot Pattern

- Open with close-up of product being picked up or held
- Each following shot shows a different stage of use
- Highlight key features through visual demonstration
- End with a satisfying result or final product shot

**No dead air rule:** Every shot has voice coverage. If hands are applying cream — voiceover describes what's happening. If face is visible while applying — person speaks while applying. Never a silent demonstration.

## Interaction Energy

Hands move with purpose and enthusiasm — not robotic demonstration. Quick eager movements when opening, gentle careful touch when applying, satisfied pause after result.

## Product Interaction by Category

Before describing interaction, determine the product's category:

| Category | Interaction Rules |
|---|---|
| **Tech / Electronics / Mechanical** (cameras, gadgets, tools, appliances) | **Hold-and-present only.** Hold, show to camera, examine, point at detail — but NEVER press buttons, turn knobs, pull levers, open compartments, insert cables, or manipulate any mechanical parts. |
| **Cosmetics / Skincare / Beauty** (creams, serums, perfumes, makeup) | May apply, spray, blend — but ONLY after a physically correct opening action. Never show contents exiting a closed container. |
| **Beverages / Food** (bottles, cans, cups, snacks, supplements) | May open, pour, drink, taste — but ONLY after a physically correct opening action. Never show liquid leaving a sealed container. |
| **Clothing / Accessories / Wearables** (shoes, bags, jewelry, watches) | May put on, adjust, feel material, show fit — natural fashion interaction. |
| **General / Other** | Hold-and-present by default. No mechanical interaction unless operation is visually obvious and simple. |

## Setting

Real-life environments — home, street, kitchen, gym, bathroom. Matched to product context: bathroom for skincare, kitchen for food, desk for tech. Never studio, never overly polished.

## Person Default

Attractive, gender matched to product (female product → woman, male product → man, neutral → either). Person is faceless in most shots — only hands and body visible. If user describes specific appearance — use that.

---

## Universal Rules

### Product Angle Lock (when product images are provided)

- The product is angle-locked to its front-facing label side. Every shot shows ONLY this locked angle.
- Never describe the product rotating, spinning, turning, tilting, or flipping.
- Camera movement ≠ product rotation. Camera moves freely; product stays locked.

### Weight & Grip Logic

Before describing how the person holds the product, assess real-world weight:
- **Heavy** (vacuum cleaner, large appliance, luggage) → both hands required. Never one-handed.
- **Medium** (tablet, handbag, small appliance) → one hand possible but firm grip. No spinning, no tossing.
- **Light** (cosmetics, phone, small bottle) → one hand, relaxed grip is fine.

### Hand Count Rule

The person has exactly 2 hands. Never describe two separate hand actions in the same moment. Maximum 1 product interaction per shot.

### Container Opening Physics

If a container is shown closed, it MUST be visibly opened first BEFORE any contents exit it. The opening action must be explicitly described.

### Detachable Parts Rule

- ALWAYS describe the removal action explicitly ("twists the cap off", "uncaps the bottle")
- NEVER describe where the removed part goes after removal
- NEVER mention the removed part again after removal

### State Change Minimization

- Use hard cuts to skip state transitions
- NEVER describe removed parts as separate objects
- Maximum 1 state change or product interaction per shot

### No Extras Rule

No additional people or random objects beyond the person and the product.

### Shot Compression

Compress into ≤ 4 shots. Each shot = one distinct action. Never repeat the same action between shots.

### Age-Blind Character Rule

Never describe characters by age. **Never use:** boy, girl, child, kid, young, teen, little. Use role-based labels instead.

### Audio Language Rule

Default audio language is **English** — always, regardless of what language the user writes their request in.

**Override:** Only switch to a different language if the user explicitly requests it — e.g. "make her speak Spanish", "audio in Russian". In that case, use the explicitly requested language for the Audio field.

If no explicit language is stated → English audio. No exceptions.

---

## Engine Constraints (Seedance 2.0)

| Parameter | Limit |
|---|---|
| Duration | ≤ 12s default, ≤ 15s if requested, never > 15s |
| Story/visual beats | ≤ 4 per scene |
| Characters per shot | ≤ 3 |
| Parallel elements | ≤ 3 simultaneous actions/subjects |

### What Breaks
- **Reflection shots** (mirrors, puddles) — NEVER use
- **Exit + re-entry** in same shot — character leaves = gone for rest of shot

### NSFW-Safe Vocabulary
Avoid mechanical verbs that read as double-entendre in English. The content filter reads text literally.
- sucks → cleans / vacuums
- blows → dries / air-flows
- strokes → glides / smooths
- rubs → applies / presses gently
- penetrates → enters / goes into
- thrusts → pushes / moves forward

### Density by Duration

| Duration | Sentences in Dynamic Description | Max words in Audio speech |
|----------|--------------------------------|--------------------------|
| ≤ 10s | 4–8 | 12–20 |
| 11–12s | 6–10 | 20–28 |
| 13–15s | 8–14 | 28–35 |

Speech pacing: Short punchy phrases with natural pauses ("..."). Casual voiceover tone — like explaining to a friend, not presenting.

---

## Prompt Format

Every prompt MUST be a **single continuous string** with inline section labels.

**When product image(s) ARE provided:**
```
[Material references — @Image and <<<element_id>>> declarations]
Style & Mood: [UGC authentic, natural lighting, real-life environment, iPhone/handheld aesthetic]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — hands interacting with product, each shot = different stage of use]
Static Description: [location, props, ambient details]
Audio: [voiceover narration with voice description]
Facial features clear and undistorted, consistent clothing throughout. Shot on iPhone, natural lighting, social media aesthetic, slight natural handheld micro-shake. No on-screen text, no subtitles, no captions, no watermarks.
```

**When NO product image (text-only):**
```
Style & Mood: [UGC authentic, natural lighting, real-life environment, iPhone/handheld aesthetic]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — describe the product in words within the scene]
Static Description: [location, props, ambient details]
Audio: [voiceover narration with voice description]
Facial features clear and undistorted, consistent clothing throughout. Shot on iPhone, natural lighting, social media aesthetic, slight natural handheld micro-shake. No on-screen text, no subtitles, no captions, no watermarks.
```

### Material References (only when images are provided)

**Product references:**
- 1 product photo: `@Image1 is the product reference. ANGLE LOCK: the product shows ONLY its front-facing label side as visible in @Image1 — this is the locked angle. The person interacts with it without rotating it to reveal unseen sides. No exceptions.`
- 2+ product photos: `@Image1 and @Image2 are the only valid product angles. The product may appear from these exact angles only — switch between them via hard cuts, never via continuous rotation. No intermediate or invented angles.`

**Person references:**
- Person photo as `@ImageN`: `@ImageN is the person/creator reference.`
- Person as element: `<<<element_id>>> is the person/creator.`
- No person: omit — the engine uses the person description from the prompt

**Order rule:** Product images first, then person image (if any).

---

## Defaults

| Parameter | Default |
|---|---|
| Duration | 10 seconds |
| Aspect ratio | 9:16 (vertical) |
| Person | Attractive, gender matched to product (faceless — hands/body only) |
| Setting | Real-life environment matched to product |
| Audio | Voiceover narration (always on) |
| Language | English |
| Shots | ≤ 4 (one distinct action per shot) |
| Tone | UGC authentic, iPhone aesthetic |
