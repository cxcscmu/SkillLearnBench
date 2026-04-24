---
name: github-metrics-aggregation
description: Aggregate GitHub PR and issue data into structured metrics, including contributor analysis, merge statistics, and bug categorization. Use this skill when compiling activity reports, computing open-source velocity metrics, or generating community pulse summaries.
---

# GitHub Metrics Aggregation

Aggregate raw GitHub PR and issue data into clean, structured metrics suitable for reports and dashboards.

## Metrics Structure

The final report follows this structure:

```json
{
  "pr": {
    "total": <int>,           # All PRs created during period
    "merged": <int>,          # PRs with state == "MERGED"
    "closed": <int>,          # PRs with state == "CLOSED" (and not merged)
    "avg_merge_days": <float>,# Average days from creation to merge
    "top_contributor": <str>  # login of contributor with most PRs
  },
  "issue": {
    "total": <int>,           # All issues created during period
    "bug": <int>,             # Issues with "bug" in any label
    "resolved_bugs": <int>    # Bug reports that were closed (any time)
  }
}
```

## PR Metrics

### Total PRs
Simply count all PR objects returned from the GitHub API query for the date range.

```python
total_prs = len(prs)
```

### Merged vs. Closed

- **Merged**: Count PRs where `state == "MERGED"`
- **Closed (not merged)**: Count PRs where `state == "CLOSED"` and not already counted as merged

```python
merged_prs = [pr for pr in prs if pr['state'] == 'MERGED']
closed_prs = [pr for pr in prs if pr['state'] == 'CLOSED']

metrics['merged'] = len(merged_prs)
metrics['closed'] = len(closed_prs)
```

### Average Merge Time

See the `time-to-merge-analysis` skill for the algorithm. Include only merged PRs.

### Top Contributor

Identify the GitHub user (`author.login`) who opened the most PRs:

```python
from collections import Counter

authors = [pr['author']['login'] for pr in prs if pr.get('author')]
author_counts = Counter(authors)
top_contributor = author_counts.most_common(1)[0][0]  # returns login string
```

**Edge case**: If no PRs exist, return empty string or "N/A".

## Issue Metrics

### Total Issues
Count all issues returned for the date range.

```python
total_issues = len(issues)
```

### Bug Reports
Use the `bug-report-identification` skill to count issues with "bug" in any label name.

### Resolved Bugs

Count issues where:
1. At least one label contains "bug" (substring match, case-insensitive)
2. `state == "CLOSED"`

Note: "Resolved bugs" counts bugs that were *created* during the period and are now closed (as of the query date), not necessarily closed during the period. Adjust this if the requirement is "bugs closed during the period" instead.

```python
def is_bug(issue):
    return any('bug' in label['name'].lower() for label in issue.get('labels', []))

resolved_bugs = sum(1 for issue in issues if is_bug(issue) and issue['state'] == 'CLOSED')
```

## Complete Aggregation Function (Python)

```python
import json
from datetime import datetime
from collections import Counter
from typing import List, Dict

def aggregate_metrics(prs: List[Dict], issues: List[Dict]) -> Dict:
    """
    Aggregate GitHub data into structured metrics.

    Args:
        prs: List of PR objects from GitHub API
        issues: List of issue objects from GitHub API

    Returns:
        Metrics dict matching the report structure
    """
    # PR Metrics
    merged_prs = [pr for pr in prs if pr['state'] == 'MERGED']
    closed_prs = [pr for pr in prs if pr['state'] == 'CLOSED']

    # Average merge time
    if merged_prs:
        total_days = 0
        for pr in merged_prs:
            created = datetime.fromisoformat(pr['createdAt'].replace('Z', '+00:00'))
            merged = datetime.fromisoformat(pr['mergedAt'].replace('Z', '+00:00'))
            days = (merged - created).total_seconds() / 86400
            total_days += days
        avg_merge_days = round(total_days / len(merged_prs), 1)
    else:
        avg_merge_days = 0.0

    # Top contributor
    authors = [pr['author']['login'] for pr in prs if pr.get('author')]
    if authors:
        author_counts = Counter(authors)
        top_contributor = author_counts.most_common(1)[0][0]
    else:
        top_contributor = ""

    # Issue Metrics
    def is_bug(issue):
        return any('bug' in label['name'].lower() for label in issue.get('labels', []))

    bug_count = sum(1 for issue in issues if is_bug(issue))
    resolved_bugs = sum(1 for issue in issues if is_bug(issue) and issue['state'] == 'CLOSED')

    return {
        "pr": {
            "total": len(prs),
            "merged": len(merged_prs),
            "closed": len(closed_prs),
            "avg_merge_days": avg_merge_days,
            "top_contributor": top_contributor
        },
        "issue": {
            "total": len(issues),
            "bug": bug_count,
            "resolved_bugs": resolved_bugs
        }
    }
```

## Output to File

Write the aggregated metrics to JSON:

```python
with open('report.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

## Validation Checklist

Before finalizing the report:
- ✓ `pr.total` ≥ `pr.merged` + `pr.closed`
- ✓ `pr.avg_merge_days` is rounded to 1 decimal place
- ✓ `pr.top_contributor` is non-empty (or handle empty case gracefully)
- ✓ `issue.bug` ≤ `issue.total`
- ✓ `issue.resolved_bugs` ≤ `issue.bug`
- ✓ All numeric values are correct type (int or float as specified)
- ✓ All string values are non-null (use empty string if needed)
