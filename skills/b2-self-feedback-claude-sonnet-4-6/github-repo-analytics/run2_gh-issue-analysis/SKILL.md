---
name: run2_gh-issue-analysis
description: How to identify bug report issues and count resolved bugs in a date range from GitHub Search API results.
---

# GitHub Issue Analysis: Bug Detection and Resolution

## Bug Report Detection
A bug report = issue with at least one label whose name contains the substring "bug" (case-insensitive).

Labels from the Search API are returned as objects:
```json
"labels": [{"id": 1234, "name": "type: bug", "color": "d73a4a", ...}]
```

```python
def is_bug_report(issue):
    """Returns True if any label name contains 'bug' (case-insensitive)."""
    labels = issue.get("labels", [])
    return any("bug" in lbl.get("name", "").lower() for lbl in labels)
```

## Counting Resolved Bugs
"Resolved bugs" = bug report issues (created in the month) that were **closed** during the same month.

```python
MONTH_START = "2024-12-01T00:00:00Z"
MONTH_END   = "2025-01-01T00:00:00Z"  # exclusive

def is_resolved_in_month(issue):
    if issue.get("state") != "closed":
        return False
    closed_at = issue.get("closed_at") or ""
    return MONTH_START <= closed_at < MONTH_END

bug_issues = [i for i in issues if is_bug_report(i)]
resolved_bugs = [i for i in bug_issues if is_resolved_in_month(i)]
```

## String Comparison for ISO 8601 Dates
ISO 8601 timestamps like `"2024-12-15T10:30:00Z"` are lexicographically sortable — direct string comparison `>=` and `<` works correctly when all strings use the same format.

## Complete Example
```python
issues = fetch_search("repo:cli/cli is:issue created:2024-12-01..2024-12-31")
total_issues = len(issues)
bug_issues = [i for i in issues if is_bug_report(i)]
resolved_bugs = [i for i in bug_issues if is_resolved_in_month(i)]

print(f"Total issues: {total_issues}")
print(f"Bug reports:  {len(bug_issues)}")
print(f"Resolved bugs: {len(resolved_bugs)}")
```
