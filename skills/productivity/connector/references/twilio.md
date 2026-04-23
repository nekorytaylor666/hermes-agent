
# Twilio (via Higgsfield MCP proxy)

Send SMS and make calls via Twilio. Exposes 16 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @twilio <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @twilio --list                    # all 16 tools
./bin/mcp2cli @twilio twilio-send-sms-verification --help   # inspect one
./bin/mcp2cli @twilio twilio-send-sms-verification --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @twilio --pretty <cmd>` — `--pretty` goes AFTER `@twilio`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @twilio --head N <cmd>` — `--head N` goes AFTER `@twilio`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 16 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `twilio-send-sms-verification`

Send an SMS verification to a phone number. [See the

| Flag | Description |
|---|---|
| `--service-sid SERVICE_SID` | The SID of the service to which the verification belongs You can use the "retrieve_options" tool using these paramete... |
| `--to TO` | The destination phone number in E.164 format. Format with a `+` and country code (e.g., `+16175551212`). |

### `twilio-send-message`

Send an SMS text with optional media files. [See the

| Flag | Description |
|---|---|
| `--from FROM` | The sender's Twilio phone number (in [E.164](https://en.wikipedia.org/wiki/E.164) format), [alphanumeric sender ID](h... |
| `--to TO` | The destination phone number in E.164 format. Format with a `+` and country code (e.g., `+16175551212`). |
| `--body BODY` | The text of the message you want to send, limited to 1600 characters. |
| `--media-url MEDIA_URL` | The URL of the media you wish to send out with the message. The media size limit is `5MB`. You may provide up to 10 m... |

### `twilio-phone-number-lookup`

Lookup information about a phone number. [See the

| Flag | Description |
|---|---|
| `--sid SID` | The phone number to lookup |

### `twilio-make-phone-call`

Make a phone call passing text, a URL, or an application that Twilio

| Flag | Description |
|---|---|
| `--from FROM` | The phone number or alphanumeric sender ID the message is from You can use the "retrieve_options" tool using these pa... |
| `--to TO` | The destination phone number in E.164 format. Format with a `+` and country code (e.g., `+16175551212`). |
| `--call-type {text,url,application}` | Whether to use `text`, a `URL`, or an `application` to handle the call |
| `--timeout TIMEOUT` | The integer number of seconds that we should allow the phone to ring before assuming there is no answer. The default ... |
| `--record` | Whether to record the call |

### `twilio-list-transcripts`

Return a list of transcripts. [See the

| Flag | Description |
|---|---|
| `--include-transcript-text` | Set to `true` to include the transcript sentences in the response |
| `--limit LIMIT` | The maximum number of results to retrieve |

### `twilio-list-messages`

Return a list of messages associated with your account. [See the

| Flag | Description |
|---|---|
| `--from FROM` | Read messages sent from only this phone number or alphanumeric sender ID. Format the phone number in E.164 format wit... |
| `--to TO` | Read messages sent to only this phone number. Format the phone number in E.164 format with a `+` and country code (e.... |
| `--limit LIMIT` | The maximum number of results to retrieve |

### `twilio-list-message-media`

Return a list of media associated with your message. [See the

| Flag | Description |
|---|---|
| `--message-id MESSAGE_ID` | The SID of the Message You can use the "retrieve_options" tool using these parameters to get the values. key: twilio-... |
| `--limit LIMIT` | The maximum number of results to retrieve |

### `twilio-list-calls`

Return a list of calls associated with your account. [See the

| Flag | Description |
|---|---|
| `--from FROM` | Only include calls from this phone number, SIP address, Client identifier or SIM SID. Format the phone number in E.16... |
| `--to TO` | Only show calls made to this phone number, SIP address, Client identifier or SIM SID. Format the phone number in E.16... |
| `--parent-call-sid PARENT_CALL_SID` | Only include calls spawned by calls with this SID. You can use the "retrieve_options" tool using these parameters to ... |
| `--status {queued,ringing,in-progress,canceled,completed,failed,busy,no-answer}` | The status of the call |
| `--limit LIMIT` | The maximum number of results to retrieve |

### `twilio-get-transcripts`

Retrieves full transcripts for the specified transcript SIDs. [See

| Flag | Description |
|---|---|
| `--transcript-sids TRANSCRIPT_SIDS` | The unique SID identifiers of the Transcripts to retrieve You can use the "retrieve_options" tool using these paramet... |

### `twilio-get-message`

Return details of a message. [See the

| Flag | Description |
|---|---|
| `--message-id MESSAGE_ID` | The SID of the Message You can use the "retrieve_options" tool using these parameters to get the values. key: twilio-... |

### `twilio-get-call`

Return call resource of an individual call. [See the

| Flag | Description |
|---|---|
| `--sid SID` | The SID of the Call You can use the "retrieve_options" tool using these parameters to get the values. key: twilio-get... |
| `--include-transcripts` | Set to `true` to include recording transcript(s) if available |

### `twilio-download-recording-media`

Download a recording media file. [See the

| Flag | Description |
|---|---|
| `--recording-id RECORDING_ID` | The SID of the Recording You can use the "retrieve_options" tool using these parameters to get the values. key: twili... |
| `--format {.mp3,.wav}` | The format of the recording audio file |
| `--file-path FILE_PATH` | The destination path in [`/tmp`](https://pipedream.com /docs/workflows/steps/code/nodejs/working-with- files/#the-tmp... |

### `twilio-delete-message`

Delete a message record from your account. [See the

| Flag | Description |
|---|---|
| `--message-id MESSAGE_ID` | The SID of the Message You can use the "retrieve_options" tool using these parameters to get the values. key: twilio-... |

### `twilio-delete-call`

Remove a call record from your account. [See the

| Flag | Description |
|---|---|
| `--sid SID` | The SID of the Call You can use the "retrieve_options" tool using these parameters to get the values. key: twilio-del... |

### `twilio-create-verification-service`

Create a verification service for sending SMS verifications. [See the

| Flag | Description |
|---|---|
| `--friendly-name FRIENDLY_NAME` | The name of the new verification service |

### `twilio-check-verification-token`

Check if user-provided token is correct. [See the

| Flag | Description |
|---|---|
| `--service-sid SERVICE_SID` | The SID of the service to which the verification belongs You can use the "retrieve_options" tool using these paramete... |
| `--to TO` | The destination phone number in E.164 format. Format with a `+` and country code (e.g., `+16175551212`). |
| `--code CODE` | The code to check |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'twilio'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@twilio` to bypass the 1h tool-list cache.
