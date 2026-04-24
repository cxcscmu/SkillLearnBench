---
name: gh-data-gathering
description: How to gather PR and issue data from a GitHub repository using the gh CLI for monthly reports. Use this skill whenever you need to fetch monthly metrics from a repository.
---

## Overview
This skill provides instructions for querying GitHub repositories using the `gh` CLI.

## Commands
- **Search PRs**: `gh pr list --repo cli/cli --created 2024-12-01..2024-12-31 --json number,title,state,createdAt,mergedAt --limit 1000`
- **Search Issues**: `gh issue list --repo cli/cli --created 2024-12-01..2024-12-31 --json number,labels,state,createdAt,closedAt --limit 1000`

## Data Handling
- Ensure you set a high `--limit` to capture all activities for the month.
- The `--json` flag is required for structured output.
