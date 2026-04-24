---
name: run2_travel-data-extraction
description: Extract and validate travel data from CSV/TXT databases ensuring city-specific matching and constraint compliance.
---

# Travel Data Extraction (Improved)

## Data Sources
- `data/background/citySet_with_states.txt` - Tab-separated city/state pairs
- `data/accommodations/clean_accommodations_2022.csv` - Columns: index, NAME, room type, price, minimum nights, review rate number, house_rules, maximum occupancy, city
- `data/restaurants/clean_restaurant_2022.csv` - Columns: index, Name, City, Cuisines, Average Cost, Aggregate Rating
- `data/attractions/attractions.csv` - Columns: Name, Latitude, Longitude, Address, Phone, Website, City
- `data/googleDistanceMatrix/distance.csv` - Columns: origin, destination, cost, duration, distance

## Critical: City-Specific Validation
When searching for entities, ALWAYS verify the city column matches. Names can appear in multiple cities:
```bash
# WRONG - may match wrong city
grep "Restaurant Name" restaurants.csv
# RIGHT - verify city match
grep "Restaurant Name.*TargetCity" restaurants.csv
```

## Pet-Friendly Accommodations
Filter: rows where `house_rules` does NOT contain "No pets". Also check:
- `maximum_occupancy` >= party size (2 for couples)
- `minimum_nights` <= planned stay length
- Price fits within budget

## Cuisine Matching
The Cuisines field is comma-separated. Match keywords: American, Mediterranean, Chinese, Italian.
Ensure all 4 cuisine types appear across the itinerary's meals.

## Distance Data
- Self-driving cost column is always empty
- Duration format: "X hours Y mins" or "X mins"
- Distance format: "X,XXX km" with comma separators
