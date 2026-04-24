---
name: route-planning
description: Use a distance matrix CSV to find travel time and distance between cities for self-driving trips.
---
# Route Planning

Calculate distance and duration from a distance matrix.

## Example Usage

```python
import pandas as pd

def get_travel_info(dist_df, origin, destination):
    row = dist_df[(dist_df['origin'] == origin) & (dist_df['destination'] == destination)]
    if not row.empty:
        return row.iloc[0]['distance'], row.iloc[0]['duration']
    return None, None
```
