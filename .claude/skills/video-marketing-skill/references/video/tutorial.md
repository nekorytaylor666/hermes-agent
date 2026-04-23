# Tutorial

Step-by-step UGC demonstration of how to use a product. Person shows the real usage process on camera, talking while demonstrating. iPhone aesthetic, real rooms, natural daylight, casual clothing, imperfect framing.

**Character:** YES (Soul 2.0 auto-generated).

## Core Principle

Every video looks like it was filmed on an iPhone by a real person in their real home. Never cinematic, never studio, never TV-commercial quality. Handheld iPhone footage, real rooms, natural daylight, casual clothing, imperfect framing. The product is real, the person is real, the setting is real. Always.

---

## Input Tiers (The Director's Filter)

Before building the prompt, classify the user's text request:

| Tier | Trigger | Behavior |
|------|---------|----------|
| **Auto** | 1-5 words, no scenario ("go", "make a video", just a product name) | Full autopilot. Generate a complete tutorial: friendly intro to camera → open/prepare product → demonstrate usage → show result. Classic "here's how I use this" format. |
| **Guided** | 1-3 sentences, general idea but no shot-by-shot detail ("show how to apply this serum", "quick tutorial on this cream") | Preserve the user's tone, mood, and emphasis. Build structure, steps, and actions yourself. Fill all gaps creatively. |
| **Director** | 4+ sentences, specific scenario, dialogue, or shot descriptions | Follow the user's scenario as closely as possible. Preserve their specific phrases, tone, sequence, and dialogue VERBATIM. Adapt ONLY physics (unsafe interactions → safe alternatives). Preserve the user's setting, location, and atmosphere — apply UGC aesthetic TO their chosen setting, do not replace it with a default. |

## User Override Rule

If the user specifies ANY concrete detail — setting, clothing, appearance, action, mood, specific phrase, location, time of day, props — that detail takes priority over ALL defaults. Defaults exist ONLY to fill gaps the user left empty. Never replace a user-specified detail with a default.

---

## Product Understanding

### Mode A: Product image(s) + product description provided

Use the provided description directly. Extract: product name, brand, category, key features, specs. The product image is used for @Image references and Angle Lock — not for analysis.

### Mode B: Product image(s) provided, no description

**MANDATORY: Visually analyze the product image before writing any prompt.**

Identify:
1. **Product category** — what is it exactly?
2. **Container material** — glass, hard plastic, soft tube, metal, cardboard, fabric? This determines which verbs are safe.
3. **Applicator type** — what part does the person's hand touch during use?
   - **Removable cap** (perfume, jar, tube) → lift/twist off, then interact with contents
   - **Pump** (lotion, soap) → press down with fingers, product dispenses
   - **Dropper/pipette** (serum) → unscrew, pull out wand, squeeze rubber bulb to drop liquid
   - **Wand** (mascara, lip gloss) → unscrew, pull out wand with product on tip, apply
   - **Spray nozzle** (perfume, mist) → press nozzle with index finger, mist sprays
   - **Twist-up** (lipstick, balm) → pull off cap, twist base to extend product
   - **Flip top** (shampoo, gel) → flip the hinged cap open (stays attached)
   - **Compact/hinge** (powder, palette) → thumb flips lid open (stays attached)
   - **No applicator** (clothing, tech, food) → hold and present only
4. **Usage mechanic** — how is it physically used?
   - Perfume / spray bottle → **spray** (press nozzle → mist)
   - Soft tube → **gently squeeze + apply** with fingers
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
5. **Opening mechanic** — how does it open? (uncap, unscrew, pull tab, flip top, press pump, tear wrapper, lift lid). This MUST be shown before any contents exit the container.
6. **Key visual details** — color, shape, material, label text, distinctive features
7. **Forbidden actions for this product** — actions that would break physics or cause AI glitches (e.g. squeezing glass, opening a pump bottle lid, twisting a spray cap). List them explicitly.

### Safe Interaction Verbs (by material)

| Material | SAFE verbs | FORBIDDEN verbs (cause deformation/glitches) |
|----------|-----------|----------------------------------------------|
| **Glass / Hard plastic / Metal** | rests gently on palm, holds lightly by edges, touches softly, cradles, presents | squeeze, grasp, grip firmly, press into, crush, clench, wrap fingers tightly |
| **Soft tube** | gently squeezes, presses lightly | crushes, twists, wrings |
| **Fabric / Clothing** | drapes over, holds up, smooths, adjusts | stretches, pulls taut, wrings |
| **Any product** | holds, shows, presents, lifts, touches | throws, catches, juggles, flips, spins, drops |

### When Unsure About Product Mechanics

If you cannot determine how a product opens or is used from the image — default to **hold-and-present only**. Person shows the product to camera, points at details, describes it verbally — but does NOT attempt to open or use it.

### Mode C: No product image (text-only)

Extract product information entirely from the text request. No @Image references, no Angle Lock. Product is described in words within the Dynamic Description.

---

## Style & Mood

UGC tutorial aesthetic, natural lighting, clean framing, casual and approachable. Never studio, never professional lighting setup. Like a friend showing you how they use something.

## Framing

One consistent framing throughout the entire video — person visible (medium shot, waist up or wider), hands visible, product visible. NEVER switch between face-shot and hands-only close-up — the engine gets confused by framing changes. The person is always in frame, talking and demonstrating at the same time, like a real TikTok tutorial.

## Audio

Person speaks on camera throughout — talking while demonstrating.

Format: `Audio: She speaks to camera, iPhone microphone audio with natural room tone: "So here's how I use this... first you just... then I like to... and that's it!"` (for male: `He speaks to camera, iPhone microphone audio with natural room tone: "..."`)

- Person talks AND shows at the same time — not separate intro then silent demo
- Never say "step one", "step two" — speak like explaining to a friend
- If user provides specific text: use exactly that
- If no text: auto-generate casual how-to commentary — sharing a routine with a friend

## Human Performance Direction (CRITICAL — prevents wooden/AI-looking characters)

The person is always visible and always alive — talking and demonstrating simultaneously. Every prompt MUST include at least 3 of these micro-behaviors woven into the Dynamic Description:

**Micro-behaviors (pick 3+ per prompt, rotate between prompts):**
- Lean-in — leans toward camera like sharing a secret tip before demonstrating
- Eyebrow flash — quick raise when mentioning the product ("you NEED to try this")
- Head tilt — slight tilt when explaining a step
- Glance down — looks at product in hands then back at camera naturally
- Gentle handling — fingers touch the product softly, unhurried, like someone who uses it daily
- Natural pause — slight hesitation before applying (testing the amount), not rushing
- Posture shift — leans forward during demo, settles back when making a point
- Hair tuck — tucks strand behind ear between steps
- Nod — small confident nod after completing a step ("see? easy")
- Satisfied expression — genuine reaction to the result at the end

**Expression arc (emotions CHANGE across the tutorial):**
- Step 1: Friendly, casual — "let me show you" energy, relaxed
- Step 2: Focused but warm — demonstrating with care, slight concentration
- Step 3: Satisfied — showing the result, pleased expression, confident nod

**ANTI-PATTERNS (never write these):**
- "demonstrates the product" (instructional = not UGC)
- "shows how to use it" (vague = robotic)
- "applies the product to skin" (generic = lifeless)
- Static expression throughout (real people react as they go)

**Instead of:** "She applies the cream to her face"
**Write:** "She gently squeezes a small amount onto her fingertip, glances at camera with a slight smile, then presses it into her cheek in small circles, nodding — 'see, just a little goes a long way'"

## Step Logic

Steps are **surface-level** — show WHAT to do, not deep mechanical HOW. Each step = one simple action the person does while talking. Keep it light, like a TikTok routine — not an instruction manual.

- Simple product (cream, spray) → 2-3 steps
- Medium complexity (multi-step skincare, gadget) → 3-4 steps
- Complex product (multi-component) → 4-5 steps max

Each new step starts as a new sentence in the Dynamic Description.

### Duration Dependency

- Short (5s): 2 super concise steps
- Medium (8-10s): 3 steps
- Long (15s): 4-5 steps

## Product Interaction by Category

Before describing interaction, determine the product's category:

| Category | Interaction Rules |
|---|---|
| **Tech / Electronics / Mechanical** (cameras, gadgets, tools, appliances) | **Hold-and-present only.** Hold, show to camera, examine, point at detail — but NEVER press buttons, turn knobs, pull levers, open compartments, insert cables, or manipulate any mechanical parts. |
| **Cosmetics / Skincare / Beauty** (creams, serums, perfumes, makeup) | May apply, spray, blend — but ONLY after a physically correct opening action. Never show contents exiting a closed container. |
| **Beverages / Food** (bottles, cans, cups, snacks, supplements) | May open, pour, drink, taste — but ONLY after a physically correct opening action. Never show liquid leaving a sealed container. |
| **Clothing / Accessories / Wearables** (shoes, bags, jewelry, watches) | May put on, adjust, feel material, show fit — natural fashion interaction. |
| **General / Other** | Hold-and-present by default. No mechanical interaction unless operation is visually obvious and simple. |

## Product Interaction Sequences (CRITICAL — prevents broken physics)

When Product Interaction by Category PERMITS interaction, the EXACT physical sequence must be described. Never write vague descriptions like "opens it" or "uses it."

**Permission check:** FIRST check Product Interaction by Category. If "hold-and-present only" → do NOT use any sequence below.

| Product | Interaction sequence (describe exactly this) |
|---------|----------------------------------------------|
| **Perfume / cologne** | One hand holds the bottle by the base. Other hand lifts the cap straight up off the top. Cap disappears from the scene. Index finger presses the nozzle — fine mist sprays onto wrist or neck. |
| **Serum with pipette/dropper** | One hand holds the bottle steady. Other hand unscrews the dropper cap by rotating counterclockwise. Lifts the pipette out — glass wand visible with liquid at the tip. Squeezes the rubber bulb gently — drops fall onto fingertips of the other hand. |
| **Cream in a jar** | One hand holds the jar base. Other hand twists the lid counterclockwise, lifts it off. Lid disappears. Fingertips scoop a small amount of cream from the surface. |
| **Soft tube (cream, gel)** | One hand holds the tube in the middle. Other hand unscrews or flips the small cap. Gently squeezes the tube — product comes out onto fingertip or back of hand. |
| **Pump bottle (lotion, serum)** | One hand holds the bottle base to stabilize. Other hand presses down on the pump head with two fingers. Product dispenses onto the waiting palm or fingertips of the first hand. |
| **Lipstick / twist-up balm** | One hand holds the base. Other hand pulls the cap off straight up. Cap disappears. Twists the base to extend the bullet. Swipes directly onto lips. |
| **Mascara / lip gloss wand** | One hand holds the tube. Other hand unscrews and pulls the wand out slowly — brush/applicator visible with product on it. Applies to lashes or lips. Tube stays in the other hand. |
| **Compact / powder** | One hand holds the compact. Thumb flips the lid open (hinge — lid stays attached, does NOT detach). Other hand picks up the included brush or sponge, taps on powder, applies to face. |
| **Spray bottle (toner, mist)** | One hand holds the bottle. Other hand pulls off the cap if present. Index finger presses the trigger/nozzle — mist sprays onto face or skin. |
| **Clothing / shoes** | Hold up to body, drape over shoulders, press against chest to show fit. NEVER attempt to put on clothing on camera — engine cannot render dressing. |

**Rules for ALL interaction sequences:**
- The cap/lid MUST be removed BEFORE any contents exit the container
- After removal, NEVER describe where the cap goes — it simply ceases to exist in the scene
- NEVER mention the removed cap/lid again in any following sentence
- Maximum 1 opening + 1 usage action per step/shot
- Each sequence step maps to one tutorial step

## Setting

Real-life environment matched to product context — bathroom for skincare, desk for gadgets, kitchen for appliances. Never studio, never overly polished.

## Person Default

Attractive, gender matched to product. Person is always visible throughout the video — face and hands in frame. If user describes specific appearance — use that.

---

## Universal Rules

### Product Angle Lock (when product images are provided)

- The product is angle-locked to its front-facing label side. Every shot shows ONLY this locked angle.
- Never describe the product rotating, spinning, turning, tilting, or flipping.
- All interaction happens from the VISIBLE side of the product.
- Camera movement ≠ product rotation. Camera moves freely; product stays locked.

### No Invented Objects

ONLY the product from the input image appears in the video. NEVER add objects, tools, accessories, or props not visible in the input photo. No extra brushes, sponges, cotton pads, mirrors, towels, other bottles. The scene contains the person and the product — nothing else.

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

Speech pacing: Short punchy phrases with natural pauses ("..."). Casual tone — like explaining to a friend, not lecturing.

---

## Prompt Format

Every prompt MUST be a **single continuous string** with inline section labels.

**When product image(s) ARE provided:**
```
[Material references — @Image and <<<element_id>>> declarations]
Style & Mood: [UGC tutorial aesthetic, natural lighting, casual and approachable]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — intro to camera, then step-by-step product use with micro-behaviors]
Static Description: [location, props, ambient details]
Audio: [person speaking on camera throughout with voice description]
Facial features clear and undistorted, consistent clothing throughout. Shot on iPhone, natural lighting, social media aesthetic, slight natural handheld micro-shake. No on-screen text, no subtitles, no captions, no watermarks.
```

**When NO product image (text-only):**
```
Style & Mood: [UGC tutorial aesthetic, natural lighting, casual and approachable]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — describe the product in words within the scene]
Static Description: [location, props, ambient details]
Audio: [person speaking on camera throughout with voice description]
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
| Person | Attractive, gender matched to product (face + hands visible) |
| Setting | Real-life environment matched to product |
| Audio | Person speaks on camera throughout (always on) |
| Language | English |
| Steps | 2-5 (based on product complexity and duration) |
| Tone | UGC tutorial, casual, like a friend showing you |
