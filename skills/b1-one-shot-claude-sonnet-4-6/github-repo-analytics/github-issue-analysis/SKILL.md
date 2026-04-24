---
name: github-issue-analysis
description: Analyze GitHub issues for a date range, counting totals, bug reports (by label substring), and closed bug reports.
---

# GitHub Issue Analysis

## Overview

Fetch issues created in a date range and compute:
- Total issue count (excluding PRs)
- Bug reports: issues with at least one label containing substring `bug`
- Resolved bugs: bug report issues closed during the same month

## Fetching Issues

```bash
# Using gh issue list with search
gh issue list -R cli/cli \
  --search "created:2024-12-01..2024-12-31" \
  --state all \
  --limit 500 \
  --json number,title,labels,state,createdAt,closedAt
```

> Note: `gh issue list` automatically excludes PRs.

## Python: Identify Bug Reports

```python
import json

with open('issues.json') as f:
    issues = json.load(f)

def is_bug(issue):
    """Returns True if any label contains 'bug' as substring (case-insensitive)."""
    return any('bug' in label['name'].lower() for label in issue.get('labels', []))

total = len(issues)
bugs = [i for i in issues if is_bug(i)]

# Closed bugs: bug issues that were closed during the month
# closedAt is within Dec 2024
def closed_in_month(issue, year=2024, month=12):
    if not issue.get('closedAt'):
        return False
    from datetime import datetime, timezone
    dt = datetime.fromisoformat(issue['closedAt'].replace('Z', '+00:00'))
    return dt.year == year and dt.month == month

resolved_bugs = [i for i in bugs if closed_in_month(i)]

print(json.dumps({
    "total": total,
    "bug": len(bugs),
    "resolved_bugs": len(resolved_bugs)
}, indent=2))
```

## Label Matching Examples

Labels that match `bug` substring:
- `bug` ✓
- `type: bug` ✓
- `kind/bug` ✓
- `bug-report` ✓
- `debug` — contains `bug` as substring ✓ (be aware)

For stricter matching (word boundary), use regex:
```python
import re
def is_bug(issue):
    return any(re.search(r'bug', label['name'], re.IGNORECASE)
               for label in issue.get('labels', []))
```

## Important: `closedAt` vs `state`

- `closedAt` is set when an issue is closed (regardless of month)
- To find bugs *closed during December*, filter `closedAt` to be within Dec 2024
- An issue created in Dec but closed in Jan would NOT count as `resolved_bugs`
