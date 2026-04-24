---
name: travel-database-parser
description: Parse and search travel-related databases including cities, accommodations, restaurants, attractions, and distances. Use this skill whenever building a travel itinerary that requires querying real-world data from CSV files or text databases. This skill helps extract relevant POIs, lodging, dining, and routing information from structured datasets.
---

# Travel Database Parser

This skill provides techniques for searching, parsing, and querying travel-related databases that store information about cities, accommodations, restaurants, attractions, and distance matrices.

## Database File Locations

The travel databases are typically organized as:
- **Cities**: `background/citySet_with_states.txt` - Contains city names and state information
- **Accommodations**: `accommodations/clean_accommodations_2022.csv` - Pet-friendly lodging options
- **Restaurants**: `restaurants/clean_restaurant_2022.csv` - Dining establishments by cuisine type
- **Attractions**: `attractions/attractions.csv` - Tourist attractions and POIs
- **Distances**: `googleDistanceMatrix/distance.csv` - Travel distances and times between cities

## Parsing Strategy

### 1. Load and Index Databases

Before searching, load each database into memory:

```python
import csv
import json

# Load cities
cities = {}
with open('background/citySet_with_states.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        city_name = parts[0].strip()
        state = parts[1].strip() if len(parts) > 1 else ''
        cities[city_name] = state

# Load accommodations
accommodations = []
with open('accommodations/clean_accommodations_2022.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        accommodations.append(row)

# Load restaurants
restaurants = []
with open('restaurants/clean_restaurant_2022.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        restaurants.append(row)

# Load attractions
attractions = []
with open('attractions/attractions.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        attractions.append(row)

# Load distances
distances = {}
with open('googleDistanceMatrix/distance.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row['from'], row['to'])
        distances[key] = row
```

### 2. Search by City

To find accommodations, restaurants, and attractions for a specific city:

```python
def find_accommodations(city, pet_friendly=False):
    results = [r for r in accommodations if r.get('city', '').lower() == city.lower()]
    if pet_friendly:
        results = [r for r in results if r.get('pet_friendly') == '1' or 'pet' in r.get('amenities', '').lower()]
    return results

def find_restaurants(city, cuisine_type=None):
    results = [r for r in restaurants if r.get('city', '').lower() == city.lower()]
    if cuisine_type:
        results = [r for r in results if cuisine_type.lower() in r.get('cuisine', '').lower()]
    return results

def find_attractions(city):
    results = [a for a in attractions if a.get('city', '').lower() == city.lower()]
    return results
```

### 3. Query Distances

Look up travel distances and times between cities:

```python
def get_distance(from_city, to_city):
    key = (from_city, to_city)
    if key in distances:
        return distances[key]
    return None
```

### 4. Filter by Constraints

When building an itinerary, apply filters for:
- **Pet-friendly**: Check accommodation amenities or pet policies
- **Cuisine types**: Match restaurants to dietary/preference requirements
- **Budget**: Filter accommodations and restaurants by price ranges
- **Distance/Travel time**: Verify feasibility of daily routes

## Key Considerations

- **Field names vary by dataset**: Always check CSV headers; common variations include `City`, `city`, `CITY`
- **Pet-friendly fields**: Check for boolean flags, amenity lists, or policy descriptions
- **Cuisine categories**: May be comma-separated or single-valued; normalize to consistent format
- **Pricing**: Some databases use price ranges (e.g., "$$$"), others use exact costs; extract numeric values where available
- **Attraction descriptions**: May be brief or detailed; concatenate multiple attractions with semicolons for clarity

## Example: Building a City Summary

```python
def summarize_city(city_name, num_accommodations=3, num_restaurants=3, num_attractions=3):
    accomodations = find_accommodations(city_name, pet_friendly=True)[:num_accommodations]
    restaurants = find_restaurants(city_name)[:num_restaurants]
    attractions = find_attractions(city_name)[:num_attractions]

    return {
        'city': city_name,
        'accommodations': accommodations,
        'restaurants': restaurants,
        'attractions': attractions
    }
```

When using these functions in a real itinerary builder, always verify that the data exists and handle empty result sets gracefully.
