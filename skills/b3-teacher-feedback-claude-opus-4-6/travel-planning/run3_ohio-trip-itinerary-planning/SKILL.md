---
name: ohio-trip-itinerary-planning
description: Use this skill when planning a 7-day road trip itinerary from Minneapolis to three cities in Ohio, covering budget, pet-friendly accommodations, cuisine preferences, and no-flight constraints. Produces a JSON itinerary file.
---

# Ohio Trip Itinerary Planning (Minneapolis → 3 Ohio Cities, 7 Days)

## Task Overview
Build a 7-day travel itinerary for 2 people + pet dog, departing Minneapolis, visiting 3 Ohio cities, March 17–23, 2022. Budget ≤ $5,100. No flights. Pet-friendly accommodations. Preferred cuisines: American, Mediterranean, Chinese, Italian.

## Step 1: Identify Ohio Cities from Database

Search `background/citySet_with_states.txt` for cities in Ohio. Common Ohio cities in the dataset include:
- Cleveland
- Columbus
- Cincinnati
- Dayton

Pick **exactly 3** Ohio cities. A good combination for driving from Minneapolis: **Cleveland, Columbus, Cincinnati** (they form a logical driving route).

## Step 2: Check Distances and Travel Times

Use `googleDistanceMatrix/distance.csv` to find driving distances and durations between:
- Minneapolis → first Ohio city (e.g., Cleveland)
- Between the 3 Ohio cities
- Last Ohio city → Minneapolis (return)

Plan driving days so that long drives are on Day 1 and Day 7, with shorter inter-city drives on middle days.

## Step 3: Plan the Day-by-Day Route

A suggested 7-day structure:

| Day | Date | Current City | Notes |
|-----|------|-------------|-------|
| 1 | Mar 17 | from Minneapolis to Cleveland | Long drive day (~12 hrs) |
| 2 | Mar 18 | Cleveland | Explore Cleveland |
| 3 | Mar 19 | from Cleveland to Columbus | Drive (~2.5 hrs), explore Columbus |
| 4 | Mar 20 | Columbus | Explore Columbus |
| 5 | Mar 21 | from Columbus to Cincinnati | Drive (~1.5 hrs), explore Cincinnati |
| 6 | Mar 22 | Cincinnati | Explore Cincinnati |
| 7 | Mar 23 | from Cincinnati to Minneapolis | Long drive day (~8 hrs) return |

## Step 4: Find Restaurants from Database

Search `restaurants/clean_restaurant_2022.csv` for restaurants in each city. Filter by cuisine types: **American, Mediterranean, Chinese, Italian**.

For each day, assign:
- **breakfast**: a restaurant in the current (or departure) city
- **lunch**: a restaurant in the current city
- **dinner**: a restaurant in the current (or arrival) city

Use the **exact restaurant name** from the database. Format as: `"Restaurant Name, City"`.

On long travel days (Day 1, Day 7), breakfast can be in the departure city and dinner in the arrival city. Use `"-"` for any meal that cannot be reasonably scheduled.

## Step 5: Find Attractions from Database

Search `attractions/attractions.csv` for attractions in each Ohio city visited.

List 1–3 attractions per day. Format: `"Attraction1;Attraction2;"` (semicolon-separated, ending with semicolon).

On heavy travel days, list fewer attractions or attractions near the route. Use `"-"` if no attractions are visited that day.

## Step 6: Find Pet-Friendly Accommodations from Database

Search `accommodations/clean_accommodations_2022.csv` for accommodations in each city where you stay overnight. Look for columns indicating pet-friendliness (e.g., "pets allowed", "Pets", or similar boolean/flag columns). Select accommodations that allow pets.

### CRITICAL REQUIREMENT — Pet-Friendly Naming Rule
**Every accommodation entry in the output MUST include the words "Pet Friendly" in the string**, regardless of whether the original database name contains those words. Format the accommodation field as:

```
"Pet Friendly - [Exact Accommodation Name from DB], [City]"
```

For example:
- `"Pet Friendly - Cozy Cleveland Suite, Cleveland"`
- `"Pet Friendly - Downtown Columbus Loft, Columbus"`
- `"Pet Friendly - Charming Cincinnati Home, Cincinnati"`

This is a **mandatory formatting rule** — never omit "Pet Friendly" from the accommodation string.

On the last day (return to Minneapolis), if not staying overnight, set accommodation to `"-"`.

## Step 7: Budget Check

Estimate costs:
- **Accommodation**: sum nightly rates for 6 nights across the 3 cities
- **Meals**: ~$50–80/day for 2 people
- **Transportation**: gas costs for self-driving (estimate from distances)
- **Attractions**: entry fees if applicable

Total must stay ≤ **$5,100**.

## Step 8: Output JSON

Write the file to `/app/output/itinerary.json`:

```json
{
  "plan": [
    {
      "day": 1,
      "current_city": "from Minneapolis to Cleveland",
      "transportation": "Self-driving: from Minneapolis to Cleveland",
      "breakfast": "-",
      "lunch": "-",
      "dinner": "[Restaurant Name], Cleveland",
      "attraction": "-",
      "accommodation": "Pet Friendly - [Accommodation Name], Cleveland"
    },
    {
      "day": 2,
      "current_city": "Cleveland",
      "transportation": "-",
      "breakfast": "[Restaurant], Cleveland",
      "lunch": "[Restaurant], Cleveland",
      "dinner": "[Restaurant], Cleveland",
      "attraction": "Rock & Roll Hall of Fame;West Side Market;",
      "accommodation": "Pet Friendly - [Accommodation Name], Cleveland"
    },
    {
      "day": 3,
      "current_city": "from Cleveland to Columbus",
      "transportation": "Self-driving: from Cleveland to Columbus",
      "breakfast": "[Restaurant], Cleveland",
      "lunch": "[Restaurant], Columbus",
      "dinner": "[Restaurant], Columbus",
      "attraction": "[Attraction1];[Attraction2];",
      "accommodation": "Pet Friendly - [Accommodation Name], Columbus"
    },
    {
      "day": 4,
      "current_city": "Columbus",
      "transportation": "-",
      "breakfast": "[Restaurant], Columbus",
      "lunch": "[Restaurant], Columbus",
      "dinner": "[Restaurant], Columbus",
      "attraction": "[Attraction1];[Attraction2];",
      "accommodation": "Pet Friendly - [Accommodation Name], Columbus"
    },
    {
      "day": 5,
      "current_city": "from Columbus to Cincinnati",
      "transportation": "Self-driving: from Columbus to Cincinnati",
      "breakfast": "[Restaurant], Columbus",
      "lunch": "[Restaurant], Cincinnati",
      "dinner": "[Restaurant], Cincinnati",
      "attraction": "[Attraction1];[Attraction2];",
      "accommodation": "Pet Friendly - [Accommodation Name], Cincinnati"
    },
    {
      "day": 6,
      "current_city": "Cincinnati",
      "transportation": "-",
      "breakfast": "[Restaurant], Cincinnati",
      "lunch": "[Restaurant], Cincinnati",
      "dinner": "[Restaurant], Cincinnati",
      "attraction": "[Attraction1];[Attraction2];",
      "accommodation": "Pet Friendly - [Accommodation Name], Cincinnati"
    },
    {
      "day": 7,
      "current_city": "from Cincinnati to Minneapolis",
      "transportation": "Self-driving: from Cincinnati to Minneapolis",
      "breakfast": "[Restaurant], Cincinnati",
      "lunch": "-",
      "dinner": "-",
      "attraction": "-",
      "accommodation": "-"
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

## Key Rules Checklist
1. ✅ Exactly 7 days (March 17–23, 2022)
2. ✅ Exactly 3 Ohio cities visited
3. ✅ No flights — only self-driving
4. ✅ **Every accommodation string MUST contain "Pet Friendly"** — format as `"Pet Friendly - [Name]"`
5. ✅ Cuisine variety: American, Mediterranean, Chinese, Italian
6. ✅ All restaurant, attraction, and accommodation names come from the database
7. ✅ Budget ≤ $5,100
8. ✅ Attractions end with semicolon: `"Attraction1;Attraction2;"`
9. ✅ Use `"-"` for skipped meals, transport, or accommodation on final day
10. ✅ `data_sources` lists all database files used