---
name: travel-data-querying
description: Querying travel planning datasets (cities, restaurants, accommodations, attractions, distances) for itinerary generation.
---

# Travel Data Querying

## Dataset Structure

All data lives under `/app/data/` with these files:

### Cities
- `background/citySet_with_states.txt` — Tab-separated: `CityName\tState`
- `background/citySet.txt` — City names only
- `background/stateSet.txt` — State names only

### Restaurants
- `restaurants/clean_restaurant_2022.csv`
- Columns: `index, Name, City, Cuisines, Average Cost, Aggregate Rating`
- Cuisines is a comma-separated string (e.g., "Tea, Pizza, Indian, Seafood")
- Average Cost is per meal (numeric)

### Accommodations
- `accommodations/clean_accommodations_2022.csv`
- Columns: `index, NAME, room type, price, minimum nights, review rate number, house_rules, maximum occupancy, city`
- `house_rules` contains constraints like "No pets", "No smoking", "No parties", "No children under 10", "No visitors"
- Price is per night

### Attractions
- `attractions/attractions.csv`
- Columns: `Name, Latitude, Longitude, Address, Phone, Website, City`

### Distances
- `googleDistanceMatrix/distance.csv`
- Columns: `origin, destination, cost, duration, distance`
- `cost` column is empty for driving (only populated for flights)
- Duration is human-readable (e.g., "3 hours 11 mins")
- Distance in km

### Flights
- `flights/clean_Flights_2022.csv` — Not used when flights are excluded

## Querying Patterns

### Find cities in a state
```bash
grep -i "ohio" data/background/citySet_with_states.txt
```

### Find restaurants by city and cuisine
```bash
grep -i "cleveland" data/restaurants/clean_restaurant_2022.csv | grep -i "italian"
```

### Find pet-friendly accommodations (exclude "No pets")
```bash
grep -i "cleveland" data/accommodations/clean_accommodations_2022.csv | grep -iv "no pets"
```

### Find driving distances between cities
```bash
grep -E "^Cleveland,Dayton," data/googleDistanceMatrix/distance.csv
```
