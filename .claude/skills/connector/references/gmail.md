
# Gmail (via Higgsfield MCP proxy)

Send, read, draft, label, and search Gmail messages. Exposes 18 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @gmail <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @gmail --list                    # all 18 tools
./bin/mcp2cli @gmail gmail-get-current-user --help   # inspect one
./bin/mcp2cli @gmail gmail-get-current-user --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @gmail --pretty <cmd>` — `--pretty` goes AFTER `@gmail`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @gmail --head N <cmd>` — `--head N` goes AFTER `@gmail`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 18 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `gmail-get-current-user`

Returns the authenticated Gmail user's name, email address, and

_No flags._

### `gmail-bulk-archive-emails`

Archive multiple emails at once. [See the

| Flag | Description |
|---|---|
| `--messages MESSAGES` | The IDs of the emails to archive. Maximum 1000 messages per request. You can use the "retrieve_options" tool using th... |

### `gmail-send-email`

Send an email from your Google Workspace email account. [See the

| Flag | Description |
|---|---|
| `--to TO` | Enter a single recipient's email or multiple emails as items in an array. (JSON array) |
| `--cc CC` | Enter a single recipient's email or multiple emails as items in an array. (JSON array) |
| `--bcc BCC` | Enter a single recipient's email or multiple emails as items in an array. (JSON array) |
| `--from-name FROM_NAME` | Specify the name that will be displayed in the "From" section of the email. |
| `--from-email FROM_EMAIL` | Specify the email address that will be displayed in the "From" section of the email. You can use the "retrieve_option... |
| `--reply-to REPLY_TO` | Specify the email address that will appear on the "Reply-To" field, if different than the sender's email. |
| `--subject SUBJECT` | Specify a subject for the email. |
| `--body BODY` | Include an email body as either plain text or HTML. If HTML, make sure to set the "Body Type" prop to `html`. |
| `--body-type {html,plaintext}` | Choose to send as plain text or HTML. Defaults to `plaintext`. |
| `--attachment-filenames ATTACHMENT_FILENAMES` | Array of the names of the files to attach. Must contain the file extension (e.g. `.jpeg`, `.txt`). Use in conjuction ... |
| `--attachment-urls-or-paths ATTACHMENT_URLS_OR_PATHS` | Array of the URLs of the download links for the files, or the local paths (e.g. `/tmp/my-file.txt`). Use in conjuctio... |
| `--in-reply-to IN_REPLY_TO` | Specify the `message-id` this email is replying to You can use the "retrieve_options" tool using these parameters to ... |
| `--mime-type MIME_TYPE` | Mime Type of attachments. Setting the mime-type will override using the filename extension to determine attachment's ... |

### `gmail-create-draft`

Create a draft from your Google Workspace email account. [See the

| Flag | Description |
|---|---|
| `--to TO` | Enter a single recipient's email or multiple emails as items in an array. (JSON array) |
| `--cc CC` | Enter a single recipient's email or multiple emails as items in an array. (JSON array) |
| `--bcc BCC` | Enter a single recipient's email or multiple emails as items in an array. (JSON array) |
| `--subject SUBJECT` | Specify a subject for the email. |
| `--body BODY` | Include an email body as either plain text or HTML. If HTML, make sure to set the "Body Type" prop to `html`. |
| `--body-type {html,plaintext}` | Choose to send as plain text or HTML. Defaults to `plaintext`. |
| `--attachment-filenames ATTACHMENT_FILENAMES` | Array of the names of the files to attach. Must contain the file extension (e.g. `.jpeg`, `.txt`). Use in conjuction ... |
| `--attachment-urls-or-paths ATTACHMENT_URLS_OR_PATHS` | Array of the URLs of the download links for the files, or the local paths (e.g. `/tmp/my-file.txt`). Use in conjuctio... |
| `--in-reply-to IN_REPLY_TO` | Specify the `message-id` this email is replying to. You can use the "retrieve_options" tool using these parameters to... |
| `--mime-type MIME_TYPE` | Mime Type of attachments. Setting the mime-type will override using the filename extension to determine attachment's ... |
| `--from-email FROM_EMAIL` | Specify the email address that will be displayed in the "From" section of the email. You can use the "retrieve_option... |
| `--signature SIGNATURE` | An HTML signature composed in the Gmail Web UI that will be included in the message. Only works with the `HTML` body ... |

### `gmail-update-primary-signature`

Update the signature for the primary email address. [See the

| Flag | Description |
|---|---|
| `--signature SIGNATURE` | The new signature. |

### `gmail-update-org-signature`

Update the signature for a specific email address in an

| Flag | Description |
|---|---|
| `--signature SIGNATURE` | The new signature. |
| `--email EMAIL` | The email address that will have the signature updated. If updating the primary address, please use **Update Signatur... |

### `gmail-remove-label-from-email`

Remove label(s) from an email message. [See the

| Flag | Description |
|---|---|
| `--message MESSAGE` | The identifier of a message You can use the "retrieve_options" tool using these parameters to get the values. key: gm... |
| `--remove-label-ids REMOVE_LABEL_IDS` | The labels to remove from the email You can use the "retrieve_options" tool using these parameters to get the values.... |

### `gmail-list-thread-messages`

List messages in a thread. [See the

| Flag | Description |
|---|---|
| `--thread-id THREAD_ID` | Identifier of the thread to list messages from You can use the "retrieve_options" tool using these parameters to get ... |

### `gmail-list-send-as-aliases`

List all send as aliases for the authenticated user. [See the

_No flags._

### `gmail-list-labels`

List all the existing labels in the connected account. [See the

_No flags._

### `gmail-get-send-as-alias`

Get a send as alias for the authenticated user. [See the

| Flag | Description |
|---|---|
| `--send-as-email SEND_AS_EMAIL` | The email address of the send as alias to get You can use the "retrieve_options" tool using these parameters to get t... |

### `gmail-find-email`

Find an email using Google's Search Engine. [See the

| Flag | Description |
|---|---|
| `--q Q` | Apply a search filter using Gmail's [standard search o perators](https://support.google.com/mail/answer/7190) |
| `--with-text-payload` | Convert the payload response into a single text field. **This reduces the size of the payload and makes it easier for... |
| `--metadata-only` | Only return metadata for the messages. This reduces the size of the payload and makes it easier for LLMs work with. |
| `--labels LABELS` | Only return messages with labels that match all of the specified labels. You can use the "retrieve_options" tool usin... |
| `--include-spam-trash` | Include messages from `SPAM` and `TRASH` in the results. Defaults to `false`. |
| `--max-results MAX_RESULTS` | Maximum number of messages to return. Defaults to `20`. |

### `gmail-download-attachment`

Download an attachment by attachmentId to the /tmp directory. [See

| Flag | Description |
|---|---|
| `--message-id MESSAGE_ID` | The identifier of a message You can use the "retrieve_options" tool using these parameters to get the values. key: gm... |
| `--attachment-id ATTACHMENT_ID` | Identifier of the attachment to download You can use the "retrieve_options" tool using these parameters to get the va... |
| `--filename FILENAME` | Name of the new file. Example: `test.jpg` |
| `--convert-to-pdf` | Whether to convert the attachment to a PDF file. Supports converting image, text, HTML, and DOCX files. |

### `gmail-delete-email`

Moves the specified message to the trash. [See the

| Flag | Description |
|---|---|
| `--message-id MESSAGE_ID` | The ID of the message to delete You can use the "retrieve_options" tool using these parameters to get the values. key... |

### `gmail-create-label`

Create a new label in the connected account. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The display name of the label |
| `--text-color {#000000,#434343,#666666,#999999,#cccccc,#efefef,#f3f3f3,#ffffff,#fb4c2f,#ffad47,#fad165,#16a766,#43d692,#4a86e8,#a479e2,#f691b3,#f6c5be,#ffe6c7,#fef1d1,#b9e4d0,#c6f3de,#c9daf8,#e4d7f5,#fcdee8,#efa093,#ffd6a2,#fce8b3,#89d3b2,#a0eac9,#a4c2f4,#d0bcf1,#fbc8d9,#e66550,#ffbc6b,#fcda83,#44b984,#68dfa9,#6d9eeb,#b694e8,#f7a7c0,#cc3a21,#eaa041,#f2c960,#149e60,#3dc789,#3c78d8,#8e63ce,#e07798,#ac2b16,#cf8933,#d5ae49,#0b804b,#2a9c68,#285bac,#653e9b,#b65775,#464646,#e7e7e7,#0d3472,#b6cff5,#0d3b44,#98d7e4,#3d188e,#e3d7ff,#711a36,#fbd3e0,#8a1c0a,#f2b2a8,#7a2e0b,#ffc8af,#7a4706,#ffdeb5,#594c05,#fbe983,#684e07,#fdedc1,#0b4f30,#b3efd3,#04502e,#a2dcc1,#c2c2c2,#4986e7,#2da2bb,#b99aff,#994a64,#f691b2,#ff7537,#f691b3,#f6c5be,#fef1d1,#b9e4d0,#c6f3de,#c9daf8,#e4d7f5,#efa093,#ffd6a2,#fce8b3,#89d3b2,#a0eac9,#a4c2f4,#d0bcf1,#fbc8d9,#e66550,#fcda83,#44b984,#68dfa9,#b694e8,#f7a7c0,#eaa041,#f2c960,#149e60,#3dc789,#3c78d8,#8e63ce,#e07798,#ac2b16,#cf8933,#d5ae49,#0b804b,#2a9c68,#285bac,#b65775,#822111,#a46a21,#aa8831,#076239,#1a764d,#1c4587,#41236d,#83334c,#464646,#e7e7e7,#0d3472,#b6cff5,#98d7e4,#3d188e,#e3d7ff,#711a36,#fbd3e0,#8a1c0a,#f2b2a8,#7a2e0b,#ffc8af,#7a4706,#ffdeb5,#594c05,#fbe983,#684e07,#fdedc1,#0b4f30,#b3efd3,#04502e,#a2dcc1,#c2c2c2,#4986e7,#2da2bb,#b99aff,#994a64,#f691b2,#ff7537,#ffad46,#662e37,#cca6ac,#094228,#42d692}` | The text color of the label |
| `--background-color {#000000,#434343,#666666,#999999,#cccccc,#efefef,#f3f3f3,#ffffff,#fb4c2f,#ffad47,#fad165,#16a766,#43d692,#4a86e8,#a479e2,#f691b3,#f6c5be,#ffe6c7,#fef1d1,#b9e4d0,#c6f3de,#c9daf8,#e4d7f5,#fcdee8,#efa093,#ffd6a2,#fce8b3,#89d3b2,#a0eac9,#a4c2f4,#d0bcf1,#fbc8d9,#e66550,#ffbc6b,#fcda83,#44b984,#68dfa9,#6d9eeb,#b694e8,#f7a7c0,#cc3a21,#eaa041,#f2c960,#149e60,#3dc789,#3c78d8,#8e63ce,#e07798,#ac2b16,#cf8933,#d5ae49,#0b804b,#2a9c68,#285bac,#653e9b,#b65775,#464646,#e7e7e7,#0d3472,#b6cff5,#0d3b44,#98d7e4,#3d188e,#e3d7ff,#711a36,#fbd3e0,#8a1c0a,#f2b2a8,#7a2e0b,#ffc8af,#7a4706,#ffdeb5,#594c05,#fbe983,#684e07,#fdedc1,#0b4f30,#b3efd3,#04502e,#a2dcc1,#c2c2c2,#4986e7,#2da2bb,#b99aff,#994a64,#f691b2,#ff7537,#f691b3,#f6c5be,#fef1d1,#b9e4d0,#c6f3de,#c9daf8,#e4d7f5,#efa093,#ffd6a2,#fce8b3,#89d3b2,#a0eac9,#a4c2f4,#d0bcf1,#fbc8d9,#e66550,#fcda83,#44b984,#68dfa9,#b694e8,#f7a7c0,#eaa041,#f2c960,#149e60,#3dc789,#3c78d8,#8e63ce,#e07798,#ac2b16,#cf8933,#d5ae49,#0b804b,#2a9c68,#285bac,#b65775,#822111,#a46a21,#aa8831,#076239,#1a764d,#1c4587,#41236d,#83334c,#464646,#e7e7e7,#0d3472,#b6cff5,#98d7e4,#3d188e,#e3d7ff,#711a36,#fbd3e0,#8a1c0a,#f2b2a8,#7a2e0b,#ffc8af,#7a4706,#ffdeb5,#594c05,#fbe983,#684e07,#fdedc1,#0b4f30,#b3efd3,#04502e,#a2dcc1,#c2c2c2,#4986e7,#2da2bb,#b99aff,#994a64,#f691b2,#ff7537,#ffad46,#662e37,#cca6ac,#094228,#42d692}` | The background color of the label |
| `--message-list-visibility {show,hide}` | The visibility of messages with this label in the message list in the Gmail web interface |
| `--label-list-visibility {labelShow,labelShowIfUnread,labelHide}` | The visibility of the label in the label list in the Gmail web interface |

### `gmail-archive-email`

Archive an email message. [See the

| Flag | Description |
|---|---|
| `--message MESSAGE` | The identifier of a message You can use the "retrieve_options" tool using these parameters to get the values. key: gm... |

### `gmail-approve-workflow`

Suspend the workflow until approved by email. [See the

| Flag | Description |
|---|---|
| `--to TO` | Enter a single recipient's email or multiple emails as items in an array. (JSON array) |
| `--subject SUBJECT` | Specify a subject for the email. |
| `--body BODY` | Include an email body to send. Supports HTML |

### `gmail-add-label-to-email`

Add label(s) to an email message. [See the

| Flag | Description |
|---|---|
| `--message MESSAGE` | The identifier of a message You can use the "retrieve_options" tool using these parameters to get the values. key: gm... |
| `--add-label-ids ADD_LABEL_IDS` | Labels are used to categorize messages and threads within the user's mailbox You can use the "retrieve_options" tool ... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'gmail'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@gmail` to bypass the 1h tool-list cache.
