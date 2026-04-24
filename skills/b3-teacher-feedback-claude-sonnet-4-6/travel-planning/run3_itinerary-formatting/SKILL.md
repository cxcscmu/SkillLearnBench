---
name: itinerary-formatting
description: Use this skill to convert a completed day-by-day travel plan into the required JSON output format and write it to /app/output/itinerary.json. Enforces field rules, naming conventions, and completeness checks.
---

# Itinerary Formatting Skill

## JSON Structure Rules

### Top-Level Keys
```json
{
  "plan": [ /* array of exactly 7 day objects */ ],
  "data_sources": [ /* array of dataset file paths used */ ]
}
```

### Per-Day Object Fields
| Field | Type | Rule |
|---|---|---|
| `day` | integer | 1 through 7, sequential |
| `current_city` | string | City name on stay days; `"from A to B"` on driving days |
| `transportation` | string | `"Self-driving: from A to B"` on driving days; `"-"` on stay days |
| `breakfast` | string | Restaurant name + city; `"-"` only if intentionally skipped |
| `lunch` | string | Restaurant name + city; `"-"` only if intentionally skipped |
| `dinner` | string | Restaurant name + city; `"-"` only if intentionally skipped |
| `attraction` | string | One or more attractions separated by `;` and ending with `;` — **never `"-"` or empty** |
| `accommodation` | string | Pet-friendly hotel/motel name + city; `"-"` on final return-home day only |

### Attraction Field — Critical Rule
**The `attraction` field must never be `"-"` or an empty string for any day, including driving/travel days.**
- On driving days: include an en-route stop or an attraction at the arrival city visited upon check-in.
- On stay days: include all planned sightseeing.
- Format: `"Attraction One;Attraction Two;"` (always end with `;`)

### Transportation Field
- Never use flights or air travel.
- Use `"Self-driving: from [City A] to [City B]"` on driving days.
- Use `"-"` on days where the traveler stays in the same city.

### data_sources Field
List every dataset file that was queried, for example:
```json
"data_sources": [
  "background/citySet_with_states.txt",
  "accommodations/clean_accommodations_2022.csv",
  "restaurants/clean_restaurant_2022.csv",
  "attractions/attractions.csv",
  "googleDistanceMatrix/distance.csv"
]
```

## Output File
Write the final JSON to `/app/output/itinerary.json`.