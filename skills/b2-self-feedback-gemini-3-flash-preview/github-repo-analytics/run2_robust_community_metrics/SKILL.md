---
name: run2_robust_community_metrics
description: Robust Python logic for community pulse metrics with substring label matching and precise PR status handling.
---

# Robust Community Metrics

This skill focuses on precision and robustness when calculating metrics from GitHub JSON data.

## Substring Label Matching (The "Bug" Filter)

To follow the requirement of matching any label containing a substring:
```python
def is_bug_report(issue, substring='bug'):
    return any(substring in label['name'].lower() for label in issue.get('labels', []))
```

## Precise PR Status (Merged vs. Closed)

In GitHub, a PR can be `open` or `closed`. A `closed` PR might be `merged`.
- **Merged**: `pull_request.merged_at` is not null.
- **Closed (Unmerged)**: `state == "closed"` AND `pull_request.merged_at` is null.

## Time-to-Merge Calculation

Always use `datetime.fromisoformat` and handle UTC offsets (replacing 'Z' with '+00:00').
```python
def get_merge_days(created_at_str, merged_at_str):
    created = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
    merged = datetime.fromisoformat(merged_at_str.replace('Z', '+00:00'))
    return (merged - created).total_seconds() / (24 * 3600)
```

## Handling Large Data Sets

When dealing with more than 100 items, ensure the processing script can merge multiple JSON files or handle an array of items.
