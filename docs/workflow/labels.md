# GitHub Labels

## Workflow (`wf-`)

Labels for tracking issue status:

| Label | Description |
|-------|-------------|
| `wf-backlog` | Ideas and future tasks |
| `wf-todo` | Ready to start |
| `wf-in-progress` | Currently being worked on |
| `wf-done` | Completed |

## Type (`t-`)

Labels for categorizing issues:

| Label | Description |
|-------|-------------|
| `t-bug` | Something isn't working |
| `t-enhancement` | New feature or request |
| `t-documentation` | Improvements or additions to documentation |
| `t-question` | Further information is requested |
| `t-code-quality` | Code refactoring, DRY principles, maintainability |
| `t-data-quality` | Issues related to data quality and consistency |

## Assignee

Use GitHub's built-in assignee feature (not labels).

```bash
gh issue list --assignee @me
gh issue list --assignee henri-klimt
```

## Milestones

| Label | Description |
|-------|-------------|
| `m1-terminology-database` | Milestone 1: Terminology Database |

### Milestone 1 Phases

| Label | Description |
|-------|-------------|
| `1a-collect-eki-terminology` | Collect terminology from EKI databases |
| `1b-match-glossary` | Match Glossary terms with EKI terminology |
| `1c-extract-daily-texts` | Extract terminology from daily meditation texts |
| `1d-collaboration` | Collaboration opportunities (optional) |

## Other

| Label | Description |
|-------|-------------|
| `wontfix` | This will not be worked on |

## Usage

Issues can have multiple labels combined, e.g.:
- `m1-terminology-database` + `1a-collect-eki-terminology` + `wf-in-progress`

### CLI Examples

```bash
# List my issues
gh issue list --assignee @me

# List in-progress issues
gh issue list --label "wf-in-progress"

# List Milestone 1 issues
gh issue list --label "m1-terminology-database"
```
