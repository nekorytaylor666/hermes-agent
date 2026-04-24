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

  # Entire optional-skills tree — nothing in it supports Higgsfield or marketing
  "optional-skills"
)

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
