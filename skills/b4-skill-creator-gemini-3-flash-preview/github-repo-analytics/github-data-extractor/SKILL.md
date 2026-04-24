---
name: github-data-extractor
description: Expert guidance on using the GitHub CLI (gh) to extract pull request and issue data for specific timeframes and repositories. Use this skill whenever you need to gather metrics for community reports, activity analysis, or repository health checks.
---

# GitHub Data Extractor

This skill provides optimized `gh` CLI commands and strategies for extracting pull request and issue data from GitHub repositories.

## Extracting Pull Requests

To list PRs created within a specific date range, use the `gh pr list` command with the `--search` flag.

### Command Pattern
```bash
gh pr list --repo <owner>/<repo> --limit 1000 --json <fields> --search "created:YYYY-MM-DD..YYYY-MM-DD"
```

### Key Fields for PRs
- `number`: PR identifier.
- `author`: For identifying contributors.
- `createdAt`: Creation timestamp.
- `mergedAt`: Merge timestamp (null if not merged).
- `closedAt`: Closure timestamp.
- `state`: MERGED, CLOSED, or OPEN.

### Example: PRs in December 2024
```bash
gh pr list --repo cli/cli --limit 1000 --json number,author,createdAt,mergedAt,closedAt,state --search "created:2024-12-01..2024-12-31"
```

## Extracting Issues

To list issues created within a specific date range, use the `gh issue list` command.

### Command Pattern
```bash
gh issue list --repo <owner>/<repo> --limit 1000 --json <fields> --search "created:YYYY-MM-DD..YYYY-MM-DD"
```

### Key Fields for Issues
- `number`: Issue identifier.
- `labels`: To identify bug reports.
- `createdAt`: Creation timestamp.
- `closedAt`: Closure timestamp.

### Example: Issues in December 2024
```bash
gh issue list --repo cli/cli --limit 1000 --json number,labels,createdAt,closedAt --search "created:2024-12-01..2024-12-31"
```

## Filtering for Bugs
A bug report is typically identified by labels. Use `jq` to filter issues where any label contains "bug".

```bash
# Example jq filter for bug labels
jq '[.[] | select(.labels[].name | contains("bug"))]'
```

## Best Practices
- **Pagination**: The `gh` CLI defaults to a limit of 30. Always use `--limit 1000` (or higher if needed) to ensure you capture all activity in the period.
- **Date Format**: ISO 8601 (YYYY-MM-DD) is required for search queries.
- **Rate Limiting**: For extremely large repositories, be mindful of secondary rate limits when fetching thousands of items.
