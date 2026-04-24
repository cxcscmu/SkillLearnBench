---
name: run2_itinerary_optimization
description: Optimized itinerary building with cuisine distribution, cost tracking, and multi-city routing for pet-friendly travel.
---

# Optimized Multi-City Itinerary Planning

## Overview
This skill addresses:
- Balanced cuisine distribution across 7 days
- Cost tracking and budget adherence
- Optimal city sequencing and travel timing
- Pet-friendly accommodation prioritization
- Realistic meal and attraction planning

## Route Optimization for 3 Ohio Cities

### Recommended Route
Minneapolis → Cleveland → Columbus → Cincinnati → Minneapolis

**Rationale:**
- Cleveland is north, good entry point
- Columbus is central, on route to Cincinnati
- Cincinnati is southwest, good final city before returning
- Minimizes backtracking

### Day Allocation
- Day 1: Travel Minneapolis → Cleveland (arrival dinner)
- Days 2-3: Cleveland (full exploration)
- Day 4: Travel Cleveland → Columbus (arrival dinner)
- Day 5: Columbus (full exploration)
- Day 6: Travel Columbus → Cincinnati (arrival dinner)
- Day 7: Cincinnati & return to Minneapolis (depart dinner/lunch only)

## Cuisine Distribution Strategy

### Assignment Pattern
Across 7 days, ensure all 4 cuisines appear:
- **American**: 2-3 occurrences (breakfast Day 1, lunch Day 5, dinner Day 7)
- **Italian**: 2 occurrences (dinner Days 2, 6)
- **Chinese**: 2 occurrences (lunch Days 3, 7)
- **Mediterranean**: 1 occurrence (lunch Day 4)

### Implementation
```python
cuisine_schedule = {
    1: {"breakfast": "American", "lunch": "American", "dinner": "Chinese"},
    2: {"breakfast": "Italian", "lunch": "Mediterranean", "dinner": "Italian"},
    3: {"breakfast": "Chinese", "lunch": "American", "dinner": "American"},
    4: {"breakfast": "Mediterranean", "lunch": "Mediterranean", "dinner": "Italian"},
    5: {"breakfast": "American", "lunch": "Italian", "dinner": "Chinese"},
    6: {"breakfast": "Italian", "lunch": "Chinese", "dinner": "Italian"},
    7: {"breakfast": "American", "lunch": "Chinese", "dinner": "-"}
}
```

## Cost Tracking

### Budget Breakdown ($5,100 for 2 people, 7 days)
- **Accommodations**: 6 nights × $120-180/night = $720-1,080
- **Meals**: 7 days × $80-120/day = $560-840
- **Attractions**: $200-300 total (entry fees)
- **Gas/Transportation**: $150-200 (est. 1,000 miles round trip)
- **Buffer**: $200-500

### Daily Budgets
```python
daily_budget = {
    "accommodation_per_night": 150,  # per night for 2 people
    "meals_per_day": 100,  # ~$17 per person per meal
    "attractions_per_day": 30-50,
    "transport_per_day": 20-30
}
```

## Meal Planning Constraints

1. **No Restaurants Repeated Across Days**
   - Even if good, pick different one next time
   - Keep cuisine diversity high

2. **Format Rule**
   - Include restaurant name + cuisine type + city
   - Example: "Italian at Via Cento, Cleveland"
   - Never: Just restaurant name or just cuisine name

3. **Travel Days**
   - Breakfast: lighter meal in departure city
   - Lunch: en route or arrival city
   - Dinner: arrival city (establish evening routine)

## Attraction Selection

### Strategy
- 2-3 attractions per day minimum
- Mix types: museums, parks, historic sites, food markets
- Prioritize based on:
  1. Availability in city
  2. Pet-friendly (where applicable - parks over indoor museums)
  3. Rating/popularity
  4. Distance from accommodation

### Format
- List attractions separated by semicolon
- **Must end with semicolon**: "Attraction1;Attraction2;"
- Never end without semicolon or without enough attractions

## Accommodation Selection Priority

1. Pet-friendly verification (explicitly no "No pets")
2. Price within budget ($100-200/night)
3. Rating > 4.0
4. Room type: Entire home/apt > Private room > Shared room
5. Minimum nights requirement = 1

### Naming Convention
- Include: "Pet-friendly" + accommodation type + city name
- Example: "Pet-friendly Studio Apartment, Cleveland"
- Avoid: Excessive special characters, Unicode issues

## Travel Day Optimization

```python
def plan_travel_day(origin_city, dest_city):
    """Structure for travel days"""
    return {
        "current_city": f"from {origin_city} to {dest_city}",
        "transportation": f"Self-driving: from {origin_city} to {dest_city}",
        "breakfast": "meal in origin city",
        "lunch": "meal en route or early arrival",
        "dinner": "meal in destination city",
        "attraction": "light attractions in destination",
        "accommodation": "in destination city"
    }
```

## Quality Assurance Checklist

Before finalizing each day:
- [ ] Exactly one city or "from X to Y" format
- [ ] Transportation includes direction and mode
- [ ] All meal fields filled (no blank values)
- [ ] Cuisines match assigned schedule
- [ ] Attractions string ends with semicolon
- [ ] Accommodation marked pet-friendly
- [ ] No restaurant repeats within 2 days
- [ ] Budget for day stays within limits
