
# HubSpot CRM (via Higgsfield MCP proxy)

HubSpot contacts, companies, deals, tickets, associations, properties. Exposes 84 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @hubspot <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @hubspot --list                    # all 84 tools
./bin/mcp2cli @hubspot hubspot-update-page --help   # inspect one
./bin/mcp2cli @hubspot hubspot-update-page --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @hubspot --pretty <cmd>` — `--pretty` goes AFTER `@hubspot`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @hubspot --head N <cmd>` — `--head N` goes AFTER `@hubspot`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 84 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `hubspot-update-page`

Update a page in Hubspot. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | The ID of the page to update. You can use the "retrieve_options" tool using these parameters to get the values. key: ... |
| `--page-name PAGE_NAME` | The name of the page. |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the page. |
| `--enable-layout-stylesheets` | Whether to enable layout stylesheets. |
| `--meta-description META_DESCRIPTION` | The meta description of the page. |
| `--attached-stylesheets ATTACHED_STYLESHEETS` | The stylesheets attached to the page. (JSON array) |
| `--password PASSWORD` | The password of the page. |
| `--publish-immediately` | Whether to publish the page immediately. |
| `--html-title HTML_TITLE` | The HTML title of the page. |
| `--translations TRANSLATIONS` | The translations of the page. (JSON object) |
| `--layout-sections LAYOUT_SECTIONS` | The layout sections of the page. (JSON object) |
| `--footer-html FOOTER_HTML` | The footer HTML of the page. |
| `--head-html HEAD_HTML` | The head HTML of the page. |
| `--template-path TEMPLATE_PATH` | The template path of the page. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--widget-containers WIDGET_CONTAINERS` | A data structure containing the data for all the modules inside the containers for this page (JSON object) |
| `--widgets WIDGETS` | A data structure containing the data for all the modules for this page (JSON object) |

### `hubspot-update-lead`

Update a lead in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | The identifier of the lead You can use the "retrieve_options" tool using these parameters to get the values. key: hub... |
| `--property-groups PROPERTY_GROUPS` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-update- lead, propName... |
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to update as a JSON object (JSON object) |

### `hubspot-update-landing-page`

Update a landing page in HubSpot. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | The ID of the page to update. You can use the "retrieve_options" tool using these parameters to get the values. key: ... |
| `--page-name PAGE_NAME` | The name of the page. |
| `--landing-folder-id LANDING_FOLDER_ID` | The ID of the folder to create the landing page in. You can use the "retrieve_options" tool using these parameters to... |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the page. |
| `--enable-layout-stylesheets` | Whether to enable layout stylesheets. |
| `--meta-description META_DESCRIPTION` | The meta description of the page. |
| `--attached-stylesheets ATTACHED_STYLESHEETS` | The stylesheets attached to the page. (JSON array) |
| `--password PASSWORD` | The password of the page. |
| `--publish-immediately` | Whether to publish the page immediately. |
| `--html-title HTML_TITLE` | The HTML title of the page. |
| `--translations TRANSLATIONS` | The translations of the page. (JSON object) |
| `--layout-sections LAYOUT_SECTIONS` | The layout sections of the page. (JSON object) |
| `--footer-html FOOTER_HTML` | The footer HTML of the page. |
| `--head-html HEAD_HTML` | The head HTML of the page. |
| `--template-path TEMPLATE_PATH` | The template path of the page. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--widget-containers WIDGET_CONTAINERS` | A data structure containing the data for all the modules inside the containers for this page (JSON object) |
| `--widgets WIDGETS` | A data structure containing the data for all the modules for this page (JSON object) |

### `hubspot-update-fields-on-the-form`

Update some of the form definition components. [See the

| Flag | Description |
|---|---|
| `--form-id FORM_ID` | The ID of the form to update. You can use the "retrieve_options" tool using these parameters to get the values. key: ... |
| `--name NAME` | The name of the form. |
| `--archived` | Whether the form is archived. |
| `--field-groups FIELD_GROUPS` | A list for objects of group type and fields. **Format: `[{ "groupType": "default_group", "richTextType": "text", "fie... |
| `--create-new-contact-for-new-email` | Whether to create a new contact when a form is submitted with an email address that doesn't match any in your existin... |
| `--editable` | Whether the form can be edited. |
| `--allow-link-to-reset-known-values` | Whether to add a reset link to the form. This removes any pre-populated content on the form and creates a new contact... |
| `--lifecycle-stages LIFECYCLE_STAGES` | A list of objects of lifecycle stages. **Format: `[{ "objectTypeId": "0-1", "value": "subscriber" }]`** [See the docu... |
| `--post-submit-action-type {thank_you,redirect_url}` | The action to take after submit. The default action is displaying a thank you message. |
| `--post-submit-action-value POST_SUBMIT_ACTION_VALUE` | The thank you text or the page to redirect to. |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the form. |
| `--pre-populate-known-values` | Whether contact fields should pre-populate with known information when a contact returns to your site. |
| `--cloneable` | Whether the form can be cloned. |
| `--notify-contact-owner` | Whether to send a notification email to the contact owner when a submission is received. |
| `--recaptcha-enabled` | Whether CAPTCHA (spam prevention) is enabled. |
| `--archivable` | Whether the form can be archived. |
| `--notify-recipients NOTIFY_RECIPIENTS` | Note - this needs to be a contact that already exists within HubSpot. You may need to add a Create or Update Contact ... |
| `--render-raw-html` | Whether the form will render as raw HTML as opposed to inside an iFrame. |
| `--css-class CSS_CLASS` | The CSS class of the form. |
| `--theme {default_style,canvas,linear,round,sharp,legacy}` | The theme used for styling the input fields. This will not apply if the form is added to a HubSpot CMS page`. |
| `--submit-button-text SUBMIT_BUTTON_TEXT` | The text displayed on the form submit button. |
| `--label-text-size LABEL_TEXT_SIZE` | The size of the label text. |
| `--legal-consent-text-color LEGAL_CONSENT_TEXT_COLOR` | The color of the legal consent text. |
| `--font-family FONT_FAMILY` | The font family of the form. |
| `--legal-consent-text-size LEGAL_CONSENT_TEXT_SIZE` | The size of the legal consent text. |
| `--background-width BACKGROUND_WIDTH` | The width of the background. |
| `--help-text-size HELP_TEXT_SIZE` | The size of the help text. |
| `--submit-font-color SUBMIT_FONT_COLOR` | The color of the submit font. |
| `--label-text-color LABEL_TEXT_COLOR` | The color of the label text. |
| `--submit-alignment {left,center,right}` | The alignment of the submit button. |
| `--submit-size SUBMIT_SIZE` | The size of the submit button. |
| `--help-text-color HELP_TEXT_COLOR` | The color of the help text. |
| `--submit-color SUBMIT_COLOR` | The color of the submit button. |
| `--legal-consent-options-type {none,legitimate_interest,explicit_consent_process,implicit_consent_process}` | The type of legal consent options. |
| `--legal-consent-options-object LEGAL_CONSENT_OPTIONS_OBJECT` | The object of legal consent options. **Format: `{"subscriptionTypeIds": [1,2,3], "lawfulBasis": "lead", "privacy": "s... |

### `hubspot-update-deal`

Update a deal in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | Hubspot's internal ID for the contact You can use the "retrieve_options" tool using these parameters to get the value... |
| `--property-groups PROPERTY_GROUPS` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-update- deal, propName... |
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to update as a JSON object (JSON object) |

### `hubspot-update-custom-object`

Update a custom object in Hubspot. [See the

| Flag | Description |
|---|---|
| `--custom-object-type CUSTOM_OBJECT_TYPE` | The type of custom object to create. This is the object's `fullyQualifiedName`, `objectTypeId`, or the short-hand cus... |
| `--object-id OBJECT_ID` | The ID of the custom object You can use the "retrieve_options" tool using these parameters to get the values. key: hu... |
| `--property-groups PROPERTY_GROUPS` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-update- custom-object,... |
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to update as a JSON object (JSON object) |

### `hubspot-update-crm-object`

Update an existing CRM record by ID. Pass only the properties you

| Flag | Description |
|---|---|
| `--object-type {contact,company,deal,ticket,call,quote,line_item,meeting,product,feedback_submission,email,note,task,lead}` | The type of CRM object to update. |
| `--object-id OBJECT_ID` | The ID of the record to update. Use **Search CRM Objects** to find record IDs. |
| `--properties PROPERTIES` | JSON object of property name-value pairs to update. Only include the properties you want to change. Example: `{"deals... |

### `hubspot-update-contact`

Update a contact in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | Hubspot's internal ID for the contact You can use the "retrieve_options" tool using these parameters to get the value... |
| `--property-groups PROPERTY_GROUPS` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-update- contact, propN... |
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to update as a JSON object (JSON object) |

### `hubspot-update-company`

Update a company in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | Hubspot's internal ID for the contact You can use the "retrieve_options" tool using these parameters to get the value... |
| `--property-groups PROPERTY_GROUPS` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-update- company, propN... |
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to update as a JSON object (JSON object) |

### `hubspot-update-blog-post`

Updates an existing blog post in HubSpot. [See the

| Flag | Description |
|---|---|
| `--blog-post-id BLOG_POST_ID` | The ID of the blog post You can use the "retrieve_options" tool using these parameters to get the values. key: hubspo... |
| `--name NAME` | The internal name of the blog post |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the blog post |
| `--slug SLUG` | The URL slug of the blog post |
| `--meta-description META_DESCRIPTION` | The meta description of the blog post |
| `--post-body POST_BODY` | The HTML content of the blog post |
| `--post-summary POST_SUMMARY` | A summary of the blog post |
| `--html-title HTML_TITLE` | The HTML title tag for the blog post |
| `--featured-image FEATURED_IMAGE` | The URL of the featured image for the blog post |
| `--featured-image-alt-text FEATURED_IMAGE_ALT_TEXT` | The alt text for the featured image |
| `--use-featured-image` | Whether to use a featured image for the blog post |
| `--author-name AUTHOR_NAME` | The name of the blog post author |
| `--blog-author-id BLOG_AUTHOR_ID` | The ID of the blog post author You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--content-group-id CONTENT_GROUP_ID` | The ID of the blog (content group) this post belongs to You can use the "retrieve_options" tool using these parameter... |
| `--publish-date PUBLISH_DATE` | The publish date for the blog post. Format: YYYY-MM- DDTHH:MM:SSZ |
| `--head-html HEAD_HTML` | Custom HTML to be added to the head section |
| `--footer-html FOOTER_HTML` | Custom HTML to be added to the footer section |
| `--enable-google-amp-output-override` | Override the AMP settings for this specific post |
| `--password PASSWORD` | Password required to view the blog post |

### `hubspot-update-blog-post-draft`

Updates the draft version of an existing blog post in HubSpot. [See

| Flag | Description |
|---|---|
| `--blog-post-id BLOG_POST_ID` | The ID of the blog post You can use the "retrieve_options" tool using these parameters to get the values. key: hubspo... |
| `--name NAME` | The internal name of the blog post |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the blog post |
| `--slug SLUG` | The URL slug of the blog post |
| `--meta-description META_DESCRIPTION` | The meta description of the blog post |
| `--post-body POST_BODY` | The HTML content of the blog post |
| `--post-summary POST_SUMMARY` | A summary of the blog post |
| `--html-title HTML_TITLE` | The HTML title tag for the blog post |
| `--featured-image FEATURED_IMAGE` | The URL of the featured image for the blog post |
| `--featured-image-alt-text FEATURED_IMAGE_ALT_TEXT` | The alt text for the featured image |
| `--use-featured-image` | Whether to use a featured image for the blog post |
| `--author-name AUTHOR_NAME` | The name of the blog post author |
| `--blog-author-id BLOG_AUTHOR_ID` | The ID of the blog post author You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--content-group-id CONTENT_GROUP_ID` | The ID of the blog (content group) this post belongs to You can use the "retrieve_options" tool using these parameter... |
| `--publish-date PUBLISH_DATE` | The publish date for the blog post. Format: YYYY-MM- DDTHH:MM:SSZ |
| `--head-html HEAD_HTML` | Custom HTML to be added to the head section |
| `--footer-html FOOTER_HTML` | Custom HTML to be added to the footer section |
| `--enable-google-amp-output-override` | Override the AMP settings for this specific post |
| `--password PASSWORD` | Password required to view the blog post |

### `hubspot-send-message`

Sends a message to a thread. [See the

| Flag | Description |
|---|---|
| `--inbox-id INBOX_ID` | The ID of an inbox You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-sen... |
| `--sender-actor-id SENDER_ACTOR_ID` | The ID of the sender actor You can use the "retrieve_options" tool using these parameters to get the values. key: hub... |
| `--channel-id CHANNEL_ID` | The ID of a channel You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-se... |
| `--thread-id THREAD_ID` | The ID of a thread You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-sen... |
| `--channel-account-id CHANNEL_ACCOUNT_ID` | The ID of a channel account You can use the "retrieve_options" tool using these parameters to get the values. key: hu... |
| `--recipient-type {HS_EMAIL_ADDRESS,HS_PHONE_NUMBER,CHANNEL_SPECIFIC_OPAQUE_ID}` | The type of identifier. HS_EMAIL_ADDRESS for email addresses; HS_PHONE_NUMBER for a phone number; CHANNEL_SPECIFIC_OP... |
| `--recipient-value RECIPIENT_VALUE` | The value of the recipient identifier. For HS_EMAIL_ADDRESS, this is the email address. For HS_PHONE_NUMBER, this is ... |
| `--text TEXT` | The text content of the message |
| `--file-id FILE_ID` | The ID of a file uploaded to HubSpot You can use the "retrieve_options" tool using these parameters to get the values... |
| `--subject SUBJECT` | The subject of the message |

### `hubspot-search-properties`

Search for property definitions (field names) on a CRM object type

| Flag | Description |
|---|---|
| `--object-type {contact,company,deal,ticket,call,quote,line_item,meeting,product,feedback_submission,email,note,task,lead}` | The CRM object type to search properties for (e.g. contact, company, deal, ticket). |
| `--keywords KEYWORDS` | Search keywords to find relevant properties by name or label. Use property name guesses, not natural language phrases... |
| `--include-read-only` | Set to `true` to include read-only / calculated properties (e.g. `createdate`, `hs_object_id`). Default: `false` — on... |

### `hubspot-search-crm`

Search companies, contacts, deals, feedback submissions, products,

| Flag | Description |
|---|---|
| `--object-type {contact,company,deal,ticket,line_item,product,feedback_submission,lead,custom_object}` | Type of CRM object to search for |
| `--exact-match` | Set to `true` to search for an exact match of the search value. If `false`, partial matches will be returned. Default... |
| `--create-if-not-found` | Set to `true` to create the Hubspot object if it doesn't exist |
| `--offset OFFSET` | The offset to start from. Used for pagination. |

### `hubspot-search-crm-objects`

Search HubSpot CRM records (contacts, companies, deals, tickets,

| Flag | Description |
|---|---|
| `--object-type {contact,company,deal,ticket,line_item,product,feedback_submission,lead}` | The CRM object type to search. |
| `--query QUERY` | Text to search across default searchable properties of the object type. Uses simple text matching (contains). Each ob... |
| `--filter-groups FILTER_GROUPS` | JSON array of filter groups for advanced filtering. Each group contains `filters` (AND logic within a group) and grou... |
| `--properties PROPERTIES` | Property names to include in results. If not specified, returns a default set of common properties for the object typ... |
| `--sorts SORTS` | JSON array of sort rules. Only one sort rule is supported. Example: `[{"propertyName": "createdate", "direction": "DE... |
| `--limit LIMIT` | Maximum number of results per page. Max: 200, default: 100. |
| `--after AFTER` | Paging cursor from a previous response for retrieving the next page of results. |

### `hubspot-schedule-blog-post`

Schedules a blog post to be published at a specified time. [See the

| Flag | Description |
|---|---|
| `--blog-post-id BLOG_POST_ID` | The ID of the blog post You can use the "retrieve_options" tool using these parameters to get the values. key: hubspo... |
| `--publish-date PUBLISH_DATE` | The date and time to publish the blog post. Format: YYYY-MM-DDTHH:MM:SSZ (e.g., 2024-03-20T14:30:00Z) |

### `hubspot-retrieve-workflows`

Retrieve a list of all workflows. [See the

_No flags._

### `hubspot-retrieve-workflow-emails`

Retrieve emails sent by a workflow by ID. [See the

| Flag | Description |
|---|---|
| `--workflow-id WORKFLOW_ID` | The ID of the workflow you wish to see metadata for. You can use the "retrieve_options" tool using these parameters t... |
| `--after AFTER` | The paging cursor token of the last successfully read resource will be returned as the `paging.next.after` JSON prope... |
| `--before BEFORE` | The paging cursor token of the last successfully read resource will be returned as the `paging.next.before` JSON prop... |
| `--limit LIMIT` | The maximum number of results to display per page. |

### `hubspot-retrieve-workflow-details`

Retrieve detailed information about a specific workflow. [See the

| Flag | Description |
|---|---|
| `--workflow-id WORKFLOW_ID` | The ID of the workflow you wish to see details for. You can use the "retrieve_options" tool using these parameters to... |

### `hubspot-retrieve-quotes`

Fetch one quote by ID or list quotes with CRM v3 pagination (`after`,

| Flag | Description |
|---|---|
| `--quote-id QUOTE_ID` | Optional. Pick a quote from the list, search by name/title, or enter a quote ID. Leave empty to list quotes (use **Af... |
| `--after AFTER` | Paging cursor from a previous list response (`paging.next.after`). Ignored when **Quote ID** is set. |
| `--limit LIMIT` | Max quotes per page when listing. Ignored when **Quote ID** is set. |
| `--properties PROPERTIES` | Optional. Select quote properties to include in the response, or leave empty for HubSpot's default set. Options load ... |

### `hubspot-retrieve-migrated-workflow-mappings`

Retrieve the IDs of v3 workflows that have been migrated to the v4

| Flag | Description |
|---|---|
| `--flow-ids FLOW_IDS` | A list of flowIds from the V4 API. You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--workflow WORKFLOW` | A list of workflowIds from the V3 API. You can use the "retrieve_options" tool using these parameters to get the valu... |

### `hubspot-push-blog-post-draft-live`

Pushes a blog post draft live, making it the published version. [See

| Flag | Description |
|---|---|
| `--blog-post-id BLOG_POST_ID` | The ID of the blog post You can use the "retrieve_options" tool using these parameters to get the values. key: hubspo... |

### `hubspot-list-threads`

Retrieves a list of threads. [See the

| Flag | Description |
|---|---|
| `--associated-contact-id ASSOCIATED_CONTACT_ID` | The ID of the contact to filter threads by You can use the "retrieve_options" tool using these parameters to get the ... |
| `--association {TICKET}` | You can specify an association type here of TICKET. If this is set the response will included a thread associations o... |
| `--archived` | Whether to return only results that have been archived |
| `--inbox-id INBOX_ID` | The ID of the conversations inbox you can optionally include to retrieve the associated messages for. This parameter ... |
| `--property PROPERTY` | A specific property to include in the thread response |
| `--after AFTER` | The paging cursor token of the last successfully read resource will be returned as the paging.next.after JSON propert... |
| `--limit LIMIT` | The maximum number of results to display per page |

### `hubspot-list-templates`

Retrieves a list of templates. [See the

| Flag | Description |
|---|---|
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `hubspot-list-pipelines-and-stages`

List all pipelines and their stages for deals or tickets. Returns

| Flag | Description |
|---|---|
| `--object-type {deal,ticket}` | The object type to list pipelines for. Only `deal` and `ticket` have pipelines. |

### `hubspot-list-pages`

Retrieves a list of site pages. [See the

| Flag | Description |
|---|---|
| `--created-at CREATED_AT` | Only return Site Pages created at exactly the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--created-after CREATED_AFTER` | Only return Site Pages created after the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--created-before CREATED_BEFORE` | Only return Site Pages created before the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-at UPDATED_AT` | Only return Site Pages updated at exactly the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-after UPDATED_AFTER` | Only return Site Pages updated after the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-before UPDATED_BEFORE` | Only return Site Pages updated before the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--archived` | Specifies whether to return deleted Site Pages |
| `--sort {name,createdAt,updatedAt,createdBy,updatedBy}` | Sort the results by the specified field |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `hubspot-list-owners`

List owners (users) in the HubSpot account. Returns owner IDs, names,

| Flag | Description |
|---|---|
| `--email EMAIL` | Filter owners by email address. Returns all owners if not provided. |

### `hubspot-list-messages`

Retrieves a list of messages in a thread. [See the

| Flag | Description |
|---|---|
| `--inbox-id INBOX_ID` | The ID of an inbox You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-lis... |
| `--channel-id CHANNEL_ID` | The ID of a channel You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-li... |
| `--thread-id THREAD_ID` | The ID of a thread You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-lis... |
| `--archived` | Whether to return only results that have been archived |
| `--after AFTER` | The paging cursor token of the last successfully read resource will be returned as the paging.next.after JSON propert... |
| `--limit LIMIT` | The maximum number of results to display per page |
| `--sort {createdAt,-createdAt}` | The sort direction |

### `hubspot-list-marketing-events`

Retrieves a list of marketing events. [See the

| Flag | Description |
|---|---|
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `hubspot-list-marketing-emails`

Retrieves a list of marketing emails. [See the

| Flag | Description |
|---|---|
| `--created-at CREATED_AT` | Only return Marketing Emails created at exactly the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--created-after CREATED_AFTER` | Only return Marketing Emails created after the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--created-before CREATED_BEFORE` | Only return Marketing Emails created before the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-at UPDATED_AT` | Only return Marketing Emails updated at exactly the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-after UPDATED_AFTER` | Only return Marketing Emails updated after the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-before UPDATED_BEFORE` | Only return Marketing Emails updated before the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--include-stats` | Include statistics with emails |
| `--archived` | Specifies whether to return deleted Marketing Emails |
| `--sort {name,createdAt,updatedAt,createdBy,updatedBy}` | Sort the results by the specified field |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `hubspot-list-inboxes`

Retrieves a list of inboxes. [See the

| Flag | Description |
|---|---|
| `--after AFTER` | The paging cursor token of the last successfully read resource will be returned as the paging.next.after JSON propert... |
| `--archived` | Whether to include archived inboxes in the response |
| `--limit LIMIT` | The maximum number of results to display per page |

### `hubspot-list-forms`

Retrieves a list of forms. [See the

| Flag | Description |
|---|---|
| `--archived` | Whether to return only results that have been archived |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `hubspot-list-crm-associations`

List CRM v4 associations from a source record to a target object

| Flag | Description |
|---|---|
| `--from-object-type FROM_OBJECT_TYPE` | Object type of the record you are listing associations from. You can use the "retrieve_options" tool using these para... |
| `--from-object-id FROM_OBJECT_ID` | The source record’s HubSpot ID. After choosing **From Object Type**, pick from the list or enter an ID (for contacts ... |
| `--to-object-type TO_OBJECT_TYPE` | Object type of associated records to return (e.g. contacts linked to this company). You can use the "retrieve_options... |

### `hubspot-list-channels`

Retrieves a list of channels. [See the

| Flag | Description |
|---|---|
| `--after AFTER` | The paging cursor token of the last successfully read resource will be returned as the paging.next.after JSON propert... |
| `--limit LIMIT` | The maximum number of results to display per page |

### `hubspot-list-campaigns`

Retrieves a list of campaigns. [See the

| Flag | Description |
|---|---|
| `--sort {hs_name,-hs_name,createdAt,-createdAt,updatedAt,-updatedAt}` | The field by which to sort the results. An optional '-' before the property name can denote descending order |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `hubspot-list-blog-posts`

Retrieves a list of blog posts. [See the

| Flag | Description |
|---|---|
| `--created-at CREATED_AT` | Only return Blog Posts created at exactly the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--created-after CREATED_AFTER` | Only return Blog Posts created after the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--created-before CREATED_BEFORE` | Only return Blog Posts created before the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-at UPDATED_AT` | Only return Blog Posts updated at exactly the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-after UPDATED_AFTER` | Only return Blog Posts updated after the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--updated-before UPDATED_BEFORE` | Only return Blog Posts updated before the specified time. Format: YYYY-MM-DDTHH:MM:SSZ |
| `--archived` | Specifies whether to return deleted Blog Posts |
| `--properties PROPERTIES` | A comma-separated list of properties to return in the response |
| `--sort {name,createdAt,updatedAt,createdBy,updatedBy}` | Sort the results by the specified field |
| `--max-results MAX_RESULTS` | The maximum number of results to return |

### `hubspot-list-association-labels`

List association type definitions (labels and type IDs) between two

| Flag | Description |
|---|---|
| `--from-object-type FROM_OBJECT_TYPE` | First object type in the association pair (directional). You can use the "retrieve_options" tool using these paramete... |
| `--to-object-type TO_OBJECT_TYPE` | Second object type in the association pair. You can use the "retrieve_options" tool using these parameters to get the... |

### `hubspot-list-associated-engagements`

List engagements (notes, tasks, calls, meetings, emails, etc.)

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | Type of CRM record to load engagements for. Legacy API: typically **company**, **deal**, or **quote**. You can use th... |
| `--object-id OBJECT_ID` | HubSpot ID of the record. After choosing **CRM Object Type**, pick from the list or enter an ID (for contacts you can... |
| `--offset OFFSET` | Pagination offset from the legacy API (default 0). |

### `hubspot-get-user-details`

Get details about the current authenticated HubSpot user, including

_No flags._

### `hubspot-get-subscription-preferences`

Retrieves the subscription preferences for a contact. [See the

| Flag | Description |
|---|---|
| `--contact-email CONTACT_EMAIL` | Note - this needs to be a contact that already exists within HubSpot. You may need to add a Create or Update Contact ... |

### `hubspot-get-properties`

Get detailed property definitions for specific properties on a CRM

| Flag | Description |
|---|---|
| `--object-type {contact,company,deal,ticket,call,quote,line_item,meeting,product,feedback_submission,email,note,task,lead}` | The CRM object type to get property definitions for (e.g. contact, company, deal, ticket). |
| `--property-names PROPERTY_NAMES` | The specific property names to retrieve full details for (e.g. `["dealstage", "pipeline", "hubspot_owner_id"]`). Use ... |

### `hubspot-get-owner`

Get a single HubSpot owner (user) by ID. Select an owner from the

| Flag | Description |
|---|---|
| `--owner-id OWNER_ID` | HubSpot CRM owner ID (use the dropdown or enter an ID manually) You can use the "retrieve_options" tool using these p... |

### `hubspot-get-meeting`

Retrieves a specific meeting by its ID. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | Hubspot's internal ID for the meeting You can use the "retrieve_options" tool using these parameters to get the value... |
| `--additional-properties ADDITIONAL_PROPERTIES` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-get- meeting, propName... |

### `hubspot-get-inbox`

Retrieves a single inbox by its ID. [See the

| Flag | Description |
|---|---|
| `--inbox-id INBOX_ID` | The ID of an inbox You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-get... |

### `hubspot-get-file-public-url`

Get a publicly available URL for a file that was uploaded using a

| Flag | Description |
|---|---|
| `--file-url FILE_URL` | The URL returned after a file has been uploaded to a HubSpot Form You can use the "retrieve_options" tool using these... |
| `--expiration-seconds EXPIRATION_SECONDS` | The number of seconds the returned public URL will be accessible for. Default is 1 hour (3600 seconds). Maximum is 6 ... |

### `hubspot-get-deal`

Gets a deal. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | Hubspot's internal ID for the deal You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--additional-properties ADDITIONAL_PROPERTIES` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-get-deal, propName: ad... |

### `hubspot-get-crm-objects`

Fetch one or more CRM objects by their IDs in a single request

| Flag | Description |
|---|---|
| `--object-type {contact,company,deal,ticket,line_item,product,feedback_submission,lead}` | The CRM object type to fetch. |
| `--object-ids OBJECT_IDS` | List of object IDs to fetch. Min 1, max 100. (JSON array) |
| `--properties PROPERTIES` | Property names to include in results. Use **Search Properties** to discover available property names. If not specifie... |

### `hubspot-get-contact`

Gets a contact. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | Hubspot's internal ID for the contact You can use the "retrieve_options" tool using these parameters to get the value... |
| `--additional-properties ADDITIONAL_PROPERTIES` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-get- contact, propName... |

### `hubspot-get-company`

Gets a company. [See the

| Flag | Description |
|---|---|
| `--object-id OBJECT_ID` | Hubspot's internal ID for the company You can use the "retrieve_options" tool using these parameters to get the value... |
| `--additional-properties ADDITIONAL_PROPERTIES` | You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-get- company, propName... |

### `hubspot-get-channel`

Retrieves a single channel by its ID. [See the

| Flag | Description |
|---|---|
| `--channel-id CHANNEL_ID` | The ID of a channel You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-ge... |

### `hubspot-get-blog-post-draft`

Retrieves the draft version of a blog post. [See the

| Flag | Description |
|---|---|
| `--blog-post-id BLOG_POST_ID` | The ID of the blog post You can use the "retrieve_options" tool using these parameters to get the values. key: hubspo... |

### `hubspot-get-associated-meetings`

Retrieves meetings associated with a specific object (contact,

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The type of the object being associated You can use the "retrieve_options" tool using these parameters to get the val... |
| `--object-id OBJECT_ID` | The ID of the object to get associated meetings for. For contacts, you can search by email. You can use the "retrieve... |
| `--timeframe {today,this_week,this_month,last_month,custom}` | Filter meetings within a specific time frame |
| `--most-recent` | Only return the most recent meeting |
| `--additional-properties ADDITIONAL_PROPERTIES` | Additional properties to retrieve for the meetings (JSON array) |

### `hubspot-get-associated-emails`

Retrieves emails associated with a specific object (contact, company,

| Flag | Description |
|---|---|
| `--object-type OBJECT_TYPE` | The type of the object the emails are associated with You can use the "retrieve_options" tool using these parameters ... |
| `--object-id OBJECT_ID` | The ID of the object to get associated emails for You can use the "retrieve_options" tool using these parameters to g... |
| `--additional-properties ADDITIONAL_PROPERTIES` | Additional properties to retrieve for the emails (JSON array) |
| `--limit LIMIT` | Maximum number of emails to retrieve |

### `hubspot-enroll-contact-into-workflow`

Add a contact to a workflow. Note: The Workflows API currently only

| Flag | Description |
|---|---|
| `--workflow WORKFLOW` | The ID of the workflow you wish to see metadata for. You can use the "retrieve_options" tool using these parameters t... |
| `--contact-email CONTACT_EMAIL` | The email of the contact to be added to the list. Note - this needs to be a contact that already exists within HubSpo... |

### `hubspot-delete-workflow`

Delete a workflow by ID. [See the

| Flag | Description |
|---|---|
| `--workflow-id WORKFLOW_ID` | The ID of the workflow to delete You can use the "retrieve_options" tool using these parameters to get the values. ke... |

### `hubspot-create-workflow`

Create a new workflow. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the workflow to create |
| `--type {DRIP_DELAY,STATIC_ANCHOR,PROPERTY_ANCHOR}` | The type of workflow to create |
| `--actions ACTIONS` | A list of objects representing the workflow actions. [See the documentation](https://developers.hubspot.com /docs/api... |

### `hubspot-create-ticket`

Create a ticket in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to create as a JSON object (JSON object) |
| `--subject SUBJECT` | The name of the ticket |
| `--hs-pipeline HS_PIPELINE` | The pipeline of the ticket You can use the "retrieve_options" tool using these parameters to get the values. key: hub... |
| `--hs-pipeline-stage HS_PIPELINE_STAGE` | The stage of the ticket You can use the "retrieve_options" tool using these parameters to get the values. key: hubspo... |

### `hubspot-create-task`

Create a new task. [See the

| Flag | Description |
|---|---|
| `--to-object-type TO_OBJECT_TYPE` | Type of object the engagement is being associated with You can use the "retrieve_options" tool using these parameters... |
| `--to-object-id TO_OBJECT_ID` | ID of object the engagement is being associated with You can use the "retrieve_options" tool using these parameters t... |
| `--association-type ASSOCIATION_TYPE` | A unique identifier to indicate the association type between the task and the other object You can use the "retrieve_... |
| `--object-properties OBJECT_PROPERTIES` | Enter the `engagement` properties as a JSON object (JSON object) |

### `hubspot-create-page`

Create a page in HubSpot. [See the

| Flag | Description |
|---|---|
| `--page-name PAGE_NAME` | The name of the page. |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the page. |
| `--enable-layout-stylesheets` | Whether to enable layout stylesheets. |
| `--meta-description META_DESCRIPTION` | The meta description of the page. |
| `--attached-stylesheets ATTACHED_STYLESHEETS` | The stylesheets attached to the page. (JSON array) |
| `--password PASSWORD` | The password of the page. |
| `--publish-immediately` | Whether to publish the page immediately. |
| `--html-title HTML_TITLE` | The HTML title of the page. |
| `--translations TRANSLATIONS` | The translations of the page. (JSON object) |
| `--layout-sections LAYOUT_SECTIONS` | The layout sections of the page. (JSON object) |
| `--footer-html FOOTER_HTML` | The footer HTML of the page. |
| `--head-html HEAD_HTML` | The head HTML of the page. |
| `--template-path TEMPLATE_PATH` | The template path of the page. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--widget-containers WIDGET_CONTAINERS` | A data structure containing the data for all the modules inside the containers for this page (JSON object) |
| `--widgets WIDGETS` | A data structure containing the data for all the modules for this page (JSON object) |

### `hubspot-create-or-update-contact`

Create or update a contact in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to create as a JSON object (JSON object) |
| `--update-if-exists` | When selected, if Hubspot returns an error upon creation the resource should be updated. |

### `hubspot-create-note`

Create a new note. [See the

| Flag | Description |
|---|---|
| `--to-object-type TO_OBJECT_TYPE` | Type of object the note is being associated with You can use the "retrieve_options" tool using these parameters to ge... |
| `--to-object-id TO_OBJECT_ID` | ID of object the note is being associated with You can use the "retrieve_options" tool using these parameters to get ... |
| `--association-type ASSOCIATION_TYPE` | A unique identifier to indicate the association type between the note and the other object You can use the "retrieve_... |

### `hubspot-create-meeting`

Creates a new meeting with optional associations to other objects

| Flag | Description |
|---|---|
| `--to-object-type TO_OBJECT_TYPE` | Type of object the meeting is being associated with You can use the "retrieve_options" tool using these parameters to... |
| `--to-object-id TO_OBJECT_ID` | ID of object the meeting is being associated with You can use the "retrieve_options" tool using these parameters to g... |
| `--association-type ASSOCIATION_TYPE` | A unique identifier to indicate the association type between the meeting and the other object You can use the "retrie... |
| `--object-properties OBJECT_PROPERTIES` | Enter the meeting properties as a JSON object. Required properties: hs_meeting_title, hs_meeting_body, hs_meeting_sta... |

### `hubspot-create-lead`

Create a lead in Hubspot. [See the

| Flag | Description |
|---|---|
| `--contact-id CONTACT_ID` | The contact to associate with the lead You can use the "retrieve_options" tool using these parameters to get the valu... |
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to create as a JSON object (JSON object) |

### `hubspot-create-landing-page`

Create a landing page in Hubspot. [See the

| Flag | Description |
|---|---|
| `--page-name PAGE_NAME` | The name of the page. |
| `--landing-folder-id LANDING_FOLDER_ID` | The ID of the folder to create the landing page in. You can use the "retrieve_options" tool using these parameters to... |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the page. |
| `--enable-layout-stylesheets` | Whether to enable layout stylesheets. |
| `--meta-description META_DESCRIPTION` | The meta description of the page. |
| `--attached-stylesheets ATTACHED_STYLESHEETS` | The stylesheets attached to the page. (JSON array) |
| `--password PASSWORD` | The password of the page. |
| `--publish-immediately` | Whether to publish the page immediately. |
| `--html-title HTML_TITLE` | The HTML title of the page. |
| `--translations TRANSLATIONS` | The translations of the page. (JSON object) |
| `--layout-sections LAYOUT_SECTIONS` | The layout sections of the page. (JSON object) |
| `--footer-html FOOTER_HTML` | The footer HTML of the page. |
| `--head-html HEAD_HTML` | The head HTML of the page. |
| `--template-path TEMPLATE_PATH` | The template path of the page. You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--widget-containers WIDGET_CONTAINERS` | A data structure containing the data for all the modules inside the containers for this page (JSON object) |
| `--widgets WIDGETS` | A data structure containing the data for all the modules for this page (JSON object) |

### `hubspot-create-form`

Create a form in HubSpot. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the form. |
| `--archived` | Whether the form is archived. |
| `--field-groups FIELD_GROUPS` | A list for objects of group type and fields. **Format: `[{ "groupType": "default_group", "richTextType": "text", "fie... |
| `--create-new-contact-for-new-email` | Whether to create a new contact when a form is submitted with an email address that doesn't match any in your existin... |
| `--editable` | Whether the form can be edited. |
| `--allow-link-to-reset-known-values` | Whether to add a reset link to the form. This removes any pre-populated content on the form and creates a new contact... |
| `--lifecycle-stages LIFECYCLE_STAGES` | A list of objects of lifecycle stages. **Format: `[{ "objectTypeId": "0-1", "value": "subscriber" }]`** [See the docu... |
| `--post-submit-action-type {thank_you,redirect_url}` | The action to take after submit. The default action is displaying a thank you message. |
| `--post-submit-action-value POST_SUBMIT_ACTION_VALUE` | The thank you text or the page to redirect to. |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the form. |
| `--pre-populate-known-values` | Whether contact fields should pre-populate with known information when a contact returns to your site. |
| `--cloneable` | Whether the form can be cloned. |
| `--notify-contact-owner` | Whether to send a notification email to the contact owner when a submission is received. |
| `--recaptcha-enabled` | Whether CAPTCHA (spam prevention) is enabled. |
| `--archivable` | Whether the form can be archived. |
| `--notify-recipients NOTIFY_RECIPIENTS` | Note - this needs to be a contact that already exists within HubSpot. You may need to add a Create or Update Contact ... |
| `--render-raw-html` | Whether the form will render as raw HTML as opposed to inside an iFrame. |
| `--css-class CSS_CLASS` | The CSS class of the form. |
| `--theme {default_style,canvas,linear,round,sharp,legacy}` | The theme used for styling the input fields. This will not apply if the form is added to a HubSpot CMS page. |
| `--submit-button-text SUBMIT_BUTTON_TEXT` | The text displayed on the form submit button. |
| `--label-text-size LABEL_TEXT_SIZE` | The size of the label text. |
| `--legal-consent-text-color LEGAL_CONSENT_TEXT_COLOR` | The color of the legal consent text. |
| `--font-family FONT_FAMILY` | The font family of the form. |
| `--legal-consent-text-size LEGAL_CONSENT_TEXT_SIZE` | The size of the legal consent text. |
| `--background-width BACKGROUND_WIDTH` | The width of the background. |
| `--help-text-size HELP_TEXT_SIZE` | The size of the help text. |
| `--submit-font-color SUBMIT_FONT_COLOR` | The color of the submit font. |
| `--label-text-color LABEL_TEXT_COLOR` | The color of the label text. |
| `--submit-alignment {left,center,right}` | The alignment of the submit button. |
| `--submit-size SUBMIT_SIZE` | The size of the submit button. |
| `--help-text-color HELP_TEXT_COLOR` | The color of the help text. |
| `--submit-color SUBMIT_COLOR` | The color of the submit button. |
| `--legal-consent-options-type {none,legitimate_interest,explicit_consent_process,implicit_consent_process}` | The type of legal consent options. |
| `--legal-consent-options-object LEGAL_CONSENT_OPTIONS_OBJECT` | The object of legal consent options. **Format: `{"subscriptionTypeIds": [1,2,3], "lawfulBasis": "lead", "privacy": "s... |

### `hubspot-create-engagement`

Create a new engagement for a contact. [See the

| Flag | Description |
|---|---|
| `--engagement-type {notes,tasks,meetings,emails,calls}` | The type of engagement to create |
| `--to-object-type TO_OBJECT_TYPE` | Type of object the engagement is being associated with You can use the "retrieve_options" tool using these parameters... |
| `--to-object-id TO_OBJECT_ID` | ID of object the engagement is being associated with You can use the "retrieve_options" tool using these parameters t... |
| `--association-type ASSOCIATION_TYPE` | A unique identifier to indicate the association type between the task and the other object You can use the "retrieve_... |
| `--object-properties OBJECT_PROPERTIES` | Enter the `engagement` properties as a JSON object (JSON object) |

### `hubspot-create-email`

Create a marketing email in Hubspot. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the email |
| `--campaign CAMPAIGN` | The ID of the campaign to create the email in. You can use the "retrieve_options" tool using these parameters to get ... |
| `--custom-reply-to CUSTOM_REPLY_TO` | The custom reply to address for the email |
| `--from-name FROM_NAME` | The name of the sender |
| `--reply-to REPLY_TO` | The reply to address for the email |
| `--limit-send-frequency` | Whether to limit the send frequency for the email |
| `--suppress-graymail` | Whether to suppress graymail for the email |
| `--include-contact-lists INCLUDE_CONTACT_LISTS` | The contact lists to include You can use the "retrieve_options" tool using these parameters to get the values. key: h... |
| `--exclude-contact-lists EXCLUDE_CONTACT_LISTS` | The contact lists to exclude You can use the "retrieve_options" tool using these parameters to get the values. key: h... |
| `--feedback-survey-id FEEDBACK_SURVEY_ID` | Hubspot's internal ID for the feedback survey. From the Hubspot UI, go to Service -> Feedback Surveys and the ID will... |
| `--rss-data RSS_DATA` | An object with the RSS data for the email. [See the do cumentation](https://developers.hubspot.com/docs/refer ence/ap... |
| `--subject SUBJECT` | The subject of the email |
| `--testing TESTING` | An object with the testing data for the email. [See the documentation](https://developers.hubspot.com/docs /reference... |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the email |
| `--content CONTENT` | An object with the content data for the email. [See the documentation](https://developers.hubspot.com/docs /reference... |
| `--webversion WEBVERSION` | An object with the webversion data for the email. [See the documentation](https://developers.hubspot.com/docs /refere... |
| `--subscription-details SUBSCRIPTION_DETAILS` | An object with the subscription details for the email. [See the documentation](https://developers.hubspot.com /docs/r... |
| `--send-on-publish` | Whether to send the email on publish |

### `hubspot-create-deal`

Create a deal in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to create as a JSON object (JSON object) |
| `--dealname DEALNAME` | Name of the deal |
| `--pipeline PIPELINE` | Pipeline of the deal You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-c... |
| `--dealstage DEALSTAGE` | Stage of the deal You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-crea... |

### `hubspot-create-custom-object`

Create a new custom object in Hubspot. [See the

| Flag | Description |
|---|---|
| `--custom-object-type CUSTOM_OBJECT_TYPE` | The type of custom object to create. This is the object's `fullyQualifiedName`, `objectTypeId`, or the short-hand cus... |
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to create as a JSON object (JSON object) |

### `hubspot-create-crm-object`

Create a new CRM record (contact, company, deal, ticket, etc.). Pass

| Flag | Description |
|---|---|
| `--object-type {contact,company,deal,ticket,call,quote,line_item,meeting,product,feedback_submission,email,note,task,lead}` | The type of CRM object to create. |
| `--properties PROPERTIES` | JSON object of property name-value pairs for the new record. Example for a contact: `{"firstname": "Jane", "lastname"... |
| `--associations ASSOCIATIONS` | Optional JSON array of associations to create alongside the new record. Each entry has `to` (object ID to associate w... |

### `hubspot-create-contact-workflow`

Create a contact workflow in Hubspot. [See the

| Flag | Description |
|---|---|
| `--can-enroll-from-salesforce` | Whether the contact workflow can enroll from Salesforce |
| `--is-enabled` | Whether the contact workflow is enabled |
| `--flow-type {WORKFLOW,ACTION_SET,UNKNOWN}` | The type of flow |
| `--name NAME` | The name of the contact workflow |
| `--description DESCRIPTION` | The description of the contact workflow |
| `--uuid UUID` | The UUID of the contact workflow |
| `--start-action START_ACTION` | The start action of the contact workflow |
| `--actions ACTIONS` | The actions of the contact workflow (JSON array) |
| `--enrollment-criteria ENROLLMENT_CRITERIA` | An object with the enrollment criteria data for the contact workflow. [See the documentation](https://deve lopers.hub... |
| `--enrollment-schedule ENROLLMENT_SCHEDULE` | An object with the enrollment schedule data for the contact workflow. [See the documentation](https://deve lopers.hub... |
| `--time-windows TIME_WINDOWS` | A list of time windows for the contact workflow. [See the documentation](https://developers.hubspot.com/chan gelog/ti... |
| `--blocked-dates BLOCKED_DATES` | A list of blocked dates for the contact workflow. [See the documentation](https://developers.hubspot.com/chan gelog/b... |
| `--custom-properties CUSTOM_PROPERTIES` | An object with the custom properties data for the contact workflow. [See the documentation](https://deve lopers.hubsp... |
| `--data-sources DATA_SOURCES` | A list of data sources for the contact workflow. [See the documentation](https://developers.hubspot.com/chan gelog/da... |
| `--suppression-list-ids SUPPRESSION_LIST_IDS` | A list of suppression list IDs for the contact workflow. [See the documentation](https://developers.h ubspot.com/chan... |
| `--goal-filter-branch GOAL_FILTER_BRANCH` | An object with the goal filter branch data for the contact workflow. [See the documentation](https://deve lopers.hubs... |
| `--event-anchor EVENT_ANCHOR` | An object with the event anchor data for the contact workflow. [See the documentation](https://developers.h ubspot.co... |
| `--un-enrollment-setting UN_ENROLLMENT_SETTING` | An object with the un enrollment setting data for the contact workflow. [See the documentation](https://deve lopers.h... |

### `hubspot-create-company`

Create a company in Hubspot. [See the

| Flag | Description |
|---|---|
| `--object-properties OBJECT_PROPERTIES` | Enter the object properties to create as a JSON object (JSON object) |

### `hubspot-create-communication`

Create a WhatsApp, LinkedIn, or SMS message. [See the

| Flag | Description |
|---|---|
| `--to-object-type TO_OBJECT_TYPE` | Type of object the communication is being associated with You can use the "retrieve_options" tool using these paramet... |
| `--to-object-id TO_OBJECT_ID` | ID of object the communication is being associated with You can use the "retrieve_options" tool using these parameter... |
| `--association-type ASSOCIATION_TYPE` | A unique identifier to indicate the association type between the communication and the other object You can use the "... |
| `--object-properties OBJECT_PROPERTIES` | Enter the `communication` properties as a JSON object (JSON object) |

### `hubspot-create-blog-post`

Creates a new blog post in HubSpot. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The internal name of the blog post |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language of the blog post |
| `--slug SLUG` | The URL slug of the blog post |
| `--meta-description META_DESCRIPTION` | The meta description of the blog post |
| `--post-body POST_BODY` | The HTML content of the blog post |
| `--post-summary POST_SUMMARY` | A summary of the blog post |
| `--html-title HTML_TITLE` | The HTML title tag for the blog post |
| `--featured-image FEATURED_IMAGE` | The URL of the featured image for the blog post |
| `--featured-image-alt-text FEATURED_IMAGE_ALT_TEXT` | The alt text for the featured image |
| `--use-featured-image` | Whether to use a featured image for the blog post |
| `--author-name AUTHOR_NAME` | The name of the blog post author |
| `--blog-author-id BLOG_AUTHOR_ID` | The ID of the blog post author You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--content-group-id CONTENT_GROUP_ID` | The ID of the blog (content group) this post belongs to You can use the "retrieve_options" tool using these parameter... |
| `--publish-date PUBLISH_DATE` | The publish date for the blog post. Format: YYYY-MM- DDTHH:MM:SSZ |
| `--head-html HEAD_HTML` | Custom HTML to be added to the head section |
| `--footer-html FOOTER_HTML` | Custom HTML to be added to the footer section |
| `--enable-google-amp-output-override` | Override the AMP settings for this specific post |
| `--password PASSWORD` | Password required to view the blog post |

### `hubspot-create-associations`

Create associations between objects. [See the

| Flag | Description |
|---|---|
| `--from-object-type FROM_OBJECT_TYPE` | The type of the object being associated You can use the "retrieve_options" tool using these parameters to get the val... |
| `--from-object-id FROM_OBJECT_ID` | The ID of the object being associated You can use the "retrieve_options" tool using these parameters to get the value... |
| `--to-object-type TO_OBJECT_TYPE` | Type of the objects the from object is being associated with You can use the "retrieve_options" tool using these para... |
| `--association-type ASSOCIATION_TYPE` | Type of the association You can use the "retrieve_options" tool using these parameters to get the values. key: hubspo... |
| `--to-object-ids TO_OBJECT_IDS` | Id's of the objects the from object is being associated with You can use the "retrieve_options" tool using these para... |

### `hubspot-create-association`

Create an association (link) between two CRM records. For example,

| Flag | Description |
|---|---|
| `--from-object-type {contact,company,deal,ticket,call,quote,line_item,meeting,product,feedback_submission,email,note,task,lead}` | The object type of the record you're associating from. |
| `--from-object-id FROM_OBJECT_ID` | The ID of the record you're associating from. |
| `--to-object-type {contact,company,deal,ticket,call,quote,line_item,meeting,product,feedback_submission,email,note,task,lead}` | The object type of the record you're associating to. |
| `--to-object-id TO_OBJECT_ID` | The ID of the record you're associating to. |
| `--association-type-id ASSOCIATION_TYPE_ID` | The numeric ID for the association type. Common types: contact→company (1), company→contact (2), deal→contact (3), co... |
| `--association-category {HUBSPOT_DEFINED,USER_DEFINED,INTEGRATOR_DEFINED}` | The category of the association. |

### `hubspot-clone-site-page`

Clone a site page in Hubspot. [See the

| Flag | Description |
|---|---|
| `--page-id PAGE_ID` | The ID of the page to clone. You can use the "retrieve_options" tool using these parameters to get the values. key: h... |
| `--clone-name CLONE_NAME` | The name of the cloned page. |

### `hubspot-clone-email`

Clone a marketing email in HubSpot. [See the

| Flag | Description |
|---|---|
| `--email-id EMAIL_ID` | The ID of the marketing email to clone. You can use the "retrieve_options" tool using these parameters to get the val... |
| `--clone-name CLONE_NAME` | The name to assign to the cloned email |
| `--language {af,ar-eg,bg,bn,cs,da,el,en,es,es-mx,fi,fr,fr-ca,he-il,hr,hu,id,it,ja,ko,lt,ms,nl,no-no,pl,pt,pt-br,ro,ru,sk,sl,sv,th,tl,uk,vi,zh-cn,zh-hk,zh-tw}` | The language code for the cloned email |

### `hubspot-batch-upsert-companies`

Upsert a batch of companies in Hubspot. [See the

| Flag | Description |
|---|---|
| `--inputs INPUTS` | Provide a **list of companies** to be upserted. [See the do cumentation](https://developers.hubspot.com/docs/referenc... |

### `hubspot-batch-update-companies`

Update a batch of companies in Hubspot. [See the

| Flag | Description |
|---|---|
| `--inputs INPUTS` | Provide a **list of companies** to be updated. [See the doc umentation](https://developers.hubspot.com/docs/reference... |

### `hubspot-batch-create-or-update-contact`

Create or update a batch of contacts by its ID or email. [See the

| Flag | Description |
|---|---|
| `--contacts CONTACTS` | Provide a **list of contacts** to be created or updated. If the provided contact has the prop ID or if the provided e... |

### `hubspot-batch-create-companies`

Create a batch of companies in Hubspot. [See the

| Flag | Description |
|---|---|
| `--inputs INPUTS` | Provide a **list of companies** to be created. [See the doc umentation](https://developers.hubspot.com/docs/reference... |

### `hubspot-add-contact-to-list`

Adds a contact to a specific static list. [See the

| Flag | Description |
|---|---|
| `--list LIST` | The list which the contact will be added to. Only static lists are shown here, as dynamic lists cannot be manually ad... |
| `--contact-id CONTACT_ID` | The contact to be added to the list You can use the "retrieve_options" tool using these parameters to get the values.... |

### `hubspot-add-comment`

Adds a comment to a thread. [See the

| Flag | Description |
|---|---|
| `--inbox-id INBOX_ID` | The ID of an inbox You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-add... |
| `--channel-id CHANNEL_ID` | The ID of a channel You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-ad... |
| `--thread-id THREAD_ID` | The ID of a thread You can use the "retrieve_options" tool using these parameters to get the values. key: hubspot-add... |
| `--text TEXT` | The text content of the comment |
| `--file-id FILE_ID` | The ID of a file uploaded to HubSpot You can use the "retrieve_options" tool using these parameters to get the values... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'hubspot'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@hubspot` to bypass the 1h tool-list cache.
