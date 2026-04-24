---
name: run2_itinerary-data-exploration
description: Explore and query travel dataset files (CSV/TXT) to find cities, restaurants, accommodations, attractions, and driving distances — with precise filtering patterns and data field notes.
---

# Itinerary Data Exploration (Improved)

## Dataset Locations and Schemas

All data is under `/app/data/`:

| File | Key Columns |
|------|-------------|
| `background/citySet_with_states.txt` | `City\tState` (tab-separated, no header) |
| `restaurants/clean_restaurant_2022.csv` | index, Name, City, Cuisines, Average Cost, Aggregate Rating |
| `accommodations/clean_accommodations_2022.csv` | index, NAME, room type, price, minimum nights, review rate number, house_rules, maximum occupancy, city |
| `attractions/attractions.csv` | Name, Latitude, Longitude, Address, Phone, Website, City |
| `googleDistanceMatrix/distance.csv` | origin, destination, cost, duration, distance |

## Key Notes on Fields

- **Restaurants `Average Cost`**: per person per meal. Multiply by number of travelers for total cost.
- **Accommodations `price`**: per night. Multiply by number of nights for total cost.
- **Accommodations `minimum nights`**: stay must be >= this value. Filter with `awk -F',' '$5 <= STAY_NIGHTS'`.
- **Accommodations `maximum occupancy`**: must be >= number of travelers. Filter with `awk`.
- **Pet-friendly**: `house_rules` must NOT contain "No pets". Use `grep -v "No pets"`.
- **Distance CSV**: some entries have empty `cost` field (driving, not paid); `duration` and `distance` are for driving.

## Query Patterns

### Find Ohio cities
```bash
grep -i "Ohio" /app/data/background/citySet_with_states.txt
```
Result: Toledo, Cleveland, Dayton, Columbus, Akron, Cincinnati

### Find driving distance/time between cities
```bash
grep "Minneapolis,Cleveland" /app/data/googleDistanceMatrix/distance.csv
# → Minneapolis,Cleveland,,11 hours 14 mins,1219 km
```

### Find all inter-city distances for Ohio cities
```bash
grep -E "Cleveland|Columbus|Cincinnati|Akron" /app/data/googleDistanceMatrix/distance.csv | \
  grep -E "Cleveland|Columbus|Cincinnati|Akron"
```

### Pet-friendly accommodations with occupancy >= 2 and min nights <= 2
```bash
grep -i ",Cleveland$" /app/data/accommodations/clean_accommodations_2022.csv | \
  grep -v "No pets" | \
  awk -F',' '$5<=2 && $(NF-1)>=2 {print}'
```

### Restaurants by city and preferred cuisine
```bash
grep -i ",Columbus," /app/data/restaurants/clean_restaurant_2022.csv | grep -i "Italian\|American"
```

### Attractions by city (exact city match at end of line)
```bash
grep -w "Columbus" /app/data/attractions/attractions.csv | grep "OH"
# Use OH filter to avoid false matches (e.g., "Columbus St" in other cities)
```

## Verification Pattern
Always verify selected items exist in data:
```bash
grep "Restaurant Name" /app/data/restaurants/clean_restaurant_2022.csv | grep CityName
grep "^INDEX," /app/data/accommodations/clean_accommodations_2022.csv
```
