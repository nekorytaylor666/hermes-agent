# Seedance 2.0 — Style Vocabulary & Genre System

## Style Keywords

| Category | Keywords |
|----------|---------|
| Quality | Cinematic feel, film-like texture, 8K, HDR, RAW quality, 16mm film, 35mm tungsten stock |
| Visual | Hollywood blockbuster, independent film, documentary, music video, commercial, 2.35:1 widescreen, anamorphic |
| Color | Warm tones, cool tones, high contrast, low saturation, Morandi color scheme, cyberpunk neon, desaturated, chiaroscuro |
| Art | Realism, Surrealism, Minimalism, Vaporwave, Cyberpunk, Chinese ink painting |
| Light | Natural light, side-backlighting, Tyndall effect, neon, moonlight, golden hour, volumetric light, God rays, practical sources |
| Animation | Chinese fantasy, ultra-detailed CG, Japanese anime cel, realistic 3D rendering |
| Texture | Film grain, heavy grain, underexposed, overexposed, shallow DOF, telephoto compression |

## Genre Modifier System

Genre controls **tempo, camera texture, palette, sound**. Scene archetype controls **shot pattern and spatial logic**.

| Genre | Tempo & Cuts | Camera Style | Palette & Light | Sound Design |
|-------|-------------|-------------|-----------------|-------------|
| **Action** | Fast cuts, whip-pans on transfers | Handheld, dynamic tracking, speed ramps | High contrast, harsh side-light | Impact SFX, low-end drone, silence before hit |
| **Horror** | Slow. Cuts rare and significant | Static wide + empty space. Slow push-in. Restricted framing | Practical only. Half-shadow. Flicker | Ambient hum, creak, distant sound. Atonal drone |
| **Comedy** | Follows timing. Setup normal, payoff hold | Wider framing, static holds. Cut for reaction | Bright, flat, even. Faces readable | Beat of silence before punchline. Exaggerated foley |
| **Noir** | Medium. Cuts on power shifts | Low-angle dominant, Dutch on compromise. Dirty OTS | Chiaroscuro. Hard light through blinds. Practical neon | Jazz, rain, glass clinking, urban night |
| **Epic** | Slow, ceremonial. Each frame = painting | Crane, aerial, extreme wides. Low-angle for authority | Volumetric God rays. Firelight. Rich saturated | Orchestral underscore. Room reverb. Distant weather |
| **Drama** | Deliberate. Each cut has weight | Close, shallow DOF, subtle dolly, eye-level | Naturalistic soft light. Single source (window, lamp) | Room tone. Breathing audible. Solo instrument or silence |

**If no genre specified:** determine camera, tempo, palette, and sound from archetype and scene content alone.

**Priority chain:** User-specified camera → Archetype spatial logic → Genre texture → Feasibility limits.

## Aspect Ratio Guidelines

| Ratio | Best For |
|-------|----------|
| 2.39:1 | Lateral movement, tight vertical, panoramic landscapes |
| 9:16 | Single-character, vertical movement, mobile format |
| 1:1 | Centered, symmetrical, social media |
| 16:9 | Default widescreen |

If not specified, don't mention in prompt.
