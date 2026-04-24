---
name: travel_data_retrieval
description: Use this skill to query the local databases for distances, cities, accommodations, restaurants, and attractions to gather real-world data for an itinerary.
---

### 1. File Locations & Data Sources
You have access to several local databases (CSV, JSON, or TXT format). Use standard shell commands (e.g., `grep`, `awk`, `cat`) or Python scripts to search them. Do not hallucinate data; only use entries found in these files. Common files include:
- `background/citySet_with_states.txt` (List of valid cities and states)
- `googleDistanceMatrix/distance.csv` (Driving distances and costs between cities)
- `accommodations/clean_accommodations_2022.csv` (Hotels and lodging)
- `restaurants/clean_restaurant_2022.csv` (Restaurants and cuisines)
- `attractions/attractions.csv` (Points of interest)

### 2. Search Strategies
- **Transportation**: Since flights are often excluded, use `googleDistanceMatrix/distance.csv` to find driving distances, times, and costs between the starting city and destination cities.
- **Accommodations**: Filter accommodations by the destination city and required amenities. If the user has a pet, grep for terms like "pet", "dog", or "cat" within the accommodation descriptions or amenities columns.
- **Restaurants**: Filter by city and the exact cuisines requested (e.g., American, Mediterranean, Chinese, Italian). Ensure you find enough unique options to cover the trip duration without unnecessary repetition.
- **Attractions**: Query the attractions database for the destination cities.

### 3. Budget Tracking
Keep a running total of the costs for:
1. Transportation (Self-driving cost is usually derived from distance).
2. Accommodations (Multiply nightly rate by number of nights and number of rooms if applicable).
3. Meals (Estimate based on standard pricing or provided data).
4. Attractions (Sum up entry fees).
Ensure the total calculated cost is strictly less than or equal to the user's budget constraint.

### 4. Logistics & Time Rules
- Only travel between cities if it makes logical geographic sense.
- Account for travel time in the daily schedule. If a day involves significant driving, limit the number of attractions and meals in different cities.