---
name: time-to-merge-analysis
description: Calculate average time-to-merge from PR creation to merge timestamps, handling edge cases like unmerged and closed PRs. Use this skill whenever computing PR velocity metrics, measuring merge turnaround, or analyzing PR lifecycle duration.
---

# Time-to-Merge Analysis

Calculate the average time it takes for pull requests to be merged from creation time.

## Calculation Overview

**Time-to-merge** is defined as the elapsed time between PR creation and merge, measured in days.

```
time_to_merge_days = (mergedAt - createdAt) / 86400  # seconds per day
```

## Algorithm

1. **Filter**: Include only PRs where `state == "MERGED"` and `mergedAt` is not null
2. **Calculate**: For each merged PR, compute `(mergedAt - createdAt)` in days
3. **Average**: Sum all durations and divide by count
4. **Round**: Round to one decimal place (e.g., 3.7 days)

## Example Calculation

Given three merged PRs:
```
PR #1: created 2024-12-01 10:00, merged 2024-12-03 14:00 → 2.17 days
PR #2: created 2024-12-05 09:00, merged 2024-12-06 17:00 → 1.33 days
PR #3: created 2024-12-10 12:00, merged 2024-12-12 12:00 → 2.00 days

Average: (2.17 + 1.33 + 2.00) / 3 = 1.8 days
```

## Implementation (Python)

```python
from datetime import datetime
from typing import List, Dict

def calculate_avg_merge_days(prs: List[Dict]) -> float:
    """
    Args:
        prs: List of PR objects from GitHub API with createdAt, mergedAt, state

    Returns:
        Average time-to-merge in days, rounded to 1 decimal place
    """
    merged_prs = [pr for pr in prs if pr['state'] == 'MERGED' and pr.get('mergedAt')]

    if not merged_prs:
        return 0.0

    total_days = 0
    for pr in merged_prs:
        created = datetime.fromisoformat(pr['createdAt'].replace('Z', '+00:00'))
        merged = datetime.fromisoformat(pr['mergedAt'].replace('Z', '+00:00'))
        days = (merged - created).total_seconds() / 86400
        total_days += days

    average = total_days / len(merged_prs)
    return round(average, 1)
```

## Edge Cases

- **Unmerged PRs**: Filter these out; they have no `mergedAt` timestamp
- **Closed without merge**: These have `state == "CLOSED"` and no `mergedAt`; exclude them
- **Same-day merges**: Valid; results in ~0.0 days (or small fraction)
- **Very fast merges**: PRs merged within minutes are normal; round appropriately

## Implementation (Bash)

If using `jq` to process JSON from `gh`:

```bash
jq -r '.[] | select(.state == "MERGED") |
  (((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400) ' \
  prs.json | \
  awk '{sum+=$1; count++} END {if(count>0) printf "%.1f\n", sum/count}'
```

## Verification

Before finalizing:
- Confirm count of merged PRs matches the "merged" count from other metrics
- Spot-check 2-3 calculations manually to ensure timestamp parsing is correct
- Verify no division-by-zero when count is 0 (return 0.0 in that case)
