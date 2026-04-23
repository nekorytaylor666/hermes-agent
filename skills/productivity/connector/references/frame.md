---
name: frame
description: Search assets, create projects/assets, and post comments on Frame.io video review. Use for any Frame.io automation task. Triggers include "frame", "frame.io".
allowed-tools: Bash(frame *), Bash(./bin/mcp2cli *), Bash(mcp2cli *)
---

# Frame.io (via Higgsfield MCP proxy)

Search assets, create projects/assets, and post comments on Frame.io video review. Exposes 6 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @frame <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @frame --list                    # all 6 tools
./bin/mcp2cli @frame frame-search-assets --help   # inspect one
./bin/mcp2cli @frame frame-search-assets --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @frame --pretty <cmd>` — `--pretty` goes AFTER `@frame`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @frame --head N <cmd>` — `--head N` goes AFTER `@frame`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 6 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `frame-search-assets`

| Flag | Description |
|---|---|
| `--account-id ACCOUNT_ID` | Select an account or provide a custom ID. You can use the "retrieve_options" tool using these parameters to get the v... |
| `--query QUERY` | Search text |
| `--sort SORT` | Sorting parameters |
| `--include-deleted` | Flag to include soft-deleted records in results |
| `--filter-type {file,folder}` | If specified, only assets of this type will be returned. |
| `--page PAGE` | The page to retrieve |
| `--page-size PAGE_SIZE` | The number of results to include in the page |

### `frame-create-project`

| Flag | Description |
|---|---|
| `--account-id ACCOUNT_ID` | Select an account or provide a custom ID. You can use the "retrieve_options" tool using these parameters to get the v... |
| `--team-id TEAM_ID` | The ID of the team. You can use the "retrieve_options" tool using these parameters to get the values. key: frame-crea... |
| `--name NAME` | The name of the project. |
| `--private` | If true, the project is private to the creating user |
| `--project-preferences PROJECT_PREFERENCES` | Preferences to set for the project. [See the documenta tion](https://developer.frame.io/api/reference/operati on/crea... |

### `frame-create-comment`

| Flag | Description |
|---|---|
| `--account-id ACCOUNT_ID` | Select an account or provide a custom ID. You can use the "retrieve_options" tool using these parameters to get the v... |
| `--asset-id ASSET_ID` | Select an asset (file) or provide a custom ID. You can use the "retrieve_options" tool using these parameters to get... |
| `--text TEXT` | The body of the comment. |
| `--annotation ANNOTATION` | Serialized list of geometry and/or drawing data. [Learn more here](https://developer.frame.io/docs/workflows- assets/... |
| `--page PAGE` | Page number for a comment (documents only). |
| `--timestamp TIMESTAMP` | Timestamp for the comment, in frames, starting at 0. |
| `--duration DURATION` | Used to produce range-based comments, this is the duration measured in frames. |
| `--private` | Set to true to make your comment a "Team-only Comment" that won't be visible to anonymous reviewers or Collaborators. |

### `frame-create-asset`

| Flag | Description |
|---|---|
| `--account-id ACCOUNT_ID` | Select an account or provide a custom ID. You can use the "retrieve_options" tool using these parameters to get the v... |
| `--asset-id ASSET_ID` | Select a parent asset (folder) or provide a custom ID. You can use the "retrieve_options" tool using these parameters... |
| `--type {file,folder}` | The type of the asset (file or folder). |
| `--name NAME` | The name the asset should have in Frame.io. This value does not have to match the name of the file on disk; it can be... |
| `--description DESCRIPTION` | Brief description of the Asset. |
| `--source-url SOURCE_URL` | The URL of the source file. |

### `retrieve-options`

| Flag | Description |
|---|---|
| `--component-key COMPONENT_KEY` | componentKey |
| `--prop-name PROP_NAME` | propName |
| `--configured-props CONFIGURED_PROPS` | Previously configured property values for this component. Pass these so that dependent options can be resolved (e.g.... |

### `configure-component`

| Flag | Description |
|---|---|
| `--component-key COMPONENT_KEY` | componentKey |
| `--prop-name PROP_NAME` | propName |
| `--configured-props CONFIGURED_PROPS` | Previously configured property values for this component. Pass these so that dependent options can be resolved (e.g.... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'frame'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@frame` to bypass the 1h tool-list cache.
