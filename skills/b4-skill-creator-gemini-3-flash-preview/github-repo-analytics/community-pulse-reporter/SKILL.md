---
name: community-pulse-reporter
description: Professional methodology for transforming raw repository activity into structured community pulse reports. Use this skill when you need to calculate metrics like merge times, contributor rankings, and bug resolution rates for meeting-ready summaries.
---

# Community Pulse Reporter

This skill details the logic and transformations required to generate a standardized community pulse report from raw data.

## Metric Calculation Logic

### 1. PR Merge Time
Calculate the average time (in days) from PR creation to merge for all PRs that were merged.
- **Formula**: `(merge_timestamp - creation_timestamp) / (24 * 3600)`
- **Rounding**: Round to one decimal place.

### 2. Top Contributor
Identify the individual who opened the most PRs within the reporting period.
- **Logic**: Count PRs grouped by author login. In case of a tie, the first alphabetical login is usually acceptable unless specified otherwise.

### 3. Bug Resolution Rate
Identify issues labeled as "bug" and track their closure status.
- **Bug Definition**: Any issue where at least one label contains the case-insensitive substring "bug".
- **Resolved Bugs**: Issues meeting the bug definition that were closed during the reporting period.

## Output Structure (report.json)

The report must follow this exact schema:

```json
{
  "pr": {
    "total": <int>,
    "merged": <int>,
    "closed": <int>,
    "avg_merge_days": <float>,
    "top_contributor": <str>
  },
  "issue": {
    "total": <int>,
    "bug": <int>,
    "resolved_bugs": <int>
  }
}
```

## Processing with Python
Python is recommended for complex calculations and JSON generation.

### Skeleton Processing Script
```python
import json
from datetime import datetime

def calculate_days(start_str, end_str):
    start = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
    return (end - start).total_seconds() / (24 * 3600)

# Load data, compute metrics, and write JSON
```
