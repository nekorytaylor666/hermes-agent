
# Discord Bot (via Higgsfield MCP proxy)

Discord channel messages, reactions, threads, webhooks. Exposes 22 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @discord <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @discord --list                    # all 22 tools
./bin/mcp2cli @discord discord-bot-send-message-with-file --help   # inspect one
./bin/mcp2cli @discord discord-bot-send-message-with-file --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @discord --pretty <cmd>` — `--pretty` goes AFTER `@discord`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @discord --head N <cmd>` — `--head N` goes AFTER `@discord`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 22 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `discord-bot-send-message-with-file`

Post a message with an attached file. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--file FILE` | Provide either a file URL or a path to a file in the `/tmp` directory (for example, `/tmp/example.pdf`) |
| `--message MESSAGE` | Enter a simple message up to 2000 characters. This is the most commonly used field. However, it's optional if you pas... |
| `--user-id USER_ID` | Select either an user or a channel You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--channel-id CHANNEL_ID` | Select either a channel or an user You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--embeds EMBEDS` | Embedded rich content (up to 6000 characters), this should be given as an array, e.g. `[{"title": "Hello, Embed!","de... |
| `--thread-id THREAD_ID` | If provided, the message will be posted to this thread |
| `--username USERNAME` | Overrides the current username |
| `--avatar-url AVATAR_URL` | If used, it overrides the default avatar |
| `--include-sent-via-pipedream` | Defaults to `true`, includes a link to this workflow at the end of your Discord message. |

### `discord-bot-send-message`

Send message to a user or a channel. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--message MESSAGE` | Enter a simple message up to 2000 characters. This is the most commonly used field. However, it's optional if you pas... |
| `--embeds EMBEDS` | Embedded rich content (up to 6000 characters), this should be given as an array, e.g. `[{"title": "Hello, Embed!","de... |
| `--thread-id THREAD_ID` | If provided, the message will be posted to this thread |
| `--username USERNAME` | Overrides the current username |
| `--avatar-url AVATAR_URL` | If used, it overrides the default avatar |
| `--include-sent-via-pipedream` | Defaults to `true`, includes a link to this workflow at the end of your Discord message. |
| `--user-id USER_ID` | Select either a user or a channel You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--channel-id CHANNEL_ID` | Select either a channel or an user You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `discord-bot-send-message-to-forum-post`

Send a message to a Discord forum. [See the

| Flag | Description |
|---|---|
| `--post-id POST_ID` | The ID of a forum post |
| `--message MESSAGE` | Enter a simple message up to 2000 characters. This is the most commonly used field. However, it's optional if you pas... |
| `--embeds EMBEDS` | Embedded rich content (up to 6000 characters), this should be given as an array, e.g. `[{"title": "Hello, Embed!","de... |
| `--username USERNAME` | Overrides the current username |
| `--avatar-url AVATAR_URL` | If used, it overrides the default avatar |
| `--include-sent-via-pipedream` | Defaults to `true`, includes a link to this workflow at the end of your Discord message. |

### `discord-bot-rename-channel`

Rename a channel to a specified name you choose

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select the channel you'd like to change its name You can use the "retrieve_options" tool using these parameter... |
| `--name NAME` | There is a 1-100 character channel name restriction |

### `discord-bot-remove-user-role`

Remove a selected role from the specified user. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--user-id USER_ID` | Please select a user You can use the "retrieve_options" tool using these parameters to get the values. key: discord_b... |
| `--role-id ROLE_ID` | Please select the role you want to remove from the user You can use the "retrieve_options" tool using these parameter... |

### `discord-bot-post-reaction-with-emoji`

Post a reaction for a message with an emoji. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |
| `--message-id MESSAGE_ID` | Please select a message from the list You can use the "retrieve_options" tool using these parameters to get the value... |
| `--emoji EMOJI` | Emoji (eg. 👍). To use custom emoji, you must encode it in the format `name:id` with the emoji name and emoji id. |

### `discord-bot-modify-guild-member`

Update attributes of a guild member. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Id of channel to move user to (if they are connected to voice) You can use the "retrieve_options" tool using these pa... |
| `--user-id USER_ID` | Please select a user You can use the "retrieve_options" tool using these parameters to get the values. key: discord_b... |
| `--nick NICK` | Value to set user's nickname to. |
| `--roles ROLES` | Please select the role you want to add to the user You can use the "retrieve_options" tool using these parameters to ... |
| `--mute` | Whether the user is muted in voice channels. Will throw a 400 error if the user is not in a voice channel |
| `--deaf` | Whether the user is deafened in voice channels. Will throw a 400 error if the user is not in a voice channel |
| `--comunication-disabled-until COMUNICATION_DISABLED_UNTIL` | When the user's [timeout](https://support.discord.com/hc/en- us/articles/4413305239191-Time-Out-FAQ) will expire and ... |

### `discord-bot-modify-channel`

Update a channel's settings. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select the channel you'd like to change its name You can use the "retrieve_options" tool using these parameter... |
| `--name NAME` | There is a 1-100 character channel name restriction |
| `--icon ICON` | base64 encoded icon. |
| `--type TYPE` | Only conversion between text and news is supported and only in guilds with the 'NEWS' feature. [See the channel types... |
| `--position POSITION` | The position of the channel in the left-hand listing |
| `--topic TOPIC` | 0-1024 character channel topic |
| `--nsfw` | [Not Safe For Wumpus](https://support.discord.com/hc/en- us/articles/115000084051-NSFW-Channels-and-Content) |
| `--bitrate BITRATE` | The bitrate (in bits) of the voice channel; 8000 to 96000 (128000 for VIP servers). |
| `--rate-limit-per-user RATE_LIMIT_PER_USER` | Amount of seconds a user has to wait before sending another message (0-21600); bots, as well as users with the permis... |
| `--user-limit USER_LIMIT` | The user limit of the voice channel; 0 refers to no limit, 1 to 99 refers to a user limit. |
| `--rtc-region RTC_REGION` | Channel [voice region](https://discord.com/developers/ docs/resources/voice#voice-region-object) id, automatic when s... |
| `--video-quality-mode VIDEO_QUALITY_MODE` | The camera [video quality mode](https://discord.com/de velopers/docs/resources/channel#channel-object-video- quality-... |
| `--default-auto-archive-duration DEFAULT_AUTO_ARCHIVE_DURATION` | The default duration for newly created threads in the channel, in minutes, to automatically archive the thread after ... |
| `--parent-id PARENT_ID` | Id of the new parent category for a channel You can use the "retrieve_options" tool using these parameters to get the... |
| `--role-permissions ROLE_PERMISSIONS` | Choose the roles you want to add to your channel You can use the "retrieve_options" tool using these parameters to ge... |
| `--member-permissions MEMBER_PERMISSIONS` | Choose the members you want to add to your channel You can use the "retrieve_options" tool using these parameters to ... |

### `discord-bot-list-users-with-emoji-reactions`

Return a list of users that reacted with a specified emoji

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |
| `--message-id MESSAGE_ID` | Copy the specific Message ID from your channel (eg. `907292892995932230`) |
| `--decoded-emoji DECODED_EMOJI` | Emoji (eg. 👍). To use custom emoji, you must encode it in the format `name:id` with the emoji name and emoji id. |
| `--max MAX` | Max number of records in the whole pagination (eg. `60`) |
| `--limit LIMIT` | Max number of members to return per page (1-1000) |
| `--after AFTER` | The highest user id in the previous page |

### `discord-bot-list-guild-members`

Return a list of guild members. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | In order to get members you might want to take a look at these [docs](https://support.discord.com/hc/en- us/articles/... |
| `--max MAX` | Max number of records in the whole pagination (eg. `60`) |
| `--limit LIMIT` | Max number of members to return per page (1-1000) |
| `--after AFTER` | The highest user id in the previous page |

### `discord-bot-list-channels`

Return a list of channels. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |

### `discord-bot-list-channel-messages`

Return the messages for a channel. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |
| `--max MAX` | Max number of records in the whole pagination (eg. `60`) |
| `--limit LIMIT` | Max number of messages to return per page (1-100) |
| `--after AFTER` | Get messages after this message ID |
| `--before BEFORE` | Get messages before this message ID |
| `--around AROUND` | Get messages around this message ID |

### `discord-bot-list-channel-invites`

Return a list of invitees for the channel. Only usable for guild

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |

### `discord-bot-get-message`

Return a specific message in a channel. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |
| `--message-id MESSAGE_ID` | Please select a message from the list You can use the "retrieve_options" tool using these parameters to get the value... |

### `discord-bot-find-user`

Find an existing user by name. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--query QUERY` | Query string to match username(s) and nickname(s) against. |

### `discord-bot-find-channel`

Find an existing channel by name. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-name CHANNEL_NAME` | Channel name to look for in the Guild |

### `discord-bot-delete-message`

Delete a message. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |
| `--message-id MESSAGE_ID` | Please select a message from the list You can use the "retrieve_options" tool using these parameters to get the value... |

### `discord-bot-delete-channel`

Delete a Channel

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |

### `discord-bot-create-guild-channel`

Create a new channel for the guild. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--name NAME` | There is a 1-100 character channel name restriction |
| `--type {0,2,4,6,13}` | Please select a channel type. In case you want to create a Store channel please read the docs [here](https://discord.... |
| `--position POSITION` | The position of the channel in the left-hand listing |
| `--topic TOPIC` | 0-1024 character channel topic |
| `--nsfw` | [Not Safe For Wumpus](https://support.discord.com/hc/en- us/articles/115000084051-NSFW-Channels-and-Content) |
| `--bitrate BITRATE` | The bitrate (in bits) of the voice channel; 8000 to 96000 (128000 for VIP servers). |
| `--rate-limit-per-user RATE_LIMIT_PER_USER` | Amount of seconds a user has to wait before sending another message (0-21600); bots, as well as users with the permis... |
| `--user-limit USER_LIMIT` | The user limit of the voice channel; 0 refers to no limit, 1 to 99 refers to a user limit. |
| `--parent-id PARENT_ID` | Id of the new parent category for a channel You can use the "retrieve_options" tool using these parameters to get the... |
| `--role-permissions ROLE_PERMISSIONS` | Choose the roles you want to add to your channel You can use the "retrieve_options" tool using these parameters to ge... |
| `--member-permissions MEMBER_PERMISSIONS` | Choose the members you want to add to your channel You can use the "retrieve_options" tool using these parameters to ... |

### `discord-bot-create-channel-invite`

Create a new invite for the channel. [See the docs

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--channel-id CHANNEL_ID` | Please select a channel You can use the "retrieve_options" tool using these parameters to get the values. key: discor... |
| `--max-age MAX_AGE` | Duration of invite in seconds before expiry 0 for never. between 0 and 604800 (7 days). |
| `--max-uses MAX_USES` | 0 for unlimited. between 0 and 100. |
| `--temporary` | Whether this invite only grants temporary membership |
| `--unique` | If true, don't try to reuse a similar invite (useful for creating many unique one time use invites) |
| `--target-type TARGET_TYPE` | The type of target for this voice channel invite. [See the docs here](https://discord.com/developers/docs/res ources/... |
| `--target-user-id TARGET_USER_ID` | The id of the user whose stream to display for this invite, required if Target type is Stream, the user must be strea... |
| `--target-application-id TARGET_APPLICATION_ID` | The id of the embedded application to open for this invite, required if Target type is Embedded Application, the appl... |

### `discord-bot-change-nickname`

Modifies the nickname of the current user in a guild

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--nick NICK` | Value to set user's nickname to. |

### `discord-bot-add-role`

Assign a role to a user. Remember that your bot requires the

| Flag | Description |
|---|---|
| `--guild-id GUILD_ID` | Discord Guild where your channel lives You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--user-id USER_ID` | Please select a user You can use the "retrieve_options" tool using these parameters to get the values. key: discord_b... |
| `--role-id ROLE_ID` | Please select the role you want to add to the user You can use the "retrieve_options" tool using these parameters to ... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'discord'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@discord` to bypass the 1h tool-list cache.
