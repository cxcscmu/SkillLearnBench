---
name: jq-data-processing
description: Process JSON data from GitHub CLI using jq to calculate metrics like average merge times, counts, and top contributors.
---

# JQ Data Processing for Repo Stats

This skill provides `jq` patterns for common repository metrics calculations.

## Common Patterns

### Counting and Filtering
Count total items:
```bash
jq 'length' data.json
```

Filter for merged PRs:
```bash
jq '[.[] | select(.mergedAt != null)]' prs.json
```

### Calculating Average Merge Time
Compute average merge time in days (assuming `createdAt` and `mergedAt` are ISO8601 strings):
```bash
jq '[.[] | select(.mergedAt != null) | ((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400] | add / length | round * 10 / 10' prs.json
```
*Note: Dividing by 86400 converts seconds to days.*

### Finding Top Contributor
Identify the author with the most entries:
```bash
jq -r '[.[] | .author.login] | group_by(.) | sort_by(-length) | .[0][0]' prs.json
```

### Complex Label Search
Count items where any label contains "bug":
```bash
jq '[.[] | select(.labels[].name | contains("bug"))] | length' issues.json
```
