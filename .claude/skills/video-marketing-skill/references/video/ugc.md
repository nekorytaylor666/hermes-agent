# UGC

Person talking directly to camera about a product. Testimonial, review, recommendation format. iPhone aesthetic, real rooms, natural daylight, casual clothing, imperfect framing. Like sharing a discovery with a best friend.

**Character:** YES (Soul 2.0 auto-generated).

## Core Principle

Every video looks like it was filmed on an iPhone by a real person in their real home. Never cinematic, never studio, never TV-commercial quality. Handheld iPhone footage, real rooms, natural daylight, casual clothing, imperfect framing. The product is real, the person is real, the setting is real. Always.

---

## Input Tiers (The Director's Filter)

Before building the prompt, classify the user's text request:

| Tier | Trigger | Behavior |
|------|---------|----------|
| **Auto** | 1-5 words, no scenario ("go", "make a video", just a product name) | Full autopilot. Generate a complete engaging UGC script: hook the viewer → show the closed product → jump cut to reaction → enthusiastic recommendation. Classic talking head. |
| **Guided** | 1-3 sentences, general idea but no shot-by-shot detail ("energetic review of this serum", "show how amazing this cream is") | Preserve the user's tone, mood, and emphasis. Build structure, shots, and actions yourself. Fill all gaps creatively. |
| **Director** | 4+ sentences, specific scenario, dialogue, or shot descriptions | Follow the user's scenario as closely as possible. Preserve their specific phrases, tone, sequence, and dialogue VERBATIM. Adapt ONLY physics (unsafe interactions → safe jump cuts). Preserve the user's setting, location, and atmosphere — apply UGC aesthetic TO their chosen setting, do not replace it with a default home setting. |

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
2. **Container material** — glass, hard plastic, soft tube, metal, cardboard? This determines which verbs are safe.
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
5. **Key visual details** — color, shape, material, label text, distinctive features
6. **Forbidden actions for this product** — actions that would break physics or cause AI glitches (e.g. squeezing glass, opening a pump bottle, twisting a spray cap). List them explicitly.

### Safe Interaction Verbs (by material)

| Material | SAFE verbs | FORBIDDEN verbs (cause deformation/glitches) |
|----------|-----------|----------------------------------------------|
| **Glass / Hard plastic / Metal** | rests gently on palm, holds lightly by edges, touches softly, cradles, presents | squeeze, grasp, grip firmly, press into, crush, clench, wrap fingers tightly |
| **Soft tube** | gently squeezes, presses lightly | crushes, twists, wrings |
| **Fabric / Clothing** | drapes over, holds up, smooths, adjusts | stretches, pulls taut, wrings |
| **Any product** | holds, shows, presents, lifts, touches | throws, catches, juggles, flips, spins, drops |

### When Unsure About Product Mechanics

If you cannot determine how a product opens or is used from the image — default to **hold-and-present only**. Person shows the product to camera, talks about it, expresses enthusiasm — but does NOT attempt to open or use it.

### Mode C: No product image (text-only)

Extract product information entirely from the text request. No @Image references, no Angle Lock. Product is described in words within the Dynamic Description.

---

## Style & Mood

UGC selfie aesthetic, warm natural lighting, front-facing camera, intimate feel, window light or soft room light. Never studio, never professional lighting setup.

## Framing

- Front-facing, selfie-style or tripod POV
- The phone is propped or on a tripod — never describe a hand holding the phone
- Eye contact with camera throughout
- Person and product both visible in frame
- Medium close-up: head, shoulders, and hands in frame

## Shot Structure

One continuous scene with jump cuts between phrases. Same person, same position, same framing throughout — cuts only between distinct moments. Never repeat the same action across cuts.

**Standard 3-4 shot arc:**
- **Shot 1 (Talk):** Person talks to camera, introduces the product. Product is closed, resting in hand.
- **Shot 2 (Open + Use):** Person opens the product ON SCREEN using the correct opening mechanic (see Product Interaction Sequences below), then performs ONE usage action.
- **Shot 3 (React):** Person reacts to the result — touches skin, smells wrist, shows the effect, expresses satisfaction.
- **Shot 4 (Close)** *(optional):* Final recommendation to camera, confident nod.

**Critical rule:** The opening and usage MUST match the real physics of the product. The prompt must describe the EXACT hand motion, direction, and grip.

## Audio

Person speaks directly on camera.

Format: `Audio: She speaks to camera, iPhone microphone audio with natural room tone: "..."` (for male: `He speaks to camera, iPhone microphone audio with natural room tone: "..."`)

- If user provides specific text: use exactly that
- If no text: auto-generate enthusiastic product description — like sharing a discovery with a best friend, highlighting real benefits

## Emotion Logic

The person genuinely loves this product. Not acting — really sharing something they're excited about.

## Human Performance Direction (CRITICAL — prevents wooden/AI-looking characters)

Every prompt MUST include at least 3 of these micro-behaviors woven into the Dynamic Description:

**Micro-behaviors (pick 3+ per prompt, rotate between prompts):**
- Weight shift — leans forward when excited, settles back when making a point
- Hair touch — tucks strand behind ear, runs fingers through hair mid-sentence
- Glance break — brief look down at the product then back to camera (NOT sustained look-away)
- Head tilt — slight tilt when asking a rhetorical question or emphasizing a point
- Eyebrow flash — quick raise on a key word ("this is SO good")
- Hand gestures — counting on fingers, pointing at product, emphatic open-palm gesture
- Posture shift — sits up straighter when making the main point, relaxes after
- Lip movement — quick lip press or bite before revealing something exciting
- Shoulder shrug — casual micro-shrug on "I wasn't sure at first but..."
- Breathing — visible inhale before an excited statement, satisfied exhale after

**Expression arc (emotions CHANGE across the video):**
- Shot 1: Casual/curious energy — natural resting face, slight smile, settling in
- Shot 2: Building interest — leans forward, eyes widen slightly, more animated gestures
- Shot 3: Peak enthusiasm — biggest smile, most expressive gestures, emphatic nod
- Shot 4 (if exists): Warm close — direct eye contact, confident nod, genuine satisfied expression

**ANTI-PATTERNS (never write these — they produce wooden AI look):**
- "smiles at the camera" (static smile = mannequin)
- "looks at the camera" (unblinking stare = creepy)
- "sits in front of the camera" (frozen pose = lifeless)
- "holds the product and talks" (robot demonstration)
- Perfectly symmetrical poses (real people are asymmetric)
- Same expression across all shots (real people's faces CHANGE)

**Instead of:** "She smiles and holds the product up to camera"
**Write:** "She leans forward with wide eyes, tucking a strand of hair behind her ear, then holds the product up with both hands, eyebrows raised, slight head tilt, mouth opening into an excited grin"

## Setting

Home/domestic — bedroom, living room, bathroom. Never studio, never outdoors unless user specifies. Real room with real furniture visible in background.

## Person Default

Attractive woman (override if user specifies or product is male-targeted). If user describes specific appearance — use that.

---

## Product Interaction Sequences (CRITICAL — prevents broken physics)

Every product interaction MUST be shown on screen with the EXACT physical sequence. Never write vague descriptions like "opens it" or "uses it."

| Product | Opening sequence (describe exactly this) |
|---------|----------------------------------------|
| **Perfume / cologne** | One hand holds the bottle by the base. Other hand lifts the cap straight up off the top. Cap disappears from the scene. Index finger presses the nozzle — fine mist sprays onto wrist or neck. |
| **Serum with pipette/dropper** | One hand holds the bottle steady. Other hand unscrews the dropper cap by rotating counterclockwise. Lifts the pipette out — glass wand visible with liquid at the tip. Squeezes the rubber bulb gently — drops fall onto fingertips of the other hand. |
| **Cream in a jar** | One hand holds the jar base. Other hand twists the lid counterclockwise, lifts it off. Lid disappears. Fingertips scoop a small amount of cream from the surface. |
| **Soft tube (cream, gel)** | One hand holds the tube in the middle. Other hand unscrews or flips the small cap. Gently squeezes the tube — product comes out onto fingertip or back of hand. |
| **Pump bottle (lotion, serum)** | One hand holds the bottle base to stabilize. Other hand presses down on the pump head with two fingers. Product dispenses onto the waiting palm or fingertips of the first hand. |
| **Lipstick / twist-up balm** | One hand holds the base. Other hand pulls the cap off straight up. Cap disappears. Twists the base to extend the bullet. Swipes directly onto lips. |
| **Mascara / lip gloss wand** | One hand holds the tube. Other hand unscrews and pulls the wand out slowly — brush/applicator visible with product on it. Applies to lashes or lips. Tube stays in the other hand. |
| **Compact / powder** | One hand holds the compact. Thumb flips the lid open (hinge — lid stays attached, does NOT detach). Other hand picks up the included brush or sponge, taps on powder, applies to face. |
| **Spray bottle (toner, mist)** | One hand holds the bottle. Other hand pulls off the cap if present. Index finger presses the trigger/nozzle — mist sprays onto face or skin. |
| **IQOS / vape** | One hand holds the device. Other hand takes a stick/pod, inserts it into the top. Presses the button on the side with thumb. Brings to lips, inhales. |
| **Tech / electronics** | Hold-and-present ONLY. Show to camera, point at details, turn slightly to show a feature. NEVER press buttons, open compartments, or plug in cables. |

**Rules for ALL opening sequences:**
- The cap/lid MUST be removed BEFORE any contents exit the container
- After removal, NEVER describe where the cap goes — it simply ceases to exist in the scene
- NEVER mention the removed cap/lid again in any following sentence
- If the product needs to appear closed again later — use a hard cut to a new shot where it appears closed
- Maximum 1 opening + 1 usage action per shot

---

## Universal Rules

### Product Angle Lock (when product images are provided)

- The product is angle-locked to its front-facing label side. Every shot shows ONLY this locked angle.
- Never describe the product rotating, spinning, turning, tilting, or flipping.
- Camera movement ≠ product rotation. Camera moves freely; product stays locked.

### Weight & Grip Logic

Before describing how the person holds the product, assess real-world weight and size:
- **Heavy** (large appliance, full bottle ≥1L, toolbox) → both hands required. Body posture adapts. Never one-handed.
- **Medium** (tablet, full-size shampoo, handbag) → one hand with firm grip, or two hands for stability.
- **Light** (cosmetics, phone, small bottle, jewelry) → one hand, relaxed grip.
- **Tiny** (single earring, pill, contact lens) → pinched between thumb and index finger, close to camera.

### Hand Count Rule

The person has exactly 2 hands. Never describe two separate hand actions in the same moment. Maximum 1 product interaction per shot.

### State Change Minimization

- NEVER describe removed parts (caps, lids, wrappers) as separate objects after removal — they disappear
- NEVER describe an object being placed down, pushed aside, or handed off — hard cut to new shot where it is absent
- Maximum 1 state change per shot

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

Speech pacing: Casual, slightly rushed, like recording a quick TikTok — not rehearsed. Short phrases with natural pauses ("..."). Emotional beats (gasps, laughs) count as words.

---

## Prompt Format

Every prompt MUST be a **single continuous string** with inline section labels.

**When product image(s) ARE provided:**
```
[Material references — @Image and <<<element_id>>> declarations]
Style & Mood: [UGC selfie aesthetic, warm natural lighting, front-facing camera, intimate feel]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — person talking, showing product, reacting, with micro-behaviors]
Static Description: [location, props, ambient details]
Audio: [person speaking on camera with voice description]
Facial features clear and undistorted, consistent clothing throughout. Shot on iPhone, natural lighting, social media aesthetic, slight natural handheld micro-shake. No on-screen text, no subtitles, no captions, no watermarks.
```

**When NO product image (text-only):**
```
Style & Mood: [UGC selfie aesthetic, warm natural lighting, front-facing camera, intimate feel]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — describe the product in words within the scene]
Static Description: [location, props, ambient details]
Audio: [person speaking on camera with voice description]
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
| Person | Attractive, gender matched to product |
| Setting | Home — bedroom or living room |
| Audio | Person speaks on camera (always on) |
| Language | English |
| Shots | ≤ 4 (talk → open+use → react → close) |
| Tone | UGC talking head, enthusiastic, genuine |
