# Concept Generation Guide

Template for generating new video concepts based on analyzed competitor content. Used by `scripts/generate_concepts.py` (Gemini 3.1 Pro API) or as a direct reference for Claude when generating concepts inline.

## Generation Template

When generating new concepts for a client, follow this structure. Replace `{{variables}}` with actual client data from `client-profiles.md`.

---

**Role:** You are an expert in creating viral short-form video content.

**Task:** Based on the reference video analysis below, generate 3 NEW video concepts adapted for **{{client.name}}**.

**Rules:**
- Do not copy the original
- Translate the core idea into the {{client.niche}} context
- Mainly iterate and sharpen the HOOKS — the hook is the most valuable part
- The first 3 seconds must stop {{client.audience}} from scrolling
- Each concept MUST cite which reference video(s) inspired it using GFM footnote syntax (`[^1]`, `[^2]`) and what specific element was adapted

**Style guidelines:**
{{client.style}}

**Reference video analysis:**
{{video_analysis}}

---

## Output Format

Each concept must follow this structure:

```
# CONCEPT 1
Text description of the concept (1-3 sentences)

## HOOK
Detailed hook description (1-3 sentences)
- What is seen in the first 2 seconds
- What is said in the first line
- Why this hook works for {{client.audience}}

## SCRIPT
Detailed script (1-20 sentences, as many as needed)
- Scene flow
- Spoken text / voiceover
- Clear payoff
- Tone matching {{client.name}}'s style

## SOURCES
- Inspired by: [^N] @creator — what specific element was adapted (hook technique, format, retention mechanism, visual style)

# CONCEPT 2
...

# CONCEPT 3
...

[^1]: @creator — platform — Source URL
[^2]: @creator — platform — Source URL

```

## Style Presets

When generating concepts, match the client's tone. Common presets:

### Authority (business, real estate, finance)
- Calm confidence > hype
- Emotional credibility > performance
- No shouting, no buzzwords, no exaggeration
- Subtle authority, not selling

### Practical (tech, AI, productivity)
- Practical value > hype
- Show, don't just tell
- No buzzwords, no exaggeration
- Demonstration of the tool or workflow

### Entertainment (lifestyle, travel, food)
- Energy and personality
- Visual storytelling > talking head
- Relatable moments > polished perfection
- Authentic reactions

### Educational (coaching, tutorials, how-to)
- Clear structure > clever delivery
- One lesson per video
- Immediate takeaway
- "You can do this too" framing
