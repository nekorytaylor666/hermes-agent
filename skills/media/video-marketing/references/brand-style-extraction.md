# Brand Style Extraction

Extracts brand identity from any source (website, Instagram, any URL) and produces a Brand Style Brief that modifies how video prompts are built — character styling, location, speech tone, motion design colors.

## When to Activate

This reference activates when the user **explicitly requests brand-styled content**. Trigger signals:

- "in the brand style", "in the style of the site/brand", "brand identity", "brand colors"
- "spokesperson for the brand", "brand representative", "brand ambassador"
- "video in the style of the website/Instagram", "match the brand", "brand aesthetic"
- Russian equivalents: "в стиле бренда", "в айдентике", "в фирменных цветах", "фирменный стиль", "стилистика сайта"

**NOT a trigger:** Just a URL + "make a video about this product" — that's normal product extraction, not brand style.

---

## Step 1: Source Detection & Fetching

Detect what the user provided and extract raw data.

### Website URL

```bash
fetchcli fetch --url "USER_URL" --formats markdown,screenshot```

This returns JSON with:

- `data.screenshot` — URL to a full-page screenshot PNG
- `data.markdown` — page text content in markdown

If the homepage is sparse, also discover more pages:

```bash
fetchcli map --url "USER_URL"```

Pick the most brand-relevant page (About, flagship product, hero page) and fetch it too.

### Instagram Profile

```bash
instagramcli user --username "USERNAME" --poll
```

Then fetch recent posts for visual analysis:

```bash
instagramcli posts --user-id "USER_ID" --count 9 --poll
```

Extract from:

- **Profile photo + bio** — brand personality
- **Recent 9 posts** — visual style, color palette, content tone
- **Post captions** — tone of voice

### Any Other URL

```bash
fetchcli fetch --url "USER_URL" --formats markdown,screenshot```

---

## Step 2: Download & Read the Screenshot (MANDATORY)

**CRITICAL: You MUST download and visually read the screenshot. Without this, you are blind to the brand's visual identity — colors, layout, typography, mood. Do NOT skip this step.**

### 2a. Download the screenshot

Extract the screenshot URL from the fetch response and download it:

```bash
curl -sL -o /tmp/brand_screenshot.png "SCREENSHOT_URL_FROM_RESPONSE"
ls -lh /tmp/brand_screenshot.png  # verify file > 10KB
```

### 2b. Read the screenshot

Use the Read tool on `/tmp/brand_screenshot.png` to visually analyze it. This is your **primary source** for brand style — text content is secondary.

### 2c. What to look for in the screenshot

Study the screenshot carefully and note:

**Background / Base tone:**

- Is the site **dark mode** (black/dark gray background)? → Location must be dark too
- Is it **light/white**? → Location can be bright and airy
- Is it **colorful**? → Location should have color accents matching the site

**Color roles — identify each separately WITH hex codes:**

- **Background color** — what fills most of the page. Estimate the hex code (e.g. black = #000000, dark charcoal = #1A1A1A, off-white = #F5F5F5)
- **Primary brand color** — logo color, header color, or the most prominent non-background color. Estimate hex (e.g. indigo = #3B3BFF, forest green = #228B22)
- **Accent/CTA color** — button color, link color, highlight color. Estimate hex (e.g. neon lime = #BFFF00, coral = #FF6B6B)
- **Text color** — main body text color (white on dark = #FFFFFF, dark gray on white = #333333)

**IMPORTANT:** Always estimate hex codes. Even approximate hex is far more useful than just "green" or "blue" — it tells the generation model the exact shade, brightness, and saturation.

**Typography vibe:**

- Bold condensed / thin elegant / rounded playful / monospace tech / serif classic?
- ALL CAPS or mixed case? Large dramatic headings or subtle?

**Overall energy:**

- Premium/luxury or accessible/casual?
- High energy/bold or calm/minimal?
- Playful or serious?

---

## Step 3: Tone of Voice Analysis

Read the markdown text content and classify the brand's communication style:

| Tone                             | Signals                                                    | Speech Style for Video                            |
| -------------------------------- | ---------------------------------------------------------- | ------------------------------------------------- |
| **Formal / Authoritative**       | Professional language, no slang, structured sentences      | Confident, measured delivery, polished vocabulary |
| **Friendly / Conversational**    | Casual language, questions, "you/your", emojis in posts    | Warm, relatable, like talking to a friend         |
| **Bold / Provocative**           | Strong claims, exclamation marks, imperative mood, slang   | Energetic, punchy, direct — no filler words       |
| **Inspirational / Aspirational** | Motivational language, vision statements, emotional appeal | Passionate, uplifting, storytelling tone          |
| **Playful / Witty**              | Humor, puns, pop culture references, informal              | Light, fun, with personality — smiles, gestures   |
| **Expert / Educational**         | Data, specifics, technical terms, how-to language          | Knowledgeable, clear, step-by-step explanation    |

---

## Step 4: Build Brand Style Brief

**CRITICAL: Every field in this brief must be derived from what you SAW in the screenshot and READ in the text. Do not guess or use generic defaults. If the site has a black background with neon green buttons — say exactly that.**

```
BRAND STYLE BRIEF
=================
Source: [URL]
Brand: [name if identifiable]

SITE MOOD: [dark/light/colorful] — [1 sentence describing the overall visual impression]

COLORS (extracted from screenshot — always include hex):
- Background: [color name + hex — e.g. "black #000000", "off-white #F5F5F5"]
- Primary brand: [color name + hex — e.g. "indigo #3B3BFF", "emerald #50C878"]
- Accent/CTA: [color name + hex — e.g. "neon lime #BFFF00", "coral #FF6B6B"]
- Text: [color name + hex — e.g. "white #FFFFFF on dark", "charcoal #333333 on light"]

CHARACTER STYLING:
- Base outfit color: [hex of a color matching site background tone — e.g. "#1A1A1A black" for dark sites]
- Accent pieces: [specific items + hex — e.g. "#BFFF00 neon lime sneakers and earrings"]
- Style: [formal/casual/sporty/streetwear — matching the site's energy]
- Overall look: [1-sentence summary with hex colors that someone could use to generate the character]

LOCATION:
- Mood: [dark/bright/colorful — MUST match the site's background tone]
- Setting: [specific location — e.g. "dark modern studio with #BFFF00 neon LED accent strip along back wall"]
- Lighting: [with hex — e.g. "low-key base with #BFFF00 neon rim light", "warm #FFD700 golden ambient"]
- Brand-colored details: [3-5 specific props/elements with hex — e.g. "#BFFF00 neon LED strip on shelf, #3B3BFF indigo throw pillow, stack of design books, sleek monitor showing creative work"]

TONE OF VOICE: [from Step 3]

SPEECH DIRECTION:
- Delivery style: [how the person speaks]
- Vocabulary level: [casual/elevated/technical]
- Energy: [calm/moderate/high]

CGI STYLING (if applicable):
- Motion design colors: [primary + accent from brand palette]
- Typography feel: [describe the font vibe from the screenshot — e.g. "bold condensed all-caps" or "thin serif elegant"]
- Background: [solid/gradient in brand colors — e.g. "black background with neon lime accents"]

SCREENSHOT_MEDIA_ID: [fill after Step 5a upload — e.g. "media_abc123"]
```

**IMPORTANT:** Fill in `SCREENSHOT_MEDIA_ID` immediately after uploading the screenshot in Step 5a. This ID is needed in Step 6 when building the video command. Do not lose it.

---

## Step 5: Upload Screenshot as Media Reference (MANDATORY)

**CRITICAL: You MUST upload the brand screenshot and include it in the `medias` array in the video generation call. This is NOT optional — it is a core part of brand-style video. Without it, the video loses its visual connection to the brand.**

### 5a. Upload the screenshot

```bash
higgsfieldcli upload --file /tmp/brand_screenshot.png --force-ip-check
```

Save the returned `id` as `SCREENSHOT_ID`. The `--force-ip-check` flag triggers the IP check and waits automatically.

### 5b. Media ordering for video generation

When building the `higgsfieldcli generate` command, the screenshot goes as the **LAST entry in the `medias` array** and gets the **LAST `@ImageN` number**:

| Media                  | `medias` array order                                                               | Prompt reference                |
| ---------------------- | ---------------------------------------------------------------------------------- | ------------------------------- |
| Character element      | `<<<element_id>>>` in prompt (no medias entry needed)                              | `<<<element_id>>>`              |
| Product photo (if any) | `{"role":"start_image","data":{"id":"PRODUCT_ID","type":"media_input"}}` (1st)     | `@Image1`                       |
| Brand screenshot       | `{"role":"start_image","data":{"id":"SCREENSHOT_ID","type":"media_input"}}` (last) | `@Image2` (or next available N) |

### 5c. How to describe the screenshot in the video prompt

The screenshot MUST be **large, clearly visible, and close to the person** — not a tiny decoration in the far background. It should fill a significant portion of the frame so the brand is immediately recognizable.

**Placement options (pick the best fit for the scene):**

| Scene type  | Screenshot placement                                                                      | Prompt wording                                                                                                                                 |
| ----------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Dark studio | Large wall-mounted flat screen directly behind the person, filling most of the background | "a large flat-screen TV mounted on the wall directly behind the person displays @ImageN, the screen fills the background behind her shoulders" |
| Home/office | Laptop or monitor on the desk RIGHT NEXT TO the person, angled toward camera              | "an open laptop on the desk beside the person shows @ImageN on its screen, clearly visible and angled toward camera"                           |
| Any scene   | Large monitor over the shoulder, partially visible                                        | "a large monitor over the person's right shoulder displays @ImageN, close enough to read"                                                      |

(where N corresponds to the screenshot's position in the `medias` array)

**Rules for screenshot placement:**

- The screen showing @ImageN must occupy **at least 20-30% of the visible background**
- It must be **close to the person** — directly behind, beside, or over the shoulder. Never far away in the background
- It must be **clearly readable** — not blurry, not tiny, not obscured by other objects
- It must be on a **physical screen** (TV, monitor, laptop) — never floating or overlaid

**Example full medias setup:**

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"<<<elem_abc>>> is the spokesperson. @Image1 is the brand website displayed on a large flat-screen TV mounted on the wall directly behind the person, the screen fills the background behind her shoulders. Style & Mood: ... Dynamic Description: <<<elem_abc>>> stands in a dark studio, the large screen behind her shows @Image1, she speaks directly to camera with confident energy, gesturing naturally...","medias":[{"role":"start_image","data":{"id":"SCREENSHOT_ID","type":"media_input"}}],"duration":10,"aspect_ratio":"9:16","generate_audio":true}]'
```

---

## Step 6: Apply Brief to Video Generation

### Pre-flight checklist (MANDATORY before running higgsfieldcli generate)

Before building the video CLI command, verify ALL of these:

- [ ] Screenshot uploaded? → SCREENSHOT_ID saved from Step 5a
- [ ] `{"role":"start_image","data":{"id":"SCREENSHOT_ID","type":"media_input"}}` included in the `medias` array?
- [ ] `@ImageN` referencing the screenshot appears in the prompt text?
- [ ] Prompt describes WHERE the screenshot appears (monitor, laptop, wall display)?

**If any of these are missing — STOP and fix before generating.** The screenshot is a core part of brand-style video.

---

The Brand Style Brief modifies the normal video generation flow. After building the brief, choose the video format (talking-head, product-demo, CGI showcase, etc.) based on normal routing logic — then apply the brief as overrides:

### For UGC formats (talking-head, product-demo, tutorial, unboxing)

**Character prompt (Soul 2.0):** Use CHARACTER STYLING from the brief instead of defaults. Use hex codes directly in the prompt for precise color matching:

```
A woman in a #1A1A1A black fitted turtleneck with #BFFF00 neon-lime earrings
```

The character's outfit base color MUST match the site's background tone. Brand accent colors go on accessories or small details — NOT as the dominant outfit color.

**CRITICAL — No objects in hands:** The Soul 2.0 character prompt must NEVER describe any object in the person's hands — no products, no props, no phones, no shoes, no accessories being held. Hands must be empty or in natural gestures (talking, resting at sides). Objects in hands during character generation cause seedance to hallucinate random items. Brand color accents go ONLY on worn items: earrings, necklace, watch, belt, shoe color, clothing trim — never held items.

**Location:** Use LOCATION from the brief instead of the default "cozy bedroom/living room." Include hex-colored details directly in the location description:

```
Dark modern studio. A #BFFF00 neon LED strip runs along the back shelf. A sleek monitor on the desk displays the brand website. #3B3BFF indigo accent cushion on a dark chair. Stack of design books. Ambient low-key lighting with #BFFF00 neon rim light from the left.
```

**CRITICAL: If the brand site is dark mode — the location MUST be dark.** Do not put a person in a bright room for a dark-mode brand. The location's mood must mirror the site's visual weight.

**Brand screenshot on set:** Upload the screenshot (Step 5) and include it in the `medias` array. In the prompt, describe a monitor/screen in the scene displaying `@ImageN` (the screenshot). This visually ties the person to the brand.

**Lighting:** Match the brand mood. Dark brand = moody/low-key lighting with colored accent light in the brand's accent hex color. Bright brand = natural/soft lighting. Bold brand = dramatic high-contrast lighting.

**Speech/voiceover:** Use SPEECH DIRECTION from the brief to set the tone. If the user provided specific text — keep their text, but adjust delivery style. If no text — generate speech that matches both the product and the brand tone.

### For CGI formats (product-showcase, social-short, product-demo-pro, virtual-try-on)

**Color grading and backgrounds:** Use hex COLORS from the brief — background hex as the base, accent hex for highlights and light effects.

**Typography (product-showcase):** Text color and style follow CGI STYLING from the brief. Use hex values.

**Motion design:** VFX particle colors, light effects, and accent elements use the brand palette hex codes.

**Brand screenshot:** Can be composited as a floating screen element or surface texture in CGI scenes.

### For narrative format (creative-ad-video)

**Scene design:** Location, lighting, and mood reflect the brand's visual identity from the screenshot. Use hex colors for set details.

**Character styling:** Same as UGC — outfit and look match the brand with hex precision.

---

## Important Rules

- **Brand extraction runs ONCE per brand URL.** If the user sends the same URL again in the same conversation, reuse the existing brief — don't re-fetch.
- **Screenshot is the primary source, text is secondary.** If the screenshot shows a dark bold site but the text is friendly — the visual style (dark, bold) wins for location and character styling. Text only drives the tone of voice.
- **Dark site = dark location. Always.** This is the #1 rule for location matching. The person's environment must feel like it belongs on the brand's website.
- **Brand accent colors go on details, not everything.** If the brand accent is neon green, the character wears a mostly dark outfit with maybe neon green sneakers or earrings — NOT head-to-toe neon green.
- **User text overrides brand tone for content, not style.** If the user says "talk about sports nutrition" but the brand is luxury — the character still dresses and speaks in a luxury manner, but the content is about sports nutrition.
- **Brand colors apply to clothing and environment — NOT to skin tone, hair color, or body type.** Never alter human appearance to match a brand palette.
- **If brand style is ambiguous** (generic white website, no clear identity) — ask the user to clarify the vibe they want, or default to Minimal / Clean archetype.

---

## Example: Design Pickle (designpickle.com)

For reference — here's how a correct brief would look for a dark-mode creative brand:

```
BRAND STYLE BRIEF
=================
Source: https://designpickle.com
Brand: Design Pickle

SITE MOOD: dark — bold black background, high-energy creative platform with neon accents

COLORS (extracted from screenshot — always include hex):
- Background: black #000000
- Primary brand: deep indigo #3B3BFF (headlines, stat numbers)
- Accent/CTA: neon lime #BFFF00 (buttons, "Get started", "Book a demo")
- Text: white #FFFFFF on dark background

CHARACTER STYLING:
- Base outfit color: #1A1A1A black (matching the dark site)
- Accent pieces: #BFFF00 neon lime drop earrings, #BFFF00 thin bracelet
- Style: modern creative professional — not corporate, not streetwear — smart casual with edge
- Overall look: Confident woman in #1A1A1A black fitted turtleneck with #BFFF00 neon-lime earrings — hands empty, no objects held

LOCATION:
- Mood: dark (matching the black #000000 site background)
- Setting: dark modern creative studio with ambient colored lighting
- Lighting: low-key base with #BFFF00 neon lime LED rim light from the left
- Brand-colored details: #BFFF00 neon LED strip along back shelf, sleek monitor displaying brand website (screenshot as @ImageN), #3B3BFF indigo accent cushion on dark chair, stack of design books, dark modern furniture

TONE OF VOICE: Bold / Provocative (strong claims: "#1 in design production", "ultimate creative partner")

SPEECH DIRECTION:
- Delivery style: confident, direct, energetic
- Vocabulary level: casual-professional
- Energy: high

CGI STYLING:
- Motion design colors: #000000 black base + #BFFF00 neon lime accents + #3B3BFF indigo highlights
- Typography feel: bold condensed all-caps (matching their headline font)
- Background: #000000 black with #BFFF00 neon lime accent elements
```

### How this translates to video generation:

1. **Soul 2.0 character prompt:** "A confident woman with straight dark hair, wearing a #1A1A1A black fitted turtleneck, #BFFF00 neon-lime drop earrings, #BFFF00 thin bracelet, black jeans. Standing in a dark modern creative studio, #BFFF00 neon LED strip glowing along the back shelf, low-key ambient lighting with #BFFF00 neon rim light from the left. Hands empty, natural gesture."

2. **Upload screenshot:** `higgsfieldcli upload --file /tmp/brand_screenshot.png --force-ip-check` → save SCREENSHOT_ID

3. **Create character element:** Soul 2.0 → `element create --category character` → save element_id

4. **Video command:**

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"<<<element_id>>> is the spokesperson. @Image1 is the brand website displayed on a large sleek monitor behind the person. Style & Mood: dark modern studio, neon #BFFF00 accent lighting, cinematic. Dynamic Description: <<<element_id>>> stands in a dark studio with #BFFF00 neon LED strip along the shelf behind her, a sleek monitor displays @Image1, she speaks directly to camera with confident energy, gesturing naturally... Static Description: dark creative studio, #BFFF00 neon LED strip on back shelf, #3B3BFF indigo cushion on dark chair, monitor showing brand site, design books stacked on side table. Audio: she speaks to camera: '...'","medias":[{"role":"start_image","data":{"id":"SCREENSHOT_ID","type":"media_input"}}],"duration":10,"aspect_ratio":"9:16","generate_audio":true}]'
```
