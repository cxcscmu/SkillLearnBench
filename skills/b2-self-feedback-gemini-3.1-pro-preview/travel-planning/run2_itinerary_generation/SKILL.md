---
name: run1_itinerary_generation
description: How to serialize the final travel itinerary to a JSON file.
---
# Itinerary Generation Skill
Use python's `json` module to dump the final itinerary in the required format.

```python
import json

itinerary = {
    "plan": [
        {
            "day": 1,
            "current_city": "Minneapolis",
            "transportation": "Self-driving: from Minneapolis to Cleveland",
            "breakfast": "...",
            "lunch": "...",
            "dinner": "...",
            "attraction": "...",
            "accommodation": "..."
        }
    ],
    "data_sources": [
        "accommodations/clean_accommodations_2022.csv"
    ]
}

with open('/app/output/itinerary.json', 'w') as f:
    json.dump(itinerary, f, indent=2)
```
