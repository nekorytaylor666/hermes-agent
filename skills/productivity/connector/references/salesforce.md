---
name: salesforce
description: Query, create, update, and delete Salesforce records (accounts, contacts, leads, opportunities, cases, campaigns, tasks) plus SOQL/SOSL and Chatter. Use for any Salesforce automation task. Triggers include "salesforce", "salesforce".
allowed-tools: Bash(salesforce *), Bash(./bin/mcp2cli *), Bash(mcp2cli *)
---

# Salesforce (via Higgsfield MCP proxy)

Query, create, update, and delete Salesforce records (accounts, contacts, leads, opportunities, cases, campaigns, tasks) plus SOQL/SOSL and Chatter. Exposes 61 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @salesforce <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @salesforce --list                    # all 61 tools
./bin/mcp2cli @salesforce salesforce-rest-api-get-current-user --help   # inspect one
./bin/mcp2cli @salesforce salesforce-rest-api-get-current-user --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @salesforce --pretty <cmd>` — `--pretty` goes AFTER `@salesforce`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @salesforce --head N <cmd>` — `--head N` goes AFTER `@salesforce`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 61 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `salesforce-rest-api-get-current-user`

_No flags._

### `salesforce-rest-api-upsert-record`

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The type of object to create a record of You can use the "retrieve_options" tool using these parameters to get the va... |

### `salesforce-rest-api-update-record`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of object to update a record of. You can use the "retrieve_options" tool using these parameters to get the v... |
| `--record-id RECORD_ID` | The record to update. You can use the "retrieve_options" tool using these parameters to get the values. key: salesfor... |
| `--fields-to-update FIELDS_TO_UPDATE` | Select the field(s) you want to update for this record. You can use the "retrieve_options" tool using these parameter... |

### `salesforce-rest-api-update-opportunity`

| Flag | Description |
|---|---|
| `--opportunity-id OPPORTUNITY_ID` | The Opportunity to update. You can use the "retrieve_options" tool using these parameters to get the values. key: sal... |
| `--close-date CLOSE_DATE` | Date when the opportunity is expected to close. |
| `--description DESCRIPTION` | Text description of the opportunity. Limit: 32,000 characters. |
| `--name NAME` | A name for this opportunity. Limit: 120 characters |
| `--stage-name {Prospecting,Qualification,Needs Analysis,Value Proposition,Id. Decision Makers,Perception Analysis,Proposal/Price Quote,Negotiation/Review,Closed Won,Closed Lost}` | Current stage of this record. This controls several other fields on an opportunity. |
| `--account-id ACCOUNT_ID` | ID of the account associated with this opportunity. You can use the "retrieve_options" tool using these parameters to... |
| `--campaign-id CAMPAIGN_ID` | ID of a related Campaign. You can use the "retrieve_options" tool using these parameters to get the values. key: sale... |
| `--owner-id OWNER_ID` | ID of the User who has been assigned to work this opportunity. You can use the "retrieve_options" tool using these pa... |
| `--pricebook2-id PRICEBOOK2_ID` | ID of a related Pricebook2 object. You can use the "retrieve_options" tool using these parameters to get the values.... |
| `--record-type-id RECORD_TYPE_ID` | ID of the record type assigned to this record. You can use the "retrieve_options" tool using these parameters to get... |
| `--amount AMOUNT` | Estimated total sale amount. For opportunities with products, the amount is the sum of the related products. |
| `--forecast-category-name {Omitted,Pipeline,Best Case,Commit,Closed}` | The name of the forecast category. |
| `--is-excluded-from-territory2-filter` | Used for Filter-Based Opportunity Territory Assignment. Indicates whether the opportunity is excluded (`true`) or inc... |
| `--lead-source {Web,Phone Inquiry,Partner Referral,Purchased List,Other}` | Source of this opportunity. |
| `--next-step NEXT_STEP` | Description of next task in closing opportunity. Limit: 255 characters. |
| `--probability PROBABILITY` | Percentage of estimated confidence in closing the opportunity. |
| `--total-opportunity-quantity TOTAL_OPPORTUNITY_QUANTITY` | Number of items included in this opportunity. |
| `--type {Existing Customer - Upgrade,Existing Customer - Replacement,Existing Customer - Downgrade,New Customer}` | Type of opportunity. |

### `salesforce-rest-api-update-note`

| Flag | Description |
|---|---|
| `--note-id NOTE_ID` | The ID of the note to update. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--body BODY` | Body of the note. Limited to 32 KB. |
| `--is-private` | If true, only the note owner or a user with the “Modify All Data” permission can view the note or query it via the API. |
| `--owner-id OWNER_ID` | ID of the user who owns the note. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--parent-id PARENT_ID` | ID of the object associated with the note. [See the do cumentation](https://developer.salesforce.com/docs/atl as.en-u... |
| `--title TITLE` | Title of the note. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-update-email-template`

| Flag | Description |
|---|---|
| `--record-id RECORD_ID` | The email template to update. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--fields-to-update FIELDS_TO_UPDATE` | Select the field(s) you want to update for this record. You can use the "retrieve_options" tool using these parameter... |

### `salesforce-rest-api-update-content-note`

| Flag | Description |
|---|---|
| `--content-note-id CONTENT_NOTE_ID` | The ID of the content note to update. You can use the "retrieve_options" tool using these parameters to get the value... |
| `--owner-id OWNER_ID` | ID of the user who owns the note. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--title TITLE` | Title of the note. |
| `--content CONTENT` | The content or body of the note, which can include properly formatted HTML or plain text. |
| `--is-read-only` | Indicates whether the note is read only. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-update-contact`

| Flag | Description |
|---|---|
| `--contact-id CONTACT_ID` | The Contact to update. You can use the "retrieve_options" tool using these parameters to get the values. key: salesfo... |
| `--description DESCRIPTION` | A description of the contact, up to 32 KB. |
| `--email EMAIL` | The contact's email address. |
| `--first-name FIRST_NAME` | The contact's first name, up to 40 characters. |
| `--last-name LAST_NAME` | The contact's last name, up to 80 characters. |
| `--phone PHONE` | Phone number for the contact. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-update-account`

| Flag | Description |
|---|---|
| `--account-id ACCOUNT_ID` | The Account to update. You can use the "retrieve_options" tool using these parameters to get the values. key: salesfo... |
| `--account-number ACCOUNT_NUMBER` | Account number assigned to this account (not the unique, system-generated ID assigned during creation). Max 40 charac... |
| `--description DESCRIPTION` | Text description of the account. Limited to 32,000 KB. |
| `--phone PHONE` | Phone number for this account. Max 40 characters. |
| `--website WEBSITE` | The website of this account. Max 255 characters. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-user`

| Flag | Description |
|---|---|
| `--alias ALIAS` | The user's alias (max 8 characters). |
| `--community-nickname COMMUNITY_NICKNAME` | Name used to identify this user in the Experience Cloud site. |
| `--digest-frequency {D,W,N}` | The send frequency of the user's Chatter personal email digest. |
| `--email EMAIL` | The user's email address. |
| `--email-encoding-key {UTF-8,ISO-8859-1,Shift_JIS,ISO-2022-JP,EUC-JP,ks_c_5601-1987,Big5,GB2312,Big5-HKSCS,x-SJIS_0213}` | The email encoding for the user. |
| `--language-locale-key {en_US,de,es,fr,it,ja,sv,ko,zh_TW,zh_CN,pt_BR,nl_NL,da,th,fi,ru,es_MX,no}` | The user's language. |
| `--last-name LAST_NAME` | The user's last name. |
| `--locale-sid-key {...many locales...}` | The locale affects formatting and parsing of values, especially numeric values, in the user interface. |
| `--profile-id PROFILE_ID` | ID of the user's Profile. Use this value to cache metadata based on profile. You can use the "retrieve_options" tool... |
| `--time-zone-sid-key {...many zones...}` | A User time zone affects the offset used when displaying or entering times in the user interface. |
| `--username USERNAME` | Contains the name that a user enters to log in to the API or the user interface. The value for this field must be in... |
| `--user-permissions-marketing-user` | Indicates whether the user is enabled to manage campaigns in the user interface (true) or not (false). |
| `--user-permissions-offline-user` | Indicates whether the user is enabled to use Offline Edition (true) or not (false). |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-task`

| Flag | Description |
|---|---|
| `--is-recurrence` | Indicates whether the task is scheduled to repeat itself (`true`) or only occurs once (`false`). |
| `--task-subtype {Task,Email,ListEmail,Cadence,Call,LinkedIn}` | The subtype of the task. |
| `--activity-date ACTIVITY_DATE` | Represents the due date of the task. |
| `--description DESCRIPTION` | A text description of the task. |
| `--priority {High,Normal,Low}` | Indicates the importance or urgency of a task, such as high or low. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-record`

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The type of object to create a record of You can use the "retrieve_options" tool using these parameters to get the va... |

### `salesforce-rest-api-create-opportunity`

| Flag | Description |
|---|---|
| `--contact-id CONTACT_ID` | ID of the contact associated with this opportunity, set as the primary contact. You can use the "retrieve_options" to... |
| `--close-date CLOSE_DATE` | Date when the opportunity is expected to close. |
| `--description DESCRIPTION` | Text description of the opportunity. Limit: 32,000 characters. |
| `--name NAME` | A name for this opportunity. Limit: 120 characters |
| `--stage-name {Prospecting,Qualification,Needs Analysis,Value Proposition,Id. Decision Makers,Perception Analysis,Proposal/Price Quote,Negotiation/Review,Closed Won,Closed Lost}` | Current stage of this record. This controls several other fields on an opportunity. |
| `--account-id ACCOUNT_ID` | ID of the account associated with this opportunity. You can use the "retrieve_options" tool using these parameters to... |
| `--campaign-id CAMPAIGN_ID` | ID of a related Campaign. You can use the "retrieve_options" tool using these parameters to get the values. key: sale... |
| `--owner-id OWNER_ID` | ID of the User who has been assigned to work this opportunity. You can use the "retrieve_options" tool using these pa... |
| `--pricebook2-id PRICEBOOK2_ID` | ID of a related Pricebook2 object. You can use the "retrieve_options" tool using these parameters to get the values.... |
| `--record-type-id RECORD_TYPE_ID` | ID of the record type assigned to this record. You can use the "retrieve_options" tool using these parameters to get... |
| `--amount AMOUNT` | Estimated total sale amount. For opportunities with products, the amount is the sum of the related products. |
| `--forecast-category-name {Omitted,Pipeline,Best Case,Commit,Closed}` | The name of the forecast category. |
| `--is-excluded-from-territory2-filter` | Used for Filter-Based Opportunity Territory Assignment. Indicates whether the opportunity is excluded (`true`) or inc... |
| `--lead-source {Web,Phone Inquiry,Partner Referral,Purchased List,Other}` | Source of this opportunity. |
| `--next-step NEXT_STEP` | Description of next task in closing opportunity. Limit: 255 characters. |
| `--probability PROBABILITY` | Percentage of estimated confidence in closing the opportunity. |
| `--total-opportunity-quantity TOTAL_OPPORTUNITY_QUANTITY` | Number of items included in this opportunity. |
| `--type {Existing Customer - Upgrade,Existing Customer - Replacement,Existing Customer - Downgrade,New Customer}` | Type of opportunity. |

### `salesforce-rest-api-create-note`

| Flag | Description |
|---|---|
| `--body BODY` | Body of the note. Limited to 32 KB. |
| `--is-private` | If true, only the note owner or a user with the “Modify All Data” permission can view the note or query it via the API. |
| `--owner-id OWNER_ID` | ID of the user who owns the note. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--parent-id PARENT_ID` | ID of the object associated with the note. [See the do cumentation](https://developer.salesforce.com/docs/atl as.en-u... |
| `--title TITLE` | Title of the note. |

### `salesforce-rest-api-create-lead`

| Flag | Description |
|---|---|
| `--is-converted` | Indicates whether the lead has been converted |
| `--company COMPANY` | The lead's company. |
| `--description DESCRIPTION` | The lead's description. |
| `--email EMAIL` | The lead's email address. |
| `--first-name FIRST_NAME` | The lead's first name. |
| `--last-name LAST_NAME` | The lead's last name. |
| `--phone PHONE` | The lead's phone number. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-event`

| Flag | Description |
|---|---|
| `--accepted-event-invitee-ids ACCEPTED_EVENT_INVITEE_IDS` | One or more Contact or Lead IDs who accepted this event. You can use the "retrieve_options" tool using these paramete... |
| `--activity-date ACTIVITY_DATE` | The date/time (`ActivityDateTime`) of the event, or only the date (`ActivityDate`) if it is an all-day event. |
| `--description DESCRIPTION` | A text description of the event. Limit: 32,000 characters. |
| `--duration-in-minutes DURATION_IN_MINUTES` | The event length in minutes. |
| `--end-date-time END_DATE_TIME` | The date/time when the event ends. |
| `--is-all-day-event` | Whether the event is an all-day event. |
| `--location LOCATION` | The location of the event. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-content-note`

| Flag | Description |
|---|---|
| `--owner-id OWNER_ID` | ID of the user who owns the note. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--title TITLE` | Title of the note. |
| `--content CONTENT` | The content or body of the note, which can include properly formatted HTML or plain text. |
| `--is-read-only` | Indicates whether the note is read only. |
| `--linked-entity-id LINKED_ENTITY_ID` | ID of the linked object. Can include Chatter users, groups, records (any that support Chatter feed tracking including... |
| `--share-type {V,C,I}` | The permission granted to the user of the shared file in a library. This is determined by the permission the user alr... |
| `--visibility {AllUsers,InternalUsers,SharedUsers}` | Specifies whether this file is available to all users, internal users, or shared users. |

### `salesforce-rest-api-create-contact`

| Flag | Description |
|---|---|
| `--description DESCRIPTION` | A description of the contact, up to 32 KB. |
| `--email EMAIL` | The contact's email address. |
| `--first-name FIRST_NAME` | The contact's first name, up to 40 characters. |
| `--last-name LAST_NAME` | The contact's last name, up to 80 characters. |
| `--phone PHONE` | Phone number for the contact. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-casecomment`

| Flag | Description |
|---|---|
| `--comment-body COMMENT_BODY` | Text of the CaseComment. Max size is 4,000 bytes. |
| `--parent-id PARENT_ID` | ID of the parent Case. You can use the "retrieve_options" tool using these parameters to get the values. key: salesfo... |
| `--is-published` | Indicates whether the CaseComment is visible to customers in the Self-Service portal. |

### `salesforce-rest-api-create-case`

| Flag | Description |
|---|---|
| `--description DESCRIPTION` | A text description of the case. Limit: 32 KB. |
| `--status {New,Working,Escalated,Closed}` | The status of the case. |
| `--supplied-email SUPPLIED_EMAIL` | The email address associated with the case. |
| `--supplied-name SUPPLIED_NAME` | The name of the case. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-campaign`

| Flag | Description |
|---|---|
| `--name NAME` | Name of the campaign. Max 80 characters. |
| `--description DESCRIPTION` | Description of the campaign. Limit: 32 KB. Only the first 255 characters display in reports. |
| `--status {Planned,In Progress,Completed,Aborted}` | Status of the campaign. Max 40 characters. |
| `--type {Conference,Webinar,Trade Show,Public Relations,Partners,Referral Program,Advertisement,Banner Ads,Direct Mail,Email,Telemarketing,Other}` | Type of campaign. Max 40 characters. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-create-attachment`

| Flag | Description |
|---|---|
| `--name NAME` | Name of the attached file. Max 255 characters. |
| `--file-path-or-content FILE_PATH_OR_CONTENT` | The file to attach. Provide either a file URL, a path to a file in the `/tmp` directory (for example, `/tmp/myFile.tx... |
| `--content-type CONTENT_TYPE` | The content type (MIME type) of the attachment. For example, `image/png`. |
| `--parent-id PARENT_ID` | ID of the parent object of the attachment. [See the do cumentation](https://developer.salesforce.com/docs/atl as.en-u... |
| `--description DESCRIPTION` | Description of the attachment. Max 500 characters. |
| `--is-private` | Whether this record is viewable only by the owner and administrators (true) or viewable by all otherwise- allowed use... |
| `--owner-id OWNER_ID` | ID of the user who owns the attachment. You can use the "retrieve_options" tool using these parameters to get the val... |

### `salesforce-rest-api-create-account`

| Flag | Description |
|---|---|
| `--name NAME` | Name of the account. Max 255 characters. |
| `--account-number ACCOUNT_NUMBER` | Account number assigned to this account (not the unique, system-generated ID assigned during creation). Max 40 charac... |
| `--description DESCRIPTION` | Text description of the account. Limited to 32,000 KB. |
| `--phone PHONE` | Phone number for this account. Max 40 characters. |
| `--website WEBSITE` | The website of this account. Max 255 characters. |
| `--use-advanced-props` | Set to true to see all available props for this object. |

### `salesforce-rest-api-update-crm-record`

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The Salesforce object API name (e.g. `Account`, `Contact`, `Opportunity`). |
| `--record-id RECORD_ID` | The ID of the record to update. Use **SOQL Query** to find the ID if you only have the record name. |
| `--properties PROPERTIES` | Field name → new value pairs. Only include fields you want to change. Example: `{"StageName": "Closed Won", "Amount":... |

### `salesforce-rest-api-text-search`

| Flag | Description |
|---|---|
| `--search-term SEARCH_TERM` | The text to search for across Salesforce records. Searches name fields and other indexed text fields. |
| `--object-types OBJECT_TYPES` | SObject types to search. Default: Account, Contact, Lead, Opportunity. Example: `["Account", "Contact", "Case"]`. (JS... |

### `salesforce-rest-api-soql-query`

| Flag | Description |
|---|---|
| `--query QUERY` | The SOQL query string to execute. Example: `SELECT Id, Name, Amount, StageName FROM Opportunity WHERE OwnerId = '005x... |

### `salesforce-rest-api-list-objects`

| Flag | Description |
|---|---|
| `--filter FILTER` | Optional keyword to filter object names and labels (case- insensitive). For example, `custom` returns only custom obj... |

### `salesforce-rest-api-get-user-info`

_No flags._

### `salesforce-rest-api-get-related-records`

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The SObject API name of the parent record (e.g. `Account`, `Contact`, `Opportunity`). |
| `--record-id RECORD_ID` | The ID of the parent record. |
| `--relationship-name RELATIONSHIP_NAME` | The API name of the relationship to traverse (e.g. `Contacts`, `Opportunities`, `Cases`, `Tasks`). This is the plural... |
| `--fields FIELDS` | Fields to return on the related records (e.g. `["Id", "Name", "Email"]`). If omitted, returns default fields. (JSON a... |

### `salesforce-rest-api-describe-object`

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The Salesforce object API name (e.g. `Account`, `Contact`, `Opportunity`, `CustomObject__c`). Use **List Objects** to... |
| `--fields-filter FIELDS_FILTER` | Optional keyword to filter field names and labels (case-insensitive). For example, `stage` returns fields like `Stage... |

### `salesforce-rest-api-delete-crm-record`

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The Salesforce object API name (e.g. `Account`, `Contact`, `Opportunity`). |
| `--record-id RECORD_ID` | The ID of the record to delete. Use **SOQL Query** to find the ID if you only have the record name. |

### `salesforce-rest-api-create-crm-record`

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The Salesforce object API name (e.g. `Account`, `Contact`, `Lead`, `Opportunity`, `Case`, `Task`, `Event`). Use **Lis... |
| `--properties PROPERTIES` | Field name → value pairs for the new record. Example for Contact: `{"FirstName": "Jane", "LastName": "Doe", "Email":... |

### `salesforce-rest-api-update-opportunities-batch`

| Flag | Description |
|---|---|
| `--csv-file-path CSV_FILE_PATH` | The path to the CSV file to process. Provide a path to a file in the `/tmp` directory (for example, `/tmp/data.csv`).... |

### `salesforce-rest-api-update-accounts-batch`

| Flag | Description |
|---|---|
| `--csv-file-path CSV_FILE_PATH` | The path to the CSV file to process. Provide a path to a file in the `/tmp` directory (for example, `/tmp/data.csv`).... |

### `salesforce-rest-api-create-opportunities-batch`

| Flag | Description |
|---|---|
| `--csv-file-path CSV_FILE_PATH` | The path to the CSV file to process. Provide a path to a file in the `/tmp` directory (for example, `/tmp/data.csv`).... |

### `salesforce-rest-api-create-accounts-batch`

| Flag | Description |
|---|---|
| `--csv-file-path CSV_FILE_PATH` | The path to the CSV file to process. Provide a path to a file in the `/tmp` directory (for example, `/tmp/data.csv`).... |

### `salesforce-rest-api-search-string`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of object to search for records You can use the "retrieve_options" tool using these parameters to get the va... |
| `--search-term SEARCH_TERM` | The term to search for |
| `--fields FIELDS` | Select the field(s) to obtain for the selected record(s) (or all records). You can use the "retrieve_options" tool us... |

### `salesforce-rest-api-send-email`

| Flag | Description |
|---|---|
| `--email-address EMAIL_ADDRESS` | The email address to send the email to |
| `--email-subject EMAIL_SUBJECT` | The subject of the email |
| `--email-body EMAIL_BODY` | The body of the email |
| `--log-email-on-send` | Indicates whether to log the email on the specified records' activity time lines |
| `--related-record-id RELATED_RECORD_ID` | The ID of a record that is not a person (for example, a case record). If `logEmailOnSend` is included, this is the ID... |
| `--add-threading-token-to-body` | Whether to create a unique token for the related record and add it to the email body. When the related record is a ca... |
| `--add-threading-token-to-subject` | The same as `Add Threading Token to Body`, but for the email subject. |
| `--sender-type {CurrentUser,DefaultWorkflowUser,OrgWideEmailAddress}` | Email address used as the email's **From** and **Reply-To** addresses. In scheduled flows, the only valid value is `O... |
| `--sender-address SENDER_ADDRESS` | If `Sender Type` is `OrgWideEmailAddress`, this is the organization-wide email address to be used as the sender. |

### `salesforce-rest-api-delete-note`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of note to delete You can use the "retrieve_options" tool using these parameters to get the values. key: sal... |
| `--record-id RECORD_ID` | The ID of the note or content note to delete You can use the "retrieve_options" tool using these parameters to get th... |

### `salesforce-rest-api-sosl-search`

| Flag | Description |
|---|---|
| `--search SEARCH` | A SOSL search query. [See the documentation](https://develo per.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_s... |

### `salesforce-rest-api-soql-search`

| Flag | Description |
|---|---|
| `--query QUERY` | A SOQL search query. [See the documentation](https://develope r.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_s... |

### `salesforce-rest-api-post-feed-to-chatter`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of object to select a record from. You can use the "retrieve_options" tool using these parameters to get the... |
| `--subject-id SUBJECT_ID` | The record that will parent the feed item. You can use the "retrieve_options" tool using these parameters to get the... |
| `--message-segments MESSAGE_SEGMENTS` | Each message segment can be a text string, which will be treated as a segment of `type: Text`, or a [message segment... |

### `salesforce-rest-api-list-object-fields`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of object to list fields of You can use the "retrieve_options" tool using these parameters to get the values... |
| `--custom-only` | Set to `true` to only list custom fields |

### `salesforce-rest-api-list-knowledge-articles`

_No flags._

### `salesforce-rest-api-list-email-templates`

_No flags._

### `salesforce-rest-api-list-email-messages`

| Flag | Description |
|---|---|
| `--case-id CASE_ID` | The ID of the case to retrieve email messages for You can use the "retrieve_options" tool using these parameters to g... |

### `salesforce-rest-api-list-case-comments`

| Flag | Description |
|---|---|
| `--case-id CASE_ID` | The ID of the record of the selected object type. You can use the "retrieve_options" tool using these parameters to g... |

### `salesforce-rest-api-insert-blob-data`

| Flag | Description |
|---|---|
| `--entiy-name ENTIY_NAME` | Name of the entity to insert as part of the form-data sent along the Salesforce API as a request with multipart/form-... |
| `--entity-document ENTITY_DOCUMENT` | Salesforce object entity to insert. |
| `--form-content-name FORM_CONTENT_NAME` | Name of the binary content to insert as part of the form-data sent along the Salesforce API as a request with multipa... |
| `--filename FILENAME` | Filename of the blob data to insert. |
| `--content-type CONTENT_TYPE` | Mime type of the content to insert. |
| `--attachment-binarycontent ATTACHMENT_BINARYCONTENT` | Binary content of the blob data to insert. |
| `--sobject-name SOBJECT_NAME` | Salesforce standard object type to insert. |

### `salesforce-rest-api-get-user`

| Flag | Description |
|---|---|
| `--user-id USER_ID` | The ID of the record of the selected object type. You can use the "retrieve_options" tool using these parameters to g... |

### `salesforce-rest-api-get-record-by-id`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of object to retrieve a record of You can use the "retrieve_options" tool using these parameters to get the... |
| `--record-id RECORD_ID` | The ID of the record to retrieve You can use the "retrieve_options" tool using these parameters to get the values. ke... |
| `--fields-to-obtain FIELDS_TO_OBTAIN` | Select the field(s) to obtain for the selected record(s) (or all records). You can use the "retrieve_options" tool us... |

### `salesforce-rest-api-get-knowledge-data-category-groups`

| Flag | Description |
|---|---|
| `--language LANGUAGE` | The language code. Defaults to `en-US`. |
| `--top-categories-only` | Return only top-level categories if `true`, entire tree if `false`. |

### `salesforce-rest-api-get-knowledge-articles`

| Flag | Description |
|---|---|
| `--language LANGUAGE` | The language code. Defaults to `en-US`. |
| `--q` | Q                 Performs an SOSL search. If this property is not set, an SOQL query runs. The characters `?` and `*... |
| `--channel {App,Pkb,Csp,Prm}` | Where articles are visible (App, Pkb, Csp, Prm). |
| `--categories CATEGORIES` | This should be a map in json format `{"group1": "category1", "group2": "category2", ...}`. It must be unique in each... |
| `--query-method {AT,BELOW,ABOVE,ABOVE_OR_BELOW}` | Only valid when categories are specified, defaults to `ABOVE_OR_BELOW`. |
| `--sort {LastPublishedDate,CreatedDate,Title,ViewScore}` | Field to sort results by. Defaults to `LastPublishedDate` for query and relevance for search |

### `salesforce-rest-api-get-case`

| Flag | Description |
|---|---|
| `--case-id CASE_ID` | The case ID to retrieve You can use the "retrieve_options" tool using these parameters to get the values. key: salesf... |

### `salesforce-rest-api-find-records`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of object to obtain records of. You can use the "retrieve_options" tool using these parameters to get the va... |
| `--fields-to-obtain FIELDS_TO_OBTAIN` | Select the field(s) to obtain for the selected record(s) (or all records). You can use the "retrieve_options" tool us... |
| `--record-ids RECORD_IDS` | The record(s) to retrieve. If not specified, all records will be retrieved. You can use the "retrieve_options" tool u... |

### `salesforce-rest-api-delete-record`

| Flag | Description |
|---|---|
| `--sobject-type SOBJECT_TYPE` | The type of object to delete a record of. You can use the "retrieve_options" tool using these parameters to get the v... |
| `--record-id RECORD_ID` | The record to delete. You can use the "retrieve_options" tool using these parameters to get the values. key: salesfor... |

### `salesforce-rest-api-delete-opportunity`

| Flag | Description |
|---|---|
| `--record-id RECORD_ID` | ID of the opportunity to delete. You can use the "retrieve_options" tool using these parameters to get the values. ke... |

### `salesforce-rest-api-convert-soap-xml-to-json`

| Flag | Description |
|---|---|
| `--xml XML` | The object received from Salesforce that will be converted. |
| `--extract-notification-only` | Whether to extract only the notification parts from the XML. Default: `true`. |
| `--fail-on-error` | Whether the action should fail if an error occurs when extracting notifications. Default: `false`. |

### `salesforce-rest-api-add-lead-to-campaign`

| Flag | Description |
|---|---|
| `--campaign-id CAMPAIGN_ID` | The Campaign to add a Lead to. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--lead-id LEAD_ID` | The Lead to add to the selected Campaign. You can use the "retrieve_options" tool using these parameters to get the v... |

### `salesforce-rest-api-add-contact-to-campaign`

| Flag | Description |
|---|---|
| `--campaign-id CAMPAIGN_ID` | The Campaign to add a Contact to. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--contact-id CONTACT_ID` | The Contact to add to the selected Campaign. You can use the "retrieve_options" tool using these parameters to get th... |

### `retrieve-options`

| Flag | Description |
|---|---|
| `--component-key COMPONENT_KEY` | componentKey |
| `--prop-name PROP_NAME` | propName |
| `--configured-props CONFIGURED_PROPS` | Previously configured property values for this component. Pass these so that dependent options can be resolved (e.g.... |

### `configure-component`

| Flag | Description |
|---|---|
| `--component-key COMPONENT_KEY` | componentKey |
| `--prop-name PROP_NAME` | propName |
| `--configured-props CONFIGURED_PROPS` | Previously configured property values for this component. Pass these so that dependent options can be resolved (e.g.... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'salesforce'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@salesforce` to bypass the 1h tool-list cache.
