
# Google Docs (via Higgsfield MCP proxy)

Create, read, edit Google Docs documents and text. Exposes 12 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @docs <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @docs --list                    # all 12 tools
./bin/mcp2cli @docs google-docs-create-document-from-template --help   # inspect one
./bin/mcp2cli @docs google-docs-create-document-from-template --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @docs --pretty <cmd>` — `--pretty` goes AFTER `@docs`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @docs --head N <cmd>` — `--head N` goes AFTER `@docs`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 12 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `google-docs-create-document-from-template`

Create a new Google Docs file from a template. Optionally include

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--template-id TEMPLATE_ID` | Select the template document you'd like to use as the template, or use a custom expression to reference a document ID... |
| `--destination-drive DESTINATION_DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--folder-id FOLDER_ID` | Select the folder of the newly created Google Doc and/or PDF, or use a custom expression to reference a folder ID fro... |
| `--name NAME` | Name of the file you want to create (eg. `myFile` will create a Google Doc called `myFile` and a pdf called `myFile.p... |
| `--mode MODE` | Specify if you want to create a Google Doc, PDF or both. (JSON array) |
| `--replace-values REPLACE_VALUES` | Replace text placeholders in the document. Use the format `{{xyz}}` in the document but exclude the curly braces in t... |

### `google-docs-replace-text`

Replace all instances of matched text in an existing document

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--replaced REPLACED` | The text that will be replaced |
| `--text TEXT` | The replacement text. Can include Markdown formatting (bold, italic, code, links, headings, lists, etc.). |
| `--enable-markdown` | Enable Markdown parsing for the replacement text. When enabled, Markdown syntax (e.g., **bold**, *italic*, [links](ur... |
| `--match-case` | Case sensitive search (`true`) or not (`false`). Defaults to `false` |
| `--tab-ids TAB_IDS` | The tab IDs to replace the text in You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `google-docs-replace-image`

Replace image in a existing document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--image-id IMAGE_ID` | The image that will be replaced You can use the "retrieve_options" tool using these parameters to get the values. key... |
| `--image-uri IMAGE_URI` | The URL of the image you want to insert into the doc |

### `google-docs-insert-text`

Insert text into a document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--text TEXT` | Enter static text (e.g., `hello world`) or a reference to a string exported by a previous step (e.g., `{{steps.foo.$r... |
| `--index INDEX` | The index to insert the text at |
| `--tab-id TAB_ID` | The Tab ID You can use the "retrieve_options" tool using these parameters to get the values. key: google_docs- insert... |

### `google-docs-insert-table`

Insert a table into a document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--rows ROWS` | The number of rows in the table |
| `--columns COLUMNS` | The number of columns in the table |
| `--index INDEX` | The index to insert the table at |
| `--tab-id TAB_ID` | The Tab ID You can use the "retrieve_options" tool using these parameters to get the values. key: google_docs- insert... |

### `google-docs-insert-page-break`

Insert a page break into a document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--index INDEX` | The index to insert the page break at |
| `--tab-id TAB_ID` | The Tab ID You can use the "retrieve_options" tool using these parameters to get the values. key: google_docs- insert... |

### `google-docs-get-tab-content`

Get the content of a tab in a document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--tab-ids TAB_IDS` | Return content for the specified tabs You can use the "retrieve_options" tool using these parameters to get the value... |

### `google-docs-get-document`

Get the contents of the latest version of a document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--include-tabs-content` | Whether to populate the `Document.tabs` field instead of the text content fields like `body` and `documentStyle` on `... |
| `--tab-ids TAB_IDS` | Only return content for the specified tabs You can use the "retrieve_options" tool using these parameters to get the ... |

### `google-docs-find-document`

Search for a specific file by name. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--name-search-term NAME_SEARCH_TERM` | Search for a file by name (equivalent to the query `name contains [value]`). |
| `--search-query SEARCH_QUERY` | Search for a file with a query. [See the documentation ](https://developers.google.com/drive/api/guides/ref- search-t... |

### `google-docs-create-document`

Create a new document. [See the

| Flag | Description |
|---|---|
| `--title TITLE` | Title of the new document |
| `--text TEXT` | Enter static text (e.g., `hello world`) or a reference to a string exported by a previous step (e.g., `{{steps.foo.$r... |
| `--use-markdown` | Enable markdown formatting support. When enabled, the text will be parsed as markdown and converted to Google Docs fo... |
| `--folder-id FOLDER_ID` | The folder in the drive You can use the "retrieve_options" tool using these parameters to get the values. key: google... |

### `google-docs-append-text`

Append text to an existing document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--text TEXT` | Enter static text (e.g., `hello world`) or a reference to a string exported by a previous step (e.g., `{{steps.foo.$r... |
| `--append-at-beginning` | Whether to append at the beginning (`true`) of the document or at the end (`false`). Defaults to `false` |

### `google-docs-append-image`

Appends an image to the end of a document. [See the

| Flag | Description |
|---|---|
| `--doc-id DOC_ID` | Search for and select a document. You can also use a custom expression to pass a value from a previous step (e.g., `{... |
| `--image-uri IMAGE_URI` | The URL of the image you want to insert into the doc |
| `--append-at-beginning` | Whether to append at the beginning (`true`) of the document or at the end (`false`). Defaults to `false` |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'docs'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@docs` to bypass the 1h tool-list cache.
