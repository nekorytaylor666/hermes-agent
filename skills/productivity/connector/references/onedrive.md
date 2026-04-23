
# Microsoft OneDrive (via Higgsfield MCP proxy)

Microsoft OneDrive files, folders, sharing. Exposes 10 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @onedrive <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @onedrive --list                    # all 10 tools
./bin/mcp2cli @onedrive microsoft-onedrive-download-file --help   # inspect one
./bin/mcp2cli @onedrive microsoft-onedrive-download-file --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @onedrive --pretty <cmd>` — `--pretty` goes AFTER `@onedrive`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @onedrive --head N <cmd>` — `--head N` goes AFTER `@onedrive`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 10 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `microsoft-onedrive-download-file`

Download a file stored in OneDrive. [See the

| Flag | Description |
|---|---|
| `--file-id FILE_ID` | The file to download. You can either search for the file here, provide a custom *File ID*, or use the `File Path` pro... |
| `--file-path FILE_PATH` | The path to the file from the root folder, e.g., `Documents/My Subfolder/File 1.docx`. You can either provide this, o... |
| `--new-file-name NEW_FILE_NAME` | The file name to save the downloaded content as, under the `/tmp` folder. Make sure to include the file extension. |
| `--convert-to-format {pdf,html}` | The format to convert the file to. See the [Format Options](https://learn.microsoft.com/en- us/graph/api/driveitem-ge... |

### `microsoft-onedrive-create-link`

Create a sharing link for a DriveItem. [See the

| Flag | Description |
|---|---|
| `--drive-item-id DRIVE_ITEM_ID` | The ID of the DriveItem to create a sharing link for. **Search for the file/folder by name.** You can use the "retrie... |
| `--type {view,edit,embed}` | The type of sharing link to create. Either `view`, `edit`, or `embed`. |
| `--scope {anonymous,organization}` | The scope of link to create. Either `anonymous` or `organization`. |

### `microsoft-onedrive-list-my-drives`

Get the signed-in user's drives. Returns a list of all the drives the

_No flags._

### `microsoft-onedrive-get-file-by-id`

Retrieves a file by ID. [See the

| Flag | Description |
|---|---|
| `--file-id FILE_ID` | The file to retrieve. You can either search for the file here, provide a custom *File ID*. You can use the "retrieve_... |

### `microsoft-onedrive-upload-file`

Upload a file to OneDrive. [See the

| Flag | Description |
|---|---|
| `--upload-folder-id UPLOAD_FOLDER_ID` | The ID of the folder where you want to upload the file. Use the "Load More" button to load subfolders. You can use th... |
| `--file-path FILE_PATH` | The file to upload. Provide either a file URL or a path to a file in the `/tmp` directory (for example, `/tmp/myFile.... |
| `--filename FILENAME` | Name of the new uploaded file |

### `microsoft-onedrive-search-files`

Search for files and folders in Microsoft OneDrive. [See the

| Flag | Description |
|---|---|
| `--q Q` | The query text used to search for items. Values may be matched across several fields including filename, metadata, an... |
| `--exclude-folders` | Set to `true` to return only files in the response. Defaults to `false` |

### `microsoft-onedrive-list-files-in-folder`

Retrieves a list of the files and/or folders directly within a

| Flag | Description |
|---|---|
| `--folder-id FOLDER_ID` | The ID of the folder. Use the "Load More" button to load subfolders. You can use the "retrieve_options" tool using th... |
| `--exclude-folders` | Set to `true` to return only files in the response. Defaults to `false` |

### `microsoft-onedrive-get-excel-table`

Retrieve a table from an Excel spreadsheet stored in OneDrive [See

| Flag | Description |
|---|---|
| `--item-id ITEM_ID` | **Search for the file by name.** Only xlsx files are supported. You can use the "retrieve_options" tool using these p... |
| `--table-name TABLE_NAME` | This is set in the **Table Design** tab of the ribbon. You can use the "retrieve_options" tool using these parameters... |
| `--remove-headers` | By default, The headers are included as the first row. |
| `--number-of-rows NUMBER_OF_ROWS` | Leave blank to return all rows. |

### `microsoft-onedrive-find-file-by-name`

Search for a file or folder by name. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the file or folder to search for |
| `--exclude-folders` | Set to `true` to return only files in the response. Defaults to `false` |

### `microsoft-onedrive-create-folder`

Create a new folder in a drive. [See the

| Flag | Description |
|---|---|
| `--parent-folder-type {default,shared}` | Whether to nest the new folder within a folder in your drive (`default`) or a shared folder (`shared`) |
| `--folder-name FOLDER_NAME` | The name of the new folder to be created. e.g. `New Folder` |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'onedrive'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@onedrive` to bypass the 1h tool-list cache.
