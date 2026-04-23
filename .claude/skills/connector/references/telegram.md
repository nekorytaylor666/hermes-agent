
# Telegram (via Higgsfield MCP proxy)

CLI wrapper over the Pipedream-hosted Telegram Bot API exposed through the Higgsfield MCP proxy. 28 tools covering sending, editing, forwarding, pinning, chat management, and member moderation.

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @telegram <command> [flags]
```

## Core workflow

```bash
# 1. Discover commands (27 telegram tools + 2 config helpers)
./bin/mcp2cli @telegram --list

# 2. Inspect one command's flags
./bin/mcp2cli @telegram telegram-bot-api-send-text-message-or-reply --help

# 3. Invoke
./bin/mcp2cli @telegram telegram-bot-api-send-text-message-or-reply \
  --chat-id "@mychannel" --text "hello"
```

## Chat ID formats

The `--chat-id` flag accepts:

- Numeric ID: `1035597319` (bot, private chat, or group)
- Public channel/group username: `@mygroup` (extract from `t.me/mygroup`)
- Private chat: numeric user ID

For `--user-id` (member management): numeric Telegram user ID only.

## Media upload: `file_id` vs URL vs upload

The file flags (`--photo`, `--video`, `--audio`, etc.) all accept:

- A Telegram `file_id` string (for files already on Telegram's servers)
- An HTTP(S) URL (Telegram fetches it)
- A local file upload is **not directly supported** via this CLI — use a URL instead

Use `--content-type` to override the MIME type when the server can't infer it.

## Parse modes

For messages with formatting, pass `--parse-mode MarkdownV2`, `--parse-mode HTML`, or `--parse-mode Markdown`. See [Telegram formatting docs](https://core.telegram.org/bots/api#formatting-options).

## Common patterns

### Send a simple text message

```bash
./bin/mcp2cli @telegram telegram-bot-api-send-text-message-or-reply \
  --chat-id "@mychannel" --text "Build completed"
```

### Reply to a message

```bash
./bin/mcp2cli @telegram telegram-bot-api-send-text-message-or-reply \
  --chat-id "@mychannel" --text "+1" --reply-to-message-id 12345
```

### Send a photo by URL

```bash
./bin/mcp2cli @telegram telegram-bot-api-send-photo \
  --chat-id "@mychannel" \
  --photo "https://example.com/pic.png" \
  --caption "Latest render"
```

### Send a formatted message (HTML)

```bash
./bin/mcp2cli @telegram telegram-bot-api-send-text-message-or-reply \
  --chat-id "@mychannel" \
  --parse-mode HTML \
  --text '<b>Alert:</b> service down'
```

### Forward a message

```bash
./bin/mcp2cli @telegram telegram-bot-api-forward-message \
  --from-chat-id "@src" --chat-id "@dst" --message-id 42
```

### Poll for incoming updates

```bash
# First call — fetch first 100 updates
./bin/mcp2cli @telegram telegram-bot-api-list-updates --limit 100

# With --auto-paging, server-side offset advances automatically.
# WARNING: --auto-paging consumes updates; they won't appear again.
./bin/mcp2cli @telegram telegram-bot-api-list-updates --auto-paging
```

### Restrict a user for 1 hour

```bash
UNTIL=$(( $(date +%s) + 3600 ))
./bin/mcp2cli @telegram telegram-bot-api-restrict-chat-member \
  --chat-id "@mygroup" --user-id 123456789 --until-date $UNTIL
```

### JSON-valued flags (reply markup, link preview, album media)

`--reply-markup`, `--link-preview-options`, and `--media` accept JSON strings. Quote carefully:

```bash
./bin/mcp2cli @telegram telegram-bot-api-send-text-message-or-reply \
  --chat-id "@mychannel" --text "Pick one" \
  --reply-markup '{"inline_keyboard":[[{"text":"Yes","callback_data":"y"},{"text":"No","callback_data":"n"}]]}'
```

### Send an album (2-10 items)

```bash
./bin/mcp2cli @telegram telegram-bot-api-send-album \
  --chat-id "@mychannel" \
  --media '[{"type":"photo","media":"https://example.com/a.jpg"},{"type":"photo","media":"https://example.com/b.jpg"}]'
```

### Pipe JSON from stdin (all commands support `--stdin`)

```bash
echo '{"chat-id":"@mychannel","text":"from stdin"}' | \
  ./bin/mcp2cli @telegram telegram-bot-api-send-text-message-or-reply --stdin
```

## Gotchas

- **`--auto-paging` on `list-updates` / `list-chats` is destructive to the offset cursor.** Updates consumed by an auto-paging call won't be returned again. For iterative polling, track `--offset` manually.
- **Unix timestamps for dates.** `--until-date` and `--expire-date` want seconds-since-epoch, not ISO dates.
- **Silent messages.** `--disable-notification` sends silently — users still see the message, just no push.
- **Channel vs group vs supergroup** — some admin flags only work on channels (e.g. `--can-post-messages`), others only on supergroups (e.g. `--can-pin-messages`). See each command's `--help` for the exact constraints.
- **`retrieve-options` / `configure-component`** are helper tools for dynamic field resolution (e.g. when a dropdown's options depend on another field). You rarely call them directly.
- **Long responses (e.g. `list-chats`) can be large.** Global flags like `--pretty` and `--head N` go **after** `@telegram`, not before: `./bin/mcp2cli @telegram --head 10 telegram-bot-api-list-chats` (putting the flag before `@telegram` makes mcp2cli enter raw mode and error).

## Security

- The JWT grants full API access for the associated Higgsfield chat/folder — rotate on compromise.
- `mcp2cli bake show telegram` masks auth headers in its output, but the raw `baked.json` file does not redact; protect it with filesystem permissions (0600).

## Command reference

Every command below is callable as:

```bash
./bin/mcp2cli @telegram [--pretty] [--head N] <command> [flags] [--stdin]
```

`--stdin` reads a JSON object from stdin in lieu of flags. `--pretty` and `--head N` are global mcp2cli flags — they go **after** `@telegram` (before the command name). Placing them before `@telegram` makes mcp2cli enter raw mode and error.

### Sending

#### `telegram-bot-api-send-text-message-or-reply`

Send a text message (or reply)

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat (numeric ID or `@username`) |
| `--text TEXT` | Message text |
| `--parse-mode {MarkdownV2,HTML,Markdown}` | Formatting mode |
| `--disable-notification` | Silent send (no push) |
| `--link-preview-options LINK_PREVIEW_OPTIONS` | JSON object for link previews |
| `--reply-to-message-id REPLY_TO_MESSAGE_ID` | Message ID this is a reply to |
| `--reply-markup REPLY_MARKUP` | JSON object: inline/reply keyboard |

#### `telegram-bot-api-send-photo`

Send a photo

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--caption CAPTION` | Photo caption |
| `--filename FILENAME` | Filename hint |
| `--photo PHOTO` | file_id, URL, or upload source |
| `--disable-notification` | Silent send |
| `--parse-mode {MarkdownV2,HTML,Markdown}` | Caption formatting |
| `--reply-to-message-id REPLY_TO_MESSAGE_ID` | Reply target |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |
| `--content-type {image/gif,image/jpeg,image/png,image/bmp,image/svg+xml}` | MIME type override |

#### `telegram-bot-api-send-video`

Send a video file

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--caption CAPTION` | Video caption |
| `--filename FILENAME` | Filename hint |
| `--video VIDEO` | file_id, URL, or upload source |
| `--content-type {video/mpeg,video/mp4,video/webm,video/ogg}` | MIME type |
| `--duration DURATION` | Duration (seconds) |
| `--width WIDTH` | Video width |
| `--height HEIGHT` | Video height |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |

#### `telegram-bot-api-send-video-note`

Send a round video note

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--filename FILENAME` | Filename hint |
| `--video-note VIDEO_NOTE` | file_id, URL, or upload source |
| `--content-type {video/mpeg,video/mp4,video/webm,video/ogg}` | MIME type |
| `--length LENGTH` | Diameter in px |
| `--duration DURATION` | Duration (seconds) |
| `--reply-to-message-id REPLY_TO_MESSAGE_ID` | Reply target |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |

#### `telegram-bot-api-send-voice-message`

Send a voice message

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--caption CAPTION` | Voice caption |
| `--filename FILENAME` | Filename hint |
| `--voice VOICE` | file_id, URL, or upload source |
| `--parse-mode {MarkdownV2,HTML,Markdown}` | Caption formatting |
| `--disable-notification` | Silent send |
| `--content-type {audio/mpeg,audio/mid,audio/webm,audio/ogg,audio/vnd.wav,video/mp4,video/webm,video/ogg}` | MIME type |
| `--duration DURATION` | Duration (seconds) |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |

#### `telegram-bot-api-send-audio-file`

Send an audio file

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--caption CAPTION` | Audio caption |
| `--filename FILENAME` | Filename hint |
| `--audio AUDIO` | file_id, URL, or upload source |
| `--parse-mode {MarkdownV2,HTML,Markdown}` | Caption formatting |
| `--disable-notification` | Silent send |
| `--duration DURATION` | Duration (seconds) |
| `--performer PERFORMER` | Performer name |
| `--title TITLE` | Track name |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |
| `--content-type {audio/mpeg,audio/mid,audio/webm,audio/ogg,audio/vnd.wav}` | MIME type |

#### `telegram-bot-api-send-document-or-image`

Send a document or image

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--caption CAPTION` | File caption |
| `--filename FILENAME` | Filename hint |
| `--doc DOC` | file_id, URL, or upload source |
| `--parse-mode {MarkdownV2,HTML,Markdown}` | Caption formatting |
| `--content-type {...wide MIME set...}` | MIME type override |
| `--disable-notification` | Silent send |
| `--reply-to-message-id REPLY_TO_MESSAGE_ID` | Reply target |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |

#### `telegram-bot-api-send-sticker`

Send a .webp sticker

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--filename FILENAME` | Filename hint |
| `--sticker STICKER` | file_id or URL |
| `--reply-to-message-id REPLY_TO_MESSAGE_ID` | Reply target |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |

#### `telegram-bot-api-send-album`

Send a group of 2-10 photos/videos as an album

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--media MEDIA` | JSON array of `{type, media, caption?}` items (2-10) |
| `--disable-notification` | Silent send |

#### `telegram-bot-api-send-media-by-url-or-id`

Send any media type by URL or file_id (generic)

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--caption CAPTION` | Caption |
| `--media-type {Document/Image,Photo,Audio,Video,Video Note,Voice,Sticker}` | Pick which type to send |
| `--media MEDIA` | URL or file_id |
| `--disable-notification` | Silent send |
| `--reply-to-message-id REPLY_TO_MESSAGE_ID` | Reply target |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |

### Editing / forwarding / deleting

#### `telegram-bot-api-edit-text-message`

Edit a previously-sent text message

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--message-id MESSAGE_ID` | Message to edit |
| `--text TEXT` | New text |
| `--disable-notification` | Silent (rarely useful for edits) |

#### `telegram-bot-api-edit-media-message`

Edit a previously-sent media message

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--message-id MESSAGE_ID` | Message to edit |
| `--type {photo,video}` | Media type |
| `--caption CAPTION` | New caption |
| `--filename FILENAME` | Filename hint |
| `--media MEDIA` | New file_id or URL |
| `--parse-mode {MarkdownV2,HTML,Markdown}` | Caption formatting |
| `--reply-markup REPLY_MARKUP` | Inline/reply keyboard JSON |

#### `telegram-bot-api-forward-message`

Forward a message from one chat to another

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Destination chat |
| `--from-chat-id FROM_CHAT_ID` | Source chat |
| `--message-id MESSAGE_ID` | Message ID in source chat |
| `--disable-notification` | Silent send |

#### `telegram-bot-api-delete-message`

Delete a message

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--message-id MESSAGE_ID` | Message to delete |

#### `telegram-bot-api-pin-message`

Pin a message in a chat

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--message-id MESSAGE_ID` | Message to pin |
| `--disable-notification` | Pin without push to members |

#### `telegram-bot-api-unpin-message`

Unpin a message

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--message-id MESSAGE_ID` | Message to unpin |

### Listing / inspecting

#### `telegram-bot-api-list-chats`

List available Telegram chats

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--offset OFFSET` | Pagination start (update ID) |
| `--limit LIMIT` | Max items 1-100 |
| `--auto-paging` | Auto-advance offset (destructive) |

#### `telegram-bot-api-list-updates`

List new updates (incoming events)

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--offset OFFSET` | Pagination start (update ID) |
| `--limit LIMIT` | Max items 1-100 |
| `--auto-paging` | Auto-advance offset (destructive) |

#### `telegram-bot-api-list-administrators-in-chat`

List admins in a chat

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |

#### `telegram-bot-api-get-num-members-in-chat`

Get member count of a chat

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |

### Member / permissions management

#### `telegram-bot-api-kick-chat-member`

Kick (ban) a user from a group/supergroup/channel

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--user-id USER_ID` | User to kick |
| `--until-date UNTIL_DATE` | Unix timestamp of unban (omit = permanent) |

#### `telegram-bot-api-restrict-chat-member`

Restrict what a user can do in a supergroup

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--user-id USER_ID` | User to restrict |
| `--until-date UNTIL_DATE` | Unix timestamp when restriction ends |
| `--can-send-messages` | Allow text/contacts/locations |
| `--can-send-media-messages` | Allow media (implies send-messages) |
| `--can-send-other-messages` | Allow stickers/gifs/inline bots |
| `--can-add-web-page-previews` | Allow link previews |

#### `telegram-bot-api-promote-chat-member`

Promote/demote a user in a supergroup or channel

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--user-id USER_ID` | User to promote/demote |
| `--can-change-info` | May edit chat title/photo |
| `--can-post-messages` | May post in channel (channels only) |
| `--can-edit-messages` | May edit others' messages (channels only) |
| `--can-delete-messages` | May delete others' messages |
| `--can-invite-users` | May invite new users |
| `--can-restrict-members` | May restrict/ban |
| `--can-pin-messages` | May pin (supergroups only) |
| `--can-promote-members` | May delegate admin rights |

#### `telegram-bot-api-set-chat-permissions`

Set default permissions for all chat members

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--can-send-messages` | Text/contacts/locations |
| `--can-send-media-messages` | Media |
| `--can-send-polls` | Polls |
| `--can-send-other-messages` | Stickers/gifs/inline bots |
| `--can-add-web-page-previews` | Link previews |
| `--can-change-info` | Change title/photo (ignored in public supergroups) |
| `--can-invite-users` | Invite |
| `--can-pin-messages` | Pin (ignored in public supergroups) |

### Invite links

#### `telegram-bot-api-create-chat-invite-link`

Create an additional invite link

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |
| `--name NAME` | Link label (0-32 chars) |
| `--expire-date EXPIRE_DATE` | Unix timestamp when it expires |
| `--member-limit MEMBER_LIMIT` | Cap of users using this link (1-99999) |
| `--creates-join-request` | Require admin approval (incompatible with member-limit) |

#### `telegram-bot-api-export-chat-invite-link`

Regenerate the chat's primary invite link

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--chat-id CHAT_ID` | Target chat |

### Dynamic configuration helpers

Used internally by the Pipedream proxy to resolve dependent dropdown options. You rarely call these directly.

#### `retrieve-options`

Fetch available option values for a configurable component field

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--component-key COMPONENT_KEY` | Which component |
| `--prop-name PROP_NAME` | Which field |
| `--configured-props CONFIGURED_PROPS` | JSON of already-set fields (dependencies) |

#### `configure-component`

Validate/apply configuration for a component field

| Flag | Description |
|---|---|
| `--stdin` | Read JSON body/arguments from stdin |
| `--component-key COMPONENT_KEY` | Which component |
| `--prop-name PROP_NAME` | Which field |
| `--configured-props CONFIGURED_PROPS` | JSON of already-set fields |

## Troubleshooting

- **`Error: no baked tool named 'telegram'`** → the `telegram` config is missing from `~/.config/mcp2cli/baked.json`. Re-run `make bake` from the mcp2cli project.
- **`PackageNotFoundError: No package metadata was found for mcp2cli`** → the bundled binary was built for a different Python minor version; rebuild with matching `PY`.
- **`@telegram` passes flags to the tool server literally** → if a flag value starts with `-`, separate with `--`: `./bin/mcp2cli @telegram ... -- --text "-leading dash"`.
