# Seedance 2.0 — Camera Type (4 Sub-Axes)

Compound axis: Camera Body + Lens + Focal Length + Aperture. Each sub-axis is injected at a different position in the prompt. All four combine freely with Camera Style, Light Style, and Color Style.

---

## Sub-Axis 1 — Camera Body

Injected as the opening line of the prompt, before character references and scene description.

### Rules

- Insert the full string as-is — never paraphrase or omit
- Camera Body defines sensor/stock and grain only — does not affect movement, light, or color
- One Camera Body per prompt
- Negative constraints are mandatory

### Presets

| Preset | Body String |
|---|---|
| **Clean Digital** | `Shot on ARRI Alexa 35 digital cinema camera, clean sensor, without grain or noise, 8K resolution, no film grain, no analog texture, no noise` |
| **Fine Film** | `Shot on Panavision Millennium XL2, 35mm Kodak Vision3 50D film stock, ultra-fine structured film grain, dense analog texture enhancing detail, rich organic color depth, smooth highlight roll-off, high micro-contrast, sharp natural optical rendering, no digital noise, pure high-budget analog film quality, 8K scan resolution` |
| **Raw 16mm** | `Shot on Arriflex 16SR, 16mm film, ultra heavy film grain, huge coarse grain particles dominating the entire frame, aggressively pushed 16mm film, severe analog noise, underexposed and pushed in development, grain crawling and boiling, harsh textured shadows, raw dirty imperfect film look, no denoising, no smoothing, no clean pixels` |

---

## Sub-Axis 2 — Lens

Two mandatory parts: **Prefix Tag** (appended to Camera Body line) + **Rendering String** (woven into scene narrative after shot composition).

### Rules

- Both parts are mandatory — prefix alone is insufficient, Seedance needs the rendering description inside the scene
- Do not describe optical effects as happening TO the character ("light dances across her face") — describe what the lens does to the image
- One Lens per prompt

### Presets

| Preset | Prefix Tag | Rendering String |
|---|---|---|
| **Vintage Haze** | `Vintage uncoated Cooke Speed Panchro lens, wide open` | `Cooke Speed Panchro soft focus rendering — overall image haze, low contrast, low micro-contrast, rainbow-edged lens flares and iridescent ghost reflections from bright sources, corner sharpness falls off heavily, chromatic fringing on high-contrast edges, creamy bokeh, no detail in out-of-focus areas, soft diffused skin` |
| **Warm Halation** | `Vintage Kowa Cine Prominar spherical lens, wide open` | `Kowa Cine Prominar halation rendering — warm glowing halos bleeding outward from every bright source, soft focus, low micro-contrast, creamy smooth skin tones, iridescent rainbow edges on blooming highlights, warm highlight roll-off, chromatic aberration on bright edges` |
| **Anamorphic** | `Panavision C-Series anamorphic lens` | `Panavision C-Series anamorphic rendering — all out-of-focus light sources render as oval horizontally stretched bokeh not round, oval bokeh prominent throughout the background, anamorphic edge falloff soft toward frame edges sharp in center, no horizontal lens flare streaks` |
| **Extreme Macro** | `Laowa 24mm probe macro lens` | `Laowa probe lens at scale-level, deep tunnel perspective, strong parallax, razor-sharp at focal plane, infinite soft depth behind, continuous push forward` |
| **Clinical Sharp** | `ARRI Signature Prime lens, large format` | `ARRI Signature Prime rendering — high resolution, soft micro-contrast, no harshness on skin, ultra-creamy round bokeh smooth edges no onion rings, strong 3D subject separation from background, clean color in out-of-focus areas` |

---

## Sub-Axis 3 — Focal Length

Woven into the first line of the shot description together with shot size. Contains `[camera motion]` placeholder — replace with movement vocabulary from the Camera Style axis (or from the chosen DP's style if Camera Style is null).

### Rules

- Focal length and shot size must be stated together (e.g., "Medium wide shot 35mm")
- Do not use focal length as a separate prefix — it is part of the shot description
- At least 1 shot must use the selected focal length; director may vary in other shots
- Seedance does not reliably distinguish telephoto above 75mm — use shot terminology (choker, ECU) instead of mm numbers for close-ups

### Presets

| Preset | Shot Description String |
|---|---|
| **8mm Fisheye** | `Ultra-wide shot 8mm fisheye — [camera motion]. Fisheye distorts all straight lines, walls curve outward into a sphere, ground bulges toward camera, exaggerated deep barrel distortion, foreground objects oversized and bent, everything from near foreground to infinity in deep focus` |
| **14mm Ultra-Wide** | `Wide shot 14mm — [camera motion]. Ultra-wide captures full environment, foreground objects disproportionately large, strong perspective exaggeration near objects huge far objects tiny, aggressive convergence of parallel lines, deep depth of field` |
| **35mm Standard** | `Medium wide shot 35mm — [camera motion]. Framed from knees up, natural perspective close to human vision, balanced spatial relationships between all depth planes, no distortion, no compression` |
| **50mm Normal** | `Medium shot 50mm — [camera motion]. Framed from waist up, natural proportions of face and body, no distortion, no compression, neutral depth, natural spatial relationships` |
| **75mm Close-Up** | `ECU extreme close-up, 75mm telephoto lens, very shallow depth of field — [camera motion]. Framed tight from chin to forehead, face filling the entire frame, telephoto compression flat perspective, background completely out of focus heavy bokeh no readable detail behind the subject, only the eyes and nose bridge critically sharp ears falling out of the thin focal plane` |

---

## Sub-Axis 4 — Aperture

Woven into the shot description after focal length, stated together with depth of field. Describes the resulting focus/blur for three depth planes (foreground, subject, background).

### Rules

- Aperture and DOF must be stated together
- Aperture is LOCKED globally — applies to ALL shots in the generation
- Describe three depth planes so Seedance has concrete rendering targets

### Presets

| Preset | Aperture String |
|---|---|
| **f/1.4 Wide Open** | `Aperture f/1.4 wide open, extremely shallow depth of field — only subject face in sharp focus, nearest foreground objects completely dissolved into soft blur, background melts into abstract color shapes and smooth circles of bokeh, maximum subject separation` |
| **f/4 Moderate** | `Aperture f/4 moderate depth of field — subject face and upper body in sharp focus, near foreground slightly soft but readable, background soft but shapes and postures recognizable, texture partially visible` |
| **f/11 Deep Focus** | `Aperture f/11 deep focus everything sharp — entire frame in sharp focus from near foreground to far background, no bokeh, no blur, scene reads as one unified sharp composition` |

---

## Seedance Limitations for Camera Type

- Focal lengths >75mm not reliably distinguished — use shot terminology (choker, ECU)
- Lens rendering must be woven into scene narrative, not as a separate prefix block
- Never describe optical effects narratively/metaphorically — Seedance renders literally ("tower merged with spine" = tower rendered inside the character)
- Prismatic effects (prism, crystal filter) do not work — artifacts walk across the character
- Petzval swirl bokeh does not work
- Lensbaby tilt-shift does not work
- Anamorphic horizontal flare streaks look bad — use only oval bokeh

---

## Combined camera_settings String Format

When Camera Body + Lens + Focal Length + Aperture arrive as a single `camera_settings` string from the UI:

```
[Body + Lens prefix] | [Lens rendering description] | [focal_length_mm], f/[aperture]
```

**Parsing:**
- Before `|` = Camera Body + Lens Prefix
- After `|` = Lens Rendering
- Second-to-last comma value = Focal Length (mm)
- Last value = Aperture

**When camera_settings is null:** director selects all four sub-axes. Default: "Shot on modern digital cinema camera, clean sensor. Focal length: 35mm, Aperture: f/2.8."
