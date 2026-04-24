---
name: gh-analytics
description: "Skills for querying GitHub API data using the `gh` CLI, specifically for extracting PR and issue metrics."
---

# GitHub Analytics with `gh` CLI

Use `gh` to retrieve data from GitHub.

## PRs
- List PRs: `gh pr list --state all --json number,title,author,createdAt,closedAt,mergedAt,labels --limit 1000 --created 2024-12-01..2024-12-31`

## Issues
- List Issues: `gh issue list --state all --json number,labels,createdAt,closedAt --limit 1000 --created 2024-12-01..2024-12-31`
