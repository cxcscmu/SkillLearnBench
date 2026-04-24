---
name: travel-itinerary-planner
description: Build a structured multi-day travel itinerary JSON from real CSV datasets. Use this skill whenever the user asks to create a travel plan, trip itinerary, or vacation schedule from a local database of cities, restaurants, accommodations, and attractions.
---

# Travel Itinerary Planner

## Purpose
Generate a valid `itinerary.json` from real-world CSV data files for a multi-city road trip, respecting budget, dietary, pet, and transportation constraints.

## Input Requirements
Collect from user prompt:
- Origin city and destination cities
- Travel dates and duration (number of days)
- Total budget (USD)
- Party size and special needs (pets, dietary preferences)
- Transportation mode (road trip = no flights)
- Meal cuisine preferences

## Dataset Locations
| Dataset | Path |
|---|---|
| City list | `data/background/citySet_with_states.txt` |
| Restaurants | `data/restaurants/clean_restaurant_2022.csv` |
| Accommodations | `data/accommodations/clean_accommodations_2022.csv` |
| Attractions | `data/attractions/attractions.csv` |
| Distances | `data/googleDistanceMatrix/distance.csv` |

## Planning Workflow

### Step 1 — Select Destination Cities
Query `citySet_with_states.txt` to confirm cities exist in the dataset for the target state.

### Step 2 — Plan Route and Travel Days
- Look up driving distances/durations in `distance.csv` (columns: `origin,destination,cost,duration,distance`)
- Assign travel days for long drives; designate full days for city exploration
- No flights allowed if user specifies road trip

### Step 3 — Select Pet-Friendly Accommodations
Filter `clean_accommodations_2022.csv`:
- `city` matches destination
- `house_rules` does NOT contain `"No pets"`
- `minimum nights` ≤ number of nights planned in that city
- Choose highest `review rate number` within budget

Accommodation cost = `price` × number of nights in that city.

### Step 4 — Select Restaurants by Cuisine
Filter `clean_restaurant_2022.csv`:
- `City` matches current city
- `Cuisines` contains one of the preferred cuisines
- Spread meals across preferred cuisine types across the trip
- Skip meals (`"-"`) on long travel days when meals aren't practical

### Step 5 — Select Attractions
From `attractions.csv`:
- `City` matches current city
- Choose 2–4 per full day in city
- Format: `"Name1;Name2;Name3;"` (semicolon-separated, trailing semicolon)

### Step 6 — Budget Check
```
Total = sum(accommodation nightly rate × nights per city) + sum(meal average costs)
Target: Total ≤ budget
```
Transport has no explicit cost in datasets (self-driving); gas/misc covered by remaining budget.

## Output JSON Structure
```json
{
  "plan": [
    {
      "day": 1,
      "current_city": "from A to B",
      "transportation": "Self-driving: from A to B",
      "breakfast": "Restaurant Name, City",
      "lunch": "-",
      "dinner": "Restaurant Name, City",
      "attraction": "-",
      "accommodation": "Accommodation Name, City"
    }
  ],
  "data_sources": [
    "background/citySet_with_states.txt",
    "accommodations/clean_accommodations_2022.csv",
    "restaurants/clean_restaurant_2022.csv",
    "attractions/attractions.csv",
    "googleDistanceMatrix/distance.csv"
  ]
}
```

## Key Rules
- Travel days: `current_city` = `"from A to B"`, skip attractions, include meals only when practical
- Staying days: `current_city` = city name, list attractions, full meals
- Last day (return): `accommodation` = `"-"` (back home)
- Always end `attraction` strings with a trailing semicolon
- All data must come from the CSV files — never invent restaurants, accommodations, or attractions
