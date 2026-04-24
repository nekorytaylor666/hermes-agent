# Skills: How to Add, Update, and Sync

Practical guide for developers working on hermes-agent skills.

---

## Overview

Skills are markdown files (`SKILL.md`) that give the agent new capabilities without writing Python code. They live in two places:

| Location | Purpose |
|----------|---------|
| `skills/` (repo) | **Bundled** — shipped with every install, auto-synced to `~/.hermes/skills/` |
| `optional-skills/` (repo) | **Official optional** — shipped but NOT auto-activated; users install via `hermes skills browse` |
| `~/.hermes/skills/` | **Runtime directory** — the single source of truth the agent reads from |

The sync mechanism (`tools/skills_sync.py`) copies bundled skills from the repo into `~/.hermes/skills/` using a manifest-based system that tracks origin hashes to detect user modifications.

---

## 1. Adding a New Bundled Skill

### Step 1: Create the skill directory

Pick an appropriate category folder under `skills/`:

```
skills/<category>/<skill-name>/
├── SKILL.md              # Required
├── references/           # Optional: supplementary docs (.md files)
├── scripts/              # Optional: helper scripts
├── templates/            # Optional: output templates
└── assets/               # Optional: other files
```

Existing categories: `apple/`, `creative/`, `data-science/`, `devops/`, `email/`, `gaming/`, `github/`, `media/`, `mlops/`, `note-taking/`, `productivity/`, `red-teaming/`, `research/`, `smart-home/`, `social-media/`, `software-development/`.

Create a new category directory if none fits.

### Step 2: Write SKILL.md

Minimal example:

```markdown
---
name: my-skill
description: One-line description shown in skill listings and search.
version: 1.0.0
author: Your Name
license: MIT
---

# My Skill Title

Brief intro explaining what this skill does.

## When to Use

- Trigger condition 1
- Trigger condition 2

## Quick Reference

Common commands or API calls in a table or code blocks.

## Procedure

Step-by-step instructions the agent follows.

## Pitfalls

Known failure modes and how to handle them.

## Verification

How the agent confirms it worked.
```

### Full frontmatter reference

```yaml
---
name: my-skill                              # Required, max 64 chars
description: Brief description              # Required, max 1024 chars
version: 1.0.0                              # Optional
author: Your Name                           # Optional
license: MIT                                # Optional
platforms: [macos, linux]                   # Optional — omit to load on all platforms
                                            #   Valid values: macos, linux, windows
required_environment_variables:             # Optional — API keys/secrets
  - name: MY_API_KEY
    prompt: "Enter your API key"
    help: "Get one at https://example.com"
    required_for: "API access"

required_credential_files:                  # Optional — OAuth tokens, certs
  - path: my_token.json                     # Relative to ~/.hermes/
    description: OAuth2 token

metadata:
  hermes:
    tags: [Category, Keywords]
    related_skills: [other-skill]
    requires_toolsets: [web]                # Only show when these toolsets are active
    requires_tools: [web_search]            # Only show when these tools exist
    fallback_for_toolsets: [browser]        # Hide when these toolsets are active
    fallback_for_tools: [browser_navigate]  # Hide when these tools exist
    config:                                 # Non-secret config.yaml settings
      - key: myskill.data_path
        description: "Path to data directory"
        default: "~/myskill-data"
        prompt: "Data directory path"

prerequisites:
  commands: [some-cli-tool]                 # Optional — CLI tools needed
---
```

### Step 3: Test locally

```bash
# Copy to runtime directory for immediate testing
cp -r skills/category/my-skill ~/.hermes/skills/category/my-skill

# Or just run sync
python tools/skills_sync.py

# Test in a chat session
hermes chat -q "Use the my-skill skill to do X"
```

### Step 4: Commit

Commit the `skills/<category>/<skill-name>/` directory. On the next `hermes update` or CLI launch, the sync mechanism will pick it up automatically.

---

## 2. Adding an Official Optional Skill

Same as above but place it under `optional-skills/<category>/<skill-name>/` instead. Optional skills:

- Ship with the repo but are NOT auto-synced to `~/.hermes/skills/`
- Are labeled "official" (builtin trust, no third-party security warning)
- Users discover them via `hermes skills browse --source official`
- Users install them via `hermes skills install official/<category>/<skill>`

---

## 3. Updating an Existing Bundled Skill

### What you need to know about the sync mechanism

The manifest at `~/.hermes/skills/.bundled_manifest` tracks every bundled skill as `skill_name:md5_hash`. The sync logic (`tools/skills_sync.py`) works as follows:

| Scenario | What happens |
|----------|-------------|
| **Skill unchanged** (bundled hash == manifest hash, user hash == manifest hash) | Skipped — nothing to do |
| **Bundled updated** (bundled hash != manifest hash, user hash == manifest hash) | User copy replaced with new bundled version, new hash recorded |
| **User modified** (user hash != manifest hash) | **Skipped** — user's changes are preserved, never overwritten |
| **User deleted** (in manifest but not on disk) | Respected — not re-added |
| **Removed from bundled** (in manifest but not in repo) | Cleaned from manifest |

### How to update

1. **Edit the skill files** in `skills/<category>/<skill-name>/` (the repo copy).

2. **That's it.** On the next sync, any user whose copy is unmodified will get the update. Users who have customized the skill will keep their version.

3. **Test** by running sync manually:
   ```bash
   python tools/skills_sync.py
   ```
   You should see `↑ my-skill (updated)` in the output.

### Forcing an update for user-modified skills

If a user has modified a bundled skill and wants to get the latest bundled version:

```bash
# Reset manifest tracking (keeps user's copy, future syncs will re-baseline)
hermes skills reset my-skill

# Or restore the bundled version entirely (deletes user's copy, re-copies from bundled)
hermes skills reset my-skill --restore
```

---

## 4. Making Hermes Sync Skills

Skills are synced automatically in three places:

### A. On every CLI launch (quiet, fast)

`hermes_cli/main.py` line ~1122:
```python
from tools.skills_sync import sync_skills
sync_skills(quiet=True)
```

This runs on every `hermes` invocation. It's fast because it skips unchanged skills (hash comparison).

### B. On `hermes update`

`hermes_cli/main.py` line ~4654:
```python
from tools.skills_sync import sync_skills
result = sync_skills(quiet=True)
```

After pulling the latest code and installing dependencies, `hermes update` syncs skills and prints a summary of new/updated/modified skills.

### C. On `hermes setup` / `setup-hermes.sh`

`setup-hermes.sh` line ~344:
```bash
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/tools/skills_sync.py"
```

Initial setup copies all bundled skills to `~/.hermes/skills/`.

### D. Manual sync

```bash
# Run the sync script directly
python tools/skills_sync.py

# Output example:
#   + new-skill
#   ↑ updated-skill (updated)
#   ~ user-modified-skill (user-modified, skipping)
#   Done: 1 new, 1 updated, 45 unchanged, 1 user-modified (kept). 48 total bundled.
```

### E. Gateway/server startup

`gateway/run.py` also calls `sync_skills(quiet=True)` on startup, so deployed instances pick up bundled skill changes too.

---

## 5. How Skills Are Loaded at Runtime

Skills use a **progressive disclosure** architecture to minimize token usage:

1. **Level 0 — Index** (`build_skills_system_prompt()` in `agent/prompt_builder.py`):
   - On every prompt, all skills in `~/.hermes/skills/` are scanned
   - Only the `name` and `description` from frontmatter are included (~3k tokens for the full index)
   - The agent sees the skill list and decides which to load

2. **Level 1 — Full content** (`skill_view(name)` in `tools/skills_tool.py`):
   - Agent calls `skill_view("my-skill")` when it decides to use a skill
   - Returns the full SKILL.md content with template substitutions (`${HERMES_SKILL_DIR}`, `${HERMES_SESSION_ID}`)
   - Config values and env var status are appended

3. **Level 2 — References** (`skill_view(name, "references/doc.md")`):
   - Agent can load specific reference files from the skill directory

---

## 6. Template Variables in SKILL.md

These tokens are substituted when the skill is loaded:

| Token | Replaced with |
|-------|---------------|
| `${HERMES_SKILL_DIR}` | Absolute path to the skill's directory |
| `${HERMES_SESSION_ID}` | Active session ID (left in place if no session) |

Use them to reference bundled scripts:

```markdown
Run the analysis:
    python ${HERMES_SKILL_DIR}/scripts/analyze.py <input>
```

Disable with `skills.template_vars: false` in `config.yaml`.

---

## 7. Quick Checklist

### New bundled skill
- [ ] Create `skills/<category>/<skill-name>/SKILL.md`
- [ ] Frontmatter has `name` and `description`
- [ ] Content follows the When to Use / Quick Reference / Procedure structure
- [ ] Tested with `hermes chat -q "..."` after running `python tools/skills_sync.py`
- [ ] Committed to repo

### Update existing skill
- [ ] Edit `skills/<category>/<skill-name>/SKILL.md` (or supporting files)
- [ ] Run `python tools/skills_sync.py` to verify the update propagates
- [ ] Committed to repo

### Sync after changes
- [ ] `python tools/skills_sync.py` for manual sync
- [ ] Or just restart `hermes` — sync runs on every launch

---

## 8. Useful CLI Commands

```bash
hermes skills list                    # List all installed skills
hermes skills search <query>          # Search by keyword
hermes skills browse                  # Browse official optional skills
hermes skills config                  # Enable/disable skills interactively
hermes skills reset <name>            # Clear user-modified tracking
hermes skills reset <name> --restore  # Restore bundled version
hermes skills audit <name>            # Re-scan for security issues
```
