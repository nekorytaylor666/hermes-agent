
# SendGrid (via Higgsfield MCP proxy)

Transactional emails, contacts, lists, templates. Exposes 20 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @sendgrid <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @sendgrid --list                    # all 20 tools
./bin/mcp2cli @sendgrid sendgrid-validate-email --help   # inspect one
./bin/mcp2cli @sendgrid sendgrid-validate-email --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @sendgrid --pretty <cmd>` — `--pretty` goes AFTER `@sendgrid`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @sendgrid --head N <cmd>` — `--head N` goes AFTER `@sendgrid`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 20 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `sendgrid-validate-email`

Validates an email address. This action requires a Sendgrid's Pro or

| Flag | Description |
|---|---|
| `--email EMAIL` | The email that you want to validate |
| `--source SOURCE` | An optional indicator of the email address's source. You may include this if you are capturing email addresses from m... |

### `sendgrid-send-email-single-recipient`

This action sends a personalized e-mail to the specified recipient

| Flag | Description |
|---|---|
| `--from-email FROM_EMAIL` | The 'From' email address used to deliver the message. This address should be a verified sender in your Twilio SendGri... |
| `--from-name FROM_NAME` | A name or title associated with the sending email address |
| `--to-email TO_EMAIL` | The intended recipient's email address |
| `--to-name TO_NAME` | The intended recipient's name |
| `--cc CC` | An array of recipients who will receive a copy of your email. Each object in this array must contain the recipient's ... |
| `--bcc BCC` | An array of recipients who will receive a blind copy of your email. Each object in this array must contain the recipi... |
| `--personalization-headers PERSONALIZATION_HEADERS` | An object containing key/value pairs allowing you to specify handling instructions for your email. You may not overwr... |
| `--substitutions SUBSTITUTIONS` | Substitutions allow you to insert data without using Dynamic Transactional Templates. This field should not be used i... |
| `--dynamic-template-data DYNAMIC_TEMPLATE_DATA` | Dynamic template data is available using Handlebars syntax in Dynamic Transactional Templates. This field should be u... |
| `--template-id TEMPLATE_ID` | An email template ID. A template that contains a subject and content — either text or html — will override any subjec... |
| `--reply-to-email REPLY_TO_EMAIL` | The email address where any replies or bounces will be returned |
| `--reply-to-name REPLY_TO_NAME` | A name or title associated with the `replyToEmail` address |
| `--subject SUBJECT` | The global or `message level` subject of your email |
| `--content CONTENT` | Content of the email in `text/html` |
| `--headers HEADERS` | An object containing key/value pairs of header names and the value to substitute for them. The key/value pairs must b... |
| `--categories CATEGORIES` | A string array of category names for this message. Each category name may not exceed 255 characters. Example: `["cate... |
| `--custom-args CUSTOM_ARGS` | Values that are specific to the entire send that will be carried along with the email and its activity data. Key/valu... |
| `--send-at SEND_AT` | An ISO 8601 formatted date-time (YYYY-MM-DDTHH:MM:SSZ) allowing you to specify when you want your email to be deliver... |
| `--asm ASM` | Advanced Suppression Manager. An object allowing you to specify how to handle unsubscribes (JSON object) |
| `--asm-group-id ASM_GROUP_ID` | Advanced Suppression Manager Group ID. The unsubscribe group to associate with this email. Will override the value se... |
| `--asm-groups-to-display ASM_GROUPS_TO_DISPLAY` | An array containing the unsubscribe groups that you would like to be displayed on the unsubscribe preferences page. W... |
| `--ip-pool-name IP_POOL_NAME` | The IP Pool that you would like to send this email from |
| `--mail-settings MAIL_SETTINGS` | A collection of different mail settings that you can use to specify how you would like this email to be handled (JSON... |
| `--tracking-settings TRACKING_SETTINGS` | Settings to determine how you would like to track the metrics of how your recipients interact with your email (JSON o... |
| `--number-of-attachments NUMBER_OF_ATTACHMENTS` | The number of attachments to be sent with the email. |

### `sendgrid-send-email-multiple-recipients`

This action sends a personalized e-mail to multiple specified

| Flag | Description |
|---|---|
| `--personalizations PERSONALIZATIONS` | An array of messages and their metadata. Each object within personalizations can be thought of as an envelope - it de... |
| `--to-emails TO_EMAILS` | The intended recipients' email addresses. Will be ignored if `personalizations` prop is used. (JSON array) |
| `--from-email FROM_EMAIL` | The 'From' email address used to deliver the message. This address should be a verified sender in your Twilio SendGri... |
| `--from-name FROM_NAME` | A name or title associated with the sending email address |
| `--dynamic-template-data DYNAMIC_TEMPLATE_DATA` | Dynamic template data is available using Handlebars syntax in Dynamic Transactional Templates. This field should be u... |
| `--template-id TEMPLATE_ID` | An email template ID. A template that contains a subject and content — either text or html — will override any subjec... |
| `--reply-to-email REPLY_TO_EMAIL` | The email address where any replies or bounces will be returned |
| `--reply-to-name REPLY_TO_NAME` | A name or title associated with the `replyToEmail` address |
| `--subject SUBJECT` | The global or `message level` subject of your email. This may be overridden by subject lines set -in personalizations. |
| `--content CONTENT` | Content of the email in `text/html` |
| `--headers HEADERS` | An object containing key/value pairs of header names and the value to substitute for them. The key/value pairs must b... |
| `--categories CATEGORIES` | A string array of category names for this message. Each category name may not exceed 255 characters. Example: `["cate... |
| `--custom-args CUSTOM_ARGS` | Values that are specific to the entire send that will be carried along with the email and its activity data. Key/valu... |
| `--send-at SEND_AT` | An ISO 8601 formatted date-time (YYYY-MM-DDTHH:MM:SSZ) allowing you to specify when you want your email to be deliver... |
| `--asm ASM` | Advanced Suppression Manager. An object allowing you to specify how to handle unsubscribes (JSON object) |
| `--asm-group-id ASM_GROUP_ID` | Advanced Suppression Manager Group ID. The unsubscribe group to associate with this email. Will override the value se... |
| `--asm-groups-to-display ASM_GROUPS_TO_DISPLAY` | An array containing the unsubscribe groups that you would like to be displayed on the unsubscribe preferences page. W... |
| `--ip-pool-name IP_POOL_NAME` | The IP Pool that you would like to send this email from |
| `--mail-settings MAIL_SETTINGS` | A collection of different mail settings that you can use to specify how you would like this email to be handled (JSON... |
| `--tracking-settings TRACKING_SETTINGS` | Settings to determine how you would like to track the metrics of how your recipients interact with your email (JSON o... |
| `--number-of-attachments NUMBER_OF_ATTACHMENTS` | The number of attachments to be sent with the email. |

### `sendgrid-search-contacts`

Searches contacts with a SGQL query. [See the docs

| Flag | Description |
|---|---|
| `--query QUERY` | The query field accepts valid SGQL for searching for a contact (.e.g `email LIKE 'hung.v%'` ). Only the first 50 cont... |
| `--query-field {alternate_emails,address_line_1,address_line_2,city,contact_id,country,email,email_domains,event_data,event_source,event_timestamp,event_type,first_name,last_name,postal_code,state_province_region,created_at,updated_at}` | Select the field to search |

### `sendgrid-remove-contact-from-list`

Allows you to remove contacts from a given list. [See the docs

| Flag | Description |
|---|---|
| `--list-id LIST_ID` | Select the list from which you'd like to remove the contact, or reference a list ID manually You can use the "retriev... |
| `--contact-ids CONTACT_IDS` | String array of contact ids to be removed from the list. You can use the "retrieve_options" tool using these paramete... |
| `--contact-emails CONTACT_EMAILS` | Array of email addresses to be removed from the list. You can use the "retrieve_options" tool using these parameters ... |

### `sendgrid-list-global-suppressions`

Allows you to get a list of all email address that are globally

| Flag | Description |
|---|---|
| `--start-time START_TIME` | Refers start of the time range in unix timestamp when an unsubscribe email was created (inclusive) |
| `--end-time END_TIME` | Refers end of the time range in unix timestamp when an unsubscribe email was created (inclusive) |
| `--number-of-supressions NUMBER_OF_SUPRESSIONS` | Indicates the max number of global suppressions to return |

### `sendgrid-list-blocks`

Allows you to list all email addresses that are currently on your

| Flag | Description |
|---|---|
| `--start-time START_TIME` | The start of the time range when a blocked email was created (inclusive). This is a unix timestamp. |
| `--end-time END_TIME` | The end of the time range when a blocked email was created (inclusive). This is a unix timestamp. |
| `--number-of-blocks NUMBER_OF_BLOCKS` | Indicates the max number of blocked emails to return |

### `sendgrid-get-contact-lists`

Allows you to get details of your contact lists. [See the docs

| Flag | Description |
|---|---|
| `--number-of-lists NUMBER_OF_LISTS` | The maximum number of contact lists to return |

### `sendgrid-get-all-bounces`

Allows you to get all of your bounces. [See the docs

| Flag | Description |
|---|---|
| `--start-time START_TIME` | Refers start of the time range in unix timestamp when a bounce was created (inclusive) |
| `--end-time END_TIME` | Refers end of the time range in unix timestamp when a bounce was created (inclusive) |

### `sendgrid-get-a-global-suppression`

Gets a global suppression. [See the docs

| Flag | Description |
|---|---|
| `--email EMAIL` | The email address of the global suppression you want to retrieve You can use the "retrieve_options" tool using these ... |

### `sendgrid-get-a-block`

Gets a specific block. [See the docs

| Flag | Description |
|---|---|
| `--email EMAIL` | The email address of the specific block You can use the "retrieve_options" tool using these parameters to get the val... |

### `sendgrid-delete-list`

Allows you to delete a specific contact list. [See the docs

| Flag | Description |
|---|---|
| `--list-id LIST_ID` | Select the list from which you'd like to remove the contact, or reference a list ID manually You can use the "retriev... |
| `--delete-contacts` | Indicates that all contacts on the list are also to be deleted |

### `sendgrid-delete-global-suppression`

Allows you to remove an email address from the global suppressions

| Flag | Description |
|---|---|
| `--email EMAIL` | The email address you want to remove from the global suppressions group You can use the "retrieve_options" tool using... |

### `sendgrid-delete-contacts`

Allows you to delete one or more contacts. [See the docs

| Flag | Description |
|---|---|
| `--delete-all-contacts` | This parameter allows you to delete all of your contacts. This can not be used with the `ids` parameter. |
| `--contact-ids CONTACT_IDS` | An array of contact IDs to delete You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--contact-emails CONTACT_EMAILS` | Array of email addresses to be deleted. You can use the "retrieve_options" tool using these parameters to get the val... |

### `sendgrid-delete-bounces`

Allows you to delete all emails on your bounces list. [See the docs

| Flag | Description |
|---|---|
| `--delete-all` | This parameter allows you to delete every email in your bounce list. This can not be used with the `emails` parameter. |
| `--emails EMAILS` | A string array of the specific blocked email addresses that you want to delete. This can not be used with the `delete... |

### `sendgrid-delete-blocks`

Allows you to delete all email addresses on your blocks list. [See

| Flag | Description |
|---|---|
| `--delete-all` | Indicates if you want to delete all blocked email addresses. This can not be used with the `emails` parameter. |
| `--emails EMAILS` | A string array of the specific blocked email addresses that you want to delete. This can not be used with the `delete... |

### `sendgrid-create-send`

Create a single send. [See the docs

| Flag | Description |
|---|---|
| `--name NAME` | The name of the Single Send. |
| `--category-ids CATEGORY_IDS` | The categories to associate with this Single Send. You can use the "retrieve_options" tool using these parameters to ... |
| `--send-at SEND_AT` | Set this property to an ISO 8601 formatted date-time (YYYY-MM-DDTHH:MM:SSZ) when you would like to send the Single Se... |
| `--all` | Set to `true` to send to All Contacts. If set to `false`, at least one `List Ids` or `Segment Ids` value must be prov... |
| `--subject SUBJECT` | The subject line of the Single Send. Do not include this field when using a `Design Id`. |
| `--html-content HTML_CONTENT` | The HTML content of the Single Send. Do not include this field when using a `Design Id`. |
| `--plain-content PLAIN_CONTENT` | The plain text content of the Single Send. Do not include this field when using a `Design Id`. |
| `--generate-plain-content` | If set to `true`, `Plain Content` is always generated from `HTML Content`. If set to false, `Plain Content` is not al... |
| `--design-id DESIGN_ID` | A design id can be used in place of `HTML Content`, `Plain Content`, and/or `Subject`. You can use the "retrieve_opti... |
| `--editor {design,code}` | The editor is used to modify the Single Send's design in the Marketing Campaigns App. |
| `--suppression-group-id SUPPRESSION_GROUP_ID` | Advanced Suppression Manager Group ID. The unsubscribe group to associate with this email. Will override the value se... |
| `--custom-unsubscribe-url CUSTOM_UNSUBSCRIBE_URL` | The URL allowing recipients to unsubscribe — you must provide this or the `Suppression Group Id`. |
| `--sender-id SENDER_ID` | The ID of the verified Sender. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--ip-pool IP_POOL` | The name of the IP Pool from which the Single Send emails are sent. |

### `sendgrid-create-contact-list`

Allows you to create a new contact list. [See the docs

| Flag | Description |
|---|---|
| `--name NAME` | Your name for your list. maxLength: 100 |

### `sendgrid-add-or-update-contact`

Adds or updates a contact. [See the docs

| Flag | Description |
|---|---|
| `--list-ids LIST_IDS` | A string array of List IDs where the contact will be added. Example: `["49eeb4d9-0065-4f6a-a7d8- dfd039b77e0f","89876... |
| `--email EMAIL` | The contact's email address You can use the "retrieve_options" tool using these parameters to get the values. key: se... |
| `--first-name FIRST_NAME` | The contact's personal name |
| `--last-name LAST_NAME` | The contact's family name |
| `--address-line1 ADDRESS_LINE` | 1 The first line of the address |
| `--address-line2 ADDRESS_LINE` | 2 An optional second line for the address |
| `--alternate-emails ALTERNATE_EMAILS` | Additional emails associated with the contact (JSON array) |
| `--city CITY` | The contact's city. |
| `--country COUNTRY` | The contact's country. Can be a full name or an abbreviation |
| `--postal-code POSTAL_CODE` | The contact's ZIP code or other postal code |
| `--state-province-region STATE_PROVINCE_REGION` | The contact's state, province, or region |
| `--custom-fields CUSTOM_FIELDS` | Custom fields for the contact (JSON object) |

### `sendgrid-add-email-to-global-suppression`

Allows you to add one or more email addresses to the global

| Flag | Description |
|---|---|
| `--recipient-emails RECIPIENT_EMAILS` | An array of email addresses to be added to the global suppressions group. Example `["email1@example.com","email2@exam... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'sendgrid'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@sendgrid` to bypass the 1h tool-list cache.
