---
name: itinerary-builder
description: Build multi-day travel itineraries in JSON format from database lookups. Use this skill when constructing day-by-day travel plans with transportation, meals, attractions, and accommodations.
---

# Itinerary Builder

## Output Format

Write to `/app/output/itinerary.json` with this structure:

```json
{
  "plan": [
    {
      "day": 1,
      "current_city": "CityA" or "from CityA to CityB",
      "transportation": "Self-driving: from CityA to CityB" or "-",
      "breakfast": "Restaurant Name, City" or "-",
      "lunch": "Restaurant Name, City" or "-",
      "dinner": "Restaurant Name, City" or "-",
      "attraction": "Attraction1;Attraction2;",
      "accommodation": "Accommodation Name"
    }
  ],
  "data_sources": ["file1.csv", "file2.csv"]
}
```

## Planning Strategy

1. **Route optimization**: Minimize backtracking. For a round-trip, choose a logical geographic loop.
2. **Travel days**: On long driving days (8+ hours), plan fewer attractions. Breakfast in departure city, dinner in arrival city.
3. **Budget tracking**: Sum accommodations (per night), meals (per meal for 2), and transport costs. Stay under budget.
4. **Cuisine variety**: Spread requested cuisine types across days. Match restaurant cuisines from the Cuisines column.
5. **Constraints**: No flights means self-driving only. Pet-friendly means exclude "No pets" accommodations. Check minimum nights and max occupancy.
6. **Attractions**: Pick 2-3 per full day in a city, 1 on travel days. End attraction list with semicolon.
7. **Accommodation**: Use same accommodation for consecutive nights in the same city.

## Data Sources to List

Always include all dataset files actually consulted:
- `background/citySet_with_states.txt`
- `accommodations/clean_accommodations_2022.csv`
- `restaurants/clean_restaurant_2022.csv`
- `attractions/attractions.csv`
- `googleDistanceMatrix/distance.csv`
