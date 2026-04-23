# Seedance 2.0 — Style System (Three-Axis + Custom)

Three independent axes control the visual identity of every generation. Each axis accepts either a **preset string** (LOCKED — inject as-is, director cannot override) or **null** (Auto Fallback — director chooses based on scene content, genre, and reference images).

When building prompts, the style axes are injected at specific positions — see the output format in `SKILL.md` for placement rules.

---

## Axis 1 — Camera Style (10 Presets)

Movement vocabulary. The director/DP name is the primary style anchor for Seedance (~70% of visual output); technical descriptors are fine-tuning (~30%).

### Injection Rules

- Insert the full string as-is into the prompt — never paraphrase, reorder, or omit
- Never add film titles — they trigger NSFW in Seedance. Use director names only
- Negative constraints at the end of each string are mandatory — always preserve
- If preset is **One Take** → force single-shot mode, no cuts
- Camera Style does not affect light or color — those are separate axes

### Presets

| Preset | Anchor | Movement Character | Best For |
|---|---|---|---|
| **Classic Static** | Hitchcock | Locked tripod, slow mechanical dolly on rails, deep one-point perspective | Formal drama, mystery, symmetrical compositions |
| **Silent Machine** | Fincher | Imperceptible motorized movement, technocrane, zero shake | Psychological thriller, precision, controlled tension |
| **One Take** | Lubezki | Single continuous Steadicam, no cuts, circular flow | Immersion, real-time experience, journey through space |
| **Epic Scale** | van Hoytema | IMAX aerial, 360° orbit, crash dolly, speed ramps | Spectacle, large-scale action, epic landscapes |
| **Intimate Observer** | Sean Baker | Subtle handheld, operator breathing, near-static micro-sway | Indie drama, observational, intimate moments |
| **Impossible Camera** | Spike Jonze | First-person flight, robotic arm, spiral orbit, passes through gaps | Fantasy, surreal, music video, inventive movement |
| **Documentary Snap** | Vinterberg | Snap zoom on sound, whip pan, camera searching then committing | Raw realism, Dogme-style, reactive journalism |
| **Raw Chaos** | Greengrass | Aggressive handheld, crowd collisions, dirt on lens, focus hunting | War zones, riots, visceral action, survival |
| **Dreamy Flow** | Doyle | Gentle sway, slow push-in, shallow DOF, intimate through narrow gaps | Romance, mood pieces, atmospheric slow-burn |

### Full Preset Strings (for prompt injection)

**Classic Static:** `Cinematographic style of Alfred Hitchcock, locked tripod static, slow mechanical dolly push and pull on rails, old dolly track vibration subtly present in frame, deep one-point perspective, centered vanishing point, classical Hollywood master shot, deliberate unhurried mechanical movement, no handheld, no Steadicam, no crane, no organic movement, no off-center composition, no mirror effect, no artificial symmetry line`

**Silent Machine:** `Cinematographic style of David Fincher, imperceptible dolly forward on rails, micro push-in on motorized slider, technocrane vertical descent, mechanical orbit on circular track, mechanically perfect stabilization, subliminal camera pressure, movement so slow it only registers after several seconds, zero shake, zero human presence in the movement, no handheld, no snap movement, no zoom, no organic texture, no visible camera operation`

**One Take:** `Cinematographic style of Emmanuel Lubezki, single continuous Steadicam shot, one unbroken take, no cuts, no montage, camera arcs and weaves through the space in continuous flow, circular journey through the environment, smooth floating movement following and discovering action, no static tripod, no locked frame, no loss of spatial continuity, one unbroken shot`

**Epic Scale:** `Cinematographic style of Hoyte van Hoytema, shot on ARRI Alexa 65 IMAX, aerial camera descent, rotating 360-degree orbit at low angle, fast dolly charge forward, slow-motion speed ramp from real time to extreme slow motion and back, epic scale large sweeping camera movements, every movement large and designed for IMAX scale, no static tripod, no subtle movement, no intimate distance, no handheld shake, no documentary feel`

**Intimate Observer:** `Cinematographic style of Sean Baker, subtle handheld with operator body weight shift, camera rises and falls gently with operator breathing, near-static micro-sway, framed through foreground objects and steam and gaps, intimate observation distance, camera watches without intervening, operator body tremor visible in gentle frame movement, no aggressive handheld, no snap movement, no crane, no dolly, no zoom, no choreographed camera path`

**Impossible Camera:** `Cinematographic style of Spike Jonze, first-person camera flight through space at high speed, robotic arm executing complex programmed path, continuous tightening spiral orbit collapsing onto subject, camera passing through physical gaps and layers, whip-pan transitions, every shot contains a camera move that feels inventive or physically impossible, no conventional coverage, no simple tripod, no documentary handheld, no drone or camera rig visible in frame`

**Documentary Snap:** `Cinematographic style of Thomas Vinterberg, handheld snap zoom punching in on subject motivated by sound, whip pan reacting to off-screen event, snap zoom overshooting and correcting, rack focus between foreground and subject, every camera reaction motivated by an in-scene event, camera searching then finding then committing to its subject, no smooth movement, no dolly, no crane, no precomposed framing`

**Raw Chaos:** `Cinematographic style of Paul Greengrass, aggressive handheld in crowd, shoulders jostling camera, crowd collisions shaking frame, rain and dirt and grime on the lens, water droplets smearing across glass, focus hunting losing and locking, camera ducking and flinching, sprint tracking alongside action, low aggressive angles, no stability, no dolly, no crane, no composed framing, no beauty, no control`

**Dreamy Flow:** `Cinematographic style of Christopher Doyle, handheld gentle sway side to side, slow push-in, intimate framing through narrow gaps between objects, slow motion achieved through high frame rate not low shutter, shallow depth of field dissolving background into soft circles, camera at arm's length intimate distance, sinking descent into the mood, no step-printing, no undercranking, no low shutter speed, no motion blur, no fast movement, no aggressive handheld`

### Control Spectrum

```
Full control:    Classic Static → Silent Machine → Epic Scale
Guided flow:     One Take → Impossible Camera → Dreamy Flow
Organic chaos:   Intimate Observer → Documentary Snap → Raw Chaos
```

### Dialogue Compatibility

- **Best:** Classic Static, Silent Machine, Intimate Observer, Dreamy Flow
- **Challenging but workable:** Epic Scale (ceremonial crane descent), Impossible Camera (tightening spiral), Documentary Snap (reactive)
- **Worst:** Raw Chaos (too unstable to read faces and micro-expressions)

---

## Axis 2 — Light Style (6 Presets + 2 Modifiers)

### Philosophy

1. **Soft light, dark shadows, high contrast.** Staged sources are always large and diffused — no bare point sources. But contrast stays high: deep dark shadows, not filled.
2. **Staged light ONLY from opposite camera side.** Cross-light, backlight, overhead-from-behind — never frontal, never from camera axis.
3. **Either fully staged or fully natural.** No hybrids.

### Injection Rules

- Insert the full string as-is — never paraphrase or omit
- Never describe light color or temperature in the Light string — that belongs to the Color axis
- Negative constraints are mandatory
- **Describe sources, not effects.** In scene description, name what emits light (lamp, window, candle) and where it is. Never describe lighting effects on surfaces ("rim light on shoulders", "spill on face"). Seedance interprets effect descriptions as direct drawing instructions and overrides natural physics.

### Staged Presets (DP-controlled, no visible sources)

**Soft Cross:** `Lighting: single large soft diffused source at 90 degrees to camera axis, lighting the subject from the side, soft shadow falloff across the face with the camera-facing side in deep dark shadow, high contrast between the lit half and the shadow half, shadow side dark but not absolute black — faint ambient keeps minimal detail, every surface in the scene follows the same single-source side lighting, no frontal light, no light from camera direction, no fill light, no flat even illumination, no hard sharp-edged shadows, no multiple light sources`

**Contre-jour:** `Lighting: single large soft diffused source behind the subject opposite the camera, soft backlight wrapping a rim of light around head and shoulders and hair, face predominantly in shadow with only faint scattered ambient making features barely readable, deep dark shadows on all camera-facing surfaces, high contrast between bright backlit edges and dark front, the background behind the subject is brighter than the subject, no frontal light, no light from camera direction, no flat even illumination, no hard sharp-edged shadows, no full silhouette — the face must remain slightly readable`

**Overhead Fall:** `Lighting: single large soft diffused source above and behind the subject angled downward, light falling onto top of head and shoulders and upper back, soft spill reaching the forehead while eyes sit in soft shadow under the brow ridge, deep dark shadows below the chest and on the lower body, high contrast between lit upper body and dark lower areas, the floor beneath the subject receives faint light spill, no frontal light, no light from camera direction, no side light, no flat even illumination, no hard sharp-edged shadows, no direct top-down overhead — the source is angled from behind not from directly above`

### Natural Presets (only real sources in frame)

**Window:** `Lighting: only natural daylight from a window, no artificial light sources, no lighting equipment, soft directional daylight entering through the window creating a natural gradient from bright near the glass to dark far from it, deep dark shadows in areas the window does not reach, high contrast between window-lit and shadow areas, the architecture alone determines where light falls, no fill light, no bounce boards, no reflectors, no practicals turned on, no overhead lights, no flat even illumination`

**Practicals:** `Lighting: only practical light sources visible within the frame — table lamps candles screens neon signs street lamps bare bulbs, no lighting equipment outside the frame, each practical creates its own pool of light on nearby surfaces, deep darkness between and beyond the pools, high contrast between lit areas and surrounding darkness, the practicals are the brightest objects in frame, no fill light, no bounce, no hidden supplemental lighting, no flat even illumination, no uniform ambient`

**Silhouette:** `Lighting: subject completely backlit by a bright background, the subject reads as a solid dark shape with no visible surface detail on the camera-facing side, only the outline and contour are defined by the bright background behind, maximum contrast between bright background and dark subject, no fill light on the face, no rim light separating the subject from dark surroundings, no readable facial features, no surface texture on the subject, no flat even illumination — only shape against light`

### Modifiers (independent toggles, on top of any preset)

| Modifier | Effect |
|---|---|
| **Haze** (on/off) | Atmospheric haze or mist, light beams partially visible, distant objects softened |
| **Volumetric Beams** (on/off) | Visible light rays in smoke/dust/fog, god rays, shafts of light as solid volumes |

---

## Axis 3 — Color Style (8 Presets)

### Injection Rules

- Insert the full string as-is — never paraphrase or omit
- The phrase "applied uniformly to the entire frame" is mandatory — without it Seedance applies color locally
- Never describe skin/face/body color in the grade — Seedance draws a colored spot, not color correction
- Never use percentages ("30% saturation") — Seedance is not calibrated to numeric values
- Film stock references belong here, not in Camera Style
- Negative constraints are mandatory

### Optional Film Reference Reinforcement

Adding `color palette of [Film Name]` to the Camera Style line improves color accuracy when the film matches the scene mood. Only use films shot digitally or with clean mastering — avoid heavy-diffusion films (Se7en, Schindler's List).

### B&W Rule

When Classic B&W is selected: strip all color adjectives from scene description. Add `Black and white film` to Camera Settings block.

### Presets

| Preset | Color Style String | Film References |
|---|---|---|
| **Naturalistic Clean** | `Kodak Vision3 250D color response, color grade applied uniformly to the entire frame: neutral balanced color, no dominant cast, true reds, true blues, true whites, open shadows, gentle highlight roll-off, zero stylization, straight from camera with minimal grading, no color cast, no teal-orange, no bleach, no desaturation` | Nomadland, Roma |
| **Bleached Warm** | `Kodak Vision3 500T color response pushed warm, color grade applied uniformly to the entire frame: single dominant amber-golden cast, shadows warm brown, highlights creamy yellow, greens suppressed, blues muted to grey-green, fluorescent lamps turn buttery, concrete walls warm tan, night sky warm umber, sun-faded vintage warmth everywhere, no teal, no neon, no cool tones, no desaturation` | Amelie, The Grand Budapest Hotel, 1917 |
| **Hyper Neon** | `Fuji Velvia color response, color grade applied uniformly to the entire frame: hyper-saturated neon palette, magenta-green split toning, magenta in highlights, green in shadows, reds glow electric crimson, blues electric cyan, fluorescent pushes acid green, blacks crushed to deep violet, all colors pushed to maximum saturation, no naturalism, no warm bleach, no desaturation, no monochrome` | Enter the Void, Only God Forgives, Spring Breakers |
| **Teal & Orange Epic** | `Kodak Vision3 500T color response, color grade applied uniformly to the entire frame: complementary split toning, shadows and cool areas pushed deep teal-cyan, warm areas pushed warm orange, fluorescent turns cyan, concrete teal in shadow, warm windows glow amber-orange, strong two-tone warm lit areas against cool shadowed areas, no neon magenta, no bleach, no monochrome, no single-note amber` | Mad Max Fury Road, Blade Runner 2049 |
| **Sodium Decay** | `Color grade applied uniformly to the entire frame: post-grade LUT applied globally, black point lifted into emerald fluorescent green, every shadow glows green-cyan never neutral black, highlights pushed into sickly sodium amber-yellow, midtones muddy brown-olive heavily desaturated, two-tone split amber above green below dominates the frame, no clean naturalism, no neutral blacks, no warm shadows, no single-note amber, no structural noise` | Zodiac |
| **Cold Steel** | `Fuji Eterna 500 color response, color grade applied uniformly to the entire frame: desaturated blue-grey wash, steel-blue midtones, shadows deep navy-slate, highlights cool and metallic with zero warmth, reds muted to dusty mauve, greens to grey-teal, yellows to dirty khaki, concrete reads cold blue-grey, clinical cold, no warm tones, no amber, no neon, no green cast` | Sicario, Prisoners, Arrival |
| **Bleach Bypass** | `Color grade applied uniformly to the entire frame: harsh contrast, heavy desaturation, crushed blacks, silvery blown highlights, reds dull to brick-grey, metallic brown tones, image reads as if metallic silver is baked into the emulsion, window lights blow out into near-white silver hot spots, stark grey-silver surfaces, no clean color, no neon, no warm gold, no full monochrome, no soft contrast` | Saving Private Ryan, Minority Report |
| **Classic B&W** | `Black and white film, color grade applied uniformly to the entire frame: full monochrome, zero color information, deep rich blacks, glowing highlights, full tonal range, composition reads through luminance only, no color tint, no sepia, no duotone, no color leak` | Roma, The Lighthouse |

---

## DP Combo Presets (8 ready-made bundles)

Pre-built combinations that set all axes at once. Use as starting points or when the user asks for a "look" by reference.

| Recipe | Camera Style | Light | Color | Body | Lens | Focal | f/ |
|---|---|---|---|---|---|---|---|
| **Monumental Atmosphere** (Deakins) | Classic Static | Window | Bleached Warm | Clean Digital | Anamorphic | 35mm | f/4 |
| **Floating Real** (Lubezki) | One Take | Window | Naturalistic Clean | Clean Digital | Clinical Sharp | 14mm | f/4 |
| **Prince of Darkness** (G. Willis) | Classic Static | Soft Cross | Bleached Warm | Fine Film | Clinical Sharp | 50mm | f/4 |
| **Neon Pulse** (Doyle) | Dreamy Flow | Practicals | Hyper Neon | Fine Film | Vintage Haze | 35mm | f/1.4 |
| **Warm Horizon** (van Hoytema) | Epic Scale | Contre-jour | Teal & Orange Epic | Clean Digital | Anamorphic | 35mm | f/4 |
| **Candle Intimacy** (B. Young) | Classic Static | Practicals | Bleached Warm | Fine Film | Warm Halation | 50mm | f/1.4 |
| **Sculpted Sci-Fi** (G. Fraser) | Silent Machine | Soft Cross | Cold Steel | Clean Digital | Clinical Sharp | 50mm | f/4 |
| **Urban Decay** (D. Khondji) | Intimate Observer | Practicals | Sodium Decay | Fine Film | Vintage Haze | 35mm | f/4 |

---

## Compatibility Guide

### Strong Combinations (tested, reliable)

- Classic Static + Window + any warm color = contemplative cinema (Deakins territory)
- Silent Machine + Soft Cross + Cold Steel = clinical thriller (Fincher territory)
- Dreamy Flow + Practicals + Hyper Neon = sensory overload (Wong Kar-wai territory)
- Classic Static + Soft Cross + Bleached Warm = golden age Hollywood (noir, drama)
- One Take + Window + Naturalistic Clean = immersive realism (Lubezki territory)

### Conflict Zones (use with caution)

- Raw Chaos + Silhouette → chaotic camera but subject is just a dark shape — nothing to track
- Epic Scale + Practicals → IMAX movement wants open space; practicals want dark interiors
- Impossible Camera + Classic Static → contradicts (inventive movement vs locked tripod)
- Documentary Snap + any staged light → snap zoom implies reaction, staged light implies control
- 8mm Fisheye + f/1.4 → fisheye has natural deep DOF, shallow DOF instruction fights the physics
- Raw 16mm + Clinical Sharp → heavy grain fights clean lens rendering

---

## Custom Styles (Beyond Presets)

Presets cover common looks. When no preset fits — compose custom style strings for any axis.

### When to Use Custom Styles

- No existing preset matches ("something between Deakins and Lubezki")
- Reference image doesn't map to any preset
- Scene needs a look not covered by the preset set
- User describes a specific DP, era, or technique not in the 10/6/8 options

### How to Build Custom Strings

Follow the same structure as presets: **anchor name → technical description → negative constraints.**

#### Camera Style — Custom Template

```
Cinematographic style of [Director/DP Name], [primary movement type], [secondary movement],
[stabilization character], [spatial relationship to subject], [emotional quality of movement],
no [anti-pattern 1], no [anti-pattern 2], no [anti-pattern 3]
```

**Additional DP anchors for custom camera styles:**

| DP/Director | Movement Character | Use When |
|---|---|---|
| Terrence Malick / Lubezki | Flowing natural light, magic-hour Steadicam, gravitational drift | Poetic realism, nature, existential |
| Wong Kar-wai / Doyle | Step-printed slo-mo, neon reflections, intimate handheld | Urban romance, loneliness, sensory |
| Denis Villeneuve / Deakins | Geometric precision, slow dolly, negative space | Sci-fi, existential tension, silence |
| Andrei Tarkovsky / Rerberg | Ultra-long take, slow lateral tracking, rain/water/fog | Spiritual, meditative, time-as-subject |
| Ridley Scott / J. Mathieson | Smoke-filled wide shots, crash zoom, handheld in chaos | Historical epic, battlefield, grit |
| Stanley Kubrick / Alcott | Symmetrical one-point, slow zoom, Steadicam corridor | Psychological horror, institutional power |
| Michael Mann / D. Spinotti | Digital night, handheld telephoto, city as organism | Crime, urban isolation, nocturnal |
| Wes Anderson / R. Yeoman | Centered framing, lateral tracking, whip-pan between setups | Comedy, symmetry, storybook |
| Park Chan-wook / C.H. Chung | Surgical crane, slow overhead descent, claustrophobic framing | Thriller, revenge, controlled violence |
| Sofia Coppola / L. Acord | Static wide holds, natural window light, negative space | Isolation, youth, languor |

#### Light Style — Custom Template

```
Lighting: [source type and position], [quality: soft/hard, diffused/direct],
[shadow character], [contrast level], [spatial falloff description],
no [anti-pattern 1], no [anti-pattern 2]
```

**Additional light approaches:**

| Style | Description | Use When |
|---|---|---|
| **Chiaroscuro** | Extreme contrast, face half-lit, Caravaggio-level drama | Noir, power scenes, moral ambiguity |
| **Firelight** | Flickering warm practicals, dancing shadows on walls | Period, intimacy, ritual |
| **Neon Wash** | Multiple colored practicals bleeding into each other, no neutral areas | Nightclub, cyberpunk, music video |
| **Moonlight** | Cool single source from high angle, blue-silver, gentle falloff | Night exterior, romantic, mysterious |
| **Fluorescent** | Overhead tubes, flat greenish, institutional, unflattering | Hospital, office, interrogation, discomfort |
| **Mixed Temperature** | Warm practicals vs cool window/ambient in same frame, split warmth | Transitional spaces, dusk, emotional conflict |

#### Color Style — Custom Template

```
[Film stock reference if applicable] color response, color grade applied uniformly to the entire frame:
[dominant cast], [shadow color], [highlight color], [midtone character],
[how specific colors shift], [saturation level],
no [anti-pattern 1], no [anti-pattern 2]
```

**Additional color approaches:**

| Style | Description | Use When |
|---|---|---|
| **Cross-processed** | Greens shift cyan, reds shift orange, lifted blacks, chemical look | 90s aesthetic, fashion, music video |
| **Day-for-night** | Blue wash over everything, crushed shadows, silver highlights | Faux moonlight, dream sequence |
| **Tobacco** | Amber-brown monochrome with olive undertones, no pure black | Western, dust, desolation |
| **Candy Pastel** | Lifted shadows, desaturated pastels, cotton-candy pinks and mints | K-pop, kawaii, Wes Anderson, soft nostalgia |
| **Infrared** | Foliage glows white/pink, sky dark, skin tones alien | Experimental, otherworldly, music video |
| **Vintage Polaroid** | Faded, lifted blacks, cyan shadow cast, warm highlight bloom | Memory, nostalgia, amateur aesthetic |

### Prefer Presets When They Fit

Presets are tested and reliable with Seedance. Use custom strings when presets genuinely don't cover the need. When composing custom, always include "applied uniformly to the entire frame" in color strings, and always include negative constraints in all axis strings.

---

## Auto Fallback Tables

When an axis is null, the director selects based on scene content, genre, archetype, and reference images.

### Camera Auto Fallback

| Scene Type | Default Choice | Rationale |
|---|---|---|
| Dialogue (psychological) | Silent Machine or Classic Static | Precision serves tension |
| Dialogue (intimate) | Dreamy Flow or Intimate Observer | Closeness serves emotion |
| Dialogue (reactive) | Documentary Snap | Camera reacts to events |
| Action — urban close-quarters, foot pursuit in tight spaces | Raw Chaos or Documentary Snap | Proximity + claustrophobia |
| Action — highway pursuit, vehicle-heavy, open terrain | Epic Scale (George Miller style — wide tracking, speed ramps, crash dolly alongside vehicles) | Scale + velocity on open road |
| Action — LINEAR flowing chase or continuous fight | One Take or Epic Scale | Immersion/scale |
| Action — precision combat, duel, martial arts | Silent Machine | Controlled intensity |
| Action — rooftop/vertical pursuit or stunt | Raw Chaos + low-angle emphasis | Height vertigo + instability |
| Action — crowded environment (market, station) | Documentary Snap or Intimate Observer | Reactive camera searching through bodies |
| General (landscape/journey) | Classic Static or Epic Scale | Stillness or scale |
| General (atmosphere) | Dreamy Flow or Intimate Observer | Mood |
| General (montage) | Documentary Snap or Classic Static | Rhythm |

### Light Auto Fallback

| Scene Mood | Default Choice |
|---|---|
| Power, dominance, muscle | Soft Cross (high-contrast side light) |
| Grounded, practical environment | Practicals |
| Scale, epic, volumetric | Add Haze + Volumetric Beams to any preset |
| Intimate, quiet | Window or Soft Cross |
| Mystery, silhouette | Contre-jour or Silhouette |
| Overhead drama, eye shadow | Overhead Fall |
| Transitional spaces (corridors, stairwells, tunnels, underpasses) | Mixed practical + ambient — warm practicals on walls vs cool ambient from openings, uneven pools of light |

### Color Auto Fallback

| Scene Mood | Default Choice |
|---|---|
| Neutral documentary | Naturalistic Clean |
| Warm nostalgia | Bleached Warm |
| Nightlife, neon, cyberpunk | Hyper Neon |
| Blockbuster, epic | Teal & Orange Epic |
| Urban decay, crime | Sodium Decay |
| Cold thriller, sci-fi | Cold Steel |
| War, gritty | Bleach Bypass |
| Art cinema, noir | Classic B&W |
| Street-lit night pursuit, sodium lamps vs cool shadow | Sodium/tungsten amber in lit pools against cold blue-steel in shadow — split warm/cool within frame, no single-cast dominance |

---

## Session Lock (Multi-Clip Consistency)

When generating multiple clips in a sequence, lock these for the entire session:

| LOCKED (set once) | Why |
|---|---|
| Camera Style | Movement vocabulary must be consistent across clips |
| Light Style | Light direction/quality is the visual thread |
| Color Style | Color grade is the most noticeable discontinuity |
| Camera Body | Grain/sensor character must match |
| Lens | Optical rendering (bokeh, haze) must match |

**Per-clip variables** (change freely): genre, focal length, aperture, global_prompt, duration.

Focal length / aperture rule: **auto for multi-shot clips** (director picks per shot), **specific value for single-shot clips** (one take needs locked focal).

### Breaking the Lock

Only on explicit user request. Warn: "This will break visual continuity with previous clips. The style shift will be visible in the final cut."
