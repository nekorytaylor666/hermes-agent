
# YouTube Analytics (via Higgsfield MCP proxy)

Query YouTube channel analytics. Exposes 3 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @youtube-analytics <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @youtube-analytics --list                    # all 3 tools
./bin/mcp2cli @youtube-analytics youtube-analytics-api-query-custom-analytics --help   # inspect one
./bin/mcp2cli @youtube-analytics youtube-analytics-api-query-custom-analytics --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @youtube-analytics --pretty <cmd>` — `--pretty` goes AFTER `@youtube-analytics`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @youtube-analytics --head N <cmd>` — `--head N` goes AFTER `@youtube-analytics`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 3 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `youtube-analytics-api-query-custom-analytics`

Execute a custom analytics query using specified metrics, dimensions,

| Flag | Description |
|---|---|
| `--start-date START_DATE` | The start date for fetching YouTube Analytics data. The value should be in `YYYY-MM-DD` format. |
| `--end-date END_DATE` | The end date for fetching YouTube Analytics data. The value should be in `YYYY-MM-DD` format. The API response contai... |
| `--dimensions DIMENSIONS` | A list of YouTube Analytics dimensions, such as `video` or `ageGroup`, `gender`. See the documentation for [channel r... |
| `--sort SORT` | A list of dimensions or metrics that determine the sort order for YouTube Analytics data. By default the sort order i... |
| `--max-results MAX_RESULTS` | The maximum number of rows to include in the response. |
| `--id-type {MINE,channelId,contentOwner}` | The type of ID to use for the query. This can be either `My Channel`, `Channel ID`, or `Content Owner`. |
| `--metrics METRICS` | Metrics, such as `views` or `likes`, `dislikes`. See the documentation for [channel reports](https://develo pers.goog... |
| `--filters FILTERS` | A list of filters that should be applied when retrieving YouTube Analytics data. The documentation for [channel repor... |

### `youtube-analytics-api-list-channel-reports`

Fetch summary analytics reports for a specified youtube channel

| Flag | Description |
|---|---|
| `--start-date START_DATE` | The start date for fetching YouTube Analytics data. The value should be in `YYYY-MM-DD` format. |
| `--end-date END_DATE` | The end date for fetching YouTube Analytics data. The value should be in `YYYY-MM-DD` format. The API response contai... |
| `--dimensions DIMENSIONS` | A list of YouTube Analytics dimensions, such as `video` or `ageGroup`, `gender`. See the documentation for [channel r... |
| `--sort SORT` | A list of dimensions or metrics that determine the sort order for YouTube Analytics data. By default the sort order i... |
| `--max-results MAX_RESULTS` | The maximum number of rows to include in the response. |
| `--id-type {MINE,channelId,contentOwner}` | The type of ID to use for the query. This can be either `My Channel`, `Channel ID`, or `Content Owner`. |

### `youtube-analytics-api-get-video-metrics`

Retrieve detailed analytics for a specific video. [See the

| Flag | Description |
|---|---|
| `--start-date START_DATE` | The start date for fetching YouTube Analytics data. The value should be in `YYYY-MM-DD` format. |
| `--end-date END_DATE` | The end date for fetching YouTube Analytics data. The value should be in `YYYY-MM-DD` format. The API response contai... |
| `--dimensions DIMENSIONS` | A list of YouTube Analytics dimensions, such as `video` or `ageGroup`, `gender`. See the documentation for [channel r... |
| `--sort SORT` | A list of dimensions or metrics that determine the sort order for YouTube Analytics data. By default the sort order i... |
| `--max-results MAX_RESULTS` | The maximum number of rows to include in the response. |
| `--id-type {MINE,channelId,contentOwner}` | The type of ID to use for the query. This can be either `My Channel`, `Channel ID`, or `Content Owner`. |
| `--video-id VIDEO_ID` | The ID of the video for which you want to retrieve metrics. Eg. `pd1FJh59zxQ`. |
| `--metrics METRICS` | Metrics, such as `views` or `likes`, `dislikes`. See the documentation for [channel reports](https://develo pers.goog... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'youtube-analytics'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@youtube-analytics` to bypass the 1h tool-list cache.
