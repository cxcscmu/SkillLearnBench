---
name: route-planning
description: Algorithmic planning of itineraries avoiding specific transport modes and allocating time based on budget constraints.
---

# Route Planning and Itinerary Construction

This skill focuses on sequentially constructing travel plans by selecting daily activities and accommodations, avoiding certain travel modes (e.g., no flights), and managing budget constraints.

## Key Concepts

- Distance/Travel time estimation without flights (driving or ground transportation only).
- Day-by-day scheduling of activities (Meals, Attractions).
- Maintaining budget variables iteratively across multiple days.

## Implementation Details

- Identify starting point and sequential destinations.
- Use a driving distance matrix to calculate time/costs.
- Iteratively assign activities and ensure costs are kept under constraints.
- Output final structured format (e.g., JSON).

```python
import json

itinerary = {
    'plan': [],
    'data_sources': ['data/distance.csv', 'data/attractions.csv']
}

# Example daily assignment
day_plan = {
    'day': 1,
    'current_city': 'Minneapolis',
    'transportation': 'Self-driving: from Minneapolis to Cleveland',
    'breakfast': 'Local Cafe',
    'lunch': 'Bistro',
    'dinner': 'Fine Dining',
    'attraction': 'City Park;Museum;',
    'accommodation': 'Pet-Friendly Inn'
}

itinerary['plan'].append(day_plan)

with open('output/itinerary.json', 'w') as f:
    json.dump(itinerary, f, indent=2)
```
