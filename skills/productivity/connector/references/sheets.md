
# Google Sheets (via Higgsfield MCP proxy)

Read, write, append, and manage Google Sheets. Exposes 39 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @sheets <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @sheets --list                    # all 39 tools
./bin/mcp2cli @sheets google-sheets-new-spreadsheet --help   # inspect one
./bin/mcp2cli @sheets google-sheets-new-spreadsheet --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @sheets --pretty <cmd>` — `--pretty` goes AFTER `@sheets`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @sheets --head N <cmd>` — `--head N` goes AFTER `@sheets`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 39 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `google-sheets-new-spreadsheet`

Create a new Google Spreadsheet with an optional worksheet name and

| Flag | Description |
|---|---|
| `--title TITLE` | The title of the new spreadsheet. |
| `--sheet-name SHEET_NAME` | Name for the first worksheet. Default: `Sheet1`. |
| `--headers HEADERS` | Column headers to add as row 1. Example: `["Name", "Email", "Score"]`. (JSON array) |

### `google-sheets-find-rows`

Search for rows matching a value in a specific column. Use **Get

| Flag | Description |
|---|---|
| `--spreadsheet-id SPREADSHEET_ID` | The spreadsheet ID from the Google Sheets URL. |
| `--sheet-name SHEET_NAME` | The worksheet (tab) name. Use **Get Spreadsheet Info** to discover worksheet names. |
| `--column COLUMN` | Column header name (e.g., `Name`, `Email`) or column letter (e.g., `A`, `B`). |
| `--search-value SEARCH_VALUE` | The value to search for. |
| `--match-type {exact,contains,starts_with}` | How to match: `exact` (case-insensitive exact match), `contains` (substring match), `starts_with`. Default: `contains`. |

### `google-sheets-read-rows`

Read rows from a Google Sheets worksheet. Returns data as objects

| Flag | Description |
|---|---|
| `--spreadsheet-id SPREADSHEET_ID` | The spreadsheet ID from the Google Sheets URL. |
| `--sheet-name SHEET_NAME` | The worksheet (tab) name. Use **Get Spreadsheet Info** to discover worksheet names. |
| `--range RANGE` | Optional A1 notation range within the sheet (e.g., `A1:D10`, `A:F`). Omit to read all data. |
| `--has-headers` | Whether row 1 contains column headers. If true, returns rows as objects with header keys. Default: `true`. |

### `google-sheets-list-spreadsheets`

List Google Spreadsheets accessible to the authenticated user

| Flag | Description |
|---|---|
| `--query QUERY` | Search spreadsheets by name. Leave empty to list all. |
| `--limit LIMIT` | Maximum number of spreadsheets to return. Default: 20. |

### `google-sheets-get-spreadsheet-info`

Get the structure of a Google Spreadsheet — worksheet names, column

| Flag | Description |
|---|---|
| `--spreadsheet-id SPREADSHEET_ID` | The spreadsheet ID from the Google Sheets URL. |

### `google-sheets-add-worksheet`

Add a new worksheet (tab) to an existing spreadsheet. Optionally set

| Flag | Description |
|---|---|
| `--spreadsheet-id SPREADSHEET_ID` | The spreadsheet ID from the Google Sheets URL. |
| `--title TITLE` | The name of the new worksheet (tab). |
| `--headers HEADERS` | Column headers to add as row 1. Example: `["Name", "Email", "Score"]`. (JSON array) |

### `google-sheets-add-rows`

Append one or more rows to a Google Sheets worksheet. Pass rows as a

| Flag | Description |
|---|---|
| `--spreadsheet-id SPREADSHEET_ID` | The spreadsheet ID from the Google Sheets URL. |
| `--sheet-name SHEET_NAME` | The worksheet (tab) name. Use **Get Spreadsheet Info** to discover worksheet names. |
| `--rows ROWS` | JSON array of rows to append. Each row can be an object with column header keys or an array of positional values. Exa... |
| `--has-headers` | Whether row 1 contains column headers. Required when passing rows as objects. Default: `true`. |

### `google-sheets-upsert-row`

Upsert a row of data in a Google Sheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--insert INSERT` | Insert statement: the row data you want to add to the Google sheet if the key *doesn't* exist. If the key *does* exis... |
| `--column COLUMN` | The column of the sheet to lookup (e.g. `A`). This column functions as the key column for the upsert operation. |
| `--value VALUE` | The value of the key to search for in **Key Column**. Defaults to the value in **Insert**'s "key" column if left blank. |
| `--updates UPDATES` | Update statment: if the spreadsheet contains duplicate key **Value** in some row in the specified **Column**, individ... |

### `google-sheets-update-row`

Update a row in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the worksheet to update. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | The spreadsheet containing the worksheet to update You can use the "retrieve_options" tool using these parameters to ... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or enter a custom expression. When referencing a spreadsheet dynamically, you must provide a custo... |
| `--has-headers` | If the first row of your document has headers, we'll retrieve them to make it easy to enter the value for each column... |
| `--row ROW` | Row Number |

### `google-sheets-update-multiple-rows`

Update multiple rows in a spreadsheet defined by a range. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the worksheet to update. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | The spreadsheet containing the worksheet to update You can use the "retrieve_options" tool using these parameters to ... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--range RANGE` | The A1 notation of the values to retrieve. E.g., `A1:E5` |
| `--rows ROWS` | Provide an array of arrays |

### `google-sheets-update-formatting`

Update the formatting of a cell in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the worksheet to update. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | The spreadsheet containing the worksheet to update You can use the "retrieve_options" tool using these parameters to ... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--range RANGE` | The range of cells to update. E.g., `A1:A10` |
| `--background-color-red-value BACKGROUND_COLOR_RED_VALUE` | The amount of red in the color as a value in the interval [0, 1] |
| `--background-color-green-value BACKGROUND_COLOR_GREEN_VALUE` | The amount of green in the color as a value in the interval [0, 1] |
| `--background-color-blue-value BACKGROUND_COLOR_BLUE_VALUE` | The amount of blue in the color as a value in the interval [0, 1] |
| `--text-color-red-value TEXT_COLOR_RED_VALUE` | The amount of red in the color as a value in the interval [0, 1] |
| `--text-color-green-value TEXT_COLOR_GREEN_VALUE` | The amount of green in the color as a value in the interval [0, 1] |
| `--text-color-blue-value TEXT_COLOR_BLUE_VALUE` | The amount of blue in the color as a value in the interval [0, 1] |
| `--font-size FONT_SIZE` | The size of the font |
| `--bold` | Whether the font should be bold |
| `--italic` | Whether the font should be italic |
| `--strikethrough` | Whether the font should be strikethrough |
| `--horizontal-alignment {LEFT,CENTER,RIGHT}` | The horizontal alignment of the text |
| `--top-border-style {DOTTED,DASHED,SOLID,SOLID_MEDIUM,SOLID_THICK,NONE,DOUBLE}` | The style of the top border |
| `--bottom-border-style {DOTTED,DASHED,SOLID,SOLID_MEDIUM,SOLID_THICK,NONE,DOUBLE}` | The style of the bottom border |
| `--left-border-style {DOTTED,DASHED,SOLID,SOLID_MEDIUM,SOLID_THICK,NONE,DOUBLE}` | The style of the left border |
| `--right-border-style {DOTTED,DASHED,SOLID,SOLID_MEDIUM,SOLID_THICK,NONE,DOUBLE}` | The style of the right border |
| `--inner-horizontal-border-style {DOTTED,DASHED,SOLID,SOLID_MEDIUM,SOLID_THICK,NONE,DOUBLE}` | The style of the inner horizontal border |
| `--inner-vertical-border-style {DOTTED,DASHED,SOLID,SOLID_MEDIUM,SOLID_THICK,NONE,DOUBLE}` | The style of the inner vertical border |

### `google-sheets-update-conditional-format-rule`

Modify existing conditional formatting rule. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--range RANGE` | The range of cells to protect (e.g., `A1:A10`) |
| `--condition-type {ONE_OF_LIST,NUMBER_GREATER,NUMBER_LESS,DATE_BEFORE,DATE_AFTER,TEXT_CONTAINS,TEXT_IS_EMAIL,TEXT_IS_URL,BOOLEAN}` | The type of data condition |
| `--condition-values CONDITION_VALUES` | Values for condition (e.g., color scales or custom formulas) (JSON array) |
| `--formatting-type {BOOLEAN_RULE,GRADIENT_RULE}` | Choose between boolean condition or gradient color scale |
| `--rgb-color RGB_COLOR` | The RGB color value (e.g., {"red": 1.0, "green": 0.5, "blue": 0.2}) (JSON object) |
| `--text-format TEXT_FORMAT` | The text format options (JSON object) |
| `--bold` | Whether the text is bold |
| `--italic` | Whether the text is italic |
| `--strikethrough` | Whether the text is strikethrough |
| `--interpolation-point-type {MIN,MAX,NUMBER,PERCENT,PERCENTILE}` | The interpolation point type |
| `--index INDEX` | The zero-based index of the rule |
| `--new-index NEW_INDEX` | The new zero-based index of the rule |

### `google-sheets-update-cell`

Update a cell in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the worksheet to update. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | The spreadsheet containing the worksheet to update You can use the "retrieve_options" tool using these parameters to ... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--cell CELL` | The A1 notation of the cell. E.g., `A1` |
| `--new-cell NEW_CELL` | The new cell value |

### `google-sheets-set-data-validation`

Add data validation rules to cells (dropdowns, checkboxes,

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--range RANGE` | The range of cells to apply validation (e.g., `A1:A10`) |
| `--validation-type {NUMBER_GREATER,NUMBER_GREATER_THAN_EQ,NUMBER_LESS_THAN_EQ,NUMBER_LESS,TEXT_CONTAINS,TEXT_NOT_CONTAINS,DATE_EQUAL_TO,ONE_OF_LIST,DATE_AFTER,DATE_ON_OR_AFTER,DATE_BEFORE,DATE_ON_OR_BEFORE,DATE_BETWEEN,TEXT_STARTS_WITH,TEXT_ENDS_WITH,TEXT_EQUAL_TO,TEXT_NOT_EQUAL_TO,CUSTOM_FORMULA,NUMBER_EQUAL_TO,NUMBER_NOT_EQUAL_TO,NUMBER_BETWEEN,NUMBER_NOT_BETWEEN}` | The type of data validation |
| `--validation-values VALIDATION_VALUES` | Values for validation (e.g., dropdown options) (JSON array) |

### `google-sheets-move-dimension`

Move a dimension in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--dimension {ROWS,COLUMNS}` | The dimension to move |
| `--start-index START_INDEX` | The start (inclusive) of the span |
| `--end-index END_INDEX` | The end (exclusive) of the span |
| `--destination-index DESTINATION_INDEX` | The zero-based start index of where to move the source data to, based on the coordinates *before* the source data is ... |

### `google-sheets-merge-cells`

Merge a range of cells into a single cell. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--range RANGE` | The range of cells to apply validation (e.g., `A1:A10`) |
| `--merge-type {MERGE_ALL,MERGE_COLUMNS,MERGE_ROWS}` | The type of merge to perform |

### `google-sheets-list-worksheets`

Get a list of all worksheets in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive to select a spreadsheet from. If you are connected with any [Google Shared Drives](https://suppo rt.google.... |
| `--sheet-id SHEET_ID` | List worksheets in the specified spreadsheet You can use the "retrieve_options" tool using these parameters to get th... |

### `google-sheets-insert-dimension`

Insert a dimension into a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--dimension {ROWS,COLUMNS}` | The dimension to insert |
| `--start-index START_INDEX` | The start (inclusive) of the span, or not set if unbounded |
| `--end-index END_INDEX` | The end (exclusive) of the span |
| `--inherit-from-before` | Whether dimension properties should be extended from the dimensions before or after the newly inserted dimensions. Tr... |

### `google-sheets-insert-comment`

Insert a comment into a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--file-id FILE_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--content CONTENT` | The comment to add to the spreadsheet. |

### `google-sheets-insert-anchored-note`

Insert a note on a spreadsheet cell. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--cell CELL` | The A1 notation of the cell. E.g., `A1` |
| `--content CONTENT` | The comment to add to the spreadsheet. |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |

### `google-sheets-get-values-in-range`

Get all values or values from a range of cells using A1 notation

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--range RANGE` | The A1 notation of the values to retrieve. E.g., `A1:E5` |

### `google-sheets-get-spreadsheet-by-id`

Returns the spreadsheet at the given ID. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](http s://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |

### `google-sheets-get-current-user`

Retrieve Google Sheets account metadata for the authenticated user by

_No flags._

### `google-sheets-get-cell`

Fetch the contents of a specific cell in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--cell CELL` | The A1 notation of the cell. E.g., `A1` |

### `google-sheets-find-row`

Find one or more rows by a column and value. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--column COLUMN` | Column Letter |
| `--value VALUE` | The value to search for |
| `--export-row` | Set to `true` to return cell values for the entire row |

### `google-sheets-delete-worksheet`

Delete a specific worksheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the spreadsheet to edit. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |

### `google-sheets-delete-rows`

Deletes the specified rows from a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the spreadsheet to edit. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--start-index START_INDEX` | Row number of the start (inclusive) of the range of rows to delete |
| `--end-index END_INDEX` | Row number of the end (exclusive) of the range of rows to delete |

### `google-sheets-delete-conditional-format-rule`

Remove conditional formatting rule by index. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--index INDEX` | The zero-based index of the rule |

### `google-sheets-create-worksheet`

Create a blank worksheet with a title. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the spreadsheet to edit. If you are connected with any [Google Shared Drives](https://s upport.g... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--title TITLE` | The title of the new worksheet |

### `google-sheets-create-spreadsheet`

Create a blank spreadsheet or duplicate an existing spreadsheet. [See

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive to create the new spreadsheet in. If you are connected with any [Google Shared Drives](https://supp ort.goo... |
| `--title TITLE` | The title of the new spreadsheet |
| `--folder-id FOLDER_ID` | The folder you want to save the file to You can use the "retrieve_options" tool using these parameters to get the val... |
| `--sheet-id SHEET_ID` | The Google spreadsheet to copy You can use the "retrieve_options" tool using these parameters to get the values. key:... |

### `google-sheets-copy-worksheet`

Copy an existing worksheet to another Google Sheets file. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the worksheet to copy. If you are connected with any [Google Shared Drives](https://supp ort.goo... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--destination-sheet-id DESTINATION_SHEET_ID` | The spreadsheet to copy the worksheet to You can use the "retrieve_options" tool using these parameters to get the va... |

### `google-sheets-clear-rows`

Delete the content of a row or rows in a spreadsheet. Deleted rows

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the spreadsheet to edit. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--start-index START_INDEX` | Row number of the start (inclusive) of the range of rows to clear |
| `--end-index END_INDEX` | Row number of the end (exclusive) of the range of rows to clear |

### `google-sheets-clear-cell`

Delete the content of a specific cell in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the spreadsheet to edit. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--cell CELL` | The A1 notation of the cell to clear. E.g., `A1` |

### `google-sheets-add-single-row`

Add a single row of data to Google Sheets. Optionally insert the row

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or enter a custom expression. When referencing a spreadsheet dynamically, you must provide a custo... |
| `--has-headers` | If the first row of your document has headers, we'll retrieve them to make it easy to enter the value for each column... |
| `--row-index ROW_INDEX` | The row number where the new row should be inserted (e.g., `2` to insert after the header row, shifting existing data... |

### `google-sheets-add-protected-range`

Add edit protection to cell range with permissions. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--protected-range-id PROTECTED_RANGE_ID` | The ID of the protected range (required for update and delete operations). This is a unique identifier assigned by Go... |
| `--range RANGE` | The range of cells to protect (e.g., `A1:A10`). Required for add and update operations |
| `--description DESCRIPTION` | A description of the protected range |
| `--requesting-user-can-edit` | If true, the user making this request can edit the protected range |
| `--protectors PROTECTORS` | Email addresses of users/groups who can edit the protected range (e.g., user@example.com) (JSON array) |

### `google-sheets-add-multiple-rows`

Add multiple rows of data to a Google Sheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--rows ROWS` | Provide an array of arrays |
| `--reset-row-format` | Reset the formatting of the rows that were added (line style to none, background to white, foreground color to black,... |

### `google-sheets-add-conditional-format-rule`

Create conditional formatting with color scales or custom formulas

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--range RANGE` | The range of cells to format (e.g., `A1:A10`) |
| `--condition-type {ONE_OF_LIST,NUMBER_GREATER,NUMBER_LESS,DATE_BEFORE,DATE_AFTER,TEXT_CONTAINS,TEXT_IS_EMAIL,TEXT_IS_URL,BOOLEAN}` | The type of data condition |
| `--condition-values CONDITION_VALUES` | Values for condition (e.g., color scales or custom formulas) (JSON array) |
| `--formatting-type {BOOLEAN_RULE,GRADIENT_RULE}` | Choose between boolean condition or gradient color scale |
| `--rgb-color RGB_COLOR` | The RGB color value (e.g., {"red": 1.0, "green": 0.5, "blue": 0.2}) (JSON object) |
| `--text-format TEXT_FORMAT` | The text format options (JSON object) |
| `--bold` | Whether the text is bold |
| `--italic` | Whether the text is italic |
| `--strikethrough` | Whether the text is strikethrough |
| `--interpolation-point-type {MIN,MAX,NUMBER,PERCENT,PERCENTILE}` | The interpolation point type |
| `--index INDEX` | The zero-based index of the rule |

### `google-sheets-add-column`

Create a new column in a spreadsheet. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the spreadsheet to edit. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | Select a spreadsheet or provide a spreadsheet ID You can use the "retrieve_options" tool using these parameters to ge... |
| `--worksheet-id WORKSHEET_ID` | Select a worksheet or provide a worksheet ID You can use the "retrieve_options" tool using these parameters to get th... |
| `--column COLUMN` | Insert new column to the RIGHT of this column. Leave blank to insert at start of sheet |

### `google-sheets-update-rows`

Update multiple rows in a spreadsheet defined by a range

| Flag | Description |
|---|---|
| `--drive DRIVE` | The drive containing the worksheet to update. If you are connected with any [Google Shared Drives](https:// support.g... |
| `--sheet-id SHEET_ID` | The spreadsheet containing the worksheet to update You can use the "retrieve_options" tool using these parameters to ... |
| `--sheet-name SHEET_NAME` | Your sheet name You can use the "retrieve_options" tool using these parameters to get the values. key: google_sheets-... |
| `--range RANGE` | The A1 notation of the values to retrieve. E.g., `A1:E5` |
| `--rows ROWS` | Provide an array of arrays. Each nested array should represent a row, with each element of the nested array represent... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'sheets'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@sheets` to bypass the 1h tool-list cache.
