---
name: run2_data-aggregation
description: Aggregate and validate GitHub API data for metrics calculation with comprehensive error handling.
---

# Data Aggregation and Metrics Calculation

## Overview
Convert raw GitHub API responses into meaningful metrics with proper validation and error handling.

## Data Validation Patterns

### Null/None Handling
```python
# Always check for None values from API
if pr.get("merged_at") is None:
    # PR not merged
    pass
```

### Timezone-Aware Datetime Conversion
```python
from datetime import datetime

def parse_github_timestamp(iso_string):
    """Convert GitHub's ISO 8601 timestamps safely."""
    if not iso_string:
        return None
    return datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
```

## Key Metrics

### 1. Time-to-Merge (days)
```python
def calculate_time_to_merge(created_at, merged_at):
    """Calculate days from creation to merge."""
    if not merged_at:
        return None
    created = parse_github_timestamp(created_at)
    merged = parse_github_timestamp(merged_at)
    if not created or not merged:
        return None
    return (merged - created).total_seconds() / 86400

# Average calculation with validation
merge_times = [t for t in times if t is not None and t >= 0]
avg_days = sum(merge_times) / len(merge_times) if merge_times else 0
avg_days = round(avg_days, 1)  # Round to 1 decimal place
```

### 2. State Counting
```python
# For PRs
merged_count = sum(1 for pr in prs if pr.get("merged_at") is not None)
closed_count = sum(1 for pr in prs if pr.get("state") == "closed")
open_count = sum(1 for pr in prs if pr.get("state") == "open")
```

### 3. Label-Based Filtering
```python
def has_label_substring(item, substring):
    """Check if any label contains substring (case-insensitive)."""
    labels = item.get("labels", [])
    if not labels:
        return False
    return any(substring.lower() in label.get("name", "").lower() for label in labels)

# Count bug reports
bug_issues = [i for i in issues if has_label_substring(i, "bug")]
```

### 4. Top Contributor
```python
from collections import Counter

def get_top_contributor(items):
    """Find person with most contributions."""
    authors = []
    for item in items:
        user = item.get("user")
        if user and user.get("login"):
            authors.append(user["login"])

    if not authors:
        return None

    return Counter(authors).most_common(1)[0][0]
```

## Data Quality Checks

```python
def validate_data(prs, issues):
    """Validate data integrity."""
    errors = []

    if not isinstance(prs, list):
        errors.append("PRs must be a list")
    if not isinstance(issues, list):
        errors.append("Issues must be a list")

    # Spot check a few items
    for pr in prs[:5]:
        if "created_at" not in pr:
            errors.append("Missing created_at in PR")
            break

    return errors
```

## Edge Cases

1. **No data**: Return 0 for counts, None for averages
2. **Invalid dates**: Skip items with parse errors, log warnings
3. **Missing authors**: Use None instead of failing
4. **Labels array empty**: Treat as no matching labels
5. **Negative time-to-merge**: Indicates data inconsistency, exclude from average

## Output Format
Return clean dictionaries with all required fields present:
```python
{
    "pr": {
        "total": int,
        "merged": int,
        "closed": int,
        "avg_merge_days": float,
        "top_contributor": str or None
    },
    "issue": {
        "total": int,
        "bug": int,
        "resolved_bugs": int
    }
}
```
