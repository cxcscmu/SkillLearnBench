---
name: itinerary-builder
description: Build multi-day travel itineraries with routing, scheduling, and constraint satisfaction. Use this skill whenever creating a structured travel plan that must span multiple days, visit specific cities, include meals and accommodations, and respect travel time and budget constraints. Essential for generating day-by-day itineraries in JSON or structured formats.
---

# Itinerary Builder

This skill provides structured methodology for constructing multi-day travel itineraries that satisfy routing, temporal, and constraint requirements.

## Itinerary Structure

A complete itinerary consists of:

```json
{
  "plan": [
    {
      "day": 1,
      "current_city": "City Name",
      "transportation": "Self-driving: from A to B",
      "breakfast": "Restaurant name, City",
      "lunch": "Restaurant name, City",
      "dinner": "Restaurant name, City",
      "attraction": "Attraction1;Attraction2;",
      "accommodation": "Hotel name, City"
    }
  ],
  "data_sources": ["file1.csv", "file2.csv"]
}
```

## Step-by-Step Building Process

### 1. Define Trip Parameters

Extract and validate:
- **Start date and duration**: Days 1-7 (March 17-23)
- **Origin city**: Minneapolis
- **Destination cities**: Three cities in Ohio (e.g., Cleveland, Columbus, Cincinnati)
- **Budget**: Total available funds and daily breakdown
- **Constraints**:
  - No flights (ground transportation only)
  - Pet-friendly accommodations required
  - Cuisine preferences: American, Mediterranean, Chinese, Italian
  - Party size: 2 people + 1 dog

### 2. Plan Route Sequence

For a 7-day trip visiting 3 Ohio cities:
- **Day 1**: Travel from Minneapolis to first Ohio city
- **Days 2-4**: Explore first city
- **Day 5**: Travel to second city
- **Days 6-7**: Explore second and third cities (or spread across remaining days)

Alternatively, create a loop route:
```
Minneapolis → City A (2 days) → City B (2 days) → City C (2 days) → Return/End
```

Calculate driving times between cities and ensure feasibility. Use distance data to estimate hours needed.

### 3. Allocate Budget

Break down the $5,100 total budget:

```
Accommodations: 6 nights × $80-120/night = $480-720
Meals (2 people): 7 days × $40-60/day = $280-420
Attractions: 7 days × $20-30/day = $140-210
Fuel/Transportation: Minneapolis→OH→Minneapolis ≈ $300-400
Contingency: 10% of above = $200-275
Total allocated: ~$1,500-2,025 (well within $5,100 budget)
```

Allocate remaining funds as buffers for higher-priced meals or attractions.

### 4. Select Accommodations

For each city/night:
- Filter for **pet-friendly** properties (essential constraint)
- Select options within daily budget allocation
- Verify availability for the specific dates
- Record property name and location

**Note**: Some datasets may label pet-friendly as:
- Boolean flag: `pet_friendly: 1` or `pet_friendly: true`
- Text field: `amenities: "pets allowed"` or `policies: "pet-friendly"`
- Separate field: `pets: "dogs welcome"`

### 5. Schedule Meals

For each day, assign breakfast, lunch, and dinner:

**Cuisine Distribution Strategy**:
- Spread preferences across the week
- Mix cuisines: don't repeat the same on consecutive days
- Vary restaurant types: fine dining, casual, quick service

**Example Schedule**:
```
Day 1: American (breakfast), Mediterranean (lunch), Italian (dinner)
Day 2: Chinese (breakfast), American (lunch), Mediterranean (dinner)
Day 3: Italian (breakfast), Chinese (lunch), American (dinner)
...
```

**Special Cases**:
- Travel days (Days 1, 5): Light or quick meals
- Multi-hour drives: Include lunch options along route
- If a meal is skipped intentionally, use `"-"` as placeholder

### 6. Select Attractions

For each city day:
- Choose 2-4 major attractions relevant to city
- Vary types: museums, parks, landmarks, historic sites
- Consider proximity to accommodations (walking distance or short drive)
- Include 1-2 outdoor activities for pet-friendly vibes

**Format**: Separate with semicolon and trailing semicolon:
```
"Rock & Roll Hall of Fame;West Side Market;Cleveland Waterfront;"
```

### 7. Plan Transportation

For each day, specify:

**Within-city**: "Local exploration; pet-friendly walks"

**Between cities**:
```
"Self-driving: from Minneapolis to Cleveland (8 hours, ~500 miles)"
"Self-driving: from Cleveland to Columbus (2 hours, ~140 miles)"
```

Include rest stops and pet breaks for dog comfort.

### 8. Validate Constraints

Before finalizing, verify:

- ✓ All 7 days populated
- ✓ No flights used (only self-driving)
- ✓ All accommodations pet-friendly
- ✓ Budget stays within $5,100
- ✓ Cuisine preferences distributed
- ✓ Dates match (March 17-23, 2022)
- ✓ Exactly 3 Ohio cities visited
- ✓ All entries reference actual data sources

### 9. Generate JSON Output

Structure the final itinerary:

```python
itinerary = {
    "plan": [day1, day2, ..., day7],
    "data_sources": [
        "background/citySet_with_states.txt",
        "accommodations/clean_accommodations_2022.csv",
        "restaurants/clean_restaurant_2022.csv",
        "attractions/attractions.csv",
        "googleDistanceMatrix/distance.csv"
    ]
}

import json
with open('/app/output/itinerary.json', 'w') as f:
    json.dump(itinerary, f, indent=2)
```

## Common Pitfalls

- **Travel time underestimated**: Always add buffer for rest and pet breaks
- **Repeating cuisine types**: Track which cuisines used each day to avoid clustering
- **Missing pet-friendly filter**: Every accommodation MUST be pet-friendly
- **Incomplete attraction data**: Verify attractions exist in database before listing
- **Budget overruns**: Sum costs incrementally; recalculate after adding each item
- **Incomplete daily entries**: All fields (breakfast, lunch, dinner, attraction, accommodation) must be filled or explicitly marked as `"-"`

## Iterative Refinement

If constraints cannot be satisfied:
1. Relax budget slightly if necessary (still within $5,100)
2. Adjust cuisine distribution if specific types unavailable in target cities
3. Modify city selection if Ohio cities don't have sufficient dining/attractions
4. Extend stay in some cities, shorten in others while maintaining 7-day total
