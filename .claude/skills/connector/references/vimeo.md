
# Vimeo (via Higgsfield MCP proxy)

Upload videos, manage albums. Exposes 3 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @vimeo <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @vimeo --list                    # all 3 tools
./bin/mcp2cli @vimeo vimeo-upload-video --help   # inspect one
./bin/mcp2cli @vimeo vimeo-upload-video --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @vimeo --pretty <cmd>` — `--pretty` goes AFTER `@vimeo`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @vimeo --head N <cmd>` — `--head N` goes AFTER `@vimeo`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 3 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `vimeo-upload-video`

Uploads a video to the user's Vimeo account. Ensure you have enough

| Flag | Description |
|---|---|
| `--video-url VIDEO_URL` | URL of the video file to upload |
| `--name NAME` | The title of the video |
| `--description DESCRIPTION` | The description of the video |

### `vimeo-delete-video`

Permanently deletes a video from the user's Vimeo account. This

| Flag | Description |
|---|---|
| `--video-id VIDEO_ID` | The ID of the video You can use the "retrieve_options" tool using these parameters to get the values. key: vimeo-dele... |

### `vimeo-add-video-to-album`

Adds an existing video to a user's album/showcase on Vimeo. [See the

| Flag | Description |
|---|---|
| `--video-id VIDEO_ID` | The ID of the video You can use the "retrieve_options" tool using these parameters to get the values. key: vimeo-add-... |
| `--album-uri ALBUM_URI` | The URI of the album to add the video to You can use the "retrieve_options" tool using these parameters to get the va... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'vimeo'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@vimeo` to bypass the 1h tool-list cache.
