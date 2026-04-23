# UGC Virtual Try On

Person tries on clothing or accessories at home, filmed on an iPhone on a tripod. They pose, show off the outfit, and react to how it looks. Real room, natural daylight, casual home vibe. Like filming yourself trying on a new delivery.

**Character:** YES (Soul 2.0 auto-generated).

## Core Principle

Every video looks like it was filmed on an iPhone on a tripod by a real person in their real bedroom or living room. Never cinematic, never studio, never lookbook quality. Real room, natural daylight, casual home vibe, imperfect background. The person is real, the outfit is real, the setting is real. Always.

---

## Input Tiers (The Director's Filter)

Before building the prompt, classify the user's text request:

| Tier | Trigger | Behavior |
|------|---------|----------|
| **Auto** | 1-5 words, no scenario ("go", "make a video", just an item name) | Full autopilot. Generate a complete try-on arc: own clothes → hard cut → new outfit reveal → posing → detail close-up → final confident pose. Classic try-on haul format. |
| **Guided** | 1-3 sentences, general idea but no shot-by-shot detail ("casual vibes trying on this dress", "show off these sneakers") | Preserve the user's tone, mood, and emphasis. Build structure, shots, and poses yourself. Fill all gaps creatively. |
| **Director** | 4+ sentences, specific scenario, dialogue, or shot descriptions | Follow the user's scenario as closely as possible. Preserve their specific phrases, tone, sequence, and dialogue VERBATIM. Adapt ONLY physics (no changing on camera → hard cuts). Preserve the user's setting, location, and atmosphere — apply UGC aesthetic TO their chosen setting, do not replace it with a default bedroom. |

## User Override Rule

If the user specifies ANY concrete detail — setting, clothing, appearance, action, mood, specific phrase, location, time of day, props — that detail takes priority over ALL defaults. Defaults exist ONLY to fill gaps the user left empty. Never replace a user-specified detail with a default.

---

## Product Understanding

### Mode A: Product image(s) + product description provided

Use the provided description directly. Extract: item name, brand, category (dress, jacket, sneakers, bag, etc.), color, material, key details. The product image is the visual reference for how the outfit must look when worn.

### Mode B: Product image(s) provided, no description

**MANDATORY: Visually analyze the product image before writing any prompt.**

Identify:
1. **Item category** — what is it? (dress, jacket, hoodie, jeans, sneakers, heels, handbag, sunglasses, watch, jewelry, etc.)
2. **How it's worn** — put on over head, zip up, button, step into, slip on, clasp, etc.
3. **Key visual details** — color, pattern, fabric texture, cut/silhouette, logos, distinctive features
4. **Styling context** — casual, streetwear, formal, athletic, evening — determines posing style

### Mode C: No product image (text-only)

Extract product information entirely from the text request. No @Image references. Outfit is described in words within the Dynamic Description.

---

## Style & Mood

UGC try-on aesthetic, iPhone on tripod, warm natural lighting from a window, real bedroom or living room. Casual home vibe — not a fitting room, not a studio, not outdoors. Like filming yourself trying on a new delivery.

## Framing

- Full-body or upper-body shot depending on the item:
  - Full outfit / dress / pants / shoes → full-body, person standing
  - Top / jacket / jewelry / sunglasses → upper body, waist up
- Framing slightly off-center — phone propped on a shelf or dresser, not perfect tripod height
- Enough room to see the outfit and movement

## Shot Structure

Hard cuts between distinct moments. NEVER show the person actually changing clothes on camera. The video follows a **before → after** arc:

- **Shot 1 (Own clothes — show the item):** Person in their casual home outfit, holding the actual clothing item in their hands (NOT a box, NOT a bag — the garment itself). They hold it up to camera, maybe unfold it slightly, talk about it excitedly. Or they pick it up from the bed/chair. This is a try-on, not an unboxing — the item is already out of any packaging. NEVER show boxes, bags, parcels, or wrapping in this shot.
- **HARD CUT**
- **Shot 2 (New outfit — reveal):** Person already wearing the new item. First reaction — looking down at themselves, adjusting the fit, checking how it sits, pleasantly surprised. The "wow" moment.
- **Shot 3 (Posing — show off):** Confident posing — turn to show side/back, hands on hips, hip pop, maybe a quick spin or hair toss. Fun energy, not model-stiff. This is the "look at me" shot.
- **Shot 4 (Detail or final pose):** Either a close-up moment — fingers touching fabric texture, showing a label, zipper detail, material quality — OR a final confident pose with a satisfied smile at camera. If duration allows (13-15s), do both via hard cut: detail close-up → final pose.

Each shot = one distinct action or pose. Never repeat the same pose between shots.

## Outfit Consistency

The outfit MUST look identical across all shots where it's worn (shots 2-4) — same color, same fit, same details. If product image is provided, the outfit MUST match the reference. Never invent different colors, patterns, or styles. Shot 1 (own clothes) uses a different casual outfit — simple, neutral, so the new item pops by contrast.

## Audio

Person speaks on camera or voiceover.

Format: `Audio: She speaks to camera, iPhone microphone audio with natural room tone: "Ok so this just came in... let me try it on..."` (for male: `He speaks to camera, iPhone microphone audio with natural room tone: "..."`)

- If user provides specific text: use exactly that
- If no text: auto-generate casual try-on commentary — anticipation before the cut, then first impression of the fit, how it feels, how it looks

## Emotion Logic

Genuine excitement about a new outfit — like trying on something you just ordered online and filming it for your followers.
- Shot 1 (own clothes): Giddy anticipation — "it finally came!"
- Shot 2 (reveal): Checking yourself out — pleasantly surprised, adjusting fit
- Shot 3 (posing): Peak confidence — feeling yourself, showing off
- Shot 4 (detail/final): Satisfied admiration — touching the fabric lovingly, or confident nod at camera

## Human Performance Direction (CRITICAL — prevents wooden/AI-looking characters)

Every prompt MUST include at least 3 of these micro-behaviors woven into the Dynamic Description:

**Micro-behaviors (pick 3+ per prompt, rotate between prompts):**
- Hair flip/toss — flips hair over shoulder while turning, tosses hair back after leaning forward
- Fabric touch — runs fingers along sleeve, feels the texture, adjusts collar or hem
- Hip pop — shifts weight to one hip, then switches to the other
- Sleeve/collar adjust — pulls sleeve up, straightens collar, tugs hem down to check length
- Confidence walk — takes a step or two toward camera, then steps back to show full look
- Quick spin — fast 180 turn to show the back, then turns back with a grin
- Look-down-then-up — checks out the outfit on themselves, then looks up at camera with a smile
- Shoulder shimmy — playful little shimmy when feeling good about the fit
- Hand through hair — runs hand through hair while posing, casual and natural
- Weight shift — rocks slightly from foot to foot, never planted like a statue
- Posture pop — straightens up suddenly when hitting a power pose, relaxes right after

**Expression arc (emotions CHANGE across the video):**
- Shot 1 (own clothes): Excited, slightly impatient — wide eyes, bouncing energy, can't wait
- Shot 2 (new outfit): Surprised satisfaction — eyebrows up, mouth slightly open, then breaking into a grin
- Shot 3 (posing): Peak confidence — smirking, playful eyes, chin slightly up
- Shot 4 (detail/final): Warm satisfaction — soft smile, gentle nod, "yeah, this is it" energy

**ANTI-PATTERNS (never write these — they produce wooden AI look):**
- "stands in front of the camera" (frozen mannequin)
- "poses in the outfit" (vague = stiff)
- "shows the outfit to camera" (robotic presentation)
- "smiles and turns" (static smile + mechanical rotation)
- Perfectly symmetrical poses (real people are asymmetric — one shoulder higher, hip shifted)
- Same expression across all shots (real people's faces CHANGE)

**Instead of:** "She stands in the outfit and poses"
**Write:** "She steps into frame already wearing the dress, one hand on her hip, head tilted, eyebrows raised as she checks herself out, then breaks into a wide grin and does a quick spin, hair swinging, before settling into a confident stance with a playful shoulder shimmy"

## Setting

Real bedroom or living room. Visible in background: bed, mirror edge (but NEVER shoot into the mirror), closet, clothing rack, window with natural light. Slightly messy is OK — real life, not styled. Never studio, never plain backdrop, never outdoors unless user specifies.

## Person Default

Attractive woman (override if user specifies or product is male-targeted). If user describes specific appearance — use that. Person's body type should look natural wearing the item.

---

## Universal Rules

### Outfit Fidelity (when product images are provided)

- The outfit MUST match the reference image exactly — color, pattern, silhouette, details.
- Never invent additional clothing items not shown or described.
- Accessories (bag, watch, jewelry) that are in the reference MUST appear consistently.

### No Changing On Camera

NEVER show the person in the process of putting on or taking off clothing. Use hard cuts — Shot 1: person without the item, Shot 2: person already wearing it. The change happens between cuts.

### Hand Count Rule

The person has exactly 2 hands. Never describe two separate hand actions in the same moment. Maximum 1 action per shot.

### State Change Minimization

- Use hard cuts between outfit states
- Maximum 1 state change per shot
- Never show clothing being pulled on, zipped, or buttoned on camera — hard cut to the finished state

### No Extras Rule

No additional people or random objects beyond the person and the outfit. Keep the scene clean.

### Shot Compression

Compress into ≤ 4 shots. Each shot = one distinct pose or moment. Never repeat the same pose between shots.

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
- **Reflection shots** (mirrors, puddles) — NEVER use. Person may stand NEAR a mirror but camera NEVER shoots into it.
- **Exit + re-entry** in same shot — character leaves = gone for rest of shot

### Density by Duration

| Duration | Sentences in Dynamic Description | Max words in Audio speech |
|----------|--------------------------------|--------------------------|
| ≤ 10s | 4–8 | 12–20 |
| 11–12s | 6–10 | 20–28 |
| 13–15s | 8–14 | 28–35 |

Speech pacing: Casual, slightly rushed, like recording a quick TikTok — not rehearsed. Short phrases with natural pauses ("...").

---

## Prompt Format

Every prompt MUST be a **single continuous string** with inline section labels.

**When product image(s) ARE provided:**
```
[Material references — @Image and <<<element_id>>> declarations]
Style & Mood: [UGC try-on aesthetic, iPhone on tripod, warm natural lighting, real bedroom]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — person wearing outfit, posing, showing details, reacting]
Static Description: [location, props, ambient details]
Audio: [person speaking on camera or voiceover with voice description]
Facial features clear and undistorted, consistent outfit throughout. Shot on iPhone, natural lighting, social media aesthetic, slight natural handheld micro-shake. No on-screen text, no subtitles, no captions, no watermarks.
```

**When NO product image (text-only):**
```
Style & Mood: [UGC try-on aesthetic, iPhone on tripod, warm natural lighting, real bedroom]
Narrative Summary: [1-sentence scene description]
Dynamic Description: [shot-by-shot prose — describe the outfit in words within the scene]
Static Description: [location, props, ambient details]
Audio: [person speaking on camera or voiceover with voice description]
Facial features clear and undistorted, consistent outfit throughout. Shot on iPhone, natural lighting, social media aesthetic, slight natural handheld micro-shake. No on-screen text, no subtitles, no captions, no watermarks.
```

### Material References (only when images are provided)

**Product references:**
- 1 product photo: `@Image1 is the outfit/item reference. The person wears this exact item — matching color, pattern, fit, and details as shown in @Image1 throughout all shots.`
- 2+ product photos: `@Image1 and @Image2 are outfit references. The person wears these exact items as shown.`

**Person references:**
- Person photo as `@ImageN`: `@ImageN is the person reference.`
- Person as element: `<<<element_id>>> is the person.`
- No person: omit — the engine uses the person description from the prompt

**Order rule:** Product images first, then person image (if any).

---

## Defaults

| Parameter | Default |
|---|---|
| Duration | 10 seconds |
| Aspect ratio | 9:16 (vertical) |
| Person | Attractive woman |
| Setting | Home — bedroom with natural window light |
| Audio | Person speaks on camera (always on) |
| Language | English |
| Shots | ≤ 4 (before → reveal → posing → detail/final) |
| Tone | UGC try-on haul, casual, excited |
