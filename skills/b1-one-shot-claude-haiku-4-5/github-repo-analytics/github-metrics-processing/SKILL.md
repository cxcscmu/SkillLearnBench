---
name: github-metrics-processing
description: Process GitHub API data to calculate PR/issue metrics including merge time averages, author rankings, and bug categorization.
---

# GitHub Metrics Processing Skill

## Overview
Process JSON data from GitHub queries to calculate publication metrics, including PR merge times, issue categorization, and contributor analysis.

## Prerequisites
- Python 3.7+ with `json` and `datetime` modules (standard library)
- Raw GitHub API JSON data from gh CLI queries

## Key Metrics to Calculate

### Pull Request Metrics

#### 1. Total PR Count
```python
total_prs = len(prs_data)
```

#### 2. Merged vs Closed PRs
```python
merged_prs = [pr for pr in prs_data if pr.get('mergedAt') is not None]
closed_prs = [pr for pr in prs_data if pr.get('closedAt') is not None and pr.get('mergedAt') is None]

merged_count = len(merged_prs)
closed_count = len(closed_prs)
```

#### 3. Average Merge Time (days)
```python
from datetime import datetime

def parse_iso8601(timestamp_str):
    """Parse ISO 8601 timestamp to datetime object"""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

def calculate_merge_days(prs):
    """Calculate average days from creation to merge"""
    merge_times = []
    for pr in prs:
        if pr.get('mergedAt'):  # Only count merged PRs
            created = parse_iso8601(pr['createdAt'])
            merged = parse_iso8601(pr['mergedAt'])
            days = (merged - created).days
            merge_times.append(days)

    if not merge_times:
        return 0.0

    avg = sum(merge_times) / len(merge_times)
    return round(avg, 1)  # Round to one decimal place
```

#### 4. Top Contributor (Most PRs)
```python
from collections import Counter

def get_top_contributor(prs):
    """Find author who opened the most PRs"""
    authors = [pr['author']['login'] for pr in prs if pr.get('author')]
    if not authors:
        return None

    author_counts = Counter(authors)
    top_author, _ = author_counts.most_common(1)[0]
    return top_author
```

### Issue Metrics

#### 1. Total Issue Count
```python
total_issues = len(issues_data)
```

#### 2. Bug Reports (label matching)
```python
def count_bug_issues(issues):
    """Count issues with 'bug' in any label name"""
    bug_count = 0
    for issue in issues:
        labels = issue.get('labels', [])
        has_bug = any('bug' in label.get('name', '').lower() for label in labels)
        if has_bug:
            bug_count += 1
    return bug_count

bug_count = count_bug_issues(issues_data)
```

#### 3. Resolved Bugs (closed during month)
```python
def count_resolved_bugs(issues, period_end):
    """Count bugs that were closed during the specified month"""
    resolved_count = 0
    for issue in issues:
        # Must have 'bug' in a label
        labels = issue.get('labels', [])
        has_bug = any('bug' in label.get('name', '').lower() for label in labels)

        # Must be closed
        closed_at = issue.get('closedAt')
        if has_bug and closed_at:
            resolved_count += 1

    return resolved_count
```

## Complete Processing Example

```python
import json
from datetime import datetime
from collections import Counter

def parse_iso8601(timestamp_str):
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

def process_github_data(prs_json, issues_json):
    """Process GitHub data and return metrics"""

    prs = json.loads(prs_json)
    issues = json.loads(issues_json)

    # PR Metrics
    merged_prs = [pr for pr in prs if pr.get('mergedAt')]
    closed_prs = [pr for pr in prs
                  if pr.get('closedAt') and not pr.get('mergedAt')]

    merge_times = []
    for pr in merged_prs:
        created = parse_iso8601(pr['createdAt'])
        merged = parse_iso8601(pr['mergedAt'])
        days = (merged - created).days
        merge_times.append(days)

    avg_merge_days = round(sum(merge_times) / len(merge_times), 1) if merge_times else 0.0

    authors = [pr['author']['login'] for pr in prs if pr.get('author')]
    top_contributor = Counter(authors).most_common(1)[0][0] if authors else None

    # Issue Metrics
    bug_issues = []
    for issue in issues:
        labels = issue.get('labels', [])
        if any('bug' in label.get('name', '').lower() for label in labels):
            bug_issues.append(issue)

    resolved_bugs = sum(1 for issue in bug_issues if issue.get('closedAt'))

    return {
        'pr': {
            'total': len(prs),
            'merged': len(merged_prs),
            'closed': len(closed_prs),
            'avg_merge_days': avg_merge_days,
            'top_contributor': top_contributor
        },
        'issue': {
            'total': len(issues),
            'bug': len(bug_issues),
            'resolved_bugs': resolved_bugs
        }
    }
```

## Edge Cases to Handle
- Null values in timestamps (still open/not merged items)
- Case-insensitive label matching for "bug"
- Authors from external contributors (verify .login field exists)
- PRs created but never merged or closed (neither count toward closed)
- Division by zero when no merged PRs exist
