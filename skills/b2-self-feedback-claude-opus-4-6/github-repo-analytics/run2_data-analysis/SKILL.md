---
name: run2_data-analysis
description: Using jq to compute statistics from GitHub API JSON responses including counts, averages, grouping, and label filtering.
---

# Data Analysis with jq for GitHub Metrics

## Counting by state
```bash
# Merged PRs (search API): closed + has merged_at
jq '[.[] | select(.pull_request.merged_at != null)] | length'

# Closed-not-merged PRs
jq '[.[] | select(.state == "closed" and .pull_request.merged_at == null)] | length'
```

## Average time-to-merge (days, 1 decimal)
```bash
jq '[.[] | select(.pull_request.merged_at != null) |
  ((.pull_request.merged_at | fromdateiso8601) - (.created_at | fromdateiso8601)) / 86400] |
  (add / length) * 10 | round / 10'
```

## Top contributor by PR count
```bash
jq '[.[] | .user.login] | group_by(.) | map({user: .[0], count: length}) | sort_by(-.count) | .[0].user'
```

## Label substring matching (case-insensitive)
```bash
# Match any label containing "bug" (case-insensitive)
jq '[.[] | select(.labels | map(.name | ascii_downcase) | any(contains("bug")))]'
```

## Filtering by closed_at date range
```bash
# Issues closed during a specific month
jq '[.[] | select(.closed_at != null and (.closed_at >= "2024-12-01") and (.closed_at < "2025-01-01"))]'
```

## Notes on date comparison in jq
- ISO 8601 strings sort lexicographically, so string comparison works for date ranges
- `fromdateiso8601` converts to epoch seconds for arithmetic
- Round to 1 decimal: `* 10 | round / 10`
