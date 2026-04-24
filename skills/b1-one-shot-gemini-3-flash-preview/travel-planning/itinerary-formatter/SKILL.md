---
name: itinerary-formatter
description: Create a JSON structure for a 7-day travel plan.
---
# Itinerary Formatter

Structure a 7-day travel plan JSON according to specific keys.

## Example Usage

```python
import json

def format_itinerary(plan_days, data_sources):
    return {
        "plan": plan_days,
        "data_sources": data_sources
    }
```
