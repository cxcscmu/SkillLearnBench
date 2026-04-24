---
name: run2_gh-pr-analysis
description: How to compute PR statistics (merged, closed, avg_merge_days, top_contributor) from GitHub Search API items using Python.
---

# GitHub PR Analysis from Search API Results

## Input Format
Each PR item from `/search/issues` has:
- `state`: `"open"` or `"closed"` (merged PRs are also `"closed"`)
- `created_at`: ISO 8601 string e.g. `"2024-12-05T10:00:00Z"`
- `pull_request.merged_at`: timestamp string or `null`
- `user.login`: author username

## Classifying PRs

```python
def classify_prs(prs):
    merged, closed, open_prs = [], [], []
    for pr in prs:
        pr_field = pr.get("pull_request") or {}
        merged_at = pr_field.get("merged_at")
        if merged_at:
            merged.append({**pr, "_merged_at": merged_at})
        elif pr["state"] == "closed":
            closed.append(pr)
        else:
            open_prs.append(pr)
    return merged, closed, open_prs
```

## Average Merge Time (days, rounded to 1 decimal)

```python
from datetime import datetime, timezone

def parse_dt(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

def avg_merge_days(merged_prs):
    if not merged_prs:
        return 0.0
    diffs = []
    for pr in merged_prs:
        pr_field = pr.get("pull_request") or {}
        merged_at = pr_field.get("merged_at")
        created_at = pr.get("created_at")
        if merged_at and created_at:
            delta = (parse_dt(merged_at) - parse_dt(created_at)).total_seconds() / 86400
            diffs.append(delta)
    return round(sum(diffs) / len(diffs), 1) if diffs else 0.0
```

## Top Contributor

```python
from collections import Counter

def top_contributor(prs):
    authors = Counter(pr["user"]["login"] for pr in prs if pr.get("user"))
    return authors.most_common(1)[0][0] if authors else "unknown"
```

## Key Distinction: "closed" means unmerged+closed
- `merged`: `pull_request.merged_at is not null`
- `closed`: `state == "closed"` AND `pull_request.merged_at is null`
- These two are mutually exclusive and exhaustive for closed PRs.
