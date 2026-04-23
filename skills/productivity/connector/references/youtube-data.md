
# YouTube Data API (via Higgsfield MCP proxy)

Manage YouTube videos, playlists, comments, channels. Exposes 18 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @youtube-data <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @youtube-data --list                    # all 18 tools
./bin/mcp2cli @youtube-data youtube-data-api-upload-video --help   # inspect one
./bin/mcp2cli @youtube-data youtube-data-api-upload-video --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @youtube-data --pretty <cmd>` — `--pretty` goes AFTER `@youtube-data`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @youtube-data --head N <cmd>` — `--head N` goes AFTER `@youtube-data`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 18 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `youtube-data-api-upload-video`

Post a video to your channel. [See the

| Flag | Description |
|---|---|
| `--title TITLE` | The video's title |
| `--description DESCRIPTION` | The video's description |
| `--file-path FILE_PATH` | Provide either a file URL or a path to a file in the /tmp directory (for example, /tmp/myFile.pdf). |
| `--privacy-status {private,public,unlisted}` | The video's privacy status |
| `--publish-at PUBLISH_AT` | The date and time when the video is scheduled to publish. If you set this, the **Privacy Status** must be set to `pri... |
| `--tags TAGS` | A list of keyword tags associated with the video. Tags may contain spaces. (JSON array) |
| `--notify-subscribers` | Set to `true` if YouTube should send a notification about the new video to users who subscribe to the video's channel. |

### `youtube-data-api-upload-thumbnail`

Uploads a custom video thumbnail to YouTube and sets it for a video

| Flag | Description |
|---|---|
| `--video-id VIDEO_ID` | Select the video to update. E.g. `wslno0wDSFQ` You can use the "retrieve_options" tool using these parameters to get ... |
| `--file-path FILE_PATH` | Provide either a file URL or a path to a file in the /tmp directory (for example, /tmp/myFile.pdf). |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-upload-channel-banner`

Uploads a channel banner image to YouTube. [See the

| Flag | Description |
|---|---|
| `--file-path FILE_PATH` | Provide either a file URL or a path to a file in the /tmp directory (for example, /tmp/myFile.pdf). |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-update-video-details`

Updates a video's metadata. [See the

| Flag | Description |
|---|---|
| `--video-id VIDEO_ID` | Select the video to update. E.g. `wslno0wDSFQ` You can use the "retrieve_options" tool using these parameters to get ... |
| `--title TITLE` | The video's title |
| `--description DESCRIPTION` | The video's description |
| `--tags TAGS` | A list of keyword tags associated with the video. Tags may contain spaces. (JSON array) |
| `--region-code REGION_CODE` | The regionCode parameter instructs the API to return results for the specified country. The parameter value is an ISO... |
| `--category-id CATEGORY_ID` | Select the video's category You can use the "retrieve_options" tool using these parameters to get the values. key: yo... |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-update-playlist`

Modifies a playlist. For example, you could change a playlist's

| Flag | Description |
|---|---|
| `--id ID` | The identifier of the playlist to update. E.g. `PLJswo-CV0rmlwxKysf33cUnyBp8JztH0k` You can use the "retrieve_options... |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-update-channel`

Updates a channel's metadata. [See the

| Flag | Description |
|---|---|
| `--channel-id CHANNEL_ID` | Select the channel to update. E.g. `UChkRx83xLq2nk55D8CRODVz` You can use the "retrieve_options" tool using these par... |
| `--description DESCRIPTION` | The channel's description |
| `--default-language DEFAULT_LANGUAGE` | The language of the text in the channel resource You can use the "retrieve_options" tool using these parameters to ge... |
| `--keywords KEYWORDS` | Keywords associated with your channel (JSON array) |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-search-videos`

Returns a list of videos that match the search parameters. [See the

| Flag | Description |
|---|---|
| `--q Q` | Search for new videos that match these keywords. |
| `--channel-id CHANNEL_ID` | The channelId parameter specifies a unique YouTube channel ID. E.g. `UChkRx83xLq2nk55D8CRODVz` |
| `--video-duration {any,long,medium,short}` | Filter the results based on video duration |
| `--video-definition {any,high,standard}` | Filter the results to only include either high definition (HD) or standard definition (SD) videos |
| `--video-caption {any,closedCaption,none}` | Indicates whether the API should filter video search results based on whether they have captions |
| `--video-license {any,creativeCommon,youtube}` | Filter the results to only include videos with a particular license |
| `--region-code REGION_CODE` | The regionCode parameter instructs the API to return results for the specified country. The parameter value is an ISO... |
| `--video-category-id VIDEO_CATEGORY_ID` | Select the video's category You can use the "retrieve_options" tool using these parameters to get the values. key: yo... |
| `--location LOCATION` | The location parameter, in conjunction with the locationRadius parameter, defines a circular geographic area and also... |
| `--location-radius LOCATION_RADIUS` | The parameter value must be a floating point number followed by a measurement unit. Valid measurement units are m, km... |
| `--sort-order {date,rating,relevance,title,viewCount}` | The method that will be used to order resources in the API response. The default value is `relevance` |
| `--max-results MAX_RESULTS` | The maximum number of items that should be returned in the result set. Acceptable values are 0 to 50, inclusive. Defa... |

### `youtube-data-api-reply-to-comment`

Creates a reply to an existing comment. [See the

| Flag | Description |
|---|---|
| `--channel-id CHANNEL_ID` | Select the channel to update. E.g. `UChkRx83xLq2nk55D8CRODVz` You can use the "retrieve_options" tool using these par... |
| `--comment-thread COMMENT_THREAD` | The top-level comment that you are replying to You can use the "retrieve_options" tool using these parameters to get ... |
| `--text TEXT` | The text of the comment |

### `youtube-data-api-list-videos`

Returns a list of videos that match the API request parameters. [See

| Flag | Description |
|---|---|
| `--use-case {id,chart,myRating}` | Select your use case to render the next properties. |

### `youtube-data-api-list-playlists`

Returns a collection of playlists that match the API request

| Flag | Description |
|---|---|
| `--use-case {id,channelId,mine}` | Select your use case to render the next properties. |

### `youtube-data-api-list-playlist-videos`

List videos in a playlist. [See the

| Flag | Description |
|---|---|
| `--playlist-id PLAYLIST_ID` | Select a **Playlist** or provide a custom *Playlist ID*. E.g. `PLJswo-CV0rmlwxKysf33cUnyBp8JztH0k` You can use the "r... |
| `--max-results MAX_RESULTS` | The maximum number of items that should be returned in the result set. Acceptable values are 0 to 50, inclusive. Defa... |

### `youtube-data-api-list-activities`

Returns a list of channel activity events that match the request

| Flag | Description |
|---|---|
| `--use-case {channelId,mine}` | Select your use case to render the next properties. |

### `youtube-data-api-delete-playlist`

Deletes a playlist. [See the

| Flag | Description |
|---|---|
| `--playlist-id PLAYLIST_ID` | Add items to the selected playlist. E.g. `PLJswo- CV0rmlwxKysf33cUnyBp8JztH0k` You can use the "retrieve_options" too... |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-delete-playlist-items`

Deletes a playlist item. [See the

| Flag | Description |
|---|---|
| `--playlist-id PLAYLIST_ID` | Add items to the selected playlist. E.g. `PLJswo- CV0rmlwxKysf33cUnyBp8JztH0k` You can use the "retrieve_options" too... |
| `--video-ids VIDEO_IDS` | Array of identifiers of the videos to be removed from the playlist. E.g. `o_U1CQn68VM` You can use the "retrieve_opti... |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-create-playlist`

Creates a playlist. [See the

| Flag | Description |
|---|---|
| `--title TITLE` | The playlist's title |
| `--description DESCRIPTION` | The playlist's description |
| `--privacy-status {private,public,unlisted}` | The playlist's privacy status |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |
| `--on-behalf-of-content-owner-channel ON_BEHALF_OF_CONTENT_OWNER_CHANNEL` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

### `youtube-data-api-create-comment-thread`

Creates a new top-level comment in a video. [See the

| Flag | Description |
|---|---|
| `--channel-id CHANNEL_ID` | Select the channel to update. E.g. `UChkRx83xLq2nk55D8CRODVz` You can use the "retrieve_options" tool using these par... |
| `--video-id VIDEO_ID` | Select the video to add comment to. E.g. `wslno0wDSFQ`. Leave blank to post comment to channel. You can use the "retr... |
| `--text TEXT` | The text of the comment |

### `youtube-data-api-channel-statistics`

Returns statistics from my YouTube Channel or by id. [See the

| Flag | Description |
|---|---|
| `--use-case {id,mine,managedByMe}` | Select your use case to render the next properties. |

### `youtube-data-api-add-playlist-items`

Adds resources to a playlist. [See the

| Flag | Description |
|---|---|
| `--playlist-id PLAYLIST_ID` | Add items to the selected playlist. E.g. `PLJswo- CV0rmlwxKysf33cUnyBp8JztH0k` You can use the "retrieve_options" too... |
| `--video-ids VIDEO_IDS` | Array of identifiers of the videos to be added to the playlist. E.g. `o_U1CQn68VM` The video ID will be located in th... |
| `--on-behalf-of-content-owner ON_BEHALF_OF_CONTENT_OWNER` | This parameter can only be used in a properly authorized request. Note: This parameter is intended exclusively for Yo... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'youtube-data'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@youtube-data` to bypass the 1h tool-list cache.
