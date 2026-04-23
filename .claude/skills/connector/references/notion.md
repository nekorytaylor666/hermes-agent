
# Notion (via Higgsfield MCP proxy)

Notion pages, databases, blocks, queries. Exposes 25 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @notion <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @notion --list                    # all 25 tools
./bin/mcp2cli @notion notion-send-file-upload --help   # inspect one
./bin/mcp2cli @notion notion-send-file-upload --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @notion --pretty <cmd>` — `--pretty` goes AFTER `@notion`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @notion --head N <cmd>` — `--head N` goes AFTER `@notion`
- **JSON input via stdin**: pipe a JSON object whose keys match CLI flag names (e.g. `{"title": "...", "parent": "..."}`). Stdin maps **keys → CLI flags**; it does **not** accept a raw Notion API payload. Use to avoid typing many flags — not to pass through Notion REST bodies.
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Gotchas

Traps that bite on first use — skim before you type a command:

- **`notion-search` needs `--title ""`** even for broad searches. `--filter page` alone returns a validation error. For "list all pages," use `--title "" --filter page`.
- **`notion-append-block --block-types` takes selector strings** (`blockIds`, `markdownContents`, `imageUrls`) — NOT raw Notion block JSON. For writing page content, prefer `notion-create-page --page-content`.
- **`--stdin` maps JSON keys → CLI flags.** It does NOT pass a raw Notion API payload through. See the `--stdin` bullet under Common patterns above.
- **Markdown content goes through `notion-create-page --page-content`.** See "Writing page content" recipe below.

## Writing page content

The cleanest path for putting Markdown into a new Notion page. `--page-content` accepts full Markdown: headings, lists, bold/italic, links, code blocks.

```bash
./bin/mcp2cli @notion notion-create-page \
  --parent "<parent-page-id-or-url>" \
  --title "Release notes — 2026-04-20" \
  --page-content "# Highlights

- Fixed auth bug
- Added **markdown** rendering
- See [docs](https://example.com)"
```

Prefer this over `notion-append-block` for content writing. Use `notion-append-block` only when you need to append blocks to an existing page by block/media reference.

## Command reference

All 25 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `notion-send-file-upload`

Send a file upload. [See the

| Flag | Description |
|---|---|
| `--file-upload-id FILE_UPLOAD_ID` | The ID of the file upload to send. You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--file FILE` | The image to process. Provide either a file URL or a path to a file in the `/tmp` directory (for example, `/tmp/myIma... |

### `notion-update-page`

Update a page's property values. To append page content, use the

| Flag | Description |
|---|---|
| `--parent-data-source PARENT_DATA_SOURCE` | Select the data source that contains the page to update. If you instead provide a data source ID in a custom expressi... |
| `--page-id PAGE_ID` | Search for a page from the data source or provide a page ID You can use the "retrieve_options" tool using these param... |
| `--archived` | Set to `true` to archive (delete) a page. Set to `false` to un-archive (restore) a page |
| `--meta-types META_TYPES` | Select one or more page attributes (such as icon and cover) (JSON array) |
| `--property-types PROPERTY_TYPES` | Select one or more page properties You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `notion-update-database`

Update a data source. [See the

| Flag | Description |
|---|---|
| `--data-source-id DATA_SOURCE_ID` | Select a data source or provide a data source ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--title TITLE` | Title of the data source as it appears in Notion. An array of [rich text objects](https://developers.notion.com/refer... |
| `--description DESCRIPTION` | An array of [rich text objects](https://developers.notion.com/reference/rich- text) that represents the description o... |
| `--properties PROPERTIES` | The properties of a data source to be changed in the request, in the form of a JSON object. If updating an existing p... |

### `notion-update-block`

Updates a child block object. [See the

| Flag | Description |
|---|---|
| `--block-id BLOCK_ID` | Block ID retrieved from the **Retrieve Page Content** action |
| `--content CONTENT` | The content of the block. **E.g. {"code": {"rich_text":[{"type":"text","text":{"content":"Updated content"}}]}}** [Se... |

### `notion-search`

Searches for a page or data source. [See the

| Flag | Description |
|---|---|
| `--title TITLE` | The object title to search for. **Required — pass `--title ""` (empty string) for broad searches.** |
| `--sort-direction {ascending,descending}` | The direction to sort by |
| `--page-size PAGE_SIZE` | The number of items from the full list desired in the response (max 100) |
| `--start-cursor START_CURSOR` | Leave blank to retrieve the first page of results. Otherwise, the response will be the page of results starting after... |
| `--filter {page,data_source}` | Whether to search for pages or data sources. |

**Gotcha:** `--title ""` is required even when you want to list everything. Passing `--filter page` alone returns a validation error. To list all pages: `notion-search --title "" --filter page`.

### `notion-retrieve-user`

Returns a user using the ID specified. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | Select a user, or provide a user ID You can use the "retrieve_options" tool using these parameters to get the values.... |

### `notion-retrieve-page`

Get details of a page. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | Search for a page or provide a page ID You can use the "retrieve_options" tool using these parameters to get the valu... |

### `notion-retrieve-page-property-item`

Get a Property Item object for a selected page and property. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | Search for a page or provide a page ID You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--property-id PROPERTY_ID` | Select a page property or provide a property ID You can use the "retrieve_options" tool using these parameters to get... |

### `notion-retrieve-file-upload`

Use this action to retrieve a file upload. [See the

| Flag | Description |
|---|---|
| `--file-upload-id FILE_UPLOAD_ID` | The ID of the file upload to send. You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `notion-retrieve-database-schema`

Get the property schema of a data source in Notion. [See the

| Flag | Description |
|---|---|
| `--data-source-id DATA_SOURCE_ID` | Select a data source or provide a data source ID You can use the "retrieve_options" tool using these parameters to ge... |

### `notion-retrieve-database-content`

Get all content of a data source. [See the

| Flag | Description |
|---|---|
| `--data-source-id DATA_SOURCE_ID` | Select a data source or provide a data source ID You can use the "retrieve_options" tool using these parameters to ge... |

### `notion-retrieve-block`

Get page content as block objects or markdown. Blocks can be text,

| Flag | Description |
|---|---|
| `--block-id BLOCK_ID` | Search for a page or provide a page ID You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--retrieve-children {All Children,Sub-Pages Only,None}` | Retrieve all the children (recursively) for the specified page, or optionally filter to include only sub-pages in the... |
| `--retrieve-markdown` | Additionally return the page content as markdown |

### `notion-query-database`

Query a data source with a specified filter. [See the

| Flag | Description |
|---|---|
| `--data-source-id DATA_SOURCE_ID` | Select a data source or provide a data source ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--filter FILTER` | The filter to apply, as a JSON-stringified object. [See the documentation for available filters](https:// developers.... |
| `--sorts SORTS` | The sort order for the query. [See the documentation for available sorts](https://developers.notion.com/reference/sor... |

### `notion-list-file-uploads`

Use this action to list file uploads. [See the

_No flags._

### `notion-list-all-users`

Returns all users in the workspace. [See the

_No flags._

### `notion-get-current-user`

Retrieve the Notion identity tied to the current OAuth token,

_No flags._

### `notion-duplicate-page`

Create a new page copied from an existing page block. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | Select a page to copy or provide a page ID You can use the "retrieve_options" tool using these parameters to get the ... |
| `--title TITLE` | The new page title |
| `--parent-id PARENT_ID` | Select a parent page for the new page being created, or provide the ID of a parent page You can use the "retrieve_opt... |

### `notion-delete-block`

Sets a Block object, including page blocks, to archived: true using

| Flag | Description |
|---|---|
| `--block-id BLOCK_ID` | Block ID retrieved from the **Retrieve Page Content** action |

### `notion-create-page`

Create a page from a parent page. [See the

| Flag | Description |
|---|---|
| `--parent PARENT` | Select a parent page or provide a page ID You can use the "retrieve_options" tool using these parameters to get the v... |
| `--title TITLE` | The page title (defaults to `Untitled`) |
| `--meta-types META_TYPES` | Select one or more page attributes (such as icon and cover) (JSON array) |
| `--page-content PAGE_CONTENT` | The content of the page, using Markdown syntax. [See the documentation](https://www.notion.com/help/writing- and-edit... |

### `notion-create-page-from-database`

Create a page from a data source. [See the

| Flag | Description |
|---|---|
| `--parent-data-source PARENT_DATA_SOURCE` | Select a parent data source or provide a data source ID You can use the "retrieve_options" tool using these parameter... |
| `--template-type {none,default,template_id}` | The type of template to use for the page. [See the doc umentation](https://developers.notion.com/docs/creatin g-pages... |
| `--property-types PROPERTY_TYPES` | Select one or more page properties. Willl override properties set in the `Properties` prop below. You can use the "re... |
| `--properties PROPERTIES` | The values of the page's properties. The schema must match the parent data source's properties. [See the do cumentati... |
| `--icon {😀,😃,😄,😁,😆,😅,🤣,😂,🙂,🙃,😉,😊,😇,🥰,😍,🤩,😘,😗,☺️,☺,😚,😙,🥲,😋,😛,😜,🤪,😝,🤑,🤗,🤭,🤫,🤔,🤐,🤨,😐,😑,😶,😶‍🌫️,😶‍🌫,😏,😒,🙄,😬,😮‍💨,🤥,😌,😔,😪,🤤,😴,😷,🤒,🤕,🤢,🤮,🤧,🥵,🥶,🥴,😵,😵‍💫,🤯,🤠,🥳,🥸,😎,🤓,🧐,😕,😟,🙁,☹️,☹,😮,😯,😲,😳,🥺,😦,😧,😨,😰,😥,😢,😭,😱,😖,😣,😞,😓,😩,😫,🥱,😤,😡,😠,🤬,😈,👿,💀,☠️,☠,💩,🤡,👹,👺,👻,👽,👾,🤖,😺,😸,😹,😻,😼,😽,🙀,😿,😾,🙈,🙉,🙊,💋,💌,💘,💝,💖,💗,💓,💞,💕,💟,❣️,❣,💔,❤️‍🔥,❤‍🔥,❤️‍🩹,❤‍🩹,❤️,❤,🧡,💛,💚,💙,💜,🤎,🖤,🤍,💯,💢,💥,💫,💦,💨,🕳️,🕳,💣,💬,👁️‍🗨️,🗨️,🗨,🗯️,🗯,💭,💤,👋🏻,👋🏼,👋🏽,👋🏾,👋🏿,👋,🤚🏻,🤚🏼,🤚🏽,🤚🏾,🤚🏿,🤚,🖐🏻,🖐🏼,🖐🏽,🖐🏾,🖐🏿,🖐️,🖐,✋🏻,✋🏼,✋🏽,✋🏾,✋🏿,✋,🖖🏻,🖖🏼,🖖🏽,🖖🏾,🖖🏿,🖖,👌🏻,👌🏼,👌🏽,👌🏾,👌🏿,👌,🤌🏻,🤌🏼,🤌🏽,🤌🏾,🤌🏿,🤌,🤏🏻,🤏🏼,🤏🏽,🤏🏾,🤏🏿,🤏,✌🏻,✌🏼,✌🏽,✌🏾,✌🏿,✌️,✌,🤞🏻,🤞🏼,🤞🏽,🤞🏾,🤞🏿,🤞,🤟🏻,🤟🏼,🤟🏽,🤟🏾,🤟🏿,🤟,🤘🏻,🤘🏼,🤘🏽,🤘🏾,🤘🏿,🤘,🤙🏻,🤙🏼,🤙🏽,🤙🏾,🤙🏿,🤙,👈🏻,👈🏼,👈🏽,👈🏾,👈🏿,👈,👉🏻,👉🏼,👉🏽,👉🏾,👉🏿,👉,👆🏻,👆🏼,👆🏽,👆🏾,👆🏿,👆,🖕🏻,🖕🏼,🖕🏽,🖕🏾,🖕🏿,🖕,👇🏻,👇🏼,👇🏽,👇🏾,👇🏿,👇,☝🏻,☝🏼,☝🏽,☝🏾,☝🏿,☝️,☝,👍🏻,👍🏼,👍🏽,👍🏾,👍🏿,👍,👎🏻,👎🏼,👎🏽,👎🏾,👎🏿,👎,✊🏻,✊🏼,✊🏽,✊🏾,✊🏿,✊,👊🏻,👊🏼,👊🏽,👊🏾,👊🏿,👊,🤛🏻,🤛🏼,🤛🏽,🤛🏾,🤛🏿,🤛,🤜🏻,🤜🏼,🤜🏽,🤜🏾,🤜🏿,🤜,👏🏻,👏🏼,👏🏽,👏🏾,👏🏿,👏,🙌🏻,🙌🏼,🙌🏽,🙌🏾,🙌🏿,🙌,👐🏻,👐🏼,👐🏽,👐🏾,👐🏿,👐,🤲🏻,🤲🏼,🤲🏽,🤲🏾,🤲🏿,🤲,🤝,🙏🏻,🙏🏼,🙏🏽,🙏🏾,🙏🏿,🙏,✍🏻,✍🏼,✍🏽,✍🏾,✍🏿,✍️,✍,💅🏻,💅🏼,💅🏽,💅🏾,💅🏿,💅,🤳🏻,🤳🏼,🤳🏽,🤳🏾,🤳🏿,🤳,💪🏻,💪🏼,💪🏽,💪🏾,💪🏿,💪,🦾,🦿,🦵🏻,🦵🏼,🦵🏽,🦵🏾,🦵🏿,🦵,🦶🏻,🦶🏼,🦶🏽,🦶🏾,🦶🏿,🦶,👂🏻,👂🏼,👂🏽,👂🏾,👂🏿,👂,🦻🏻,🦻🏼,🦻🏽,🦻🏾,🦻🏿,🦻,👃🏻,👃🏼,👃🏽,👃🏾,👃🏿,👃,🧠,🫀,🫁,🦷,🦴,👀,👁️,👁,👅,👄,👶🏻,👶🏼,👶🏽,👶🏾,👶🏿,👶,🧒🏻,🧒🏼,🧒🏽,🧒🏾,🧒🏿,🧒,👦🏻,👦🏼,👦🏽,👦🏾,👦🏿,👦,👧🏻,👧🏼,👧🏽,👧🏾,👧🏿,👧,🧑🏻,🧑🏼,🧑🏽,🧑🏾,🧑🏿,🧑,👱🏻,👱🏼,👱🏽,👱🏾,👱🏿,👱,👨🏻,👨🏼,👨🏽,👨🏾,👨🏿,👨,🧔🏻,🧔🏼,🧔🏽,🧔🏾,🧔🏿,🧔,🧔🏻‍♂️,🧔🏼‍♂️,🧔🏽‍♂️,🧔🏾‍♂️,🧔🏿‍♂️,🧔‍♂️,🧔‍♂,🧔🏻‍♀️,🧔🏼‍♀️,🧔🏽‍♀️,🧔🏾‍♀️,🧔🏿‍♀️,🧔‍♀️,🧔‍♀,👨🏻‍🦰,👨🏼‍🦰,👨🏽‍🦰,👨🏾‍🦰,👨🏿‍🦰,👨‍🦰,👨🏻‍🦱,👨🏼‍🦱,👨🏽‍🦱,👨🏾‍🦱,👨🏿‍🦱,👨‍🦱,👨🏻‍🦳,👨🏼‍🦳,👨🏽‍🦳,👨🏾‍🦳,👨🏿‍🦳,👨‍🦳,👨🏻‍🦲,👨🏼‍🦲,👨🏽‍🦲,👨🏾‍🦲,👨🏿‍🦲,👨‍🦲,👩🏻,👩🏼,👩🏽,👩🏾,👩🏿,👩,👩🏻‍🦰,👩🏼‍🦰,👩🏽‍🦰,👩🏾‍🦰,👩🏿‍🦰,👩‍🦰,🧑🏻‍🦰,🧑🏼‍🦰,🧑🏽‍🦰,🧑🏾‍🦰,🧑🏿‍🦰,🧑‍🦰,👩🏻‍🦱,👩🏼‍🦱,👩🏽‍🦱,👩🏾‍🦱,👩🏿‍🦱,👩‍🦱,🧑🏻‍🦱,🧑🏼‍🦱,🧑🏽‍🦱,🧑🏾‍🦱,🧑🏿‍🦱,🧑‍🦱,👩🏻‍🦳,👩🏼‍🦳,👩🏽‍🦳,👩🏾‍🦳,👩🏿‍🦳,👩‍🦳,🧑🏻‍🦳,🧑🏼‍🦳,🧑🏽‍🦳,🧑🏾‍🦳,🧑🏿‍🦳,🧑‍🦳,👩🏻‍🦲,👩🏼‍🦲,👩🏽‍🦲,👩🏾‍🦲,👩🏿‍🦲,👩‍🦲,🧑🏻‍🦲,🧑🏼‍🦲,🧑🏽‍🦲,🧑🏾‍🦲,🧑🏿‍🦲,🧑‍🦲,👱🏻‍♀️,👱🏼‍♀️,👱🏽‍♀️,👱🏾‍♀️,👱🏿‍♀️,👱‍♀️,👱‍♀,👱🏻‍♂️,👱🏼‍♂️,👱🏽‍♂️,👱🏾‍♂️,👱🏿‍♂️,👱‍♂️,👱‍♂,🧓🏻,🧓🏼,🧓🏽,🧓🏾,🧓🏿,🧓,👴🏻,👴🏼,👴🏽,👴🏾,👴🏿,👴,👵🏻,👵🏼,👵🏽,👵🏾,👵🏿,👵,🙍🏻,🙍🏼,🙍🏽,🙍🏾,🙍🏿,🙍,🙍🏻‍♂️,🙍🏼‍♂️,🙍🏽‍♂️,🙍🏾‍♂️,🙍🏿‍♂️,🙍‍♂️,🙍‍♂,🙍🏻‍♀️,🙍🏼‍♀️,🙍🏽‍♀️,🙍🏾‍♀️,🙍🏿‍♀️,🙍‍♀️,🙍‍♀,🙎🏻,🙎🏼,🙎🏽,🙎🏾,🙎🏿,🙎,🙎🏻‍♂️,🙎🏼‍♂️,🙎🏽‍♂️,🙎🏾‍♂️,🙎🏿‍♂️,🙎‍♂️,🙎‍♂,🙎🏻‍♀️,🙎🏼‍♀️,🙎🏽‍♀️,🙎🏾‍♀️,🙎🏿‍♀️,🙎‍♀️,🙎‍♀,🙅🏻,🙅🏼,🙅🏽,🙅🏾,🙅🏿,🙅,🙅🏻‍♂️,🙅🏼‍♂️,🙅🏽‍♂️,🙅🏾‍♂️,🙅🏿‍♂️,🙅‍♂️,🙅‍♂,🙅🏻‍♀️,🙅🏼‍♀️,🙅🏽‍♀️,🙅🏾‍♀️,🙅🏿‍♀️,🙅‍♀️,🙅‍♀,🙆🏻,🙆🏼,🙆🏽,🙆🏾,🙆🏿,🙆,🙆🏻‍♂️,🙆🏼‍♂️,🙆🏽‍♂️,🙆🏾‍♂️,🙆🏿‍♂️,🙆‍♂️,🙆‍♂,🙆🏻‍♀️,🙆🏼‍♀️,🙆🏽‍♀️,🙆🏾‍♀️,🙆🏿‍♀️,🙆‍♀️,🙆‍♀,💁🏻,💁🏼,💁🏽,💁🏾,💁🏿,💁,💁🏻‍♂️,💁🏼‍♂️,💁🏽‍♂️,💁🏾‍♂️,💁🏿‍♂️,💁‍♂️,💁‍♂,💁🏻‍♀️,💁🏼‍♀️,💁🏽‍♀️,💁🏾‍♀️,💁🏿‍♀️,💁‍♀️,💁‍♀,🙋🏻,🙋🏼,🙋🏽,🙋🏾,🙋🏿,🙋,🙋🏻‍♂️,🙋🏼‍♂️,🙋🏽‍♂️,🙋🏾‍♂️,🙋🏿‍♂️,🙋‍♂️,🙋‍♂,🙋🏻‍♀️,🙋🏼‍♀️,🙋🏽‍♀️,🙋🏾‍♀️,🙋🏿‍♀️,🙋‍♀️,🙋‍♀,🧏🏻,🧏🏼,🧏🏽,🧏🏾,🧏🏿,🧏,🧏🏻‍♂️,🧏🏼‍♂️,🧏🏽‍♂️,🧏🏾‍♂️,🧏🏿‍♂️,🧏‍♂️,🧏‍♂,🧏🏻‍♀️,🧏🏼‍♀️,🧏🏽‍♀️,🧏🏾‍♀️,🧏🏿‍♀️,🧏‍♀️,🧏‍♀,🙇🏻,🙇🏼,🙇🏽,🙇🏾,🙇🏿,🙇,🙇🏻‍♂️,🙇🏼‍♂️,🙇🏽‍♂️,🙇🏾‍♂️,🙇🏿‍♂️,🙇‍♂️,🙇‍♂,🙇🏻‍♀️,🙇🏼‍♀️,🙇🏽‍♀️,🙇🏾‍♀️,🙇🏿‍♀️,🙇‍♀️,🙇‍♀,🤦🏻,🤦🏼,🤦🏽,🤦🏾,🤦🏿,🤦,🤦🏻‍♂️,🤦🏼‍♂️,🤦🏽‍♂️,🤦🏾‍♂️,🤦🏿‍♂️,🤦‍♂️,🤦‍♂,🤦🏻‍♀️,🤦🏼‍♀️,🤦🏽‍♀️,🤦🏾‍♀️,🤦🏿‍♀️,🤦‍♀️,🤦‍♀,🤷🏻,🤷🏼,🤷🏽,🤷🏾,🤷🏿,🤷,🤷🏻‍♂️,🤷🏼‍♂️,🤷🏽‍♂️,🤷🏾‍♂️,🤷🏿‍♂️,🤷‍♂️,🤷‍♂,🤷🏻‍♀️,🤷🏼‍♀️,🤷🏽‍♀️,🤷🏾‍♀️,🤷🏿‍♀️,🤷‍♀️,🤷‍♀,🧑🏻‍⚕️,🧑🏼‍⚕️,🧑🏽‍⚕️,🧑🏾‍⚕️,🧑🏿‍⚕️,🧑‍⚕️,🧑‍⚕,👨🏻‍⚕️,👨🏼‍⚕️,👨🏽‍⚕️,👨🏾‍⚕️,👨🏿‍⚕️,👨‍⚕️,👨‍⚕,👩🏻‍⚕️,👩🏼‍⚕️,👩🏽‍⚕️,👩🏾‍⚕️,👩🏿‍⚕️,👩‍⚕️,👩‍⚕,🧑🏻‍🎓,🧑🏼‍🎓,🧑🏽‍🎓,🧑🏾‍🎓,🧑🏿‍🎓,🧑‍🎓,👨🏻‍🎓,👨🏼‍🎓,👨🏽‍🎓,👨🏾‍🎓,👨🏿‍🎓,👨‍🎓,👩🏻‍🎓,👩🏼‍🎓,👩🏽‍🎓,👩🏾‍🎓,👩🏿‍🎓,👩‍🎓,🧑🏻‍🏫,🧑🏼‍🏫,🧑🏽‍🏫,🧑🏾‍🏫,🧑🏿‍🏫,🧑‍🏫,👨🏻‍🏫,👨🏼‍🏫,👨🏽‍🏫,👨🏾‍🏫,👨🏿‍🏫,👨‍🏫,👩🏻‍🏫,👩🏼‍🏫,👩🏽‍🏫,👩🏾‍🏫,👩🏿‍🏫,👩‍🏫,🧑🏻‍⚖️,🧑🏼‍⚖️,🧑🏽‍⚖️,🧑🏾‍⚖️,🧑🏿‍⚖️,🧑‍⚖️,🧑‍⚖,👨🏻‍⚖️,👨🏼‍⚖️,👨🏽‍⚖️,👨🏾‍⚖️,👨🏿‍⚖️,👨‍⚖️,👨‍⚖,👩🏻‍⚖️,👩🏼‍⚖️,👩🏽‍⚖️,👩🏾‍⚖️,👩🏿‍⚖️,👩‍⚖️,👩‍⚖,🧑🏻‍🌾,🧑🏼‍🌾,🧑🏽‍🌾,🧑🏾‍🌾,🧑🏿‍🌾,🧑‍🌾,👨🏻‍🌾,👨🏼‍🌾,👨🏽‍🌾,👨🏾‍🌾,👨🏿‍🌾,👨‍🌾,👩🏻‍🌾,👩🏼‍🌾,👩🏽‍🌾,👩🏾‍🌾,👩🏿‍🌾,👩‍🌾,🧑🏻‍🍳,🧑🏼‍🍳,🧑🏽‍🍳,🧑🏾‍🍳,🧑🏿‍🍳,🧑‍🍳,👨🏻‍🍳,👨🏼‍🍳,👨🏽‍🍳,👨🏾‍🍳,👨🏿‍🍳,👨‍🍳,👩🏻‍🍳,👩🏼‍🍳,👩🏽‍🍳,👩🏾‍🍳,👩🏿‍🍳,👩‍🍳,🧑🏻‍🔧,🧑🏼‍🔧,🧑🏽‍🔧,🧑🏾‍🔧,🧑🏿‍🔧,🧑‍🔧,👨🏻‍🔧,👨🏼‍🔧,👨🏽‍🔧,👨🏾‍🔧,👨🏿‍🔧,👨‍🔧,👩🏻‍🔧,👩🏼‍🔧,👩🏽‍🔧,👩🏾‍🔧,👩🏿‍🔧,👩‍🔧,🧑🏻‍🏭,🧑🏼‍🏭,🧑🏽‍🏭,🧑🏾‍🏭,🧑🏿‍🏭,🧑‍🏭,👨🏻‍🏭,👨🏼‍🏭,👨🏽‍🏭,👨🏾‍🏭,👨🏿‍🏭,👨‍🏭,👩🏻‍🏭,👩🏼‍🏭,👩🏽‍🏭,👩🏾‍🏭,👩🏿‍🏭,👩‍🏭,🧑🏻‍💼,🧑🏼‍💼,🧑🏽‍💼,🧑🏾‍💼,🧑🏿‍💼,🧑‍💼,👨🏻‍💼,👨🏼‍💼,👨🏽‍💼,👨🏾‍💼,👨🏿‍💼,👨‍💼,👩🏻‍💼,👩🏼‍💼,👩🏽‍💼,👩🏾‍💼,👩🏿‍💼,👩‍💼,🧑🏻‍🔬,🧑🏼‍🔬,🧑🏽‍🔬,🧑🏾‍🔬,🧑🏿‍🔬,🧑‍🔬,👨🏻‍🔬,👨🏼‍🔬,👨🏽‍🔬,👨🏾‍🔬,👨🏿‍🔬,👨‍🔬,👩🏻‍🔬,👩🏼‍🔬,👩🏽‍🔬,👩🏾‍🔬,👩🏿‍🔬,👩‍🔬,🧑🏻‍💻,🧑🏼‍💻,🧑🏽‍💻,🧑🏾‍💻,🧑🏿‍💻,🧑‍💻,👨🏻‍💻,👨🏼‍💻,👨🏽‍💻,👨🏾‍💻,👨🏿‍💻,👨‍💻,👩🏻‍💻,👩🏼‍💻,👩🏽‍💻,👩🏾‍💻,👩🏿‍💻,👩‍💻,🧑🏻‍🎤,🧑🏼‍🎤,🧑🏽‍🎤,🧑🏾‍🎤,🧑🏿‍🎤,🧑‍🎤,👨🏻‍🎤,👨🏼‍🎤,👨🏽‍🎤,👨🏾‍🎤,👨🏿‍🎤,👨‍🎤,👩🏻‍🎤,👩🏼‍🎤,👩🏽‍🎤,👩🏾‍🎤,👩🏿‍🎤,👩‍🎤,🧑🏻‍🎨,🧑🏼‍🎨,🧑🏽‍🎨,🧑🏾‍🎨,🧑🏿‍🎨,🧑‍🎨,👨🏻‍🎨,👨🏼‍🎨,👨🏽‍🎨,👨🏾‍🎨,👨🏿‍🎨,👨‍🎨,👩🏻‍🎨,👩🏼‍🎨,👩🏽‍🎨,👩🏾‍🎨,👩🏿‍🎨,👩‍🎨,🧑🏻‍✈️,🧑🏼‍✈️,🧑🏽‍✈️,🧑🏾‍✈️,🧑🏿‍✈️,🧑‍✈️,🧑‍✈,👨🏻‍✈️,👨🏼‍✈️,👨🏽‍✈️,👨🏾‍✈️,👨🏿‍✈️,👨‍✈️,👨‍✈,👩🏻‍✈️,👩🏼‍✈️,👩🏽‍✈️,👩🏾‍✈️,👩🏿‍✈️,👩‍✈️,👩‍✈,🧑🏻‍🚀,🧑🏼‍🚀,🧑🏽‍🚀,🧑🏾‍🚀,🧑🏿‍🚀,🧑‍🚀,👨🏻‍🚀,👨🏼‍🚀,👨🏽‍🚀,👨🏾‍🚀,👨🏿‍🚀,👨‍🚀,👩🏻‍🚀,👩🏼‍🚀,👩🏽‍🚀,👩🏾‍🚀,👩🏿‍🚀,👩‍🚀,🧑🏻‍🚒,🧑🏼‍🚒,🧑🏽‍🚒,🧑🏾‍🚒,🧑🏿‍🚒,🧑‍🚒,👨🏻‍🚒,👨🏼‍🚒,👨🏽‍🚒,👨🏾‍🚒,👨🏿‍🚒,👨‍🚒,👩🏻‍🚒,👩🏼‍🚒,👩🏽‍🚒,👩🏾‍🚒,👩🏿‍🚒,👩‍🚒,👮🏻,👮🏼,👮🏽,👮🏾,👮🏿,👮,👮🏻‍♂️,👮🏼‍♂️,👮🏽‍♂️,👮🏾‍♂️,👮🏿‍♂️,👮‍♂️,👮‍♂,👮🏻‍♀️,👮🏼‍♀️,👮🏽‍♀️,👮🏾‍♀️,👮🏿‍♀️,👮‍♀️,👮‍♀,🕵🏻,🕵🏼,🕵🏽,🕵🏾,🕵🏿,🕵️,🕵,🕵🏻‍♂️,🕵🏼‍♂️,🕵🏽‍♂️,🕵🏾‍♂️,🕵🏿‍♂️,🕵️‍♂️,🕵🏻‍♀️,🕵🏼‍♀️,🕵🏽‍♀️,🕵🏾‍♀️,🕵🏿‍♀️,🕵️‍♀️,💂🏻,💂🏼,💂🏽,💂🏾,💂🏿,💂,💂🏻‍♂️,💂🏼‍♂️,💂🏽‍♂️,💂🏾‍♂️,💂🏿‍♂️,💂‍♂️,💂‍♂,💂🏻‍♀️,💂🏼‍♀️,💂🏽‍♀️,💂🏾‍♀️,💂🏿‍♀️,💂‍♀️,💂‍♀,🥷🏻,🥷🏼,🥷🏽,🥷🏾,🥷🏿,🥷,👷🏻,👷🏼,👷🏽,👷🏾,👷🏿,👷,👷🏻‍♂️,👷🏼‍♂️,👷🏽‍♂️,👷🏾‍♂️,👷🏿‍♂️,👷‍♂️,👷‍♂,👷🏻‍♀️,👷🏼‍♀️,👷🏽‍♀️,👷🏾‍♀️,👷🏿‍♀️,👷‍♀️,👷‍♀,🤴🏻,🤴🏼,🤴🏽,🤴🏾,🤴🏿,🤴,👸🏻,👸🏼,👸🏽,👸🏾,👸🏿,👸,👳🏻,👳🏼,👳🏽,👳🏾,👳🏿,👳,👳🏻‍♂️,👳🏼‍♂️,👳🏽‍♂️,👳🏾‍♂️,👳🏿‍♂️,👳‍♂️,👳‍♂,👳🏻‍♀️,👳🏼‍♀️,👳🏽‍♀️,👳🏾‍♀️,👳🏿‍♀️,👳‍♀️,👳‍♀,👲🏻,👲🏼,👲🏽,👲🏾,👲🏿,👲,🧕🏻,🧕🏼,🧕🏽,🧕🏾,🧕🏿,🧕,🤵🏻,🤵🏼,🤵🏽,🤵🏾,🤵🏿,🤵,🤵🏻‍♂️,🤵🏼‍♂️,🤵🏽‍♂️,🤵🏾‍♂️,🤵🏿‍♂️,🤵‍♂️,🤵‍♂,🤵🏻‍♀️,🤵🏼‍♀️,🤵🏽‍♀️,🤵🏾‍♀️,🤵🏿‍♀️,🤵‍♀️,🤵‍♀,👰🏻,👰🏼,👰🏽,👰🏾,👰🏿,👰,👰🏻‍♂️,👰🏼‍♂️,👰🏽‍♂️,👰🏾‍♂️,👰🏿‍♂️,👰‍♂️,👰‍♂,👰🏻‍♀️,👰🏼‍♀️,👰🏽‍♀️,👰🏾‍♀️,👰🏿‍♀️,👰‍♀️,👰‍♀,🤰🏻,🤰🏼,🤰🏽,🤰🏾,🤰🏿,🤰,🤱🏻,🤱🏼,🤱🏽,🤱🏾,🤱🏿,🤱,👩🏻‍🍼,👩🏼‍🍼,👩🏽‍🍼,👩🏾‍🍼,👩🏿‍🍼,👩‍🍼,👨🏻‍🍼,👨🏼‍🍼,👨🏽‍🍼,👨🏾‍🍼,👨🏿‍🍼,👨‍🍼,🧑🏻‍🍼,🧑🏼‍🍼,🧑🏽‍🍼,🧑🏾‍🍼,🧑🏿‍🍼,🧑‍🍼,👼🏻,👼🏼,👼🏽,👼🏾,👼🏿,👼,🎅🏻,🎅🏼,🎅🏽,🎅🏾,🎅🏿,🎅,🤶🏻,🤶🏼,🤶🏽,🤶🏾,🤶🏿,🤶,🧑🏻‍🎄,🧑🏼‍🎄,🧑🏽‍🎄,🧑🏾‍🎄,🧑🏿‍🎄,🧑‍🎄,🦸🏻,🦸🏼,🦸🏽,🦸🏾,🦸🏿,🦸,🦸🏻‍♂️,🦸🏼‍♂️,🦸🏽‍♂️,🦸🏾‍♂️,🦸🏿‍♂️,🦸‍♂️,🦸‍♂,🦸🏻‍♀️,🦸🏼‍♀️,🦸🏽‍♀️,🦸🏾‍♀️,🦸🏿‍♀️,🦸‍♀️,🦸‍♀,🦹🏻,🦹🏼,🦹🏽,🦹🏾,🦹🏿,🦹,🦹🏻‍♂️,🦹🏼‍♂️,🦹🏽‍♂️,🦹🏾‍♂️,🦹🏿‍♂️,🦹‍♂️,🦹‍♂,🦹🏻‍♀️,🦹🏼‍♀️,🦹🏽‍♀️,🦹🏾‍♀️,🦹🏿‍♀️,🦹‍♀️,🦹‍♀,🧙🏻,🧙🏼,🧙🏽,🧙🏾,🧙🏿,🧙,🧙🏻‍♂️,🧙🏼‍♂️,🧙🏽‍♂️,🧙🏾‍♂️,🧙🏿‍♂️,🧙‍♂️,🧙‍♂,🧙🏻‍♀️,🧙🏼‍♀️,🧙🏽‍♀️,🧙🏾‍♀️,🧙🏿‍♀️,🧙‍♀️,🧙‍♀,🧚🏻,🧚🏼,🧚🏽,🧚🏾,🧚🏿,🧚,🧚🏻‍♂️,🧚🏼‍♂️,🧚🏽‍♂️,🧚🏾‍♂️,🧚🏿‍♂️,🧚‍♂️,🧚‍♂,🧚🏻‍♀️,🧚🏼‍♀️,🧚🏽‍♀️,🧚🏾‍♀️,🧚🏿‍♀️,🧚‍♀️,🧚‍♀,🧛🏻,🧛🏼,🧛🏽,🧛🏾,🧛🏿,🧛,🧛🏻‍♂️,🧛🏼‍♂️,🧛🏽‍♂️,🧛🏾‍♂️,🧛🏿‍♂️,🧛‍♂️,🧛‍♂,🧛🏻‍♀️,🧛🏼‍♀️,🧛🏽‍♀️,🧛🏾‍♀️,🧛🏿‍♀️,🧛‍♀️,🧛‍♀,🧜🏻,🧜🏼,🧜🏽,🧜🏾,🧜🏿,🧜,🧜🏻‍♂️,🧜🏼‍♂️,🧜🏽‍♂️,🧜🏾‍♂️,🧜🏿‍♂️,🧜‍♂️,🧜‍♂,🧜🏻‍♀️,🧜🏼‍♀️,🧜🏽‍♀️,🧜🏾‍♀️,🧜🏿‍♀️,🧜‍♀️,🧜‍♀,🧝🏻,🧝🏼,🧝🏽,🧝🏾,🧝🏿,🧝,🧝🏻‍♂️,🧝🏼‍♂️,🧝🏽‍♂️,🧝🏾‍♂️,🧝🏿‍♂️,🧝‍♂️,🧝‍♂,🧝🏻‍♀️,🧝🏼‍♀️,🧝🏽‍♀️,🧝🏾‍♀️,🧝🏿‍♀️,🧝‍♀️,🧝‍♀,🧞,🧞‍♂️,🧞‍♂,🧞‍♀️,🧞‍♀,🧟,🧟‍♂️,🧟‍♂,🧟‍♀️,🧟‍♀,💆🏻,💆🏼,💆🏽,💆🏾,💆🏿,💆,💆🏻‍♂️,💆🏼‍♂️,💆🏽‍♂️,💆🏾‍♂️,💆🏿‍♂️,💆‍♂️,💆‍♂,💆🏻‍♀️,💆🏼‍♀️,💆🏽‍♀️,💆🏾‍♀️,💆🏿‍♀️,💆‍♀️,💆‍♀,💇🏻,💇🏼,💇🏽,💇🏾,💇🏿,💇,💇🏻‍♂️,💇🏼‍♂️,💇🏽‍♂️,💇🏾‍♂️,💇🏿‍♂️,💇‍♂️,💇‍♂,💇🏻‍♀️,💇🏼‍♀️,💇🏽‍♀️,💇🏾‍♀️,💇🏿‍♀️,💇‍♀️,💇‍♀,🚶🏻,🚶🏼,🚶🏽,🚶🏾,🚶🏿,🚶,🚶🏻‍♂️,🚶🏼‍♂️,🚶🏽‍♂️,🚶🏾‍♂️,🚶🏿‍♂️,🚶‍♂️,🚶‍♂,🚶🏻‍♀️,🚶🏼‍♀️,🚶🏽‍♀️,🚶🏾‍♀️,🚶🏿‍♀️,🚶‍♀️,🚶‍♀,🧍🏻,🧍🏼,🧍🏽,🧍🏾,🧍🏿,🧍,🧍🏻‍♂️,🧍🏼‍♂️,🧍🏽‍♂️,🧍🏾‍♂️,🧍🏿‍♂️,🧍‍♂️,🧍‍♂,🧍🏻‍♀️,🧍🏼‍♀️,🧍🏽‍♀️,🧍🏾‍♀️,🧍🏿‍♀️,🧍‍♀️,🧍‍♀,🧎🏻,🧎🏼,🧎🏽,🧎🏾,🧎🏿,🧎,🧎🏻‍♂️,🧎🏼‍♂️,🧎🏽‍♂️,🧎🏾‍♂️,🧎🏿‍♂️,🧎‍♂️,🧎‍♂,🧎🏻‍♀️,🧎🏼‍♀️,🧎🏽‍♀️,🧎🏾‍♀️,🧎🏿‍♀️,🧎‍♀️,🧎‍♀,🧑🏻‍🦯,🧑🏼‍🦯,🧑🏽‍🦯,🧑🏾‍🦯,🧑🏿‍🦯,🧑‍🦯,👨🏻‍🦯,👨🏼‍🦯,👨🏽‍🦯,👨🏾‍🦯,👨🏿‍🦯,👨‍🦯,👩🏻‍🦯,👩🏼‍🦯,👩🏽‍🦯,👩🏾‍🦯,👩🏿‍🦯,👩‍🦯,🧑🏻‍🦼,🧑🏼‍🦼,🧑🏽‍🦼,🧑🏾‍🦼,🧑🏿‍🦼,🧑‍🦼,👨🏻‍🦼,👨🏼‍🦼,👨🏽‍🦼,👨🏾‍🦼,👨🏿‍🦼,👨‍🦼,👩🏻‍🦼,👩🏼‍🦼,👩🏽‍🦼,👩🏾‍🦼,👩🏿‍🦼,👩‍🦼,🧑🏻‍🦽,🧑🏼‍🦽,🧑🏽‍🦽,🧑🏾‍🦽,🧑🏿‍🦽,🧑‍🦽,👨🏻‍🦽,👨🏼‍🦽,👨🏽‍🦽,👨🏾‍🦽,👨🏿‍🦽,👨‍🦽,👩🏻‍🦽,👩🏼‍🦽,👩🏽‍🦽,👩🏾‍🦽,👩🏿‍🦽,👩‍🦽,🏃🏻,🏃🏼,🏃🏽,🏃🏾,🏃🏿,🏃,🏃🏻‍♂️,🏃🏼‍♂️,🏃🏽‍♂️,🏃🏾‍♂️,🏃🏿‍♂️,🏃‍♂️,🏃‍♂,🏃🏻‍♀️,🏃🏼‍♀️,🏃🏽‍♀️,🏃🏾‍♀️,🏃🏿‍♀️,🏃‍♀️,🏃‍♀,💃🏻,💃🏼,💃🏽,💃🏾,💃🏿,💃,🕺🏻,🕺🏼,🕺🏽,🕺🏾,🕺🏿,🕺,🕴🏻,🕴🏼,🕴🏽,🕴🏾,🕴🏿,🕴️,🕴,👯,👯‍♂️,👯‍♂,👯‍♀️,👯‍♀,🧖🏻,🧖🏼,🧖🏽,🧖🏾,🧖🏿,🧖,🧖🏻‍♂️,🧖🏼‍♂️,🧖🏽‍♂️,🧖🏾‍♂️,🧖🏿‍♂️,🧖‍♂️,🧖‍♂,🧖🏻‍♀️,🧖🏼‍♀️,🧖🏽‍♀️,🧖🏾‍♀️,🧖🏿‍♀️,🧖‍♀️,🧖‍♀,🧗🏻,🧗🏼,🧗🏽,🧗🏾,🧗🏿,🧗,🧗🏻‍♂️,🧗🏼‍♂️,🧗🏽‍♂️,🧗🏾‍♂️,🧗🏿‍♂️,🧗‍♂️,🧗‍♂,🧗🏻‍♀️,🧗🏼‍♀️,🧗🏽‍♀️,🧗🏾‍♀️,🧗🏿‍♀️,🧗‍♀️,🧗‍♀,🤺,🏇🏻,🏇🏼,🏇🏽,🏇🏾,🏇🏿,🏇,⛷️,⛷,🏂🏻,🏂🏼,🏂🏽,🏂🏾,🏂🏿,🏂,🏌🏻,🏌🏼,🏌🏽,🏌🏾,🏌🏿,🏌️,🏌,🏌🏻‍♂️,🏌🏼‍♂️,🏌🏽‍♂️,🏌🏾‍♂️,🏌🏿‍♂️,🏌️‍♂️,🏌🏻‍♀️,🏌🏼‍♀️,🏌🏽‍♀️,🏌🏾‍♀️,🏌🏿‍♀️,🏌️‍♀️,🏄🏻,🏄🏼,🏄🏽,🏄🏾,🏄🏿,🏄,🏄🏻‍♂️,🏄🏼‍♂️,🏄🏽‍♂️,🏄🏾‍♂️,🏄🏿‍♂️,🏄‍♂️,🏄‍♂,🏄🏻‍♀️,🏄🏼‍♀️,🏄🏽‍♀️,🏄🏾‍♀️,🏄🏿‍♀️,🏄‍♀️,🏄‍♀,🚣🏻,🚣🏼,🚣🏽,🚣🏾,🚣🏿,🚣,🚣🏻‍♂️,🚣🏼‍♂️,🚣🏽‍♂️,🚣🏾‍♂️,🚣🏿‍♂️,🚣‍♂️,🚣‍♂,🚣🏻‍♀️,🚣🏼‍♀️,🚣🏽‍♀️,🚣🏾‍♀️,🚣🏿‍♀️,🚣‍♀️,🚣‍♀,🏊🏻,🏊🏼,🏊🏽,🏊🏾,🏊🏿,🏊,🏊🏻‍♂️,🏊🏼‍♂️,🏊🏽‍♂️,🏊🏾‍♂️,🏊🏿‍♂️,🏊‍♂️,🏊‍♂,🏊🏻‍♀️,🏊🏼‍♀️,🏊🏽‍♀️,🏊🏾‍♀️,🏊🏿‍♀️,🏊‍♀️,🏊‍♀,⛹🏻,⛹🏼,⛹🏽,⛹🏾,⛹🏿,⛹️,⛹,⛹🏻‍♂️,⛹🏼‍♂️,⛹🏽‍♂️,⛹🏾‍♂️,⛹🏿‍♂️,⛹️‍♂️,⛹🏻‍♀️,⛹🏼‍♀️,⛹🏽‍♀️,⛹🏾‍♀️,⛹🏿‍♀️,⛹️‍♀️,🏋🏻,🏋🏼,🏋🏽,🏋🏾,🏋🏿,🏋️,🏋,🏋🏻‍♂️,🏋🏼‍♂️,🏋🏽‍♂️,🏋🏾‍♂️,🏋🏿‍♂️,🏋️‍♂️,🏋🏻‍♀️,🏋🏼‍♀️,🏋🏽‍♀️,🏋🏾‍♀️,🏋🏿‍♀️,🏋️‍♀️,🚴🏻,🚴🏼,🚴🏽,🚴🏾,🚴🏿,🚴,🚴🏻‍♂️,🚴🏼‍♂️,🚴🏽‍♂️,🚴🏾‍♂️,🚴🏿‍♂️,🚴‍♂️,🚴‍♂,🚴🏻‍♀️,🚴🏼‍♀️,🚴🏽‍♀️,🚴🏾‍♀️,🚴🏿‍♀️,🚴‍♀️,🚴‍♀,🚵🏻,🚵🏼,🚵🏽,🚵🏾,🚵🏿,🚵,🚵🏻‍♂️,🚵🏼‍♂️,🚵🏽‍♂️,🚵🏾‍♂️,🚵🏿‍♂️,🚵‍♂️,🚵‍♂,🚵🏻‍♀️,🚵🏼‍♀️,🚵🏽‍♀️,🚵🏾‍♀️,🚵🏿‍♀️,🚵‍♀️,🚵‍♀,🤸🏻,🤸🏼,🤸🏽,🤸🏾,🤸🏿,🤸,🤸🏻‍♂️,🤸🏼‍♂️,🤸🏽‍♂️,🤸🏾‍♂️,🤸🏿‍♂️,🤸‍♂️,🤸‍♂,🤸🏻‍♀️,🤸🏼‍♀️,🤸🏽‍♀️,🤸🏾‍♀️,🤸🏿‍♀️,🤸‍♀️,🤸‍♀,🤼,🤼‍♂️,🤼‍♂,🤼‍♀️,🤼‍♀,🤽🏻,🤽🏼,🤽🏽,🤽🏾,🤽🏿,🤽,🤽🏻‍♂️,🤽🏼‍♂️,🤽🏽‍♂️,🤽🏾‍♂️,🤽🏿‍♂️,🤽‍♂️,🤽‍♂,🤽🏻‍♀️,🤽🏼‍♀️,🤽🏽‍♀️,🤽🏾‍♀️,🤽🏿‍♀️,🤽‍♀️,🤽‍♀,🤾🏻,🤾🏼,🤾🏽,🤾🏾,🤾🏿,🤾,🤾🏻‍♂️,🤾🏼‍♂️,🤾🏽‍♂️,🤾🏾‍♂️,🤾🏿‍♂️,🤾‍♂️,🤾‍♂,🤾🏻‍♀️,🤾🏼‍♀️,🤾🏽‍♀️,🤾🏾‍♀️,🤾🏿‍♀️,🤾‍♀️,🤾‍♀,🤹🏻,🤹🏼,🤹🏽,🤹🏾,🤹🏿,🤹,🤹🏻‍♂️,🤹🏼‍♂️,🤹🏽‍♂️,🤹🏾‍♂️,🤹🏿‍♂️,🤹‍♂️,🤹‍♂,🤹🏻‍♀️,🤹🏼‍♀️,🤹🏽‍♀️,🤹🏾‍♀️,🤹🏿‍♀️,🤹‍♀️,🤹‍♀,🧘🏻,🧘🏼,🧘🏽,🧘🏾,🧘🏿,🧘,🧘🏻‍♂️,🧘🏼‍♂️,🧘🏽‍♂️,🧘🏾‍♂️,🧘🏿‍♂️,🧘‍♂️,🧘‍♂,🧘🏻‍♀️,🧘🏼‍♀️,🧘🏽‍♀️,🧘🏾‍♀️,🧘🏿‍♀️,🧘‍♀️,🧘‍♀,🛀🏻,🛀🏼,🛀🏽,🛀🏾,🛀🏿,🛀,🛌🏻,🛌🏼,🛌🏽,🛌🏾,🛌🏿,🛌,🧑🏻‍🤝‍🧑🏻,🧑🏻‍🤝‍🧑🏼,🧑🏻‍🤝‍🧑🏽,🧑🏻‍🤝‍🧑🏾,🧑🏻‍🤝‍🧑🏿,🧑🏼‍🤝‍🧑🏻,🧑🏼‍🤝‍🧑🏼,🧑🏼‍🤝‍🧑🏽,🧑🏼‍🤝‍🧑🏾,🧑🏼‍🤝‍🧑🏿,🧑🏽‍🤝‍🧑🏻,🧑🏽‍🤝‍🧑🏼,🧑🏽‍🤝‍🧑🏽,🧑🏽‍🤝‍🧑🏾,🧑🏽‍🤝‍🧑🏿,🧑🏾‍🤝‍🧑🏻,🧑🏾‍🤝‍🧑🏼,🧑🏾‍🤝‍🧑🏽,🧑🏾‍🤝‍🧑🏾,🧑🏾‍🤝‍🧑🏿,🧑🏿‍🤝‍🧑🏻,🧑🏿‍🤝‍🧑🏼,🧑🏿‍🤝‍🧑🏽,🧑🏿‍🤝‍🧑🏾,🧑🏿‍🤝‍🧑🏿,🧑‍🤝‍🧑,👭,👫,👬,💏,💑,👪,👨‍👩‍👦,👨‍👩‍👧,👨‍👩‍👧‍👦,👨‍👩‍👦‍👦,👨‍👩‍👧‍👧,👨‍👨‍👦,👨‍👨‍👧,👨‍👨‍👧‍👦,👨‍👨‍👦‍👦,👨‍👨‍👧‍👧,👩‍👩‍👦,👩‍👩‍👧,👩‍👩‍👧‍👦,👩‍👩‍👦‍👦,👩‍👩‍👧‍👧,👨‍👦,👨‍👦‍👦,👨‍👧,👨‍👧‍👦,👨‍👧‍👧,👩‍👦,👩‍👦‍👦,👩‍👧,👩‍👧‍👦,👩‍👧‍👧,🗣️,🗣,👤,👥,🫂,👣,🐵,🐒,🦍,🦧,🐶,🐕,🦮,🐕‍🦺,🐩,🐺,🦊,🦝,🐱,🐈,🐈‍⬛,🦁,🐯,🐅,🐆,🐴,🐎,🦄,🦓,🦌,🦬,🐮,🐂,🐃,🐄,🐷,🐖,🐗,🐽,🐏,🐑,🐐,🐪,🐫,🦙,🦒,🐘,🦣,🦏,🦛,🐭,🐁,🐀,🐹,🐰,🐇,🐿️,🐿,🦫,🦔,🦇,🐻,🐻‍❄️,🐻‍❄,🐨,🐼,🦥,🦦,🦨,🦘,🦡,🐾,🦃,🐔,🐓,🐣,🐤,🐥,🐦,🐧,🕊️,🕊,🦅,🦆,🦢,🦉,🦤,🪶,🦩,🦚,🦜,🐸,🐊,🐢,🦎,🐍,🐲,🐉,🦕,🦖,🐳,🐋,🐬,🦭,🐟,🐠,🐡,🦈,🐙,🐚,🐌,🦋,🐛,🐜,🐝,🪲,🐞,🦗,🪳,🕷️,🕷,🕸️,🕸,🦂,🦟,🪰,🪱,🦠,💐,🌸,💮,🏵️,🏵,🌹,🥀,🌺,🌻,🌼,🌷,🌱,🪴,🌲,🌳,🌴,🌵,🌾,🌿,☘️,☘,🍀,🍁,🍂,🍃,🍇,🍈,🍉,🍊,🍋,🍌,🍍,🥭,🍎,🍏,🍐,🍑,🍒,🍓,🫐,🥝,🍅,🫒,🥥,🥑,🍆,🥔,🥕,🌽,🌶️,🌶,🫑,🥒,🥬,🥦,🧄,🧅,🍄,🥜,🌰,🍞,🥐,🥖,🫓,🥨,🥯,🥞,🧇,🧀,🍖,🍗,🥩,🥓,🍔,🍟,🍕,🌭,🥪,🌮,🌯,🫔,🥙,🧆,🥚,🍳,🥘,🍲,🫕,🥣,🥗,🍿,🧈,🧂,🥫,🍱,🍘,🍙,🍚,🍛,🍜,🍝,🍠,🍢,🍣,🍤,🍥,🥮,🍡,🥟,🥠,🥡,🦀,🦞,🦐,🦑,🦪,🍦,🍧,🍨,🍩,🍪,🎂,🍰,🧁,🥧,🍫,🍬,🍭,🍮,🍯,🍼,🥛,☕,🫖,🍵,🍶,🍾,🍷,🍸,🍹,🍺,🍻,🥂,🥃,🥤,🧋,🧃,🧉,🧊,🥢,🍽️,🍽,🍴,🥄,🔪,🏺,🌍,🌎,🌏,🌐,🗺️,🗺,🗾,🧭,🏔️,🏔,⛰️,⛰,🌋,🗻,🏕️,🏕,🏖️,🏖,🏜️,🏜,🏝️,🏝,🏞️,🏞,🏟️,🏟,🏛️,🏛,🏗️,🏗,🧱,🪨,🪵,🛖,🏘️,🏘,🏚️,🏚,🏠,🏡,🏢,🏣,🏤,🏥,🏦,🏨,🏩,🏪,🏫,🏬,🏭,🏯,🏰,💒,🗼,🗽,⛪,🕌,🛕,🕍,⛩️,⛩,🕋,⛲,⛺,🌁,🌃,🏙️,🏙,🌄,🌅,🌆,🌇,🌉,♨️,♨,🎠,🎡,🎢,💈,🎪,🚂,🚃,🚄,🚅,🚆,🚇,🚈,🚉,🚊,🚝,🚞,🚋,🚌,🚍,🚎,🚐,🚑,🚒,🚓,🚔,🚕,🚖,🚗,🚘,🚙,🛻,🚚,🚛,🚜,🏎️,🏎,🏍️,🏍,🛵,🦽,🦼,🛺,🚲,🛴,🛹,🛼,🚏,🛣️,🛣,🛤️,🛤,🛢️,🛢,⛽,🚨,🚥,🚦,🛑,🚧,⚓,⛵,🛶,🚤,🛳️,🛳,⛴️,⛴,🛥️,🛥,🚢,✈️,✈,🛩️,🛩,🛫,🛬,🪂,💺,🚁,🚟,🚠,🚡,🛰️,🛰,🚀,🛸,🛎️,🛎,🧳,⌛,⏳,⌚,⏰,⏱️,⏱,⏲️,⏲,🕰️,🕰,🕛,🕧,🕐,🕜,🕑,🕝,🕒,🕞,🕓,🕟,🕔,🕠,🕕,🕡,🕖,🕢,🕗,🕣,🕘,🕤,🕙,🕥,🕚,🕦,🌑,🌒,🌓,🌔,🌕,🌖,🌗,🌘,🌙,🌚,🌛,🌜,🌡️,🌡,☀️,☀,🌝,🌞,🪐,⭐,🌟,🌠,🌌,☁️,☁,⛅,⛈️,⛈,🌤️,🌤,🌥️,🌥,🌦️,🌦,🌧️,🌧,🌨️,🌨,🌩️,🌩,🌪️,🌪,🌫️,🌫,🌬️,🌬,🌀,🌈,🌂,☂️,☂,☔,⛱️,⛱,⚡,❄️,❄,☃️,☃,⛄,☄️,☄,🔥,💧,🌊,🎃,🎄,🎆,🎇,🧨,✨,🎈,🎉,🎊,🎋,🎍,🎎,🎏,🎐,🎑,🧧,🎀,🎁,🎗️,🎗,🎟️,🎟,🎫,🎖️,🎖,🏆,🏅,🥇,🥈,🥉,⚽,⚾,🥎,🏀,🏐,🏈,🏉,🎾,🥏,🎳,🏏,🏑,🏒,🥍,🏓,🏸,🥊,🥋,🥅,⛳,⛸️,⛸,🎣,🤿,🎽,🎿,🛷,🥌,🎯,🪀,🪁,🎱,🔮,🪄,🧿,🎮,🕹️,🕹,🎰,🎲,🧩,🧸,🪅,🪆,♠️,♠,♥️,♥,♦️,♦,♣️,♣,♟️,♟,🃏,🀄,🎴,🎭,🖼️,🖼,🎨,🧵,🪡,🧶,🪢,👓,🕶️,🕶,🥽,🥼,🦺,👔,👕,👖,🧣,🧤,🧥,🧦,👗,👘,🥻,🩱,🩲,🩳,👙,👚,👛,👜,👝,🛍️,🛍,🎒,🩴,👞,👟,🥾,🥿,👠,👡,🩰,👢,👑,👒,🎩,🎓,🧢,🪖,⛑️,⛑,📿,💄,💍,💎,🔇,🔈,🔉,🔊,📢,📣,📯,🔔,🔕,🎼,🎵,🎶,🎙️,🎙,🎚️,🎚,🎛️,🎛,🎤,🎧,📻,🎷,🪗,🎸,🎹,🎺,🎻,🪕,🥁,🪘,📱,📲,☎️,☎,📞,📟,📠,🔋,🔌,💻,🖥️,🖥,🖨️,🖨,⌨️,⌨,🖱️,🖱,🖲️,🖲,💽,💾,💿,📀,🧮,🎥,🎞️,🎞,📽️,📽,🎬,📺,📷,📸,📹,📼,🔍,🔎,🕯️,🕯,💡,🔦,🏮,🪔,📔,📕,📖,📗,📘,📙,📚,📓,📒,📃,📜,📄,📰,🗞️,🗞,📑,🔖,🏷️,🏷,💰,🪙,💴,💵,💶,💷,💸,💳,🧾,💹,✉️,✉,📧,📨,📩,📤,📥,📦,📫,📪,📬,📭,📮,🗳️,🗳,✏️,✏,✒️,✒,🖋️,🖋,🖊️,🖊,🖌️,🖌,🖍️,🖍,📝,💼,📁,📂,🗂️,🗂,📅,📆,🗒️,🗒,🗓️,🗓,📇,📈,📉,📊,📋,📌,📍,📎,🖇️,🖇,📏,📐,✂️,✂,🗃️,🗃,🗄️,🗄,🗑️,🗑,🔒,🔓,🔏,🔐,🔑,🗝️,🗝,🔨,🪓,⛏️,⛏,⚒️,⚒,🛠️,🛠,🗡️,🗡,⚔️,⚔,🔫,🪃,🏹,🛡️,🛡,🪚,🔧,🪛,🔩,⚙️,⚙,🗜️,🗜,⚖️,⚖,🦯,🔗,⛓️,⛓,🪝,🧰,🧲,🪜,⚗️,⚗,🧪,🧫,🧬,🔬,🔭,📡,💉,🩸,💊,🩹,🩺,🚪,🛗,🪞,🪟,🛏️,🛏,🛋️,🛋,🪑,🚽,🪠,🚿,🛁,🪤,🪒,🧴,🧷,🧹,🧺,🧻,🪣,🧼,🪥,🧽,🧯,🛒,🚬,⚰️,⚰,🪦,⚱️,⚱,🗿,🪧,🏧,🚮,🚰,♿,🚹,🚺,🚻,🚼,🚾,🛂,🛃,🛄,🛅,⚠️,⚠,🚸,⛔,🚫,🚳,🚭,🚯,🚱,🚷,📵,🔞,☢️,☢,☣️,☣,⬆️,⬆,↗️,↗,➡️,➡,↘️,↘,⬇️,⬇,↙️,↙,⬅️,⬅,↖️,↖,↕️,↕,↔️,↔,↩️,↩,↪️,↪,⤴️,⤴,⤵️,⤵,🔃,🔄,🔙,🔚,🔛,🔜,🔝,🛐,⚛️,⚛,🕉️,🕉,✡️,✡,☸️,☸,☯️,☯,✝️,✝,☦️,☦,☪️,☪,☮️,☮,🕎,🔯,♈,♉,♊,♋,♌,♍,♎,♏,♐,♑,♒,♓,⛎,🔀,🔁,🔂,▶️,▶,⏩,⏭️,⏭,⏯️,⏯,◀️,◀,⏪,⏮️,⏮,🔼,⏫,🔽,⏬,⏸️,⏸,⏹️,⏹,⏺️,⏺,⏏️,⏏,🎦,🔅,🔆,📶,📳,📴,♀️,♀,♂️,♂,⚧️,⚧,✖️,✖,➕,➖,➗,♾️,♾,‼️,‼,⁉️,⁉,❓,❔,❕,❗,〰️,〰,💱,💲,⚕️,⚕,♻️,♻,⚜️,⚜,🔱,📛,🔰,⭕,✅,☑️,☑,✔️,✔,❌,❎,➰,➿,〽️,〽,✳️,✳,✴️,✴,❇️,❇,©️,©,®️,®,™️,™,#️⃣,#⃣,*️⃣,*⃣,0️⃣,0⃣,1️⃣,1⃣,2️⃣,2⃣,3️⃣,3⃣,4️⃣,4⃣,5️⃣,5⃣,6️⃣,6⃣,7️⃣,7⃣,8️⃣,8⃣,9️⃣,9⃣,🔟,🔠,🔡,🔢,🔣,🔤,🅰️,🅰,🆎,🅱️,🅱,🆑,🆒,🆓,ℹ️,ℹ,🆔,Ⓜ️,Ⓜ,🆕,🆖,🅾️,🅾,🆗,🅿️,🅿,🆘,🆙,🆚,🈁,🈂️,🈂,🈷️,🈷,🈶,🈯,🉐,🈹,🈚,🈲,🉑,🈸,🈴,🈳,㊗️,㊗,㊙️,㊙,🈺,🈵,🔴,🟠,🟡,🟢,🔵,🟣,🟤,⚫,⚪,🟥,🟧,🟨,🟩,🟦,🟪,🟫,⬛,⬜,◼️,◼,◻️,◻,◾,◽,▪️,▪,▫️,▫,🔶,🔷,🔸,🔹,🔺,🔻,💠,🔘,🔳,🔲,🏁,🚩,🎌,🏴,🏳️,🏳,🏳️‍🌈,🏳‍🌈,🏳️‍⚧️,🏴‍☠️,🏴‍☠,🇦🇨,🇦🇩,🇦🇪,🇦🇫,🇦🇬,🇦🇮,🇦🇱,🇦🇲,🇦🇴,🇦🇶,🇦🇷,🇦🇸,🇦🇹,🇦🇺,🇦🇼,🇦🇽,🇦🇿,🇧🇦,🇧🇧,🇧🇩,🇧🇪,🇧🇫,🇧🇬,🇧🇭,🇧🇮,🇧🇯,🇧🇱,🇧🇲,🇧🇳,🇧🇴,🇧🇶,🇧🇷,🇧🇸,🇧🇹,🇧🇻,🇧🇼,🇧🇾,🇧🇿,🇨🇦,🇨🇨,🇨🇩,🇨🇫,🇨🇬,🇨🇭,🇨🇮,🇨🇰,🇨🇱,🇨🇲,🇨🇳,🇨🇴,🇨🇵,🇨🇷,🇨🇺,🇨🇻,🇨🇼,🇨🇽,🇨🇾,🇨🇿,🇩🇪,🇩🇬,🇩🇯,🇩🇰,🇩🇲,🇩🇴,🇩🇿,🇪🇦,🇪🇨,🇪🇪,🇪🇬,🇪🇭,🇪🇷,🇪🇸,🇪🇹,🇪🇺,🇫🇮,🇫🇯,🇫🇰,🇫🇲,🇫🇴,🇫🇷,🇬🇦,🇬🇧,🇬🇩,🇬🇪,🇬🇫,🇬🇬,🇬🇭,🇬🇮,🇬🇱,🇬🇲,🇬🇳,🇬🇵,🇬🇶,🇬🇷,🇬🇸,🇬🇹,🇬🇺,🇬🇼,🇬🇾,🇭🇰,🇭🇲,🇭🇳,🇭🇷,🇭🇹,🇭🇺,🇮🇨,🇮🇩,🇮🇪,🇮🇱,🇮🇲,🇮🇳,🇮🇴,🇮🇶,🇮🇷,🇮🇸,🇮🇹,🇯🇪,🇯🇲,🇯🇴,🇯🇵,🇰🇪,🇰🇬,🇰🇭,🇰🇮,🇰🇲,🇰🇳,🇰🇵,🇰🇷,🇰🇼,🇰🇾,🇰🇿,🇱🇦,🇱🇧,🇱🇨,🇱🇮,🇱🇰,🇱🇷,🇱🇸,🇱🇹,🇱🇺,🇱🇻,🇱🇾,🇲🇦,🇲🇨,🇲🇩,🇲🇪,🇲🇫,🇲🇬,🇲🇭,🇲🇰,🇲🇱,🇲🇲,🇲🇳,🇲🇴,🇲🇵,🇲🇶,🇲🇷,🇲🇸,🇲🇹,🇲🇺,🇲🇻,🇲🇼,🇲🇽,🇲🇾,🇲🇿,🇳🇦,🇳🇨,🇳🇪,🇳🇫,🇳🇬,🇳🇮,🇳🇱,🇳🇴,🇳🇵,🇳🇷,🇳🇺,🇳🇿,🇴🇲,🇵🇦,🇵🇪,🇵🇫,🇵🇬,🇵🇭,🇵🇰,🇵🇱,🇵🇲,🇵🇳,🇵🇷,🇵🇸,🇵🇹,🇵🇼,🇵🇾,🇶🇦,🇷🇪,🇷🇴,🇷🇸,🇷🇺,🇷🇼,🇸🇦,🇸🇧,🇸🇨,🇸🇩,🇸🇪,🇸🇬,🇸🇭,🇸🇮,🇸🇯,🇸🇰,🇸🇱,🇸🇲,🇸🇳,🇸🇴,🇸🇷,🇸🇸,🇸🇹,🇸🇻,🇸🇽,🇸🇾,🇸🇿,🇹🇦,🇹🇨,🇹🇩,🇹🇫,🇹🇬,🇹🇭,🇹🇯,🇹🇰,🇹🇱,🇹🇲,🇹🇳,🇹🇴,🇹🇷,🇹🇹,🇹🇻,🇹🇼,🇹🇿,🇺🇦,🇺🇬,🇺🇲,🇺🇳,🇺🇸,🇺🇾,🇺🇿,🇻🇦,🇻🇨,🇻🇪,🇻🇬,🇻🇮,🇻🇳,🇻🇺,🇼🇫,🇼🇸,🇽🇰,🇾🇪,🇾🇹,🇿🇦,🇿🇲,🇿🇼,🏴󠁧󠁢󠁥󠁮󠁧󠁿,🏴󠁧󠁢󠁳󠁣󠁴󠁿,🏴󠁧󠁢󠁷󠁬󠁳󠁿}` | Page Icon [Emoji](https://developers.notion.com/reference/emoji- object) |
| `--cover COVER` | Cover [External URL](https://developers.notion.com/reference/file- object#external-file-objects) |
| `--page-content PAGE_CONTENT` | The content of the page, using Markdown syntax. [See the documentation](https://www.notion.com/help/writing- and-edit... |

### `notion-create-file-upload`

Create a file upload. [See the

| Flag | Description |
|---|---|
| `--mode {single_part,multi_part,external_url}` | How the file is being sent. Use `Multi Part` for files larger than 20MB. Use `External URL` for files that are tempor... |
| `--filename FILENAME` | Name of the file to be created. Required when mode is multi_part or external_url. Otherwise optional, and used to ove... |
| `--content-type CONTENT_TYPE` | MIME type of the file to be created. Recommended when sending the file in multiple parts. Must match the content type... |
| `--number-of-parts NUMBER_OF_PARTS` | When mode is `Multi Part`, the number of parts you are uploading. Must be between 1 and 1,000. This must match the nu... |
| `--external-url EXTERNAL_URL` | When mode is `External URL`, provide the HTTPS URL of a publicly accessible file to import into your workspace. |

### `notion-create-database`

Create a database and its initial data source. [See the

| Flag | Description |
|---|---|
| `--parent PARENT` | Select a parent page or provide a page ID You can use the "retrieve_options" tool using these parameters to get the v... |
| `--title TITLE` | Title of database as it appears in Notion. An array of [rich text objects](https://developers.notion.com/reference/ri... |
| `--properties PROPERTIES` | Property schema of database. The keys are the names of properties as they appear in Notion and the values are [proper... |

### `notion-create-comment`

Create a comment in a page or existing discussion thread. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | Search for a page or provide a page ID You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--discussion-id DISCUSSION_ID` | The ID of a discussion thread. [See the documentation] (https://developers.notion.com/docs/working-with- comments#ret... |
| `--comment COMMENT` | The comment text |

### `notion-complete-file-upload`

Use this action to finalize a `mode=multi_part` file upload after all

| Flag | Description |
|---|---|
| `--file-upload-id FILE_UPLOAD_ID` | The ID of the file upload to send. You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `notion-append-block`

Append new and/or existing blocks to the specified parent. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | Select a parent block/page or provide its ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--block-types BLOCK_TYPES` | Selector strings for what kind of content you're appending. Accepted values: `blockIds`, `markdownContents`, `imageUrls`. **NOT raw Notion block JSON** — passing block objects throws a type error. |

**Gotcha:** the `--block-types` name looks like it accepts Notion API block objects (the way the REST API does), but it only accepts the three selector strings above. Input paths for the actual content are non-obvious and this command frequently returns `"Nothing to append"`. **For writing page content, prefer `notion-create-page --page-content` (see "Writing page content" recipe above).** Use `notion-append-block` only when you specifically need to append to an existing page by block/media reference.

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'notion'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@notion` to bypass the 1h tool-list cache.
