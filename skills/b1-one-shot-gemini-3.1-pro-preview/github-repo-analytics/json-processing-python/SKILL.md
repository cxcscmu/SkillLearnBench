---
name: python-datetime-metrics
description: Parse datetime strings and compute time durations/averages for datasets (like PR merge times) in Python.
---

# Python Datetime Metrics

When working with GitHub APIs or any JSON data, you often need to parse ISO-8601 formatted datetime strings and compute derived metrics, such as "average time to merge" or "issue resolution duration".

## Installation / Setup
Built-in `datetime` module is all you need.

## Key Concepts
- `datetime.strptime()` or `datetime.fromisoformat()` can convert strings to datetime objects.
- Subtracting two `datetime` objects yields a `timedelta` object.
- A `timedelta` object can be converted to numeric seconds or days using `.total_seconds()` or `.days`.

## Code Example

```python
from datetime import datetime

def calculate_avg_merge_days(prs):
    merge_times = []
    
    for pr in prs:
        # Check if the PR was actually merged
        if pr.get('pull_request', {}).get('merged_at'):
            created_at_str = pr['created_at']
            merged_at_str = pr['pull_request']['merged_at']
            
            # Use replace('Z', '+00:00') to handle standard ISO-8601 strings from APIs
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
            merged_at = datetime.fromisoformat(merged_at_str.replace('Z', '+00:00'))
            
            # Calculate difference in days (as a float)
            diff_days = (merged_at - created_at).total_seconds() / (24 * 3600)
            merge_times.append(diff_days)
            
    if not merge_times:
        return 0.0
        
    avg_days = sum(merge_times) / len(merge_times)
    # Round to 1 decimal place
    return round(avg_days, 1)

# Example output:
# avg_days = calculate_avg_merge_days(pr_list)
# print(f"Average merge time: {avg_days} days")
```

## Best Practices
- Consider timezone-aware parsing. `replace('Z', '+00:00')` works well for basic UTC strings from GitHub.
- Guard against divide-by-zero errors. Always check `if not data_points` before averaging.
- Remember `merged_at` vs `closed_at`: closed does not mean merged. Ensure you pick the right metric!
