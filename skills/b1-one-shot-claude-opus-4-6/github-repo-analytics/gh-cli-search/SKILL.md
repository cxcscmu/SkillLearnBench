---
name: gh-cli-search
description: Using the gh CLI to search and list GitHub issues and pull requests with date filters and label queries.
---

# GitHub CLI: Searching Issues and Pull Requests

## Overview
The `gh` CLI provides powerful commands for listing and searching issues and PRs in any public repository. Key subcommands: `gh pr list`, `gh issue list`, and `gh search` variants.

## Listing PRs by Date Range

```bash
# List PRs created in a date range (returns up to --limit items)
gh pr list --repo owner/repo --state all --search "created:2024-12-01..2024-12-31" --limit 500 --json number,state,author,createdAt,mergedAt,closedAt
```

Key flags:
- `--state all` includes open, closed, and merged PRs
- `--search` accepts GitHub search qualifiers like `created:YYYY-MM-DD..YYYY-MM-DD`
- `--json` selects fields; available fields include: `number`, `state`, `author`, `createdAt`, `mergedAt`, `closedAt`, `title`, `labels`
- `--limit N` controls max results (default 30)

## Listing Issues by Date Range

```bash
# List issues created in a date range
gh issue list --repo owner/repo --state all --search "created:2024-12-01..2024-12-31" --limit 500 --json number,state,labels,createdAt,closedAt
```

Note: `gh issue list` excludes pull requests by default.

## Searching with Labels

```bash
# Search for issues with a label containing "bug"
gh issue list --repo owner/repo --state all --search "created:2024-12-01..2024-12-31 label:bug" --limit 500 --json number,state,labels,closedAt
```

For labels with spaces or special characters, quote them: `label:"type: bug"`.

## Pagination / Limits
- The `--limit` flag can go up to 1000 per call.
- For very large result sets, paginate using `gh api` with `--paginate`.

## Using `gh api` for More Control

```bash
# Direct API call with search endpoint
gh api search/issues --method GET \
  -f q='repo:owner/repo is:pr created:2024-12-01..2024-12-31' \
  -f per_page=100 \
  --paginate
```
