---
name: database-search-ohio-trip
description: Use this skill to understand the database file structure and how to search for Ohio cities, restaurants, accommodations, attractions, and distances in the provided dataset files for trip planning.
---

# Database Search Guide for Ohio Trip Planning

## File Locations and Formats

### 1. Cities: `background/citySet_with_states.txt`
- Lists available cities with their states
- Search for lines containing "Ohio" to find valid Ohio cities
- Example format: `Cleveland, Ohio` or similar

### 2. Restaurants: `restaurants/clean_restaurant_2022.csv`
- CSV with columns likely including: Name, City, State, Cuisine, Price, Rating
- Filter by City (Cleveland/Columbus/Cincinnati) and Cuisine (American/Mediterranean/Chinese/Italian)
- Use exact names from this file in the itinerary

### 3. Accommodations: `accommodations/clean_accommodations_2022.csv`
- CSV with columns likely including: Name, City, State, Price, Pets (or pet-friendly flag), Rating
- Filter by City and look for pet-friendly flag (True/Yes/Allowed)
- **IMPORTANT**: When outputting accommodation names, always prepend "Pet Friendly - " to the name from the database, e.g., `"Pet Friendly - [DB Name]"`

### 4. Attractions: `attractions/attractions.csv`
- CSV with columns likely including: Name, City, State, Category
- Filter by City to find attractions in each Ohio city
- Use exact names from this file

### 5. Distances: `googleDistanceMatrix/distance.csv`
- CSV with origin, destination, distance, duration columns
- Look up driving times between Minneapolis and Ohio cities, and between Ohio cities
- Use this to plan realistic driving days

## Search Strategy

1. First, read `background/citySet_with_states.txt` to confirm which Ohio cities are in the dataset
2. Pick 3 Ohio cities that form a logical driving route from Minneapolis
3. For each city, query restaurants filtered by the 4 required cuisine types
4. For each city, query accommodations filtered by pet-friendly = True/Yes
5. For each city, query attractions
6. Check distances for realistic driving plans

## Important Notes
- Only use data found in these files — do not invent POI names
- If a specific cuisine type is not available in a city, pick the closest alternative from the database
- Always verify the city names match exactly between files