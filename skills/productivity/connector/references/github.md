
# GitHub (via Higgsfield MCP proxy)

Issues, PRs, repos, files, comments, workflow runs. Exposes 32 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @github <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @github --list                    # all 32 tools
./bin/mcp2cli @github github-list-repositories --help   # inspect one
./bin/mcp2cli @github github-list-repositories --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @github --pretty <cmd>` — `--pretty` goes AFTER `@github`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @github --head N <cmd>` — `--head N` goes AFTER `@github`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 32 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `github-list-repositories`

List repositories that the authenticated user has access to. [See the

| Flag | Description |
|---|---|
| `--name NAME` | Case-insensitive substring match on repository name. Example: `api` matches `payments-api` and `internal- api-tools`. |
| `--visibility {all,public,private}` | Limit results to repositories with the specified visibility |
| `--affiliation AFFILIATION` | Limit results to repositories with the specified affiliation (JSON array) |
| `--type {all,owner,public,private,member}` | Limit results to repositories of the specified type. Not for use with `visibility` or `affiliation`. |
| `--sort {created,updated,pushed,full_name}` | The field to sort the results by |
| `--direction {asc,desc}` | The direction to sort the results by |
| `--since SINCE` | Only show repositories updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM- DDTHH:MM:SSZ. |
| `--before BEFORE` | Only show repositories updated before the given time. This is a timestamp in ISO 8601 format: YYYY-MM- DDTHH:MM:SSZ. |

### `github-update-pull-request`

Updates an existing pull request with new title, body, state, or base

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The repository where the pull request exists. You can use the "retrieve_options" tool using these parameters to get t... |
| `--pull-number PULL_NUMBER` | The number of the pull request to update. You can use the "retrieve_options" tool using these parameters to get the v... |
| `--title TITLE` | The title of the pull request. |
| `--body BODY` | The contents of the pull request body. Supports markdown. |
| `--state {open,closed}` | The desired state of the pull request. |
| `--base BASE` | The name of the branch you want your changes pulled into. This should be an existing branch on the current repository... |
| `--maintainer-can-modify` | Indicates whether [maintainers can modify](https://docs.github.com/articles/allowing- changes-to-a-pull-request-branc... |

### `github-update-project-v2-item-status`

Update the status of an item in the selected Project (V2). [See the

| Flag | Description |
|---|---|
| `--org ORG` | The name of the GitHub organization (not case sensitive). You can use the "retrieve_options" tool using these paramet... |
| `--repo REPO` | The repository in a organization You can use the "retrieve_options" tool using these parameters to get the values. ke... |
| `--project PROJECT` | The project (V2) in a repository You can use the "retrieve_options" tool using these parameters to get the values. ke... |
| `--item ITEM` | The project item to update You can use the "retrieve_options" tool using these parameters to get the values. key: git... |
| `--status STATUS` | The status to set for the item You can use the "retrieve_options" tool using these parameters to get the values. key:... |
| `--move-to-top` | If true, moves the item to the top of the column instead of the bottom. |

### `github-update-issue`

Update a new issue in a GitHub repo. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--issue-number ISSUE_NUMBER` | The number that identifies the issue. You can use the "retrieve_options" tool using these parameters to get the value... |
| `--title TITLE` | The title of the issue |
| `--body BODY` | The text body of the issue |

### `github-update-gist`

Allows you to update a gist's description and to update, delete, or

| Flag | Description |
|---|---|
| `--gist-id GIST_ID` | The Gist Id to perform your action You can use the "retrieve_options" tool using these parameters to get the values. ... |
| `--description DESCRIPTION` | The description of the gist |
| `--files FILES` | The gist files to be updated, renamed, or deleted. Each key must match the current filename (including extension) of ... |

### `github-sync-fork-branch-with-upstream`

Sync a forked branch with the upstream branch. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--branch BRANCH` | The branch to sync with the upstream repository You can use the "retrieve_options" tool using these parameters to get... |

### `github-star-repo`

Star a repository. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |

### `github-search-issues-and-pull-requests`

Find issues and pull requests by state and keyword. [See the

| Flag | Description |
|---|---|
| `--query QUERY` | The query contains one or more search keywords and qualifiers. [See the documentation](https://docs.github.com/en/sea... |
| `--max-results MAX_RESULTS` | The maximum amount of items to retrieve |

### `github-list-workflow-runs`

List workflowRuns for a repository [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--limit LIMIT` | The maximum quantity to be returned. |

### `github-list-releases`

List releases for a repository [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |

### `github-list-organizations`

List all organizations in the authenticated user's account. [See the

_No flags._

### `github-list-organization-repositories`

List repositories for an organization. [See the

| Flag | Description |
|---|---|
| `--org ORG` | The name of the GitHub organization (not case sensitive). You can use the "retrieve_options" tool using these paramet... |
| `--type {all,public,private,forks,sources,member}` | Limit results to repositories of the specified type |
| `--sort {created,updated,pushed,full_name}` | The field to sort the results by |
| `--direction {asc,desc}` | The direction to sort the results by |

### `github-list-gists-for-a-user`

Lists public gists for the specified user. [See the

| Flag | Description |
|---|---|
| `--since SINCE` | Only show notifications updated since the given time. This should be a timestamp in ISO 8601 format, e.g. `2018-05-16... |

### `github-list-commits`

List commits in a GitHub repo. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--sha SHA` | SHA or branch to start listing commits from. Default: the repository's default branch (usually main). You can use the... |
| `--path PATH` | Only commits containing this file path will be returned |
| `--author AUTHOR` | GitHub username or email address to use to filter by commit author. |
| `--committer COMMITTER` | GitHub username or email address to use to filter by commit committer |
| `--since SINCE` | Only show results that were last updated after the given time. This is a timestamp in ISO 8601 format: `YYYY-MM-DDTHH... |
| `--until UNTIL` | Only commits before this date will be returned. This is a timestamp in ISO 8601 format: `YYYY-MM- DDTHH:MM:SSZ` |
| `--max-results MAX_RESULTS` | The maximum number of results to return. Defaults: `100` |

### `github-get-workflow-run`

Gets a specific workflow run. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--workflow-run-id WORKFLOW_RUN_ID` | The Id of the workflow Run. You can use the "retrieve_options" tool using these parameters to get the values. key: gi... |

### `github-get-reviewers`

Get reviewers for a PR ([see

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--pr-or-commit {Pull Request,Commit SHA}` | Whether to get reviewers for a [pull request](https:// docs.github.com/en/rest/pulls/reviews#list-reviews- for-a-pull... |
| `--review-states REVIEW_STATES` | Filter by these review states (JSON array) |

### `github-get-repository`

Get information for a specific repository. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |

### `github-get-repository-content`

Get the content of a file or directory in a specific repository. [See

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--path PATH` | The file path or directory to retrieve. Defaults to the repository's root directory. |
| `--media-type {application/vnd.github.raw+json,application/vnd.github.html+json,application/vnd.github.object+json}` | The media type of the response. [See the documentation ](https://docs.github.com/en/rest/repos/contents?apiVe rsion=2... |
| `--branch BRANCH` | The branch to use. Defaults to the repository's default branch (usually `main` or `master`) You can use the "retrieve... |

### `github-get-issue`

Get details of an issue in a GitHub repository. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--issue-number ISSUE_NUMBER` | The issue number You can use the "retrieve_options" tool using these parameters to get the values. key: github-get-is... |

### `github-get-issue-assignees`

Get assignees for an issue in a GitHub repo. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--issue-number ISSUE_NUMBER` | The number that identifies the issue. You can use the "retrieve_options" tool using these parameters to get the value... |

### `github-get-current-user`

Gather a full snapshot of the authenticated GitHub actor, combining

_No flags._

### `github-get-commit`

Get a commit in a GitHub repo. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--commit-sha COMMIT_SHA` | A commit SHA to retrieve You can use the "retrieve_options" tool using these parameters to get the values. key: githu... |

### `github-enable-workflow`

Enables a workflow and sets the **state** of the workflow to

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--workflow-id WORKFLOW_ID` | The Id of the workflow. You can use the "retrieve_options" tool using these parameters to get the values. key: github... |

### `github-disable-workflow`

Disables a workflow and sets the **state** of the workflow to

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--workflow-id WORKFLOW_ID` | The Id of the workflow. You can use the "retrieve_options" tool using these parameters to get the values. key: github... |

### `github-create-workflow-dispatch`

Creates a new workflow dispatch event. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--workflow-id WORKFLOW_ID` | The Id of the workflow. You can use the "retrieve_options" tool using these parameters to get the values. key: github... |
| `--ref REF` | The git reference for the workflow. The reference can be a branch or tag name. |
| `--inputs INPUTS` | Input keys and values configured in the workflow file. The maximum number of properties is 10. Any default properties... |

### `github-create-repository`

Creates a new repository for the authenticated user. [See the

| Flag | Description |
|---|---|
| `--name NAME` | The name of the repository. |
| `--team-id TEAM_ID` | The id of the team that will be granted access to this repository. This is only valid when creating a repository in a... |
| `--description DESCRIPTION` | A short description of the repository. |
| `--homepage HOMEPAGE` | A URL with more information about the repository. |
| `--private` | Whether the repository is private. |
| `--has-issues` | Whether issues are enabled. |
| `--has-projects` | Whether projects are enabled. |
| `--has-wiki` | Whether the wiki is enabled. |
| `--has-discussions` | Whether discussions are enabled. |
| `--auto-init` | Whether the repository is initialized with a minimal README. |
| `--has-downloads` | Whether downloads are enabled. |
| `--is-template` | Whether this repository acts as a template that can be used to generate new repositories. |

### `github-create-pull-request`

Creates a new pull request for a specified repository. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The base repository, where the pull request will be created. You can use the "retrieve_options" tool using these para... |
| `--base BASE` | The base branch, where the changes will be received. You can use the "retrieve_options" tool using these parameters t... |
| `--head-repo HEAD_REPO` | The head repository, where the changes originate from. This can, but does not have to, be the same repository. You ca... |
| `--head HEAD` | The head branch, where the changes originate from You can use the "retrieve_options" tool using these parameters to g... |
| `--body BODY` | The text description of the pull request. |
| `--maintainer-can-modify` | Indicates whether [maintainers can modify](https://docs.github.com/articles/allowing- changes-to-a-pull-request-branc... |
| `--draft` | Indicates whether the pull request is a draft. See "[Draft Pull Requests](https://docs.github.com/articles/about-pull... |
| `--title TITLE` | The title of the pull request. |
| `--issue ISSUE` | An issue in the repository to convert to a pull request. The issue title, body, and comments will become the title, b... |

### `github-create-or-update-file-contents`

Create or update a file in a repository. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--path PATH` | The full path of the file to create. *If the file already exists, it will be updated.* Example: `path/to/file.txt` |
| `--file-content FILE_CONTENT` | The raw contents of the file. *If the file already exists, the entire file will be overwritten.* |
| `--commit-message COMMIT_MESSAGE` | The commit message for this change. |
| `--branch BRANCH` | The branch to use. Defaults to the repository's default branch (usually `main` or `master`) You can use the "retrieve... |

### `github-create-issue`

Create a new issue in a GitHub repo. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--title TITLE` | The title of the issue |
| `--body BODY` | The text body of the issue |

### `github-create-issue-comment`

Create a new comment in a issue. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--issue-number ISSUE_NUMBER` | The number that identifies the issue. You can use the "retrieve_options" tool using these parameters to get the value... |
| `--body BODY` | The contents of the comment |

### `github-create-gist`

Allows you to add a new gist with one or more files. [See the

| Flag | Description |
|---|---|
| `--description DESCRIPTION` | The description of the gist |
| `--files FILES` | The files that will be added to the gist. The key is the file name and the value is the content of the file. Ex: `{"f... |
| `--public` | Indicates whether the gist is public or not |

### `github-create-branch`

Create a new branch in a GitHub repo. [See the

| Flag | Description |
|---|---|
| `--repo-fullname REPO_FULLNAME` | The name of the repository (not case sensitive). The format should be `owner/repo` (for example, `PipedreamHQ/pipedre... |
| `--branch-name BRANCH_NAME` | The name of the new branch that will be created |
| `--branch-sha BRANCH_SHA` | The source branch that will be used to create the new branch. Defaults to the repository's default branch (usually `m... |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'github'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@github` to bypass the 1h tool-list cache.
