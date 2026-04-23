
# Linear (via Higgsfield MCP proxy)

Linear issues, comments, projects, teams, cycles. Exposes 15 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @linear <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @linear --list                    # all 15 tools
./bin/mcp2cli @linear linear-app-update-issue --help   # inspect one
./bin/mcp2cli @linear linear-app-update-issue --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @linear --pretty <cmd>` — `--pretty` goes AFTER `@linear`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @linear --head N <cmd>` — `--head N` goes AFTER `@linear`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 15 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `linear-app-update-issue`

Updates an existing Linear issue. Can modify title, description,

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | The identifier or key of the team associated with the issue You can use the "retrieve_options" tool using these param... |
| `--issue-id ISSUE_ID` | The issue to update You can use the "retrieve_options" tool using these parameters to get the values. key: linear_app... |
| `--title TITLE` | The title of the issue. |
| `--description DESCRIPTION` | The issue description in markdown format |
| `--team-id-to-update TEAM_ID_TO_UPDATE` | The identifier or key of the team to update the issue to You can use the "retrieve_options" tool using these paramete... |
| `--state-id STATE_ID` | The state (status) to assign to the issue You can use the "retrieve_options" tool using these parameters to get the v... |
| `--assignee-id ASSIGNEE_ID` | The user to assign to the issue You can use the "retrieve_options" tool using these parameters to get the values. key... |
| `--label-ids LABEL_IDS` | The labels in the issue You can use the "retrieve_options" tool using these parameters to get the values. key: linear... |
| `--project-id PROJECT_ID` | The identifier or key of the project associated with the issue You can use the "retrieve_options" tool using these pa... |
| `--priority PRIORITY` | The priority of the issue |

### `linear-app-update-initiative`

Update an initiative in Linear. [See the

| Flag | Description |
|---|---|
| `--initiative-id INITIATIVE_ID` | The identifier or key of the initiative to update You can use the "retrieve_options" tool using these parameters to g... |
| `--name NAME` | The name of the initiative |
| `--description DESCRIPTION` | The description of the initiative |
| `--status {Active,Completed,Planned}` | The status of the initiative |
| `--target-date TARGET_DATE` | The target date of the initiative in ISO 8601 format |

### `linear-app-search-issues`

Searches Linear issues by team, project, assignee, labels, state, or

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | The identifier or key of the team associated with the issue You can use the "retrieve_options" tool using these param... |
| `--project-id PROJECT_ID` | The identifier or key of the project associated with the issue You can use the "retrieve_options" tool using these pa... |
| `--query QUERY` | Search string to look for in issue titles. The query is used to filter issues where the title contains the query text... |
| `--state-id STATE_ID` | Filter issues by their workflow state (status). States are scoped to the selected team. You can use the "retrieve_opt... |
| `--assignee-id ASSIGNEE_ID` | The user to assign to the issue You can use the "retrieve_options" tool using these parameters to get the values. key... |
| `--issue-labels ISSUE_LABELS` | The labels in the issue You can use the "retrieve_options" tool using these parameters to get the values. key: linear... |
| `--order-by {createdAt,updatedAt}` | By which field should the pagination order by. Available options are `createdAt` (default) and `updatedAt`. |
| `--include-archived` | Should archived resources be included? (default: `false`) |
| `--limit LIMIT` | Maximum number of issues to return. If no query is provided, this defaults to 20 to avoid returning too many results. |

### `linear-app-remove-label-from-issue`

Remove a label from an issue in Linear. [See the

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | Filter selected issues by team You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--issue-id ISSUE_ID` | The ID of the issue to remove the label from You can use the "retrieve_options" tool using these parameters to get th... |
| `--label-id LABEL_ID` | The ID of the label to remove from the issue You can use the "retrieve_options" tool using these parameters to get th... |

### `linear-app-list-views`

List views in Linear. [See the

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | Filter views by team You can use the "retrieve_options" tool using these parameters to get the values. key: linear_ap... |
| `--order-by {createdAt,updatedAt}` | By which field should the pagination order by. Available options are `createdAt` (default) and `updatedAt`. |
| `--first FIRST` | The number of views to return |
| `--after AFTER` | The cursor to return the next page of views |

### `linear-app-list-projects`

List projects in Linear. [See the

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | The identifier or key of the team associated with the issue You can use the "retrieve_options" tool using these param... |
| `--order-by {createdAt,updatedAt}` | By which field should the pagination order by. Available options are `createdAt` (default) and `updatedAt`. |
| `--first FIRST` | The number of projects to return |
| `--after AFTER` | The cursor to return the next page of projects |

### `linear-app-list-initiatives`

List initiatives in Linear. [See the

| Flag | Description |
|---|---|
| `--name NAME` | Search for initiatives that contain the provided name |
| `--status {Active,Completed,Planned}` | The status of the initiative |
| `--order-by {createdAt,updatedAt}` | By which field should the pagination order by. Available options are `createdAt` (default) and `updatedAt`. |
| `--first FIRST` | The number of initiatives to return |
| `--after AFTER` | The cursor to return the next page of initiatives |

### `linear-app-list-comments`

List comments in Linear. [See the

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | Filter issue selection by team You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--issue-id ISSUE_ID` | Filter results by issue You can use the "retrieve_options" tool using these parameters to get the values. key: linear... |
| `--body BODY` | Search for comments containing this text |
| `--order-by {createdAt,updatedAt}` | By which field should the pagination order by. Available options are `createdAt` (default) and `updatedAt`. |
| `--first FIRST` | The number of comments to return |
| `--after AFTER` | The cursor to return the next page of comments |

### `linear-app-get-view-issues`

Get issues from a custom view in Linear. [See the

| Flag | Description |
|---|---|
| `--view-id VIEW_ID` | The identifier or key of the custom view to get issues from You can use the "retrieve_options" tool using these param... |
| `--order-by {createdAt,updatedAt}` | By which field should the pagination order by. Available options are `createdAt` (default) and `updatedAt`. |
| `--first FIRST` | The number of issues to return |
| `--after AFTER` | The cursor to return the next page of issues |

### `linear-app-get-teams`

Retrieves all teams in your Linear workspace. Returns array of team

| Flag | Description |
|---|---|
| `--limit LIMIT` | Maximum number of teams to return. Defaults to 20 if not specified. |

### `linear-app-get-issue`

Retrieves a Linear issue by its ID or identifier. Returns complete

| Flag | Description |
|---|---|
| `--issue-id ISSUE_ID` | The issue ID You can use the "retrieve_options" tool using these parameters to get the values. key: linear_app-get-is... |
| `--issue-identifier ISSUE_IDENTIFIER` | The identifier of the issue. Example: `APP-1234` You can use the "retrieve_options" tool using these parameters to ge... |

### `linear-app-create-project`

Create a project in Linear. [See the

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | The identifier or key of the team associated with the issue You can use the "retrieve_options" tool using these param... |
| `--name NAME` | The name of the project |
| `--description DESCRIPTION` | The description of the project |
| `--status-id STATUS_ID` | The ID of the status of the project You can use the "retrieve_options" tool using these parameters to get the values.... |
| `--priority PRIORITY` | The priority of the project |
| `--member-ids MEMBER_IDS` | The IDs of the members of the project You can use the "retrieve_options" tool using these parameters to get the value... |
| `--start-date START_DATE` | The start date of the project in ISO 8601 format |
| `--target-date TARGET_DATE` | The target date of the project in ISO 8601 format |
| `--label-ids LABEL_IDS` | The IDs of the labels for the project You can use the "retrieve_options" tool using these parameters to get the value... |

### `linear-app-create-issue`

Creates a new issue in Linear. Requires team ID and title. Optional:

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | The identifier or key of the team associated with the issue You can use the "retrieve_options" tool using these param... |
| `--project-id PROJECT_ID` | The identifier or key of the project associated with the issue You can use the "retrieve_options" tool using these pa... |
| `--title TITLE` | The title of the issue. |
| `--description DESCRIPTION` | The issue description in markdown format |
| `--assignee-id ASSIGNEE_ID` | The user to assign to the issue You can use the "retrieve_options" tool using these parameters to get the values. key... |
| `--state-id STATE_ID` | The state (status) to assign to the issue You can use the "retrieve_options" tool using these parameters to get the v... |
| `--label-ids LABEL_IDS` | The labels in the issue You can use the "retrieve_options" tool using these parameters to get the values. key: linear... |
| `--priority PRIORITY` | The priority of the issue |

### `linear-app-create-initiative`

Create an initiative in Linear. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the initiative |
| `--description DESCRIPTION` | The description of the initiative |
| `--content CONTENT` | The content of the initiative in markdown format |
| `--status {Active,Completed,Planned}` | The status of the initiative |
| `--color COLOR` | The color of the initiative |
| `--target-date TARGET_DATE` | The target date of the initiative in ISO 8601 format |
| `--owner-id OWNER_ID` | The user to assign to the initiative You can use the "retrieve_options" tool using these parameters to get the values... |

### `linear-app-create-comment`

Create a comment in Linear. [See the

| Flag | Description |
|---|---|
| `--team-id TEAM_ID` | Filter issue selection by team You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--issue-id ISSUE_ID` | The issue to create the comment on You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--body BODY` | The body of the comment |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'linear'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@linear` to bypass the 1h tool-list cache.
