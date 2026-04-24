---
name: gh-activity-query
description: >
  Query GitHub repository activity (PRs, issues) for a date range using the gh CLI.
  Use this skill whenever you need to fetch pull request or issue data from a GitHub
  repository, compute statistics like counts, merge times, or identify top contributors.
  Triggers on tasks involving GitHub activity reports, community pulse summaries, or
  repository metrics gathering.
---

# GitHub Activity Query

Fetch and analyze pull request and issue data from GitHub repositories using the `gh` CLI.

## Pull Request Queries

### List PRs created in a date range

```bash
gh pr list --repo OWNER/REPO --state all --search "created:YYYY-MM-DD..YYYY-MM-DD" \
  --json number,author,createdAt,mergedAt,closedAt,state --limit 300
```

- `--state all` includes open, closed, and merged PRs.
- `--search` uses GitHub search qualifiers; `created:START..END` filters by creation date.
- `--json` selects fields; `author` returns `{login}`, `state` is `OPEN|CLOSED|MERGED`.
- `--limit` defaults to 30; raise it to capture all results for busy repos.

### Counting and classifying PRs

- **Total**: length of the result array.
- **Merged**: items where `state == "MERGED"` (or `mergedAt` is non-null).
- **Closed (not merged)**: items where `state == "CLOSED"` and `mergedAt` is null.
- **Time-to-merge**: difference between `mergedAt` and `createdAt` in days.

### Top contributor

Group by `author.login`, count PRs per author, pick the one with the highest count.

## Issue Queries

### List issues created in a date range

```bash
gh issue list --repo OWNER/REPO --state all --search "created:YYYY-MM-DD..YYYY-MM-DD" \
  --json number,labels,createdAt,closedAt,state --limit 300
```

- Labels come as `[{name, ...}]`; check if any label's `name` contains the substring `bug` (case-insensitive).

### Bug detection

A bug report is any issue where at least one label's name contains the substring `bug`.

### Resolved bugs

A bug is "resolved" if it is a bug report AND its `closedAt` falls within the target month (or it has `state == "CLOSED"` if checking as-of-now status). Clarify the definition with the requester — "closed during the month" vs "closed as of today".

## Pagination

The `gh` CLI `--limit` flag controls how many results to return. For months with heavy activity, use `--limit 500` or higher. If the result count equals the limit exactly, there may be more results — increase the limit and re-run.
