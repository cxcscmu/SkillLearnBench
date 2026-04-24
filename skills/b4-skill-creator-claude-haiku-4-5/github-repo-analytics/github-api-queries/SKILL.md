---
name: github-api-queries
description: Query GitHub API for pull requests and issues within a date range, retrieving all metadata needed for metrics collection. Use this skill whenever you need to fetch GitHub PR or issue data with date filtering, especially when gathering activity reports or computing statistics across a time period.
---

# GitHub API Queries for Metrics Collection

This skill demonstrates how to query the GitHub API for pull requests and issues using the `gh` CLI tool, extracting all necessary metadata for downstream analysis.

## Prerequisites

- `gh` CLI installed and authenticated to GitHub
- Target repository in the format `owner/repo` (e.g., `cli/cli`)
- Date range for filtering (e.g., `2024-12-01..2024-12-31`)

## Querying Pull Requests

Use `gh pr list` with date filtering to retrieve all PRs created during a period:

```bash
gh pr list --repo cli/cli \
  --state all \
  --search "created:2024-12-01..2024-12-31" \
  --json number,title,author,createdAt,mergedAt,closedAt,state \
  --limit 1000
```

**Key flags:**
- `--state all`: Includes both open and closed PRs
- `--search "created:2024-12-01..2024-12-31"`: GitHub search syntax for date ranges
- `--json`: Specify exact fields needed (number, author, timestamps, state)
- `--limit 1000`: Fetch up to 1000 results (pagination handled by `gh`)

**Important fields for metrics:**
- `number`: PR identifier
- `author`: Object with `login` field for contributor tracking
- `createdAt`: ISO timestamp for PR creation
- `mergedAt`: ISO timestamp for merge (null if not merged)
- `closedAt`: ISO timestamp for closure (null if still open)
- `state`: OPEN, CLOSED, or MERGED

## Querying Issues

Use `gh issue list` for issues:

```bash
gh issue list --repo cli/cli \
  --state all \
  --search "created:2024-12-01..2024-12-31" \
  --json number,title,labels,createdAt,closedAt,state \
  --limit 1000
```

**Key fields for metrics:**
- `labels`: Array of label objects with `name` field (use for bug detection)
- `closedAt`: Timestamp for closure (null if still open)

## Error Handling

If `gh` returns a rate limit error, wait and retry:
```bash
# Check remaining API quota
gh api rate_limit
```

If authentication fails, ensure:
```bash
gh auth status
```

## Output Format

Both queries return JSON arrays. Each item includes the fields specified in `--json`. Example PR object:

```json
{
  "number": 12345,
  "title": "Add feature X",
  "author": {
    "login": "octocat"
  },
  "createdAt": "2024-12-05T14:30:00Z",
  "mergedAt": "2024-12-10T16:45:00Z",
  "closedAt": null,
  "state": "MERGED"
}
```

## Date Format

All timestamps use ISO 8601 format (UTC). For calculations, parse with standard datetime libraries:
- Python: `datetime.fromisoformat()`
- JavaScript: `new Date()` or `Date.parse()`
- Bash: Convert via epoch for arithmetic

## Tips for Reliability

- Always use `--limit 1000` or higher to ensure all results are captured (verify count matches expectation)
- Dates must use `YYYY-MM-DD` format in search queries
- Include both endpoints of the range (results are inclusive of both dates)
- When comparing timestamps, ensure consistent timezone handling (all GitHub timestamps are UTC)
