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
gh issue list --assignee thersgo
```

## Milestones

| Milestone | Description |
|-----------|-------------|
| Project Foundation (M0) | Infrastructure, coding standards, documentation, tooling |
| Terminology Database (M1) | Foundation for everything. Collects, organizes, and manages translation terms |

### Milestone 1 Phases

| Label | Description |
|-------|-------------|
| `1a-glossary-sources` | Phase 1A: Glossary Sources (EN) - WSO materials |
| `1b-estonian-translations` | Phase 1B: Add Estonian translations from dictionaries |
| `1c-atl-translations` | Phase 1C: Extract from existing ATL translations |
| `1d-collaboration` | Phase 1D: Collaboration opportunities (optional) |

## Other

| Label | Description |
|-------|-------------|
| `wontfix` | This will not be worked on |

## Usage

Issues can have multiple labels combined, e.g.:
- `1a-glossary-sources` + `wf-in-progress`

### CLI Examples

```bash
# List my issues
gh issue list --assignee @me

# List in-progress issues
gh issue list --label "wf-in-progress"

# List Phase 1A issues
gh issue list --label "1a-glossary-sources"

# List by milestone
gh issue list --milestone "Terminology Database"
```
