name: itinerary-data-researcher
description: How to extract travel data from the project's CSV files. Use this skill when searching for accommodations, restaurants, attractions, or distances.

## Data Extraction Guidelines

### 1. Accommodations (data/accommodations/clean_accommodations_2022.csv)
- **Columns:** `,NAME,room type,price,minimum nights,review rate number,house_rules,maximum occupancy,city`
- **Pet-Friendly Check:** Search for `house_rules` that DO NOT contain "No pets". Use `grep` to filter for the city and then check rules.
- **Price:** Ensure `price` fits within the daily budget (approx. $200-$400 per night).

### 2. Restaurants (data/restaurants/clean_restaurant_2022.csv)
- **Columns:** `,Name,City,Cuisines,Average Cost,Aggregate Rating`
- **Cuisine Matching:** Filter by `City` and then by `Cuisines` (American, Mediterranean, Chinese, Italian).
- **Cost:** `Average Cost` is for two people.

### 3. Attractions (data/attractions/attractions.csv)
- **Columns:** `Name,Latitude,Longitude,Address,Phone,Website,City`
- **Selection:** Filter by `City` and select popular or interesting POIs.

### 4. Distances (data/googleDistanceMatrix/distance.csv)
- **Columns:** `origin,destination,cost,duration,distance`
- **Travel Planning:** Use `duration` to estimate travel time. Ensure no flights are used.
