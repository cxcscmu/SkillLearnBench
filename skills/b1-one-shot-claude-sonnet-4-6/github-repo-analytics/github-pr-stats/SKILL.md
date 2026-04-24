---
name: github-pr-stats
description: Compute PR statistics (total, merged, closed, avg merge time, top contributor) from GitHub API data using Python or jq.
---

# GitHub PR Statistics

## Overview

After fetching PR data from the GitHub API, use Python or jq to compute:
- Total PR count
- Merged vs closed counts
- Average time-to-merge (days)
- Top contributor by PR count

## Fetching PRs for a Date Range

```bash
# Using gh search (handles pagination, date filtering)
gh pr list -R cli/cli \
  --search "created:2024-12-01..2024-12-31" \
  --state all \
  --limit 500 \
  --json number,author,createdAt,mergedAt,closedAt,state
```

## Python: Compute Stats from JSON

```python
import json
from datetime import datetime, timezone
from collections import Counter

# Load PR data (from gh pr list --json output)
with open('prs.json') as f:
    prs = json.load(f)

total = len(prs)

# Count merged vs closed-but-not-merged
merged = [pr for pr in prs if pr['mergedAt']]
closed = [pr for pr in prs if not pr['mergedAt'] and pr['state'] == 'CLOSED']

# Average time to merge (creation -> mergedAt), in days
def parse_dt(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

merge_days = []
for pr in merged:
    created = parse_dt(pr['createdAt'])
    merged_at = parse_dt(pr['mergedAt'])
    delta = (merged_at - created).total_seconds() / 86400
    merge_days.append(delta)

avg_merge_days = round(sum(merge_days) / len(merge_days), 1) if merge_days else 0.0

# Top contributor
authors = Counter(pr['author']['login'] for pr in prs)
top_contributor = authors.most_common(1)[0][0]

print(json.dumps({
    "total": total,
    "merged": len(merged),
    "closed": len(closed),
    "avg_merge_days": avg_merge_days,
    "top_contributor": top_contributor
}, indent=2))
```

## Notes on State Values

- `gh pr list --json` returns `state` as `"OPEN"`, `"CLOSED"`, or `"MERGED"`
- `mergedAt` is non-null only for merged PRs
- A PR with `state == "CLOSED"` and `mergedAt == null` is truly closed (not merged)

## Notes on the Search API

- `created:2024-12-01..2024-12-31` is inclusive on both ends
- Dec 31 means up to `2024-12-31T23:59:59Z`
- Use `--limit 500` to avoid truncation for active repos
