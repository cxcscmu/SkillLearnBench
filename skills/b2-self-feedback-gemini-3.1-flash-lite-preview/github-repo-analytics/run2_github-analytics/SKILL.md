---
name: run2_github-analytics
description: Advanced skills for fetching, filtering, and aggregating GitHub data using `gh` CLI and `jq`.
---
# Advanced GitHub Analytics

## Data Collection
Use `gh` with `--json` and `--jq` flags for efficient data retrieval.
Example: `gh pr list -R owner/repo -S "created:2024-12-01..2024-12-31" --json number,createdAt,mergedAt,author --jq .[]`

## Processing
Use `jq` to perform calculations on JSON outputs.
Example (count PRs): `gh pr list -R owner/repo --json number | jq length`

