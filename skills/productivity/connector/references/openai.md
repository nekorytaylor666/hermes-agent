---
name: openai
description: Transcribe audio to text via OpenAI Whisper (openai-create-transcription only). Use for any OpenAI Whisper Transcription automation task. Triggers include "openai", "openai whisper transcription".
allowed-tools: Bash(openai *), Bash(./bin/mcp2cli *), Bash(mcp2cli *)
---

# OpenAI Whisper Transcription (via Higgsfield MCP proxy)

Transcribe audio to text via OpenAI Whisper (openai-create-transcription only). Exposes 1 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @openai <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @openai --list                    # all 1 tools
./bin/mcp2cli @openai openai-create-transcription --help   # inspect one
./bin/mcp2cli @openai openai-create-transcription --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @openai --pretty <cmd>` — `--pretty` goes AFTER `@openai`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @openai --head N <cmd>` — `--head N` goes AFTER `@openai`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 1 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `openai-create-transcription`

| Flag | Description |
|---|---|
| `--file FILE` | The file to process. Provide either a file URL or a path to a file in the `/tmp` directory (for example, `/tmp/myFile... |
| `--model {gpt-4o-transcribe,gpt-4o-mini-transcribe,whisper-1}` | ID of the model to use |
| `--include INCLUDE` | Additional information to include in the transcription response. `logprobs` will return the log probabilities of the... |
| `--language LANGUAGE` | The language of the input audio. Supplying the input language in [ISO-639- 1](https://en.wikipedia.org/wiki/List_of_I... |
| `--prompt PROMPT` | An optional text to guide the model's style or continue a previous audio segment. The [prompt](https: //platform.open... |
| `--response-format {json,text,srt,verbose_json,vtt}` | The format of the output. For `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`, the only supported format is `json`. |
| `--temperature TEMPERATURE` | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower value... |
| `--timestamp-granularities TIMESTAMP_GRANULARITIES` | The timestamp granularities to populate for this transcription. `response_format` must be set `verbose_json` to use t... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'openai'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@openai` to bypass the 1h tool-list cache.
