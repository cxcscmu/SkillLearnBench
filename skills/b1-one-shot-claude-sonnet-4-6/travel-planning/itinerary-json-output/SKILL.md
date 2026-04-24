---
name: itinerary-json-output
description: How to structure and write a valid travel itinerary JSON file matching the required schema for /app/output/itinerary.json.
---

# Itinerary JSON Output Format

## File path
`/app/output/itinerary.json`

## Top-level structure
```json
{
  "plan": [ /* array of exactly 7 day objects */ ],
  "data_sources": [ /* list of dataset files used */ ]
}
```

## Day object fields
| Field | Type | Notes |
|-------|------|-------|
| `day` | integer | 1–7 |
| `current_city` | string | City name, OR `"from A to B"` when traveling |
| `transportation` | string | `"Self-driving: from A to B"` — no flights |
| `breakfast` | string | `"Restaurant Name, City"` or `"-"` |
| `lunch` | string | `"Restaurant Name, City"` or `"-"` |
| `dinner` | string | `"Restaurant Name, City"` or `"-"` |
| `attraction` | string | `"Name1;Name2;"` — semicolon-separated, trailing semicolon |
| `accommodation` | string | Pet-friendly lodging name |

## Rules
- Use `"-"` for meals intentionally skipped (e.g., long driving days).
- `transportation` is `"-"` when staying in same city.
- Attractions end with `;` even if only one.
- `accommodation` is `"-"` on final day if returning home.
- Restaurant format: `"Name, City"` (matches CSV `Name` and `City` columns).

## Example day object
```json
{
  "day": 2,
  "current_city": "Cleveland",
  "transportation": "-",
  "breakfast": "Master Bakers, Cleveland",
  "lunch": "Green Leaf, Cleveland",
  "dinner": "Bruncheez, Cleveland",
  "attraction": "Rock & Roll Hall of Fame;West Side Market;Great Lakes Science Center;",
  "accommodation": "Cozy minimalist room close to train (1), Cleveland"
}
```

## data_sources list
Always include all dataset files actually consulted:
```json
"data_sources": [
  "background/citySet_with_states.txt",
  "accommodations/clean_accommodations_2022.csv",
  "restaurants/clean_restaurant_2022.csv",
  "attractions/attractions.csv",
  "googleDistanceMatrix/distance.csv"
]
```
