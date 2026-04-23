
# WhatsApp Business (via Higgsfield MCP proxy)

Send WhatsApp Business messages, templates, voice. Exposes 4 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @whatsapp <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @whatsapp --list                    # all 4 tools
./bin/mcp2cli @whatsapp whatsapp-business-send-text-using-template --help   # inspect one
./bin/mcp2cli @whatsapp whatsapp-business-send-text-using-template --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @whatsapp --pretty <cmd>` — `--pretty` goes AFTER `@whatsapp`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @whatsapp --head N <cmd>` — `--head N` goes AFTER `@whatsapp`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 4 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `whatsapp-business-send-text-using-template`

Send a text message using a pre-defined template. Variables can be

| Flag | Description |
|---|---|
| `--phone-number-id PHONE_NUMBER_ID` | Phone number ID that will be used to send the message. You can use the "retrieve_options" tool using these parameters... |
| `--recipient-phone-number RECIPIENT_PHONE_NUMBER` | Enter the recipient's phone number. For example, `15101234567`. |
| `--message-template MESSAGE_TEMPLATE` | Select the template you'd like to use. You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--header-vars HEADER_VARS` | Array of header variables for programmatic/AI-agent use. Takes precedence over individual header props if provided. (... |
| `--body-vars BODY_VARS` | Array of body variables for programmatic/AI-agent use. Takes precedence over individual body props if provided. (JSON... |
| `--button-vars BUTTON_VARS` | Array of button variables for programmatic/AI-agent use. Takes precedence over individual button props if provided. (... |

### `whatsapp-business-send-voice-message`

Sends a voice message. [See the

| Flag | Description |
|---|---|
| `--phone-number-id PHONE_NUMBER_ID` | Phone number ID that will be used to send the message. You can use the "retrieve_options" tool using these parameters... |
| `--recipient-phone-number RECIPIENT_PHONE_NUMBER` | Enter the recipient's phone number. For example, `15101234567`. |
| `--file-path FILE_PATH` | Provide either a file URL or a path to a file in the /tmp directory (for example, /tmp/myFile.pdf). |
| `--type {audio/aac,audio/mp4,audio/mpeg,audio/amr,audio/ogg,audio/opus}` | The mime-type of media file being uploaded |

### `whatsapp-business-send-text-message`

Sends a text message. [See the

| Flag | Description |
|---|---|
| `--phone-number-id PHONE_NUMBER_ID` | Phone number ID that will be used to send the message. You can use the "retrieve_options" tool using these parameters... |
| `--recipient-phone-number RECIPIENT_PHONE_NUMBER` | Enter the recipient's phone number. For example, `15101234567`. |
| `--message-body MESSAGE_BODY` | The text content of the message. |

### `whatsapp-business-list-message-templates`

Lists message templates. [See the

_No flags._

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'whatsapp'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@whatsapp` to bypass the 1h tool-list cache.
