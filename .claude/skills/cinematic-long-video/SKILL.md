---
name: cinematic-long-video
description: |
  Long-form video production (>15s). Loaded by video-agent when a single video exceeds 15 seconds.
  Breaks the video into shots, generates each via video-skill, assembles via montage.
---

# Cinematic Long Video Skill

Produces videos longer than 15 seconds by decomposing them into a multi-shot storyboard. Each shot is generated individually (≤15s each via Seedance 2.0), then assembled into a final video.

## When This Skill Applies

- User requests a single continuous video >15 seconds (30s, 1 minute, etc.)
- Film, documentary, music video, brand story, narrative — any non-marketing long-form video

## When This Skill Does NOT Apply

- Multiple separate short videos (even if total duration >15s) → use video-skill per video
- Marketing/product videos of any length → marketing-agent handles those

## Pipeline

Follow these stages in order:

1. **Requirements capture** — [requirements-capture.md](requirements-capture.md)
2. **Storyboard design** — [storyboard-design.md](storyboard-design.md) — decompose into shots ≤15s each
3. **Visual references** — [visual-references.md](visual-references.md) — generate reference images for consistency
4. **Shot generation** — [shot-generation.md](shot-generation.md) — generate each shot as a separate video
5. **Continuity** — [continuity.md](continuity.md) — maintain visual consistency across shots
6. **Assembly** — suggest montage to stitch all shots into final video

Full orchestration details: [pipeline.md](pipeline.md)

## Rules

- Present each stage to the user for approval before proceeding to the next.
- Track all generated assets (job IDs, element IDs) across stages.
- After the final shot is generated, suggest montage assembly.
