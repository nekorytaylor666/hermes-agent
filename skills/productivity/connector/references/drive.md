
# Google Drive (via Higgsfield MCP proxy)

Upload, download, search, and manage Google Drive files. Exposes 38 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @drive <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @drive --list                    # all 38 tools
./bin/mcp2cli @drive google-drive-upload-file --help   # inspect one
./bin/mcp2cli @drive google-drive-upload-file --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @drive --pretty <cmd>` — `--pretty` goes AFTER `@drive`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @drive --head N <cmd>` — `--head N` goes AFTER `@drive`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 38 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `google-drive-upload-file`

Upload a file to Google Drive. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--parent-id PARENT_ID` | The folder you want to upload the file to. If not specified, the file will be placed directly in the drive's top-leve... |
| `--file-path FILE_PATH` | Provide either a file URL or a path to a file in the /tmp directory (for example, /tmp/myFile.pdf). |
| `--name NAME` | The name of the new file (e.g. `/myFile.csv`). By default, the name is the same as the source file's. |
| `--mime-type MIME_TYPE` | The file's MIME type (e.g., `image/jpeg`). Google Drive will attempt to automatically detect an appropriate value fro... |
| `--upload-type {media,resumable,multipart}` | The type of upload request to the /upload URI. Required if you are uploading data, but not if are creating a metadata... |
| `--file-id FILE_ID` | ID of the file to replace. Leave it empty to upload a new file. You can use the "retrieve_options" tool using these p... |
| `--metadata METADATA` | Additional metadata to supply in the upload. [See the documentation](https://developers.google.com/workspace /drive/a... |

### `google-drive-update-shared-drive`

Update an existing shared drive. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Select a [shared drive](https://support.google.com/a/u sers/answer/9310351) to update You can use the "retrieve_optio... |
| `--use-domain-admin-access` | Issue the request as a domain administrator |
| `--theme-id THEME_ID` | The theme from which the background image and color will be set. Cannot be set if `Color` or `Background Image Link` ... |
| `--background-image-link BACKGROUND_IMAGE_LINK` | A link to the new background image for the shared drive. Cannot be set if `Theme ID` is used (it already sets the bac... |
| `--color-rgb COLOR_RGB` | The new color of this shared drive as an RGB hex string. Cannot be set if `Theme ID` is used (it already sets the col... |
| `--restrictions RESTRICTIONS` | A set of restrictions that apply to this shared drive or items inside this shared drive. See `restrictions` in the [D... |

### `google-drive-update-reply`

Update a reply on a specific comment. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to obtain info for. You can select a file or use a file ID from a previous step. You can use the "retrieve_o... |
| `--comment-id COMMENT_ID` | The comment to get info for. You can select a comment or use a comment ID from a previous step. You can use the "retr... |
| `--reply-id REPLY_ID` | The reply to get info for. You can select a reply or use a reply ID from a previous step. You can use the "retrieve_o... |
| `--action {resolve,reopen}` | The action the reply performed to the parent comment. |
| `--content CONTENT` | The plain text content of the reply. |

### `google-drive-update-file`

Update a file's metadata and/or content. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to update You can use the "retrieve_options" tool using these parameters to get the values. key: google_driv... |
| `--file-path FILE_PATH` | The file content to upload. Provide either a file URL or a path to a file in the `/tmp` directory (for example, `/tmp... |
| `--name NAME` | The new name of the file |
| `--mime-type MIME_TYPE` | The file's MIME type (e.g., `image/jpeg`). The value cannot be changed unless a new revision is uploaded. You can use... |
| `--add-parents ADD_PARENTS` | A list of parent folder IDs to add You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--remove-parents REMOVE_PARENTS` | A list of parent folder IDs to remove You can use the "retrieve_options" tool using these parameters to get the value... |
| `--keep-revision-forever` | Whether to set the 'keepForever' field in the new head revision. This is only applicable to files with binary content... |
| `--ocr-language {und,ab,aa,af,ak,sq,am,ar,an,hy,as,av,ae,ay,az,bm,ba,eu,be,bn,bh,bi,nb,bs,br,bg,my,ca,km,ch,ce,ny,zh,cu,cv,kw,co,cr,hr,cs,da,dv,nl,dz,en,eo,et,ee,fo,fj,fi,fr,ff,gd,gl,lg,ka,de,el,gn,gu,ht,ha,he,hz,hi,ho,hu,is,io,ig,id,ia,ie,iu,ik,ga,it,ja,jv,kl,kn,kr,ks,kk,ki,rw,ky,kv,kg,ko,kj,ku,lo,la,lv,li,ln,lt,lu,lb,mk,mg,ms,ml,mt,gv,mi,mr,mh,mn,na,nv,nd,nr,ng,ne,se,no,nn,oc,oj,or,om,os,pi,pa,fa,pl,pt,ps,qu,ro,rm,rn,ru,sm,sg,sa,sc,sr,sn,ii,sd,si,sk,sl,so,st,es,su,sw,ss,sv,tl,ty,tg,ta,tt,te,th,bo,ti,to,ts,tn,tr,tk,tw,ug,uk,ur,uz,ve,vi,vo,wa,cy,fy,wo,xh,yi,yo,za,zu}` | A language hint for OCR processing during image import (ISO 639-1 code) |
| `--use-content-as-indexable-text` | Whether to use the uploaded content as indexable text |
| `--advanced ADVANCED` | Any additional parameters to pass in the request. [See the documentation](https://developers.google.com/drive /api/v3... |

### `google-drive-update-comment`

Update the content of a specific comment. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to obtain info for. You can select a file or use a file ID from a previous step. You can use the "retrieve_o... |
| `--comment-id COMMENT_ID` | The comment to get info for. You can select a comment or use a comment ID from a previous step. You can use the "retr... |
| `--content CONTENT` | The new content of the comment. |

### `google-drive-search-shared-drives`

Search for shared drives with query options. [See the

| Flag | Description |
|---|---|
| `--q Q` | The [shared drives](https://support.google.com/a/users /answer/9310351) search query. See [query terms](https://devel... |
| `--use-domain-admin-access` | Issue the request as a domain administrator |

### `google-drive-resolve-comment`

Mark a comment as resolved. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file containing the comment to resolve. You can use the "retrieve_options" tool using these parameters to get the... |
| `--comment-id COMMENT_ID` | The ID of the comment to resolve. You can use the "retrieve_options" tool using these parameters to get the values. k... |

### `google-drive-resolve-access-proposal`

Accept or deny a request for access to a file or folder in Google

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-or-folder-id FILE_OR_FOLDER_ID` | The file or folder in the drive You can use the "retrieve_options" tool using these parameters to get the values. key... |
| `--access-proposal-id ACCESS_PROPOSAL_ID` | The identifier of an access proposal (when a user requests access to a file/folder) You can use the "retrieve_options... |
| `--action {ACCEPT,DENY}` | The action to take on the AccessProposal |
| `--roles ROLES` | The roles to allow. Note: This field is required for the `ACCEPT` action. (JSON array) |
| `--send-notification` | Whether to send an email to the requester when the AccessProposal is denied or accepted |

### `google-drive-reply-to-comment`

Add a reply to an existing comment. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file containing the comment to reply to. You can use the "retrieve_options" tool using these parameters to get th... |
| `--comment-id COMMENT_ID` | The ID of the comment to reply to. You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--content CONTENT` | The text content of the reply to add |

### `google-drive-remove-file-sharing-permission`

Remove a [sharing

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--use-file-or-folder {File,Folder}` | Whether to use a file or a folder for this action |
| `--permission-id PERMISSION_ID` | The ID of the permission to remove You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `google-drive-move-file`

Move a file from one folder to another. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to move You can use the "retrieve_options" tool using these parameters to get the values. key: google_drive-... |
| `--folder-id FOLDER_ID` | The folder you want to move the file to You can use the "retrieve_options" tool using these parameters to get the val... |

### `google-drive-move-file-to-trash`

Move a file or folder to trash. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--file-id FILE_ID` | The file or folder to move to trash You can use the "retrieve_options" tool using these parameters to get the values.... |

### `google-drive-list-replies`

List replies to a specific comment. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to obtain info for. You can select a file or use a file ID from a previous step. You can use the "retrieve_o... |
| `--comment-id COMMENT_ID` | The comment to get info for. You can select a comment or use a comment ID from a previous step. You can use the "retr... |
| `--include-deleted` | Whether to include deleted replies. |

### `google-drive-list-files`

List files from a specific folder. [See the

| Flag | Description |
|---|---|
| `--include-items-from-all-drives` | If `true`, include items from all drives. If `false`, include items from the drive specified in the `drive` prop. |
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--folder-id FOLDER_ID` | The ID of the parent folder which contains the file. If not specified, it will list files from the drive's top-level ... |
| `--fields FIELDS` | The fields you want included in the response [(see the documentation for available fields)](https://developer s.googl... |
| `--filter-text FILTER_TEXT` | Filter by file name that contains a specific text |
| `--trashed` | If `true`, list **only** trashed files. If `false`, list **only** non-trashed files. Keep it empty to include both. |

### `google-drive-list-comments`

List all comments on a file. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--file-id FILE_ID` | The file to list comments for. You can use the "retrieve_options" tool using these parameters to get the values. key:... |

### `google-drive-list-access-proposals`

List access proposals for a file or folder. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-or-folder-id FILE_OR_FOLDER_ID` | The file or folder in the drive You can use the "retrieve_options" tool using these parameters to get the values. key... |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `google-drive-get-shared-drive`

Get metadata for one or all shared drives. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Select a [Shared Drive](https://support.google.com/a/u sers/answer/9310351) or leave blank to retrieve all available ... |
| `--use-domain-admin-access` | Issue the request as a domain administrator |

### `google-drive-get-reply`

Get reply by ID on a specific comment. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to obtain info for. You can select a file or use a file ID from a previous step. You can use the "retrieve_o... |
| `--comment-id COMMENT_ID` | The comment to get info for. You can select a comment or use a comment ID from a previous step. You can use the "retr... |
| `--reply-id REPLY_ID` | The reply to get info for. You can select a reply or use a reply ID from a previous step. You can use the "retrieve_o... |

### `google-drive-get-folder-id-for-path`

Retrieve a folderId for a path. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--path PATH` | The path to the folder (e.g., `myFolder/mySubFolder1/mySubFolder2`) |

### `google-drive-get-file-by-id`

Get info on a specific file. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--file-id FILE_ID` | The file to obtain info for. You can select a file or use a file ID from a previous step. You can use the "retrieve_o... |
| `--fields FIELDS` | Customize the fields to obtain for the file. [See the doc umentation](https://developers.google.com/drive/api/refer e... |

### `google-drive-get-current-user`

Retrieve Google Drive account metadata for the authenticated user via

_No flags._

### `google-drive-get-comment`

Get comment by ID on a specific file. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to obtain info for. You can select a file or use a file ID from a previous step. You can use the "retrieve_o... |
| `--comment-id COMMENT_ID` | The comment to get info for. You can select a comment or use a comment ID from a previous step. You can use the "retr... |
| `--include-deleted` | Whether to include deleted comments. |

### `google-drive-find-spreadsheets`

Search for a specific spreadsheet by name. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--folder-id FOLDER_ID` | The ID of the parent folder which contains the file. If not specified, it will list files from the drive's top-level ... |
| `--name-search-term NAME_SEARCH_TERM` | Search for a file by name (equivalent to the query `name contains [value]`). |
| `--search-query SEARCH_QUERY` | Search for a file with a query. [See the documentation ](https://developers.google.com/drive/api/guides/ref- search-t... |

### `google-drive-find-forms`

List Google Form documents or search for a Form by name. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--folder-id FOLDER_ID` | The ID of the parent folder which contains the file. If not specified, it will list files from the drive's top-level ... |
| `--name-search-term NAME_SEARCH_TERM` | Search for a file by name (equivalent to the query `name contains [value]`). |
| `--search-query SEARCH_QUERY` | Search for a file with a query. [See the documentation ](https://developers.google.com/drive/api/guides/ref- search-t... |

### `google-drive-find-folder`

Search for a specific folder by name. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--name-search-term NAME_SEARCH_TERM` | The name of the folder to search for |
| `--include-trashed` | If set to true, returns all matches including items currently in the trash. Defaults to `false`. |

### `google-drive-find-file`

Search for a specific file by name. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--name-search-term NAME_SEARCH_TERM` | Search for a file by name (equivalent to the query `name contains [value]`). |
| `--search-query SEARCH_QUERY` | Search for a file with a query. [See the documentation ](https://developers.google.com/drive/api/guides/ref- search-t... |

### `google-drive-download-file`

Download a file. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to download You can use the "retrieve_options" tool using these parameters to get the values. key: google_dr... |
| `--file-path FILE_PATH` | The destination file name or path [in the `/tmp` direc tory](https://pipedream.com/docs/workflows/steps/code/ nodejs/... |
| `--mime-type MIME_TYPE` | The format to which to convert the downloaded file if it is a [Google Workspace document](https://developers .google.... |
| `--get-buffer-response` | Whether to return the file content as a buffer instead of writing to a file path |

### `google-drive-delete-shared-drive`

Delete a shared drive without any content. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Select a [shared drive](https://support.google.com/a/users/answer/9310351) to delete. You can use the "retrieve_optio... |

### `google-drive-delete-reply`

Delete a reply on a specific comment. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file to obtain info for. You can select a file or use a file ID from a previous step. You can use the "retrieve_o... |
| `--comment-id COMMENT_ID` | The comment to get info for. You can select a comment or use a comment ID from a previous step. You can use the "retr... |
| `--reply-id REPLY_ID` | The reply to get info for. You can select a reply or use a reply ID from a previous step. You can use the "retrieve_o... |

### `google-drive-delete-file`

Permanently delete a file or folder without moving it to the trash

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--file-id FILE_ID` | The file or folder to delete You can use the "retrieve_options" tool using these parameters to get the values. key: g... |

### `google-drive-delete-comment`

Delete a specific comment (Requires ownership or permissions). [See

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--file-id FILE_ID` | The file containing the comment to delete. You can use the "retrieve_options" tool using these parameters to get the ... |
| `--comment-id COMMENT_ID` | The ID of the comment to delete. You can use the "retrieve_options" tool using these parameters to get the values. ke... |

### `google-drive-create-shared-drive`

Create a new shared drive. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the new shared drive |

### `google-drive-create-folder`

Create a new empty folder. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--parent-id PARENT_ID` | Select a folder in which to place the new folder. If not specified, the folder will be placed directly in the drive's... |
| `--name NAME` | The name of the new folder |
| `--create-if-unique` | If the folder already exists, **do not** create. This option defaults to `false` for backwards compatibility and to b... |

### `google-drive-create-file-from-text`

Create a new file from plain text. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--parent-id PARENT_ID` | The folder you want to add the file to. If not specified, the file will be placed directly in the drive's top-level f... |
| `--name NAME` | The name of the file you want to create (e.g., `myFile.txt`) |
| `--content CONTENT` | Enter text to create the file with. |
| `--mime-type {text/plain,text/markdown,text/html,application/rtf,text/csv}` | The [format](https://developers.google.com/drive/api/v 3/ref-export-formats) in which the text is presented |

### `google-drive-create-file-from-template`

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

### `google-drive-copy-file`

Create a copy of the specified file. [See the

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--file-id FILE_ID` | The file to copy You can use the "retrieve_options" tool using these parameters to get the values. key: google_drive-... |

### `google-drive-add-file-sharing-preference`

Add a [sharing

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](htt ps://support.google.com/a/users/answer/9310351) instead, selec... |
| `--use-file-or-folder {File,Folder}` | Whether to use a file or a folder for this action |
| `--type {user,group,domain,anyone}` | The type of the grantee. Sharing with a domain is only valid for G Suite users. |

### `google-drive-add-comment`

Add an unanchored comment to a Google Doc (general feedback, no text

| Flag | Description |
|---|---|
| `--drive DRIVE` | Defaults to `My Drive`. To select a [Shared Drive](https://support.google.com/a/users/answer/9310351) instead, select... |
| `--file-id FILE_ID` | The file to add a comment to. You can use the "retrieve_options" tool using these parameters to get the values. key: ... |
| `--content CONTENT` | The text content of the comment to add |
| `--anchor ANCHOR` | A region of the document represented as a JSON string. For details on defining anchor properties, refer to [Manage co... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'drive'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@drive` to bypass the 1h tool-list cache.
