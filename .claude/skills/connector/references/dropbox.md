
# Dropbox (via Higgsfield MCP proxy)

Upload, download, share, and manage Dropbox files and folders. Exposes 19 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @dropbox <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @dropbox --list                    # all 19 tools
./bin/mcp2cli @dropbox dropbox-upload-multiple-files --help   # inspect one
./bin/mcp2cli @dropbox dropbox-upload-multiple-files --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @dropbox --pretty <cmd>` — `--pretty` goes AFTER `@dropbox`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @dropbox --head N <cmd>` — `--head N` goes AFTER `@dropbox`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 19 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `dropbox-upload-multiple-files`

Uploads multiple file to a selected folder. [See the

| Flag | Description |
|---|---|
| `--path PATH` | The folder to upload to. Type the folder name to search for it in the user's Dropbox. You can use the "retrieve_optio... |
| `--files-paths FILES_PATHS` | Provide an array of either file URLs or paths to a files in the /tmp directory (for example, /tmp/myFile.pdf). (JSON ... |
| `--filenames FILENAMES` | An array of filenames for the new files. Please provide a name for each URL and/or Path. Make sure to include the fil... |
| `--autorename` | If there's a conflict, have Dropbox try to autorename the file to avoid the conflict. |
| `--mute` | Normally, users are made aware of any file modifications in their Dropbox account via notifications in the client sof... |
| `--strict-conflict` | Be more strict about how each WriteMode detects conflict. For example, always return a conflict error when mode = Wri... |
| `--mode {add,overwrite,update}` | Selects what to do if the file already exists. |

### `dropbox-upload-file`

Uploads a file to a selected folder. [See the

| Flag | Description |
|---|---|
| `--path PATH` | Type the folder name to search for it in the user's Dropbox. If not filled, it will be created in the root folder. Yo... |
| `--name NAME` | The name of your new file (make sure to include the file extension). |
| `--file-path FILE_PATH` | Provide either a file URL or a path to a file in the /tmp directory (for example, /tmp/myFile.pdf). |
| `--autorename` | If there's a conflict, have Dropbox try to autorename the folder to avoid the conflict. |
| `--mute` | Normally, users are made aware of any file modifications in their Dropbox account via notifications in the client sof... |
| `--strict-conflict` | Be more strict about how each WriteMode detects conflict. For example, always return a conflict error when mode = Wri... |
| `--mode {add,overwrite,update}` | Selects what to do if the file already exists. |

### `dropbox-search-files-folders`

Searches for files and folders by name. [See the

| Flag | Description |
|---|---|
| `--query QUERY` | The string to search for. May match across multiple fields based on the request arguments. |
| `--path PATH` | Type the folder name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these para... |
| `--order-by {relevance,last_modified_time}` | By default, results are sorted by relevance. |
| `--file-status {active,deleted}` | Restricts search to the given file status. |
| `--filename-only` | Restricts search to only match on filenames. |
| `--file-categories FILE_CATEGORIES` | Restricts search to only the file categories specified. Only supported for active file search. (JSON array) |
| `--file-extensions FILE_EXTENSIONS` | Restricts search to only the extensions specified. Only supported for active file search. (JSON array) |
| `--include-highlights` | Whether to include highlight span from file title. |
| `--limit LIMIT` | Specify a max amount of register to be fetched. Defaults to `100` if left blank. |

### `dropbox-restore-a-file`

Restores a previous file version. [See the

| Flag | Description |
|---|---|
| `--path PATH` | Type the file name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these parame... |
| `--rev REV` | The revision to restore. You can use the "retrieve_options" tool using these parameters to get the values. key: dropb... |

### `dropbox-rename-file-folder`

Renames a file or folder in the user's Dropbox [See the

| Flag | Description |
|---|---|
| `--path-from PATH_FROM` | Type the file or folder name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using th... |
| `--new-name NEW_NAME` | The file's new name (make sure to include the file extension). |
| `--autorename` | If there's a conflict, have Dropbox try to autorename the folder to avoid the conflict. |
| `--allow-ownership-transfer` | Allow moves by owner even if it would result in an ownership transfer for the content being moved. This does not appl... |

### `dropbox-move-file-folder`

Moves a file or folder to a different location in the user's Dropbox

| Flag | Description |
|---|---|
| `--path-from PATH_FROM` | Type the file or folder name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using th... |
| `--path-to PATH_TO` | Type the folder name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these para... |
| `--autorename` | If there's a conflict, have Dropbox try to autorename the folder to avoid the conflict. |
| `--allow-ownership-transfer` | Allow moves by owner even if it would result in an ownership transfer for the content being moved. This does not appl... |

### `dropbox-list-shared-links`

Retrieves a list of shared links for a given path. [See the

| Flag | Description |
|---|---|
| `--path PATH` | Type the file or folder name to search for it in the user's Dropbox You can use the "retrieve_options" tool using the... |

### `dropbox-list-file-revisions`

Retrieves a list of file revisions needed to recover previous

| Flag | Description |
|---|---|
| `--path PATH` | Type the file name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these parame... |
| `--mode {path,id}` | Determines the behavior of the API in listing the revisions for a given file path or id. In `path` (default) mode, al... |
| `--limit LIMIT` | The maximum number of revision entries returned. |

### `dropbox-list-file-folders-in-a-folder`

Retrieves a list of files or subfolders in a specified folder [See

| Flag | Description |
|---|---|
| `--path PATH` | Type the folder name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these para... |
| `--recursive` | If `true`, the list folder operation will be applied recursively to all subfolders and the response will contain cont... |
| `--include-deleted` | If `true`, the results will include files and folders that used to exist but were deleted. |
| `--include-has-explicit-shared-members` | If `true`, the results will include a flag for each file indicating whether or not that file has any explicit members. |
| `--include-mounted-folders` | If `true`, the results will include entries under mounted folders which includes app folder, shared folder and team f... |
| `--include-non-downloadable-files` | If `true`, include files that are not downloadable, i.e. Google Docs. |
| `--limit LIMIT` | Specify a max amount of register to be fetched. Defaults to `100` if left blank. |

### `dropbox-get-shared-link-metadata`

Retrieves the shared link metadata for a given shared link. [See the

| Flag | Description |
|---|---|
| `--shared-link-url SHARED_LINK_URL` | The URL of a shared link You can use the "retrieve_options" tool using these parameters to get the values. key: dropb... |
| `--link-password LINK_PASSWORD` | The password required to access the shared link |

### `dropbox-get-shared-link-file`

Get a file from a shared link. [See the

| Flag | Description |
|---|---|
| `--shared-link-url SHARED_LINK_URL` | The URL of a shared link You can use the "retrieve_options" tool using these parameters to get the values. key: dropb... |
| `--link-password LINK_PASSWORD` | The password required to access the shared link |

### `dropbox-download-file-to-tmp`

Download a specific file to the temporary directory. [See the

| Flag | Description |
|---|---|
| `--path PATH` | Type the file name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these parame... |
| `--name NAME` | The new name of the file to be saved, including its extension. e.g: `myFile.csv` |

### `dropbox-download-file-preview`

Download a file preview from Dropbox. [See the

| Flag | Description |
|---|---|
| `--path PATH` | Type the file name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these parame... |
| `--name NAME` | The new name of the file to be saved, including its extension. e.g: `myFile.pdf` |

### `dropbox-download-and-export`

Export a file from a user's Dropbox. If file is not exportable, it

| Flag | Description |
|---|---|
| `--path PATH` | Type the file name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using these parame... |
| `--name NAME` | The new name of the file to be saved, including its extension. e.g: `myFile.html`. |
| `--export-format EXPORT_FORMAT` | The format to export the file in. Required for exportable files. Only supports exporting files that cannot be downloa... |

### `dropbox-delete-file-folder`

Permanently removes a file/folder from the server. [See

| Flag | Description |
|---|---|
| `--path PATH` | Type the file or folder name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using th... |

### `dropbox-create-update-share-link`

Creates or updates a public share link to the file or folder (It

| Flag | Description |
|---|---|
| `--path PATH` | Type the file or folder name to search for it in the user's Dropbox. You can use the "retrieve_options" tool using th... |

### `dropbox-create-or-append-to-a-text-file`

Adds a new line to an existing text file, or creates a file if it

| Flag | Description |
|---|---|
| `--name NAME` | Your new file name |
| `--path PATH` | Type the folder name to search for it in the user's Dropbox. If not filled, it will be created in the root folder. Yo... |
| `--content CONTENT` | The content to be written |

### `dropbox-create-folder`

Create a Folder. [See the

| Flag | Description |
|---|---|
| `--name NAME` | Your new folder name. |
| `--path PATH` | Type the folder name to search for it in the user's Dropbox. If not filled, it will be created in the root folder. Yo... |
| `--autorename` | If there's a conflict, have Dropbox try to autorename the folder to avoid the conflict. |

### `dropbox-create-a-text-file`

Creates a brand new text file from plain text content you specify

| Flag | Description |
|---|---|
| `--name NAME` | Your new file name. Example: `textfile.txt` |
| `--path PATH` | Type the folder name to search for it in the user's Dropbox. If not filled, it will be created in the root folder. Yo... |
| `--content CONTENT` | The content of your new file |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'dropbox'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@dropbox` to bypass the 1h tool-list cache.
