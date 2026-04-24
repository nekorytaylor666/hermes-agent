#!/usr/bin/env bash
# Prune skills that are not relevant to the Higgsfield + marketing-research
# focus of the Hermes fork.
#
# Scope:
#   - skills/ subtrees that are clearly off-focus (apple, gaming, smart-home, etc.)
#   - individual sibling skills under skills/autonomous-ai-agents/ (keep hermes-agent)
#   - the entire optional-skills/ tree
#   - empty placeholder DESCRIPTION.md-only categories
#
# Judgment-call skills from the review are NOT touched here — decide per-skill
# and rerun with an extended list if needed.
#
# Usage:
#   ./scripts/prune-skills-for-higgsfield-marketing.sh            # stage the deletes
#   ./scripts/prune-skills-for-higgsfield-marketing.sh --dry-run  # print only
#
# After running, inspect with `git status` / `git diff --staged` and commit.

set -euo pipefail

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

# Resolve repo root relative to this script so the paths below are portable.
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Sanity: we must be in a git repo.
git rev-parse --is-inside-work-tree >/dev/null

TARGETS=(
  # Off-focus top-level skill categories
  "skills/apple"
  "skills/gaming"
  "skills/smart-home"
  "skills/red-teaming"
  "skills/data-science"
  "skills/mlops"
  "skills/software-development"
  "skills/github"
  "skills/devops"
  "skills/note-taking"

  # Empty placeholder categories (DESCRIPTION.md only)
  "skills/domain"
  "skills/feeds"
  "skills/gifs"
  "skills/diagramming"
  "skills/inference-sh"

  # Rival-CLI skills under autonomous-ai-agents (keep hermes-agent)
  "skills/autonomous-ai-agents/claude-code"
  "skills/autonomous-ai-agents/codex"
  "skills/autonomous-ai-agents/opencode"

  # optional-skills tree — prune everything except the two keepers below
  # (honcho memory skill and meme-generation), which are handled by the
  # per-child fan-out after this loop.
)

# Keepers under optional-skills/ (explicitly preserved):
#   - optional-skills/autonomous-ai-agents/honcho  (Honcho memory)
#   - optional-skills/creative/meme-generation     (meme generator)
#
# Fan out optional-skills/: delete every child except those two keepers, and
# delete every sibling inside the two parent categories so only the keeper
# subdirs remain.
OPTIONAL_KEEP_TOP=("autonomous-ai-agents" "creative")
KEEP_IN_AUTONOMOUS="honcho"
KEEP_IN_CREATIVE="meme-generation"

if [[ -d optional-skills ]]; then
  # 1) Remove every top-level entry in optional-skills/ that is not a keeper parent.
  while IFS= read -r entry; do
    name="$(basename "$entry")"
    keep=0
    for k in "${OPTIONAL_KEEP_TOP[@]}"; do
      [[ "$name" == "$k" ]] && keep=1 && break
    done
    if (( ! keep )); then
      TARGETS+=("optional-skills/$name")
    fi
  done < <(find optional-skills -mindepth 1 -maxdepth 1)

  # 2) Inside the two keeper parents, remove every sibling except the keeper child.
  if [[ -d optional-skills/autonomous-ai-agents ]]; then
    while IFS= read -r entry; do
      name="$(basename "$entry")"
      if [[ "$name" != "$KEEP_IN_AUTONOMOUS" && "$name" != "DESCRIPTION.md" ]]; then
        TARGETS+=("optional-skills/autonomous-ai-agents/$name")
      fi
    done < <(find optional-skills/autonomous-ai-agents -mindepth 1 -maxdepth 1)
  fi

  if [[ -d optional-skills/creative ]]; then
    while IFS= read -r entry; do
      name="$(basename "$entry")"
      if [[ "$name" != "$KEEP_IN_CREATIVE" && "$name" != "DESCRIPTION.md" ]]; then
        TARGETS+=("optional-skills/creative/$name")
      fi
    done < <(find optional-skills/creative -mindepth 1 -maxdepth 1)
  fi
fi

removed=0
missing=0

for path in "${TARGETS[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "skip (missing): $path"
    missing=$((missing + 1))
    continue
  fi

  if (( DRY_RUN )); then
    echo "would rm: $path"
  else
    # -r for directories, -q to keep output focused on the summary below.
    git rm -rq -- "$path"
    echo "removed: $path"
  fi
  removed=$((removed + 1))
done

echo
echo "Targets processed: ${#TARGETS[@]}"
echo "Removed/queued:    $removed"
echo "Missing (skipped): $missing"

if (( DRY_RUN )); then
  echo
  echo "Dry run complete. Re-run without --dry-run to actually stage the deletes."
else
  echo
  echo "Deletes staged. Review with:"
  echo "  git status"
  echo "  git diff --staged --stat"
  echo "Then commit when you're happy."
fi
