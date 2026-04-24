---
name: travel-data-lookup
description: Look up travel data from the local CSV/TXT database for cities, restaurants, accommodations, attractions, and distances. Use this skill whenever planning a trip, building an itinerary, or querying travel-related datasets in /app/data/.
---

# Travel Data Lookup

## Data Sources

All travel data lives under `/app/data/` with these files:

| File | Description | Key Columns |
|------|-------------|-------------|
| `background/citySet_with_states.txt` | City-to-state mapping (tab-separated) | city, state |
| `restaurants/clean_restaurant_2022.csv` | 9,550 restaurant listings | Name, City, Cuisines, Average Cost, Aggregate Rating |
| `accommodations/clean_accommodations_2022.csv` | 5,062 accommodation listings | NAME, room type, price, minimum nights, review rate number, house_rules, maximum occupancy, city |
| `attractions/attractions.csv` | 5,301 attractions | Name, Latitude, Longitude, Address, Phone, Website, City |
| `googleDistanceMatrix/distance.csv` | 17,601 city-pair distances | origin, destination, cost, duration, distance |
| `flights/clean_Flights_2022.csv` | Flight records (avoid if no-fly constraint) | Flight Number, Price, DepTime, ArrTime, FlightDate, OriginCityName, DestCityName |

## Querying Patterns

- **Find cities in a state**: `grep -i "state_name" data/background/citySet_with_states.txt`
- **Find restaurants by city**: `grep -i ",CityName" data/restaurants/clean_restaurant_2022.csv` (city is last column; anchor with trailing match)
- **Filter by cuisine**: After getting city restaurants, filter lines containing target cuisine keywords (American, Italian, Chinese, Mediterranean, etc.)
- **Pet-friendly accommodations**: Filter OUT rows with "No pets" in house_rules column. Also check `maximum occupancy >= party_size` and `minimum nights <= stay_duration`.
- **Distances between cities**: `grep -i "origin_city" data/googleDistanceMatrix/distance.csv | grep -i "dest_city"`. Note: cost column is often empty for driving; use distance for gas estimation.

## Budget Estimation

- **Accommodations**: price column is per-night rate
- **Restaurants**: Average Cost column is cost for two people
- **Self-driving cost**: Estimate ~$0.15/km for gas based on distance column (strip commas and "km")
- **No cost data in distance matrix**: The cost column for self-driving routes is typically empty; estimate from distance

## Pet-Friendly Filter

The `house_rules` column contains rules like "No pets", "No smoking", "No parties", "No visitors", "No children under 10". To find pet-friendly places, exclude any row where house_rules contains "No pets" (case-insensitive).
