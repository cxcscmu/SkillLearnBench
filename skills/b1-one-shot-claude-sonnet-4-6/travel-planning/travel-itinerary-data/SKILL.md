---
name: travel-itinerary-data
description: How to query and filter travel itinerary datasets (restaurants, accommodations, attractions, distances) to build constraint-satisfying travel plans.
---

# Travel Itinerary Data Querying

## Dataset locations (relative to `/app/data/`)
| File | Key columns |
|------|-------------|
| `background/citySet_with_states.txt` | `city TAB state` — enumerate valid cities |
| `restaurants/clean_restaurant_2022.csv` | `id, Name, City, Cuisines, Average Cost, Aggregate Rating` |
| `accommodations/clean_accommodations_2022.csv` | `id, NAME, room type, price, minimum nights, review rate number, house_rules, maximum occupancy, city` |
| `attractions/attractions.csv` | `Name, Latitude, Longitude, Address, Phone, Website, City` |
| `googleDistanceMatrix/distance.csv` | `origin, destination, cost, duration, distance` |

## Common grep patterns

### Find cities in a state
```bash
grep -i "ohio" data/background/citySet_with_states.txt
# → Toledo, Cleveland, Dayton, Columbus, Akron, Cincinnati
```

### Find distances between two cities
```bash
grep -i "^Minneapolis," data/googleDistanceMatrix/distance.csv | grep -i "Cleveland"
# → Minneapolis,Cleveland,,11 hours 14 mins,1219 km
```

### Find pet-friendly accommodations in a city
```bash
# "No pets" in house_rules = NOT pet-friendly; absence = pet-friendly
grep -i ",Cleveland$" data/accommodations/clean_accommodations_2022.csv | grep -v "No pets"
```

### Filter by min occupancy
```bash
# column 8 (0-indexed) = maximum_occupancy
grep -i ",Columbus$" data/accommodations/clean_accommodations_2022.csv \
  | grep -v "No pets" \
  | awk -F',' '$8 >= 2'
```

### Find restaurants by cuisine and city
```bash
grep -i ",Cleveland," data/restaurants/clean_restaurant_2022.csv \
  | grep -i "american\|mediterranean\|chinese\|italian"
```

### Find attractions in a city
```bash
grep -i ",Cleveland$" data/attractions/attractions.csv | cut -d',' -f1
```

## Budget calculation approach
1. **Accommodation**: `price × number_of_nights`; respect `minimum nights`.
2. **Meals**: `Average Cost` in the restaurant CSV is the estimated cost for the meal.
3. **No flights** means all travel is self-driving; use the `distance.csv` for durations.

## Itinerary structure tips
- Travel days (`from A to B`): skip lunch; mark breakfast/dinner based on departure/arrival.
- Minimum nights constraint must be satisfied: e.g., if `minimum nights = 3`, do not book for only 2 nights.
- Pet-friendly = no "No pets" text anywhere in `house_rules`.
- Cover all requested cuisines across the trip, not necessarily each day.
