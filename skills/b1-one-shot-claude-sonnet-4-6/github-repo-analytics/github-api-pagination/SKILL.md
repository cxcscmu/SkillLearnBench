---
name: github-api-pagination
description: How to use `gh api` with pagination to retrieve all results from GitHub REST API endpoints, including PRs and issues.
---

# GitHub API Pagination with `gh api`

## Overview

GitHub REST API returns paginated results (default 30, max 100 per page). Use `gh api` with `--paginate` to automatically fetch all pages.

## Basic Usage

```bash
# Fetch all pages automatically
gh api --paginate /repos/OWNER/REPO/pulls \
  -X GET \
  -f state=all \
  -f per_page=100

# Use GraphQL for complex queries (no pagination needed for small sets)
gh api graphql -f query='...'
```

## REST API: List PRs with Date Filtering

```bash
# Get all PRs created in December 2024 (state=all includes open/closed/merged)
gh api --paginate \
  "repos/cli/cli/pulls?state=all&per_page=100&sort=created&direction=desc" \
  --jq '.[] | select(.created_at >= "2024-12-01T00:00:00Z" and .created_at < "2025-01-01T00:00:00Z")'
```

> Note: `--jq` applies a jq filter to each page's output.

## REST API: List Issues with Date Filtering

```bash
gh api --paginate \
  "repos/cli/cli/issues?state=all&per_page=100&sort=created&direction=desc" \
  --jq '.[] | select(.pull_request == null)'  # exclude PRs from issues endpoint
```

## Search API (Efficient for Date Ranges)

The Search API is better for date-bounded queries:

```bash
# PRs created in Dec 2024
gh api --paginate \
  "search/issues?q=repo:cli/cli+is:pr+created:2024-12-01..2024-12-31&per_page=100" \
  --jq '.items[]'

# Issues created in Dec 2024
gh api --paginate \
  "search/issues?q=repo:cli/cli+is:issue+created:2024-12-01..2024-12-31&per_page=100" \
  --jq '.items[]'
```

## Combining Pages into a Single JSON Array

```bash
# Collect all pages into a single JSON array using --paginate + jq slurp
gh api --paginate \
  "repos/cli/cli/pulls?state=all&per_page=100" \
  --jq '.[]' | jq -s '.'
```

## Key Fields

| Field | Description |
|-------|-------------|
| `created_at` | ISO8601 timestamp when PR/issue was created |
| `merged_at` | ISO8601 timestamp when PR was merged (null if not merged) |
| `closed_at` | ISO8601 timestamp when PR/issue was closed |
| `state` | `open`, `closed` |
| `pull_request.merged_at` | For search API results |
| `labels[].name` | Array of label objects with `name` field |
| `user.login` | Author's GitHub username |

## Rate Limits

- REST API: 5000 requests/hour (authenticated)
- Search API: 30 requests/minute (authenticated)
- Use `gh api -i` to see rate limit headers
