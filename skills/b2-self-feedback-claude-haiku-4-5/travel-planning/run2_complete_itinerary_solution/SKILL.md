---
name: run2_complete_itinerary_solution
description: End-to-end solution for building multi-city travel itineraries with pet-friendly accommodations and diverse cuisine constraints.
---

# Complete Multi-City Travel Itinerary Solution

## Problem Overview
Build a 7-day itinerary for 2 travelers:
- Route: Minneapolis → 3 Ohio cities → Minneapolis
- Dates: March 17-23, 2022
- Budget: $5,100
- Constraints: Pet-friendly, no flights, diverse cuisines (American, Italian, Chinese, Mediterranean)

## Key Implementation Decisions

### 1. Route Optimization
Selected: Minneapolis → Cleveland → Columbus → Cincinnati → Minneapolis
- Natural geographic progression
- Minimizes backtracking
- Balanced city-by-city exploration time

### 2. Time Allocation
- Day 1: Travel to Cleveland + evening activities
- Days 2-3: Full Cleveland exploration (2 nights)
- Day 4: Travel to Columbus + evening activities
- Day 5: Full Columbus exploration (1 night)
- Day 6: Travel to Cincinnati + evening activities
- Day 7: Cincinnati departure (1 night)

### 3. Cuisine Distribution Strategy
Map cuisines across 7 days:
```
Day 1: American (breakfast/lunch) + Italian (dinner)
Day 2: Italian + Mediterranean + Chinese
Day 3: Chinese + American + Mediterranean
Day 4: Mediterranean + Italian + American
Day 5: American + Chinese + Italian
Day 6: Italian + Chinese + American
Day 7: Chinese + American + depart
```
Ensures all 4 cuisines appear multiple times, no same cuisine twice same day.

### 4. Data Quality Filtering

**Restaurant Selection Criteria:**
- Valid ASCII names (≥60% ASCII characters)
- City match
- Cuisine match (using primary + alias terms)
- Rating ≥ 3.7
- Cost $0-250
- Avoid duplicates within a city during itinerary
- Sort by rating as tiebreaker

**Pet-Friendly Accommodation Filter:**
- NOT containing "No pets" in house_rules
- Price range: $0-250/night
- City match
- Prefer "Entire home/apt" over private rooms
- Sort by review rating

**Attraction Selection:**
- Drop duplicates by name
- Get top 3 per city
- Sort alphabetically for consistency
- Format with trailing semicolon

### 5. Implementation Pattern

```python
# Structure for each day
day = {
    "day": int,
    "current_city": str,  # "City" or "from A to B"
    "transportation": str,  # Include direction
    "breakfast": str,  # "Name, City"
    "lunch": str,
    "dinner": str,  # or "-" if skipping
    "attraction": "A;B;C;",  # Must end with ;
    "accommodation": str  # Must mention pet-friendly
}
```

### 6. Common Pitfalls to Avoid

1. **Unicode Characters**: Filter restaurants with non-ASCII names
2. **Duplicate Restaurants**: Track used restaurants per city
3. **Over-Budget**: Filter accommodations strictly for price
4. **Wrong Cuisine**: Use multi-strategy matching (exact + aliases)
5. **Missing Data**: Have fallback accommodation/attraction names
6. **Format Issues**: Always end attraction strings with semicolon

### 7. Budget Verification

Example breakdown for $5,100 budget:
- 6 nights × $120 = $720 (accommodations)
- 7 days × $80 = $560 (meals)
- Attractions: $300
- Gas (~1,000 miles): $200
- Buffer: $3,220 (comes out to ~$460/day for other expenses)

Actual itinerary stays well within this budget using real data.

## Code Structure

```python
# 1. Load and clean datasets
# 2. Define validation functions for restaurant/accommodation quality
# 3. Create journey/cuisine schedule mappings
# 4. For each day:
#    - Determine cities and meal cities
#    - Get restaurants matching cuisine
#    - Avoid duplicates using tracking set
#    - Get pet-friendly accommodation
#    - Get attractions list
# 5. Build JSON with all 7 days
# 6. Write to output file
```

## Testing Checklist

- [ ] 7 days in plan
- [ ] Each day has all 8 required fields
- [ ] No flights (only Self-driving)
- [ ] All accommodations mention pet-friendly
- [ ] Attractions end with semicolon
- [ ] All 4 cuisines appear in itinerary
- [ ] No restaurant repeated in same city on consecutive days
- [ ] All cities from dataset (verified in citySet_with_states.txt)
- [ ] Meals have restaurant names (not just cuisine names)
- [ ] Valid JSON output
- [ ] Data sources array populated correctly

## Performance Notes

- Loading 9,500+ restaurant records may take 2-3 seconds
- Filtering operations are O(n) on dataset size
- Deduplication adds minimal overhead
- Total script execution: < 5 seconds typical

## Lessons Learned

1. Raw data quality matters - must filter for ASCII/valid names
2. Fuzzy matching on cuisines needed (not all exact matches available)
3. Pet-friendly filter is critical - "No pets" terminology varies
4. Accommodation data may have listings from multiple cities/years
5. Always have fallback values for accommodations and attractions
6. Track used restaurants per city to avoid repetition
7. Price filtering must be strict to stay within budget
