---
name: github-cli-queries
description: Query GitHub repositories for PRs and issues using gh CLI with date filtering and structured output.
---

# GitHub CLI Query Skill

## Overview
Use the `gh` CLI tool to efficiently query GitHub pull requests and issues with filtering, date range support, and structured JSON output.

## Installation & Setup
```bash
# gh CLI is typically pre-installed on most systems
gh --version

# Ensure you're authenticated
gh auth status

# If not authenticated
gh auth login
```

## Basic Patterns

### Query Pull Requests by Date Range
```bash
# List PRs created in December 2024 with JSON output
gh pr list --repo cli/cli --state all --created "2024-12-01..2024-12-31" --json number,title,createdAt,mergedAt,closedAt,author --limit 500

# Key fields in JSON output:
# - number: PR number
# - title: PR title
# - createdAt: when PR was created (ISO 8601)
# - mergedAt: when PR was merged (null if not merged)
# - closedAt: when PR was closed (null if still open)
# - author: {login: string, name: string}
```

### Query Issues by Date Range
```bash
# List issues created in December 2024
gh issue list --repo cli/cli --state all --created "2024-12-01..2024-12-31" --json number,title,createdAt,closedAt,labels --limit 500

# Key fields:
# - number: issue number
# - title: issue title
# - createdAt: when issue was created (ISO 8601)
# - closedAt: when issue was closed (null if still open)
# - labels: array of label objects with name and description
```

## Date Format
- Use ISO 8601 format: `YYYY-MM-DD`
- Date ranges: `YYYY-MM-DD..YYYY-MM-DD`
- The range is inclusive on both ends

## State Filtering
- `--state all`: Include open, closed, and merged (for PRs)
- `--state open`: Only open items
- `--state closed`: Only closed items (for issues) or merged/closed (for PRs)

## Common Flags
- `--limit N`: Set maximum results (default 30, max typically 500)
- `--json <fields>`: Request specific fields as JSON
- `--repo owner/repo`: Specify repository

## Date Parsing Tips
- Always capture both `createdAt` and `mergedAt`/`closedAt` to calculate deltas
- Handle null values when calculating metrics
- Parse ISO 8601 timestamps in your processing language

## Example: Full PR Data Export
```bash
gh pr list --repo cli/cli --state all --created "2024-12-01..2024-12-31" \
  --json number,title,createdAt,mergedAt,closedAt,author,labels \
  --limit 500 > prs.json
```

## Performance Notes
- Large result sets (500+ items) may take time to process
- Use `--limit` to control result size
- JSON output is faster than parsing text output
- Paginate if needed by using multiple queries with different date ranges
