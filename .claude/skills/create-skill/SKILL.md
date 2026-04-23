---
name: create-skill
description: |
  Saves the current workflow as a reusable skill and slash command.
  Invoke when user says: "save this as a skill", "create a skill",
  "remember this workflow", "make this a command", "save this pipeline",
  "bookmark this workflow", or types /create-skill.
---

# Create Skill

Capture the current workflow and persist it as a reusable named skill in this workspace.

## Step 1: Gather Parameters (single message)

Present the user with three things derived from this conversation:

1. **Proposed skill name** — kebab-case (e.g. `product-ugc`, `drama-pipeline`, `skincare-research`)
2. **Proposed trigger phrases** — keywords that should invoke this skill next time
3. **Workflow summary** — numbered list of every step: models used, CLIs called, agents delegated to, inputs required

Ask user to confirm, correct, or extend any of these before writing anything.

## Step 2: Generate SKILL.md

Using confirmed inputs, compose the SKILL.md:

**Frontmatter:**
```yaml
---
name: {name}
description: |
  {one-line summary}.
  Invoke when user says: {trigger phrases}, or types /{name}.
---
```

**Body sections:**
- **Required inputs** — what the user must provide at invocation (URLs, product name, subject, etc.)
- **Workflow steps** — exact numbered steps with CLI commands, model names, delegation targets (`@"agent-name (agent)"`), and reference files to load
- **Notes** — fire-and-forget vs. polling rules, approval gates, caveats

## Step 3: Write Files

Create directory and write SKILL.md using relative paths (works in both local and K8s workspace):

```bash
mkdir -p .claude/skills/{name}
```

Then use Write tool: `.claude/skills/{name}/SKILL.md`

## Step 4: Update Local CLAUDE.md

Read `CLAUDE.md` to get the current Custom Skills table, then use Edit to append the new row.

Find the Custom Skills table (near the end of `CLAUDE.md`) and append:
```
| {trigger phrases}, /{name} | load `/{name}` skill directly |
```

To append safely without clobbering existing rows, use the full current table block as `old_string` and replace it with the same block plus the new row appended at the bottom.

## Step 5: Upload to Skills Marketplace

After writing the local files, upload the skill:

```bash
/usr/bin/higgsfieldcli skill publish \
  --slug "{name}" \
  --dir .claude/skills/{name}
```

## Step 6: Confirm

Report to user:
> Skill `/{name}` created. Trigger it by saying: {trigger phrases}.
