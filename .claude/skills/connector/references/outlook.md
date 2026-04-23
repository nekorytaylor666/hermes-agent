
# Microsoft Outlook (via Higgsfield MCP proxy)

Outlook emails, drafts, contacts, calendar events. Exposes 19 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @outlook <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @outlook --list                    # all 19 tools
./bin/mcp2cli @outlook microsoft-outlook-get-current-user --help   # inspect one
./bin/mcp2cli @outlook microsoft-outlook-get-current-user --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @outlook --pretty <cmd>` — `--pretty` goes AFTER `@outlook`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @outlook --head N <cmd>` — `--head N` goes AFTER `@outlook`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 19 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `microsoft-outlook-get-current-user`

Returns the authenticated Microsoft user's ID, display name, email,

_No flags._

### `microsoft-outlook-update-contact`

Update an existing contact, [See the

| Flag | Description |
|---|---|
| `--contact CONTACT` | The contact to be updated You can use the "retrieve_options" tool using these parameters to get the values. key: micr... |
| `--given-name GIVEN_NAME` | Given name of the contact |
| `--surname SURNAME` | Surname of the contact |
| `--email-addresses EMAIL_ADDRESSES` | Email addresses (JSON array) |
| `--business-phones BUSINESS_PHONES` | Array of phone numbers (JSON array) |
| `--expand EXPAND` | Additional contact details, [See object definition](https://docs.microsoft.com/en- us/graph/api/resources/contact) (J... |

### `microsoft-outlook-send-email`

Send an email to one or multiple recipients, [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--recipients RECIPIENTS` | Array of email addresses (JSON array) |
| `--cc-recipients CC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--bcc-recipients BCC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--subject SUBJECT` | Subject of the email |
| `--content-type {text,html}` | Content type (default `text`) |
| `--content CONTENT` | Content of the email in text or html format |
| `--files FILES` | Provide either an array of file URLs or an array of paths to a files in the /tmp directory (for example, /tmp/myFile.... |
| `--expand EXPAND` | Additional email details, [See object definition](https://docs.microsoft.com/en- us/graph/api/resources/message) (JSO... |

### `microsoft-outlook-reply-to-email`

Reply to an email in Microsoft Outlook. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--message-id MESSAGE_ID` | The identifier of the message to reply to You can use the "retrieve_options" tool using these parameters to get the v... |
| `--recipients RECIPIENTS` | Array of email addresses (JSON array) |
| `--cc-recipients CC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--bcc-recipients BCC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--subject SUBJECT` | Subject of the email |
| `--comment COMMENT` | Content of the reply in text format |
| `--files FILES` | Provide either an array of file URLs or an array of paths to a files in the /tmp directory (for example, /tmp/myFile.... |
| `--expand EXPAND` | Additional email details, [See object definition](https://docs.microsoft.com/en- us/graph/api/resources/message) (JSO... |

### `microsoft-outlook-remove-label-from-email`

Removes a label/category from an email in Microsoft Outlook. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--message-id MESSAGE_ID` | The identifier of the message to update You can use the "retrieve_options" tool using these parameters to get the val... |
| `--label LABEL` | The name of the label/category to remove You can use the "retrieve_options" tool using these parameters to get the va... |

### `microsoft-outlook-move-email-to-folder`

Moves an email to the specified folder in Microsoft Outlook. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--message-id MESSAGE_ID` | The identifier of the message to update You can use the "retrieve_options" tool using these parameters to get the val... |
| `--folder-id FOLDER_ID` | The identifier of the folder to move the selected message to You can use the "retrieve_options" tool using these para... |

### `microsoft-outlook-list-labels`

Get all the labels/categories that have been defined for a user. [See

_No flags._

### `microsoft-outlook-list-important-mail`

Get the most important mail from the user's Inbox. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--max-results MAX_RESULTS` | The maximum number of messages to return. |

### `microsoft-outlook-list-folders`

Retrieves a list of all folders in Microsoft Outlook. [See the

| Flag | Description |
|---|---|
| `--max-results MAX_RESULTS` | The maximum number of results to return |
| `--include-subfolders` | If `true`, the list of folders will include subfolders |
| `--include-hidden-folders` | If `true`, the list of folders will include hidden folders |

### `microsoft-outlook-list-contacts`

Get a contact collection from the default contacts folder, [See the

| Flag | Description |
|---|---|
| `--filter-address FILTER_ADDRESS` | If this is given, only contacts with the given address will be retrieved. |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `microsoft-outlook-find-shared-folder-email`

Search for an email in a shared folder in Microsoft Outlook. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The ID of the user to get messages for You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--shared-folder-id SHARED_FOLDER_ID` | The ID of the shared folder to get messages for You can use the "retrieve_options" tool using these parameters to get... |
| `--search SEARCH` | Search for an email in Microsoft Outlook. Can search for specific message properties such as `"to:example@example.com... |
| `--filter FILTER` | Filters results. For example, `contains(subject, 'meet for lunch?')` will include messages whose subject contains ‘me... |
| `--order-by ORDER_BY` | Order results by a property. For example, `receivedDateTime desc` will order messages by the received date in descend... |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `microsoft-outlook-find-email`

Search for an email in Microsoft Outlook. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--search SEARCH` | Search for an email in Microsoft Outlook. Can search for specific message properties such as `"to:example@example.com... |
| `--filter FILTER` | Filters results. For example, `contains(subject, 'meet for lunch?')` will include messages whose subject contains ‘me... |
| `--order-by ORDER_BY` | Order results by a property. For example, `receivedDateTime desc` will order messages by the received date in descend... |
| `--max-results MAX_RESULTS` | The maximum number of results to return |
| `--include-attachments` | If true, returns additional info for message attachments. |

### `microsoft-outlook-find-contacts`

Finds contacts with the given search string. [See the

| Flag | Description |
|---|---|
| `--search-string SEARCH_STRING` | Provide email address, given name, surname or display name (case sensitive) |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `microsoft-outlook-download-attachment`

Downloads an attachment to the /tmp directory. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--message-id MESSAGE_ID` | The identifier of the message containing the attachment to download You can use the "retrieve_options" tool using the... |
| `--attachment-id ATTACHMENT_ID` | The identifier of the attachment to download You can use the "retrieve_options" tool using these parameters to get th... |
| `--filename FILENAME` | The filename to save the attachment as in the /tmp directory |
| `--convert-to-pdf` | Whether to convert the attachment to a PDF file. Supports converting image, text, HTML, and DOCX files. |

### `microsoft-outlook-create-draft-reply`

Create a draft reply to an email. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--message-id MESSAGE_ID` | The identifier of the message to update You can use the "retrieve_options" tool using these parameters to get the val... |
| `--recipients RECIPIENTS` | Array of email addresses (JSON array) |
| `--cc-recipients CC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--bcc-recipients BCC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--subject SUBJECT` | Subject of the email |
| `--comment COMMENT` | Content of the reply in text format |
| `--files FILES` | Provide either an array of file URLs or an array of paths to a files in the /tmp directory (for example, /tmp/myFile.... |
| `--expand EXPAND` | Additional email details, [See object definition](https://docs.microsoft.com/en- us/graph/api/resources/message) (JSO... |

### `microsoft-outlook-create-draft-email`

Create a draft email, [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--recipients RECIPIENTS` | Array of email addresses (JSON array) |
| `--cc-recipients CC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--bcc-recipients BCC_RECIPIENTS` | Array of email addresses (JSON array) |
| `--subject SUBJECT` | Subject of the email |
| `--content-type {text,html}` | Content type (default `text`) |
| `--content CONTENT` | Content of the email in text or html format |
| `--files FILES` | Provide either an array of file URLs or an array of paths to a files in the /tmp directory (for example, /tmp/myFile.... |
| `--expand EXPAND` | Additional email details, [See object definition](https://docs.microsoft.com/en- us/graph/api/resources/message) (JSO... |

### `microsoft-outlook-create-contact`

Add a contact to the root Contacts folder, [See the

| Flag | Description |
|---|---|
| `--given-name GIVEN_NAME` | Given name of the contact |
| `--surname SURNAME` | Surname of the contact |
| `--email-addresses EMAIL_ADDRESSES` | Email addresses (JSON array) |
| `--business-phones BUSINESS_PHONES` | Array of phone numbers (JSON array) |
| `--expand EXPAND` | Additional contact details, [See object definition](https://docs.microsoft.com/en- us/graph/api/resources/contact) (J... |

### `microsoft-outlook-approve-workflow`

Suspend the workflow until approved by email. [See the

| Flag | Description |
|---|---|
| `--recipients RECIPIENTS` | Array of email addresses (JSON array) |
| `--subject SUBJECT` | Subject of the email |

### `microsoft-outlook-add-label-to-email`

Adds a label/category to an email in Microsoft Outlook. [See the

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The User ID of a shared mailbox. If not provided, defaults to the authenticated user's mailbox. You can use the "retr... |
| `--message-id MESSAGE_ID` | The identifier of the message to update You can use the "retrieve_options" tool using these parameters to get the val... |
| `--label LABEL` | The name of the label/category to add You can use the "retrieve_options" tool using these parameters to get the value... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'outlook'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@outlook` to bypass the 1h tool-list cache.
