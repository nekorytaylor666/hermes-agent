
# Todoist (via Higgsfield MCP proxy)

Todoist tasks, projects, sections, labels, comments. Exposes 42 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @todoist <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @todoist --list                    # all 42 tools
./bin/mcp2cli @todoist todoist-update-task --help   # inspect one
./bin/mcp2cli @todoist todoist-update-task --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @todoist --pretty <cmd>` — `--pretty` goes AFTER `@todoist`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @todoist --head N <cmd>` — `--head N` goes AFTER `@todoist`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 42 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `todoist-update-task`

Updates a task. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | The project containing the task to be updated You can use the "retrieve_options" tool using these parameters to get t... |
| `--task TASK` | The task to update You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-upd... |
| `--content CONTENT` | Task Content |
| `--description DESCRIPTION` | Task description |
| `--labels LABELS` | Select labels to add to the task. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--priority PRIORITY` | Task priority from 1 (normal) to 4 (urgent) |
| `--due-string DUE_STRING` | [Human defined](https://todoist.com/help/articles/205325931) task due date (ex.: "next Monday", "Tomorrow"). Value is... |
| `--due-date DUE_DATE` | Specific date in `YYYY-MM-DD` format relative to user’s timezone |
| `--due-datetime DUE_DATETIME` | Specific date and time in [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) format in UTC. |
| `--due-lang DUE_LANG` | 2-letter code specifying language in case `due_string` is not written in English |
| `--assignee ASSIGNEE` | The responsible user (if set, and only for shared tasks) You can use the "retrieve_options" tool using these paramete... |

### `todoist-update-section`

Updates a section. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--section SECTION` | The section to update You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-... |
| `--name NAME` | Enter the new name |

### `todoist-update-project`

Updates a project. [See the

| Flag | Description |
|---|---|
| `--project-id PROJECT_ID` | The project to update You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-... |
| `--name NAME` | Enter the new name |
| `--color COLOR` | A numeric ID representing a color (automatically converted to v1 API format). Refer to the id column in the [Colors](... |
| `--favorite` | Whether this is a favorite |

### `todoist-update-label`

Updates a label. [See the

| Flag | Description |
|---|---|
| `--label LABEL` | The label to update You can use the "retrieve_options" tool using these parameters to get the values. key: todoist- u... |
| `--name NAME` | Enter the new name |
| `--order ORDER` | Order in a list |
| `--color COLOR` | A numeric ID representing a color (automatically converted to v1 API format). Refer to the id column in the [Colors](... |
| `--favorite` | Whether this is a favorite |

### `todoist-update-filter`

Updates a filter. [See the

| Flag | Description |
|---|---|
| `--filter FILTER` | Select the filter to update You can use the "retrieve_options" tool using these parameters to get the values. key: to... |
| `--name NAME` | Enter the new name |
| `--query QUERY` | The query to search for. [Examples of searches](https://todoist.com/help/articles/introduction- to-filters) can be fo... |
| `--color COLOR` | A numeric ID representing a color (automatically converted to v1 API format). Refer to the id column in the [Colors](... |
| `--order ORDER` | Order in a list |
| `--favorite` | Whether this is a favorite |

### `todoist-update-comment`

Updates a comment. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Project containing the comment to update You can use the "retrieve_options" tool using these parameters to get the va... |
| `--task TASK` | Task containing the comment to update You can use the "retrieve_options" tool using these parameters to get the value... |
| `--comment-id COMMENT_ID` | Select a comment You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-updat... |
| `--content CONTENT` | Comment content |

### `todoist-uncomplete-task`

Uncompletes a task. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--task-id TASK_ID` | Select the task to reopen You can use the "retrieve_options" tool using these parameters to get the values. key: todo... |

### `todoist-search-tasks`

Search tasks by name, label, project and/or section. [See the

| Flag | Description |
|---|---|
| `--name NAME` | Returns tasks that contain the specified string in their name |
| `--label LABEL` | Select a label to filter results by You can use the "retrieve_options" tool using these parameters to get the values.... |
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--section SECTION` | Select a section to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-move-task-to-section`

Move a Task to a different section within the same project. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Project containing the task to move You can use the "retrieve_options" tool using these parameters to get the values.... |
| `--task TASK` | Select a task to move You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-... |
| `--section SECTION` | The section to move the task to You can use the "retrieve_options" tool using these parameters to get the values. key... |

### `todoist-mark-task-completed`

Marks a task as being completed. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--task-id TASK_ID` | The task to mark as complete You can use the "retrieve_options" tool using these parameters to get the values. key: t... |

### `todoist-list-uncompleted-tasks`

Returns a list of uncompleted tasks by project, section, and/or

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--section SECTION` | Select a section to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--label LABEL` | Select a label to filter results by You can use the "retrieve_options" tool using these parameters to get the values.... |

### `todoist-list-task-comments`

Returns a list of comments for a task. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--task TASK` | Select a task to filter results by You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `todoist-list-sections`

Returns a list of all sections. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-list-projects`

Returns a list of all projects. [See the

_No flags._

### `todoist-list-project-comments`

Returns a list of comments for a project. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-list-labels`

Returns a list of all labels. [See the

_No flags._

### `todoist-list-filters`

Returns a list of all filters. [See the

_No flags._

### `todoist-invite-user-to-project`

Sends email to a person, inviting them to use one of your projects

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--email EMAIL` | Email Address |

### `todoist-import-tasks`

Import tasks into a selected project. [See the

| Flag | Description |
|---|---|
| `--path PATH` | The .csv file to upload. Provide either a file URL or a path to a file in the `/tmp` directory (for example, `/tmp/my... |
| `--project PROJECT` | Project to import tasks into You can use the "retrieve_options" tool using these parameters to get the values. key: t... |

### `todoist-get-task`

Returns info about a task. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--task TASK` | Select a task to filter results by You can use the "retrieve_options" tool using these parameters to get the values. ... |

### `todoist-get-task-comment`

Returns info about a task comment. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--task TASK` | Select a task to filter results by You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--comment-id COMMENT_ID` | Select a comment You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-get-t... |

### `todoist-get-section`

Returns info about a section. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--section-id SECTION_ID` | Select a section to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-get-project`

Returns info about a project. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-get-project-comment`

Returns info about a project comment. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Project containing the comment You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--comment-id COMMENT_ID` | Select a comment You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-get-p... |

### `todoist-get-label`

Returns info about a label. [See the

| Flag | Description |
|---|---|
| `--label LABEL` | Select a label to filter results by You can use the "retrieve_options" tool using these parameters to get the values.... |

### `todoist-find-user`

Searches by email for a user who is connected/shared with your

| Flag | Description |
|---|---|
| `--email EMAIL` | Email Address |

### `todoist-find-task`

Finds a task by name. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--content CONTENT` | The name of the task to search for/create |
| `--create-if-not-found` | Create this item if it is not found |

### `todoist-find-project`

Finds a project (by name/title). [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the project to search for/create |
| `--create-if-not-found` | Create this item if it is not found |

### `todoist-export-tasks`

Export project task names as comma separated file. Returns path to

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-delete-task`

Deletes a task. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--task TASK` | Select the task to delete You can use the "retrieve_options" tool using these parameters to get the values. key: todo... |

### `todoist-delete-section`

Deletes a section. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--section SECTION` | Select a section to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-delete-project`

Deletes a project. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |

### `todoist-delete-label`

Deletes a label. [See the

| Flag | Description |
|---|---|
| `--label LABEL` | Select a label to filter results by You can use the "retrieve_options" tool using these parameters to get the values.... |

### `todoist-delete-filter`

Deletes a filter. [See the

| Flag | Description |
|---|---|
| `--filter FILTER` | Select the filter to update You can use the "retrieve_options" tool using these parameters to get the values. key: to... |

### `todoist-delete-comment`

Deletes a comment. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Project containing the comment to delete You can use the "retrieve_options" tool using these parameters to get the va... |
| `--task TASK` | Task containing the comment to delete You can use the "retrieve_options" tool using these parameters to get the value... |
| `--comment-id COMMENT_ID` | Select a comment You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-delet... |

### `todoist-create-task`

Creates a task. [See the

| Flag | Description |
|---|---|
| `--content CONTENT` | Task Content |
| `--description DESCRIPTION` | Task description |
| `--project PROJECT` | Task project. If not set, task is put to user's Inbox. You can use the "retrieve_options" tool using these parameters... |
| `--section SECTION` | The section to put task into You can use the "retrieve_options" tool using these parameters to get the values. key: t... |
| `--parent PARENT` | Parent task You can use the "retrieve_options" tool using these parameters to get the values. key: todoist-create-tas... |
| `--order ORDER` | Order in a list |
| `--labels LABELS` | Select labels to add to the task. You can use the "retrieve_options" tool using these parameters to get the values. k... |
| `--priority PRIORITY` | Task priority from 1 (normal) to 4 (urgent) |
| `--due-string DUE_STRING` | [Human defined](https://todoist.com/help/articles/205325931) task due date (ex.: "next Monday", "Tomorrow"). Value is... |
| `--due-date DUE_DATE` | Specific date in `YYYY-MM-DD` format relative to user’s timezone |
| `--due-datetime DUE_DATETIME` | Specific date and time in [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) format in UTC. |
| `--due-lang DUE_LANG` | 2-letter code specifying language in case `due_string` is not written in English |
| `--assignee ASSIGNEE` | The responsible user (if set, and only for shared tasks) You can use the "retrieve_options" tool using these paramete... |

### `todoist-create-task-comment`

Adds a comment to a task. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Project containing the task to add a comment to You can use the "retrieve_options" tool using these parameters to get... |
| `--task TASK` | Task to add new comment to You can use the "retrieve_options" tool using these parameters to get the values. key: tod... |
| `--content CONTENT` | Comment content |

### `todoist-create-section`

Creates a section. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Select a project to filter results by You can use the "retrieve_options" tool using these parameters to get the value... |
| `--name NAME` | Enter the new name |
| `--order ORDER` | Order in a list |

### `todoist-create-project`

Creates a project. [See the

| Flag | Description |
|---|---|
| `--name NAME` | Enter the new name |
| `--parent PARENT` | Optional parent project You can use the "retrieve_options" tool using these parameters to get the values. key: todois... |
| `--color COLOR` | A numeric ID representing a color (automatically converted to v1 API format). Refer to the id column in the [Colors](... |
| `--favorite` | Whether this is a favorite |

### `todoist-create-project-comment`

Adds a comment to a project. [See the

| Flag | Description |
|---|---|
| `--project PROJECT` | Project to add a comment to You can use the "retrieve_options" tool using these parameters to get the values. key: to... |
| `--content CONTENT` | Comment content |

### `todoist-create-label`

Creates a label. [See the

| Flag | Description |
|---|---|
| `--name NAME` | Enter the new name |
| `--order ORDER` | Order in a list |
| `--color COLOR` | A numeric ID representing a color (automatically converted to v1 API format). Refer to the id column in the [Colors](... |
| `--favorite` | Whether this is a favorite |

### `todoist-create-filter`

Creates a filter. [See the

| Flag | Description |
|---|---|
| `--name NAME` | Enter the new name |
| `--query QUERY` | The query to search for. [Examples of searches](https://todoist.com/help/articles/introduction-to- filters) can be fo... |
| `--color COLOR` | A numeric ID representing a color (automatically converted to v1 API format). Refer to the id column in the [Colors](... |
| `--order ORDER` | Order in a list |
| `--favorite` | Whether this is a favorite |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'todoist'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@todoist` to bypass the 1h tool-list cache.
