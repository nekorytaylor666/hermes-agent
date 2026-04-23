
# Slack (via Higgsfield MCP proxy)

Send messages, reactions, files, users, channels. Exposes 36 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @slack <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @slack --list                    # all 36 tools
./bin/mcp2cli @slack slack-verify-slack-signature --help   # inspect one
./bin/mcp2cli @slack slack-verify-slack-signature --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @slack --pretty <cmd>` — `--pretty` goes AFTER `@slack`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @slack --head N <cmd>` — `--head N` goes AFTER `@slack`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 36 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `slack-verify-slack-signature`

Verifying requests from Slack, slack signs its requests using a

| Flag | Description |
|---|---|
| `--slack-signing-secret SLACK_SIGNING_SECRET` | Slack [Signing Secret](https://api.slack.com/authentic ation/verifying-requests-from-slack#:~:text=Slack%20Si gning%2... |
| `--slack-signature SLACK_SIGNATURE` | Slack signature (from X-Slack-Signature header). |
| `--slack-request-timestamp SLACK_REQUEST_TIMESTAMP` | Slack request timestamp (from X-Slack-Request- Timestamp header). |
| `--request-body REQUEST_BODY` | The body of the request to be verified. |

### `slack-upload-file`

Upload a file. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--content CONTENT` | The file to upload. Provide either a file URL or a path to a file in the `/tmp` directory (for example, `/tmp/myFile.... |
| `--initial-comment INITIAL_COMMENT` | Will be added as an initial comment before the image |

### `slack-update-profile`

Update basic profile field such as name or title. [See the

| Flag | Description |
|---|---|
| `--display-name DISPLAY_NAME` | The display name the user has chosen to identify themselves by in their workspace profile |
| `--first-name FIRST_NAME` | The user's first name |
| `--last-name LAST_NAME` | The user's last name |
| `--phone PHONE` | The user's phone number, in any format |
| `--pronouns PRONOUNS` | The user's pronouns |
| `--title TITLE` | The user's title |
| `--email EMAIL` | The user's email address. You cannot update your own email using this method. This field can only be changed by admin... |
| `--user USER` | ID of user to change. This argument may only be specified by admins on paid teams. You can use the "retrieve_options"... |

### `slack-update-message`

Update a message. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--timestamp TIMESTAMP` | Timestamp of a message. e.g. `1403051575.000407`. |
| `--text TEXT` | Text of the message to send (see Slack's [formatting d ocs](https://api.slack.com/reference/surfaces/formatti ng)). T... |
| `--as-user` | Pass true to update the message as the authed user. Bot users in this context are considered authed users. |
| `--attachments ATTACHMENTS` | A JSON-based array of structured attachments, presented as a URL-encoded string (e.g., `[{"pretext": "pre-hello", "te... |

### `slack-update-group-members`

Update the list of users for a User Group. [See the

| Flag | Description |
|---|---|
| `--user-group USER_GROUP` | The encoded ID of the User Group. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--users-to-add USERS_TO_ADD` | A list of encoded user IDs that represent the users to add to the group. You can use the "retrieve_options" tool usin... |
| `--users-to-remove USERS_TO_REMOVE` | A list of encoded user IDs that represent the users to remove from the group. You can use the "retrieve_options" tool... |
| `--team TEAM` | Encoded team id where the user group exists, required if org token is used. You can use the "retrieve_options" tool u... |

### `slack-set-status`

Set the current status for a user. [See the

| Flag | Description |
|---|---|
| `--status-text STATUS_TEXT` | The displayed text |
| `--status-emoji STATUS_EMOJI` | The emoji to display with the status You can use the "retrieve_options" tool using these parameters to get the values... |
| `--status-expiration STATUS_EXPIRATION` | The datetime of when the status will expire in ISO 8601 format. (Example: `2014-01-01T00:00:00Z`) |

### `slack-set-channel-topic`

Set the topic on a selected channel. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--topic TOPIC` | Text of the new channel topic. |

### `slack-set-channel-description`

Change the description or purpose of a channel. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--purpose PURPOSE` | Text of the new channel purpose. |

### `slack-send-message`

Send a message to a user, group, private channel or public channel

| Flag | Description |
|---|---|
| `--channel-type CHANNEL_TYPE` | The type of channel to send to. User/Direct Message (im), Group (mpim), Private Channel or Public Channel You can use... |
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--text TEXT` | Text of the message to send (see Slack's [formatting d ocs](https://api.slack.com/reference/surfaces/formatti ng)). T... |
| `--mrkdwn` | `true` by default. Pass `false` to disable Slack markup parsing. [See docs here](https://api.slack.com/ reference/sur... |
| `--as-user` | Optionally pass `true` to post the message as the authenticated user, instead of as a bot. Defaults to `false`. |
| `--post-at POST_AT` | Messages can only be scheduled up to 120 days in advance, and cannot be scheduled for the past. The datetime should b... |
| `--include-sent-via-pipedream-flag` | Defaults to `true`, includes a link to Pipedream at the end of your Slack message. |
| `--customize-bot-settings` | Customize the username and/or icon of the Bot |
| `--reply-to-thread` | Reply to an existing thread |
| `--add-message-metadata` | Set the metadata event type and payload |
| `--configure-unfurl-settings` | Configure settings for unfurling links and media |

### `slack-send-message-to-user-or-group`

Send a message to a user or group. [See the

| Flag | Description |
|---|---|
| `--users USERS` | Select the user(s) to message You can use the "retrieve_options" tool using these parameters to get the values. key: ... |
| `--conversation CONVERSATION` | Select the group to message You can use the "retrieve_options" tool using these parameters to get the values. key: sl... |
| `--text TEXT` | Text of the message to send (see Slack's [formatting d ocs](https://api.slack.com/reference/surfaces/formatti ng)). T... |
| `--mrkdwn` | `true` by default. Pass `false` to disable Slack markup parsing. [See docs here](https://api.slack.com/ reference/sur... |
| `--as-user` | Optionally pass `true` to post the message as the authenticated user, instead of as a bot. Defaults to `false`. |
| `--post-at POST_AT` | Messages can only be scheduled up to 120 days in advance, and cannot be scheduled for the past. The datetime should b... |
| `--include-sent-via-pipedream-flag` | Defaults to `true`, includes a link to Pipedream at the end of your Slack message. |
| `--customize-bot-settings` | Customize the username and/or icon of the Bot |
| `--reply-to-thread` | Reply to an existing thread |
| `--add-message-metadata` | Set the metadata event type and payload |
| `--configure-unfurl-settings` | Configure settings for unfurling links and media |

### `slack-send-message-to-channel`

Send a message to a public or private channel. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--text TEXT` | Text of the message to send (see Slack's [formatting d ocs](https://api.slack.com/reference/surfaces/formatti ng)). T... |
| `--mrkdwn` | `true` by default. Pass `false` to disable Slack markup parsing. [See docs here](https://api.slack.com/ reference/sur... |
| `--as-user` | Optionally pass `true` to post the message as the authenticated user, instead of as a bot. Defaults to `false`. |
| `--post-at POST_AT` | Messages can only be scheduled up to 120 days in advance, and cannot be scheduled for the past. The datetime should b... |
| `--include-sent-via-pipedream-flag` | Defaults to `true`, includes a link to Pipedream at the end of your Slack message. |
| `--customize-bot-settings` | Customize the username and/or icon of the Bot |
| `--reply-to-thread` | Reply to an existing thread |
| `--add-message-metadata` | Set the metadata event type and payload |
| `--configure-unfurl-settings` | Configure settings for unfurling links and media |

### `slack-send-message-advanced`

Customize advanced setttings and send a message to a channel, group

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--text TEXT` | If you're using `blocks`, this is used as a fallback string to display in notifications. If you aren't, this is the m... |
| `--mrkdwn` | `true` by default. Pass `false` to disable Slack markup parsing. [See docs here](https://api.slack.com/ reference/sur... |
| `--attachments ATTACHMENTS` | A JSON-based array of structured attachments, presented as a URL-encoded string (e.g., `[{"pretext": "pre-hello", "te... |
| `--parse PARSE` | Change how messages are treated. Defaults to none. By default, URLs will be hyperlinked. Set `parse` to `none` to rem... |
| `--link-names` | Find and link channel names and usernames. |
| `--as-user` | Optionally pass `true` to post the message as the authenticated user, instead of as a bot. Defaults to `false`. |
| `--post-at POST_AT` | Messages can only be scheduled up to 120 days in advance, and cannot be scheduled for the past. The datetime should b... |
| `--include-sent-via-pipedream-flag` | Defaults to `true`, includes a link to Pipedream at the end of your Slack message. |
| `--customize-bot-settings` | Customize the username and/or icon of the Bot |
| `--reply-to-thread` | Reply to an existing thread |
| `--add-message-metadata` | Set the metadata event type and payload |
| `--configure-unfurl-settings` | Configure settings for unfurling links and media |
| `--pass-array-or-configure {array,configure}` | Would you like to reference an array of blocks from a previous step (for example, `{{steps.blocks.$return_value}}`), ... |

### `slack-send-large-message`

Send a large message (more than 3000 characters) to a channel, group

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--text TEXT` | Text of the message to send (see Slack's [formatting d ocs](https://api.slack.com/reference/surfaces/formatti ng)). T... |
| `--mrkdwn` | `true` by default. Pass `false` to disable Slack markup parsing. [See docs here](https://api.slack.com/ reference/sur... |
| `--as-user` | Optionally pass `true` to post the message as the authenticated user, instead of as a bot. Defaults to `false`. |
| `--post-at POST_AT` | Messages can only be scheduled up to 120 days in advance, and cannot be scheduled for the past. The datetime should b... |
| `--include-sent-via-pipedream-flag` | Defaults to `true`, includes a link to Pipedream at the end of your Slack message. |
| `--customize-bot-settings` | Customize the username and/or icon of the Bot |
| `--reply-to-thread` | Reply to an existing thread |
| `--add-message-metadata` | Set the metadata event type and payload |
| `--configure-unfurl-settings` | Configure settings for unfurling links and media |

### `slack-send-block-kit-message`

Configure custom blocks and send to a channel, group, or user. [See

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--text TEXT` | Optionally provide a string for Slack to display as the new message notification (if you do not provide this, notific... |
| `--as-user` | Optionally pass `true` to post the message as the authenticated user, instead of as a bot. Defaults to `false`. |
| `--post-at POST_AT` | Messages can only be scheduled up to 120 days in advance, and cannot be scheduled for the past. The datetime should b... |
| `--include-sent-via-pipedream-flag` | Defaults to `true`, includes a link to Pipedream at the end of your Slack message. |
| `--customize-bot-settings` | Customize the username and/or icon of the Bot |
| `--reply-to-thread` | Reply to an existing thread |
| `--add-message-metadata` | Set the metadata event type and payload |
| `--configure-unfurl-settings` | Configure settings for unfurling links and media |
| `--pass-array-or-configure {array,configure}` | Would you like to reference an array of blocks from a previous step (for example, `{{steps.blocks.$return_value}}`), ... |

### `slack-reply-to-a-message`

Send a message as a threaded reply. See

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--text TEXT` | Text of the message to send (see Slack's [formatting d ocs](https://api.slack.com/reference/surfaces/formatti ng)). T... |
| `--mrkdwn` | `true` by default. Pass `false` to disable Slack markup parsing. [See docs here](https://api.slack.com/ reference/sur... |
| `--as-user` | Optionally pass `true` to post the message as the authenticated user, instead of as a bot. Defaults to `false`. |
| `--post-at POST_AT` | Messages can only be scheduled up to 120 days in advance, and cannot be scheduled for the past. The datetime should b... |
| `--include-sent-via-pipedream-flag` | Defaults to `true`, includes a link to Pipedream at the end of your Slack message. |
| `--customize-bot-settings` | Customize the username and/or icon of the Bot |
| `--thread-ts THREAD_TS` | Timestamp of a message. e.g. `1403051575.000407`. |
| `--thread-broadcast` | If `true`, posts in the thread and channel. Used in conjunction with `Message Timestamp` and indicates whether reply ... |
| `--add-message-metadata` | Set the metadata event type and payload |
| `--configure-unfurl-settings` | Configure settings for unfurling links and media |

### `slack-list-users`

Return a list of all users in a workspace. [See the

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | Select a team. You can use the "retrieve_options" tool using these parameters to get the values. key: slack- list-use... |
| `--page-size PAGE_SIZE` | The number of results to include in a page. Default: 250 |
| `--num-pages NUM_PAGES` | The number of pages to retrieve. Default: 1 |

### `slack-list-replies`

Retrieve a thread of messages posted to a conversation. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--timestamp TIMESTAMP` | Timestamp of a message. e.g. `1403051575.000407`. |
| `--page-size PAGE_SIZE` | The number of results to include in a page. Default: 250 |
| `--num-pages NUM_PAGES` | The number of pages to retrieve. Default: 1 |

### `slack-list-messages`

Retrieve messages from a Slack conversation, including reactions

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--page-size PAGE_SIZE` | The number of results to include in a page. Default: 250 |
| `--num-pages NUM_PAGES` | The number of pages to retrieve. Default: 1 |

### `slack-list-members-in-channel`

Retrieve members of a channel. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--return-usernames` | Optionally, return usernames in addition to IDs |
| `--page-size PAGE_SIZE` | The number of results to include in a page. Default: 250 |
| `--num-pages NUM_PAGES` | The number of pages to retrieve. Default: 1 |

### `slack-list-group-members`

List all users in a User Group. [See the

| Flag | Description |
|---|---|
| `--user-group USER_GROUP` | The encoded ID of the User Group. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--team TEAM` | Encoded team id where the user group exists, required if org token is used. You can use the "retrieve_options" tool u... |
| `--page-size PAGE_SIZE` | The number of results to include in a page. Default: 250 |
| `--num-pages NUM_PAGES` | The number of pages to retrieve. Default: 1 |

### `slack-list-files`

Return a list of files within a team. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--team-id TEAM_ID` | Select a team. You can use the "retrieve_options" tool using these parameters to get the values. key: slack- list-fil... |
| `--user USER` | Select a user You can use the "retrieve_options" tool using these parameters to get the values. key: slack- list-file... |
| `--page-size PAGE_SIZE` | The number of results to include in a page. Default: 250 |
| `--num-pages NUM_PAGES` | The number of pages to retrieve. Default: 1 |

### `slack-list-emojis`

List all available emojis in the Slack workspace. Optionally include

| Flag | Description |
|---|---|
| `--include-emoji-image` | If true, returns emoji name and its value (image URL or alias reference). If false, returns only emoji names. |
| `--include-categories` | If true, includes Unicode emoji categories provided by Slack. |

### `slack-list-channels`

Return a list of all channels in a workspace. [See the

| Flag | Description |
|---|---|
| `--page-size PAGE_SIZE` | The number of results to include in a page. Default: 250 |
| `--num-pages NUM_PAGES` | The number of pages to retrieve. Default: 1 |

### `slack-kick-user`

Remove a user from a conversation. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--user USER` | Select a user You can use the "retrieve_options" tool using these parameters to get the values. key: slack- kick-user... |

### `slack-invite-user-to-channel`

Invite a user to an existing channel. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--user USER` | Select a user You can use the "retrieve_options" tool using these parameters to get the values. key: slack- invite-us... |

### `slack-get-file`

Return information about a file. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--file FILE` | Specify a file by providing its ID. You can use the "retrieve_options" tool using these parameters to get the values.... |

### `slack-get-current-user`

Retrieve comprehensive context about the authenticated Slack member,

_No flags._

### `slack-find-user-by-email`

Find a user by matching against their email. [See the

| Flag | Description |
|---|---|
| `--email EMAIL` | An email address belonging to a user in the workspace |

### `slack-find-message`

Find a Slack message. [See the

| Flag | Description |
|---|---|
| `--query QUERY` | Search query. |
| `--team-id TEAM_ID` | Select a team. You can use the "retrieve_options" tool using these parameters to get the values. key: slack- find-mes... |
| `--max-results MAX_RESULTS` | The maximum number of messages to return |
| `--sort {score,timestamp}` | Return matches sorted by either `score` or `timestamp` |
| `--sort-direction {desc,asc}` | Sort ascending (asc) or descending (desc)` |

### `slack-delete-message`

Delete a message. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--timestamp TIMESTAMP` | Timestamp of a message. e.g. `1403051575.000407`. |
| `--as-user` | Pass true to update the message as the authed user. Bot users in this context are considered authed users. |

### `slack-delete-file`

Delete a file. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--file FILE` | Specify a file by providing its ID. You can use the "retrieve_options" tool using these parameters to get the values.... |

### `slack-create-reminder`

Create a reminder. [See the

| Flag | Description |
|---|---|
| `--text TEXT` | Text of the message to send (see Slack's [formatting d ocs](https://api.slack.com/reference/surfaces/formatti ng)). T... |
| `--timestamp TIMESTAMP` | When this reminder should happen: the Unix timestamp (up to five years from now), the number of seconds until the rem... |
| `--team-id TEAM_ID` | Select a team. You can use the "retrieve_options" tool using these parameters to get the values. key: slack- create-r... |
| `--user USER` | Select a user You can use the "retrieve_options" tool using these parameters to get the values. key: slack- create-re... |

### `slack-create-channel`

Create a new channel. [See the

| Flag | Description |
|---|---|
| `--channel-name CHANNEL_NAME` | Name of the public or private channel to create |
| `--is-private` | `false` by default. Pass `true` to create a private channel instead of a public one. |

### `slack-archive-channel`

Archive a channel. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |

### `slack-approve-workflow`

Suspend the workflow until approved by a Slack message. [See the

| Flag | Description |
|---|---|
| `--channel-type CHANNEL_TYPE` | The type of channel to send to. User/Direct Message (im), Group (mpim), Private Channel or Public Channel You can use... |
| `--conversation CONVERSATION` | Select a public or private channel, or a user or group You can use the "retrieve_options" tool using these parameters... |
| `--message MESSAGE` | Text to include with the Approve and Cancel Buttons |

### `slack-add-emoji-reaction`

Add an emoji reaction to a message. [See the

| Flag | Description |
|---|---|
| `--conversation CONVERSATION` | Channel where the message to add reaction to was posted. You can use the "retrieve_options" tool using these paramete... |
| `--timestamp TIMESTAMP` | Timestamp of the message to add reaction to. e.g. `1403051575.000407`. |
| `--icon-emoji ICON_EMOJI` | Provide an emoji to use as the icon for this reaction. E.g. `fire` You can use the "retrieve_options" tool using thes... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'slack'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@slack` to bypass the 1h tool-list cache.
