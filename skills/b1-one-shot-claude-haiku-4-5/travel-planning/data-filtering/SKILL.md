---
name: data-filtering
description: Filter accommodations, restaurants, and attractions by travel requirements
---

# Data Filtering Skill

## Overview
Filter travel data by specific criteria like pet-friendly status, cuisine type, location, and price range.

## Common Filter Scenarios

### Accommodations
- Pet-friendly filter
- Price range (budget, mid-range, luxury)
- Location (city, zip code)
- Amenities (WiFi, parking, breakfast)

### Restaurants
- Cuisine type (American, Mediterranean, Chinese, Italian, etc.)
- Location/city
- Price range
- Rating/reviews

### Attractions
- City location
- Category (museum, park, historical, etc.)
- Open during trip dates

## Python Code Example

```python
from typing import List, Dict
import re

def filter_pet_friendly_accommodations(
    accommodations: List[Dict],
    pet_friendly_field: str = 'pet_friendly'
) -> List[Dict]:
    """Filter accommodations that allow pets"""
    result = []
    for acc in accommodations:
        pet_field = acc.get(pet_friendly_field, '').lower()
        # Handle various formats: 'yes', 'true', '1', 'pet-friendly'
        if pet_field in ['yes', 'true', '1', 'pet friendly', 'pets allowed']:
            result.append(acc)
        elif 'pet' in pet_field and 'no' not in pet_field:
            result.append(acc)
    return result

def filter_by_cuisine(
    restaurants: List[Dict],
    cuisine_type: str,
    cuisine_field: str = 'Cuisine'
) -> List[Dict]:
    """Filter restaurants by cuisine type"""
    result = []
    cuisine_lower = cuisine_type.lower()

    for rest in restaurants:
        cuisines = rest.get(cuisine_field, '').lower()
        # Handle comma-separated cuisines
        if ',' in cuisines:
            cuisines_list = [c.strip() for c in cuisines.split(',')]
            if any(cuisine_lower in c for c in cuisines_list):
                result.append(rest)
        elif cuisine_lower in cuisines:
            result.append(rest)

    return result

def filter_by_city(
    data: List[Dict],
    city: str,
    city_field: str = 'City'
) -> List[Dict]:
    """Filter data by city"""
    result = []
    city_lower = city.lower()

    for item in data:
        item_city = item.get(city_field, '').lower()
        if item_city == city_lower:
            result.append(item)

    return result

def filter_by_price_range(
    data: List[Dict],
    min_price: float,
    max_price: float,
    price_field: str = 'Price'
) -> List[Dict]:
    """Filter data by price range"""
    result = []

    for item in data:
        try:
            price = float(item.get(price_field, 0))
            if min_price <= price <= max_price:
                result.append(item)
        except (ValueError, TypeError):
            continue

    return result

def filter_attractions_by_city(
    attractions: List[Dict],
    city: str,
    city_field: str = 'City'
) -> List[Dict]:
    """Filter attractions by city"""
    return filter_by_city(attractions, city, city_field)

def combine_filters(
    data: List[Dict],
    filters: Dict
) -> List[Dict]:
    """
    Apply multiple filters to data.
    filters dict: {'city': 'Cleveland', 'price_max': 100, ...}
    """
    result = data

    # Apply city filter
    if 'city' in filters:
        result = filter_by_city(
            result,
            filters['city'],
            filters.get('city_field', 'City')
        )

    # Apply price range filter
    if 'price_min' in filters or 'price_max' in filters:
        min_price = filters.get('price_min', 0)
        max_price = filters.get('price_max', float('inf'))
        result = filter_by_price_range(
            result,
            min_price,
            max_price,
            filters.get('price_field', 'Price')
        )

    # Apply cuisine filter
    if 'cuisine' in filters:
        result = filter_by_cuisine(
            result,
            filters['cuisine'],
            filters.get('cuisine_field', 'Cuisine')
        )

    return result

def select_diverse_options(
    data: List[Dict],
    num_selections: int,
    key_field: str = 'Name'
) -> List[Dict]:
    """Select diverse options avoiding duplicates"""
    seen = set()
    result = []

    for item in data:
        key = item.get(key_field, '').lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
            if len(result) >= num_selections:
                break

    return result
```

## Filter Priority for Trip Planning

1. **Accommodations**: Must be pet-friendly first, then price/location
2. **Restaurants**: Filter by city first, then cuisine type, then price
3. **Attractions**: Filter by city, then availability/type

## Usage Example

```python
# Filter accommodations for Cleveland
cleveland_hotels = filter_by_city(accommodations, 'Cleveland')
pet_friendly = filter_pet_friendly_accommodations(cleveland_hotels)
budget_friendly = filter_by_price_range(pet_friendly, 0, 300)

# Filter restaurants by city and cuisine
cleveland_italian = filter_by_city(restaurants, 'Cleveland')
italian_only = filter_by_cuisine(cleveland_italian, 'Italian')
affordable_italian = filter_by_price_range(italian_only, 0, 80)

# Combine multiple filters
filters = {
    'city': 'Columbus',
    'cuisine': 'Mediterranean',
    'price_max': 100
}
results = combine_filters(restaurants, filters)
```
