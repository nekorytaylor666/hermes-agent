
# Atlassian Jira (via Higgsfield MCP proxy)

Jira issues, comments, sprints, projects, transitions. Exposes 37 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @jira <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @jira --list                    # all 37 tools
./bin/mcp2cli @jira jira-get-current-user --help   # inspect one
./bin/mcp2cli @jira jira-get-current-user --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @jira --pretty <cmd>` — `--pretty` goes AFTER `@jira`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @jira --head N <cmd>` — `--head N` goes AFTER `@jira`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 37 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `jira-get-current-user`

Returns the authenticated Jira user's account ID, display name,

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-current... |

### `jira-update-issue`

Updates an issue. A transition may be applied and issue properties

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- update-issu... |
| `--history-metadata HISTORY_METADATA` | Additional issue history details (JSON object) |
| `--properties PROPERTIES` | Details of issue properties to be added or updated. Please provide an array of objects with keys and values. |
| `--update UPDATE` | A Map containing the field name and a list of operations to perform on the issue screen field. Note that fields inclu... |
| `--additional-properties ADDITIONAL_PROPERTIES` | Extra properties of any type may be provided to this object (JSON object) |
| `--project-id PROJECT_ID` | The project ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- update-is... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--issue-type-id ISSUE_TYPE_ID` | An ID identifying the type of issue. [Check the API do cs](https://developer.atlassian.com/cloud/jira/platfor m/rest/... |
| `--notify-users` | Whether a notification email about the issue update is sent to all watchers. To disable the notification, administer ... |
| `--override-screen-security` | Whether screen security should be overridden to enable hidden fields to be edited. Available to Connect app users wit... |
| `--override-editable-flag` | Whether screen security should be overridden to enable uneditable fields to be edited. Available to Connect app users... |
| `--transition-id TRANSITION_ID` | The ID of the issue transition. Retrieving options requires a static `issueIdOrKey`. Required when specifying a trans... |
| `--transition-looped` | Whether the transition is looped |

### `jira-update-comment`

Updates a comment. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- update-comm... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--comment-id COMMENT_ID` | The ID of the comment You can use the "retrieve_options" tool using these parameters to get the values. key: jira-upd... |
| `--body BODY` | The comment text in [Atlassian Document Format](https: //developer.atlassian.com/cloud/jira/platform/apis/doc ument/s... |
| `--comment COMMENT` | The comment text |
| `--visibility VISIBILITY` | The group or role to which this comment is visible, See `Visibility` section of [doc](https://developer.at lassian.co... |
| `--properties PROPERTIES` | Details of issue properties to be added or updated. Please provide an array of objects with keys and values. |
| `--additional-properties ADDITIONAL_PROPERTIES` | Extra properties of any type may be provided to this object (JSON object) |
| `--notify-users` | Whether users are notified when a comment is updated |
| `--expand EXPAND` | Use expand to include additional information about comments in the response. This parameter accepts `renderedBody`, w... |

### `jira-transition-issue`

Performs an issue transition and, if the transition has a screen,

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- transition-... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--transition TRANSITION` | Details of a transition. Required when performing a transition, optional when creating or editing an issue, See `Tran... |
| `--fields FIELDS` | List of issue screen fields to update, specifying the sub-field to update and its value for each field. This field pr... |
| `--update UPDATE` | List of operations to perform on issue screen fields. Note that fields included here cannot be included in fields. (J... |
| `--history-metadata HISTORY_METADATA` | Additional issue history details. See `HistoryMetadata` section of [doc](https://developer.a tlassian.com/cloud/jira/... |
| `--properties PROPERTIES` | Details of issue properties to be add or update |
| `--additional-properties ADDITIONAL_PROPERTIES` | Extra properties of any type may be provided to this object (JSON object) |

### `jira-search-issues-with-jql`

Search for issues using JQL (Jira Query Language). [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- search-issu... |
| `--jql JQL` | The JQL query to search for issues. [See the documentation for syntax and examples](https://support.atlassian.com/jir... |
| `--max-results MAX_RESULTS` | Maximum number of issues to return (default: 50) |
| `--fields FIELDS` | Comma-separated list of fields to return for each issue |
| `--expand EXPAND` | Use expand to include additional information about the issues in the response (JSON array) |
| `--properties PROPERTIES` | A list of up to 5 issue properties to include in the results. This parameter accepts a comma-separated list. |
| `--fields-by-keys` | Reference fields by their key (rather than ID). The default is `false`. |
| `--fail-fast` | Fail this request early if we can't retrieve all field data |

### `jira-search-issues-with-jql-post`

Searches for issues using JQL with enhanced search capabilities. [See

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- search-issu... |
| `--jql JQL` | The JQL that defines the search. If no JQL expression is provided, all issues are returned. Note: `username` and `use... |
| `--max-results MAX_RESULTS` | The maximum number of items to return per page |
| `--next-page-token NEXT_PAGE_TOKEN` | Token for pagination. Use the token from a previous response to get the next page of results |
| `--fields FIELDS` | A list of fields to return for each issue. Use it to retrieve a subset of fields. Examples: `summary,comment` or `*al... |
| `--expand EXPAND` | Use expand to include additional information about issues in the response (JSON array) |
| `--properties PROPERTIES` | A list of issue property keys for issue properties to include in the results. A maximum of 5 issue property keys can ... |
| `--fields-by-keys` | Reference fields by their key (rather than ID) |
| `--reconcile-issues RECONCILE_ISSUES` | A list of issue IDs or keys to reconcile for read- after-write consistency. This ensures that recently created or upd... |

### `jira-move-issues-to-sprint`

Moves issues to a sprint, for a given sprint ID. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- move-issues... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-move-... |
| `--sprint-id SPRINT_ID` | The ID of the sprint You can use the "retrieve_options" tool using these parameters to get the values. key: jira-move... |
| `--issues ISSUES` | The IDs or keys of the issues to move to the sprint. You can use the "retrieve_options" tool using these parameters t... |

### `jira-list-sprints`

Returns all sprints from a board, for the given board ID. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- list-sprint... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-list-... |
| `--start-at START_AT` | The starting index of the returned sprints. Base index: 0. |
| `--max-results MAX_RESULTS` | The maximum number of sprints to return. |
| `--state STATE` | Filters results to sprints in the specified states. Accepts a comma-separated list of: `future`, `active`, `closed`. |

### `jira-list-sprint-issues`

Returns all issues in a sprint. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- list-sprint... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-list-... |
| `--sprint-id SPRINT_ID` | The ID of the sprint You can use the "retrieve_options" tool using these parameters to get the values. key: jira-list... |
| `--start-at START_AT` | The starting index of the returned issues. Base index: 0. |
| `--max-results MAX_RESULTS` | The maximum number of issues to return. |
| `--jql JQL` | Filters results using a JQL query. |
| `--fields FIELDS` | A list of fields to return for each issue. Accepts a comma-separated list. |
| `--expand EXPAND` | The Jira REST API uses resource expansion, which means that some parts of a resource are not returned unless specifie... |

### `jira-list-issue-comments`

Lists all comments for an issue. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- list-issue-... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--order-by {created,+created,-created}` | [Order](https://developer.atlassian.com/cloud/jira/pla tform/rest/v3/intro/#ordering) the results by a field. Accepts... |
| `--expand EXPAND` | Use expand to include additional information about comments in the response. This parameter accepts `renderedBody`, w... |

### `jira-list-epics`

Returns all epics from a board, for the given board ID. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- list-epics,... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-list-... |
| `--start-at START_AT` | The starting index of the returned epics. Base index: 0. |
| `--max-results MAX_RESULTS` | The maximum number of epics to return. |
| `--done` | Filters results to epics that are either done or not done. If not provided, all epics are returned. |

### `jira-list-epic-issues`

Returns all issues that belong to an epic on the given board. [See

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- list-epic-i... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-list-... |
| `--epic-id EPIC_ID` | The ID of the epic You can use the "retrieve_options" tool using these parameters to get the values. key: jira-list-e... |
| `--start-at START_AT` | The starting index of the returned issues. Base index: 0. |
| `--max-results MAX_RESULTS` | The maximum number of issues to return. |
| `--jql JQL` | Filters results using a JQL query. |
| `--fields FIELDS` | A list of fields to return for each issue. Accepts a comma-separated list. |
| `--expand EXPAND` | The Jira REST API uses resource expansion, which means that some parts of a resource are not returned unless specifie... |

### `jira-list-boards`

Returns all boards. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- list-boards... |
| `--start-at START_AT` | The starting index of the returned boards. Base index: 0. |
| `--max-results MAX_RESULTS` | The maximum number of boards to return. |
| `--type {scrum,kanban,simple}` | Filters results to boards of the specified type. |
| `--name NAME` | Filters results to boards that match or partially match the specified name. |
| `--project-key-or-id PROJECT_KEY_OR_ID` | Filters results to boards that are relevant to a project. |

### `jira-list-board-issues`

Returns all issues from a board, for the given board ID. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- list-board-... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-list-... |
| `--start-at START_AT` | The starting index of the returned issues. Base index: 0. |
| `--max-results MAX_RESULTS` | The maximum number of issues to return. |
| `--jql JQL` | Filters results using a JQL query. |
| `--fields FIELDS` | A list of fields to return for each issue. Accepts a comma-separated list. |
| `--expand EXPAND` | The Jira REST API uses resource expansion, which means that some parts of a resource are not returned unless specifie... |

### `jira-get-users`

Gets the details for a list of users. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-users, ... |
| `--query QUERY` | Filter for a name or term |

### `jira-get-user`

Gets details of user. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-user, p... |
| `--account-id ACCOUNT_ID` | The account ID of the user, which uniquely identifies the user across all Atlassian products, For example, `5b10ac8d8... |
| `--expand EXPAND` | Use expand to include additional information about users in the response. This parameter accepts a comma- separated l... |

### `jira-get-transitions`

Gets either all transitions or a transition that can be performed by

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-transit... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--transition-id TRANSITION_ID` | The ID of the transition You can use the "retrieve_options" tool using these parameters to get the values. key: jira-... |
| `--skip-remote-only-condition` | Whether transitions with the condition *Hide From User Condition* are included in the response |
| `--include-unavailable-transitions` | Whether details of transitions that fail a condition are included in the response |
| `--sort-by-ops-bar-and-status` | Whether the transitions are sorted by ops-bar sequence value first then category order (Todo, In Progress, Done) or o... |
| `--expand EXPAND` | Use expand to include additional information about transitions in the response. This parameter accepts `transitions.f... |

### `jira-get-task`

Gets the status of a long-running asynchronous task. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-task, p... |
| `--task-id TASK_ID` | The ID of the task to get details of. A task is a resource that represents a [long-running asynchronous t asks](https... |

### `jira-get-sprint`

Returns the sprint for a given sprint ID. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-sprint,... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-get-s... |
| `--sprint-id SPRINT_ID` | The ID of the sprint You can use the "retrieve_options" tool using these parameters to get the values. key: jira-get-... |

### `jira-get-issue`

Gets the details for an issue. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-issue, ... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--fields FIELDS` | A list of fields to return for the issue. This parameter accepts a comma-separated list. Use it to retrieve a subset ... |
| `--fields-by-keys` | Whether `fields` in fields are referenced by keys rather than IDs. This parameter is useful where fields have been ad... |
| `--properties PROPERTIES` | A list of issue properties to return for the issue. This parameter accepts a comma-separated list. Allowed values: `*... |
| `--update-history` | Whether the project in which the issue is created is added to the user's Recently viewed project list, as shown under... |
| `--expand EXPAND` | Use expand to include additional information about the issues in the response. This parameter accepts a comma-separat... |

### `jira-get-issue-types`

Gets the available issue types. If a project ID is provided, returns

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-issue-t... |
| `--project-id PROJECT_ID` | The project ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-issue... |

### `jira-get-issue-picker-suggestions`

Returns lists of issues matching a query string. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-issue-p... |
| `--query QUERY` | A string to match against text fields in the issue such as title, description, or comments |
| `--current-jql CURRENT_JQL` | A JQL query defining a list of issues to search for the query term. Note that `username` and `userkey` cannot be used... |
| `--current-issue-key CURRENT_ISSUE_KEY` | The key of an issue to exclude from search results. For example, the issue the user is viewing when they perform this... |
| `--current-project-id CURRENT_PROJECT_ID` | The ID of a project that suggested issues must belong to You can use the "retrieve_options" tool using these paramete... |
| `--show-sub-tasks` | Indicate whether to include subtasks in the suggestions list |
| `--show-sub-task-parent` | When `currentIssueKey` is a subtask, whether to include the parent issue in the suggestions if it matches the query |

### `jira-get-cloud-id`

Gets the cloud ID and details of all accessible Jira Cloud sites

_No flags._

### `jira-get-board`

Returns the board for the given board ID. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-board, ... |
| `--board-id BOARD_ID` | The ID of the board You can use the "retrieve_options" tool using these parameters to get the values. key: jira-get-b... |

### `jira-get-all-projects`

Gets metadata on all projects. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- get-all-pro... |
| `--recent RECENT` | Returns the user's most recently accessed projects. You may specify the number of results to return up to a maximum o... |
| `--properties PROPERTIES` | Details of issue properties to be added or updated. Please provide an array of objects with keys and values. |
| `--expand EXPAND` | Use expand to include additional information in the response. This parameter accepts a comma-separated list. Expanded... |

### `jira-delete-project`

Deletes a project. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- delete-proj... |
| `--project-id PROJECT_ID` | The project ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- delete-pr... |
| `--enable-undo` | Whether this project is placed in the Jira recycle bin where it will be available for restoration |

### `jira-create-version`

Creates a project version. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- create-vers... |
| `--project-id PROJECT_ID` | The project ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- create-ve... |
| `--name NAME` | The unique name of the version. The maximum length is 255 characters. |
| `--description DESCRIPTION` | The description of the version |
| `--archived` | Indicates that the version is archived |
| `--start-date START_DATE` | The start date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). |
| `--release-date RELEASE_DATE` | The release date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). |
| `--expand EXPAND` | Use expand to include additional information about the version in the response. This parameter accepts a comma-separa... |

### `jira-create-issue`

Creates an issue or, where the option to create subtasks is enabled

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- create-issu... |
| `--history-metadata HISTORY_METADATA` | Additional issue history details (JSON object) |
| `--properties PROPERTIES` | Details of issue properties to be added or updated. Please provide an array of objects with keys and values. |
| `--update UPDATE` | A Map containing the field name and a list of operations to perform on the issue screen field. Note that fields inclu... |
| `--additional-properties ADDITIONAL_PROPERTIES` | Extra properties of any type may be provided to this object (JSON object) |
| `--update-history` | Whether the project in which the issue is created is added to the user's **Recently viewed** project list, as shown u... |
| `--project-id PROJECT_ID` | The project ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- create-is... |
| `--issue-type-id ISSUE_TYPE_ID` | An ID identifying the type of issue. [Check the API do cs](https://developer.atlassian.com/cloud/jira/platfor m/rest/... |

### `jira-create-future-sprint`

Creates a future sprint. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- create-futu... |
| `--board-id BOARD_ID` | The ID of the board the sprint will be created on. You can use the "retrieve_options" tool using these parameters to ... |
| `--name NAME` | The name of the sprint. |
| `--goal GOAL` | The goal of the sprint. |
| `--start-date START_DATE` | The start date of the sprint in ISO 8601 format (e.g. `2024-01-01T00:00:00.000Z`). |
| `--end-date END_DATE` | The end date of the sprint in ISO 8601 format (e.g. `2024-01-15T00:00:00.000Z`). |

### `jira-create-custom-field-options-context`

Create a context for custom field options. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- create-cust... |
| `--field-id FIELD_ID` | The ID of the field You can use the "retrieve_options" tool using these parameters to get the values. key: jira-creat... |
| `--context-id CONTEXT_ID` | The ID of the context You can use the "retrieve_options" tool using these parameters to get the values. key: jira-cre... |
| `--options OPTIONS` | Options to create. Each option should be a JSON object with the following structure as an example: `{ "value": "Manha... |

### `jira-count-issues-using-jql`

Provide an estimated count of the issues that match the JQL. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- count-issue... |
| `--jql JQL` | The JQL query to count issues. The JQL must be bounded. Example: `project = HSP` |

### `jira-check-issues-against-jql`

Checks whether one or more issues would be returned by one or more

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- check-issue... |
| `--issue-ids ISSUE_IDS` | A list of issue IDs to check against the JQL queries. Example: `["10001", "10042"]` You can use the "retrieve_options... |
| `--jqls JQLS` | A list of JQL query strings to check the issues against. Example: `["project = FOO", "issuetype = Bug"]` (JSON array) |

### `jira-assign-issue`

Assigns an issue to a user. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- assign-issu... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--account-id ACCOUNT_ID` | The account ID of the user, which uniquely identifies the user across all Atlassian products, For example, `5b10ac8d8... |

### `jira-add-watcher-to-issue`

Adds a user as a watcher of an issue by passing the account ID of the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- add-watcher... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--account-id ACCOUNT_ID` | The account ID of the user, which uniquely identifies the user across all Atlassian products, For example, `5b10ac8d8... |

### `jira-add-multiple-attachments-to-issue`

Adds multiple attachments to an issue. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- add-multipl... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--files FILES` | Provide either an array of file URLs or paths to files in the /tmp directory (for example, /tmp/myFile.pdf). (JSON ar... |

### `jira-add-comment-to-issue`

Adds a new comment to an issue. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- add-comment... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--comment COMMENT` | The comment text |
| `--body BODY` | The comment text in [Atlassian Document Format](https: //developer.atlassian.com/cloud/jira/platform/apis/doc ument/s... |
| `--visibility VISIBILITY` | The group or role to which this comment is visible, See `Visibility` section of [doc](https://developer.at lassian.co... |
| `--properties PROPERTIES` | A list of comment properties. |
| `--additional-properties ADDITIONAL_PROPERTIES` | Extra properties of any type may be provided to this object (JSON object) |
| `--expand EXPAND` | The Jira REST API uses resource expansion, which means that some parts of a resource are not returned unless specifie... |

### `jira-add-attachment-to-issue`

Adds an attachment to an issue. [See the

| Flag | Description |
|---|---|
| `--cloud-id CLOUD_ID` | The cloud ID You can use the "retrieve_options" tool using these parameters to get the values. key: jira- add-attachm... |
| `--issue-id-or-key ISSUE_ID_OR_KEY` | The ID or key of an issue You can use the "retrieve_options" tool using these parameters to get the values. key: jira... |
| `--file FILE` | Provide either a file URL or a path to a file in the /tmp directory (for example, /tmp/myFile.pdf). |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'jira'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@jira` to bypass the 1h tool-list cache.
