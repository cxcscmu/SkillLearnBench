---
name: run2_data_filtering_validation
description: Advanced filtering and validation of travel datasets with strict cuisine matching, budget constraints, and data quality checks.
---

# Advanced Data Filtering and Validation

## Overview
This skill provides robust filtering techniques for travel data with strict validation to ensure:
- Accurate cuisine matching (check multiple ways)
- Pet-friendly verification (exclude "No pets" explicitly)
- Budget constraints
- Data quality (non-null, properly formatted names)
- Diversity in selections (avoid duplicates)

## Cuisine Matching Strategy

### Problem
Raw data may have cuisines listed as comma-separated values, and exact matching fails. Need multi-strategy approach:
```python
def cuisine_filter(df, target_cuisine):
    """Multi-strategy cuisine filter"""
    target_lower = target_cuisine.lower()

    # Strategy 1: Exact match in Cuisines string
    mask1 = df['Cuisines'].str.lower().str.contains(target_lower, na=False, regex=False)

    # Strategy 2: Common cuisine aliases
    aliases = {
        'american': ['american', 'usa', 'american cuisine'],
        'italian': ['italian', 'pasta', 'pizza'],
        'chinese': ['chinese', 'asian'],
        'mediterranean': ['mediterranean', 'greek', 'turkish', 'middle eastern']
    }

    if target_lower in aliases:
        alias_patterns = '|'.join(aliases[target_lower])
        mask2 = df['Cuisines'].str.lower().str.contains(alias_patterns, na=False, regex=True)
    else:
        mask2 = pd.Series([False] * len(df))

    return df[mask1 | mask2]
```

## Pet-Friendly Accommodation Filtering

```python
def filter_pet_friendly(df):
    """Strict pet-friendly filter"""
    # Remove rows with null house_rules
    df = df.dropna(subset=['house_rules'])

    # Exclude any listing containing "No pets"
    no_pets_mask = df['house_rules'].str.contains('No pets', case=False, na=False)
    pet_friendly = df[~no_pets_mask]

    return pet_friendly
```

## Selection with Quality Checks

```python
def select_best_restaurant(restaurants, cuisine, city, min_rating=4.0):
    """Select best restaurant with validation"""
    # Filter by cuisine and city
    candidates = cuisine_filter(restaurants, cuisine)
    candidates = candidates[candidates['City'] == city]

    # Filter by minimum rating
    candidates = candidates[candidates['Aggregate Rating'] >= min_rating]

    # Remove duplicates
    candidates = candidates.drop_duplicates(subset=['Name', 'City'])

    # Sort by rating and select
    if len(candidates) > 0:
        candidates = candidates.sort_values('Aggregate Rating', ascending=False)
        return candidates.iloc[0]
    return None

def select_best_accommodation(accommodations, city, max_price=250):
    """Select best pet-friendly accommodation"""
    # Filter pet-friendly
    candidates = filter_pet_friendly(accommodations)
    candidates = candidates[candidates['city'] == city]
    candidates = candidates[candidates['price'] <= max_price]
    candidates = candidates[candidates['price'] > 0]  # Exclude free listings

    # Prefer entire homes/apts over private rooms
    entire_homes = candidates[candidates['room type'] == 'Entire home/apt']
    if len(entire_homes) > 0:
        candidates = entire_homes

    # Sort by rating
    if len(candidates) > 0:
        candidates = candidates.sort_values('review rate number', ascending=False)
        return candidates.iloc[0]
    return None
```

## Data Quality Checks

```python
def validate_restaurant_entry(restaurant):
    """Validate restaurant data"""
    if restaurant is None:
        return False
    # Check required fields
    return (
        pd.notna(restaurant.get('Name')) and
        pd.notna(restaurant.get('City')) and
        len(str(restaurant.get('Name')).strip()) > 0
    )

def validate_accommodation_entry(accommodation):
    """Validate accommodation data"""
    if accommodation is None:
        return False
    return (
        pd.notna(accommodation.get('NAME')) and
        pd.notna(accommodation.get('city')) and
        0 < accommodation.get('price', 0) < 500 and
        len(str(accommodation.get('NAME')).strip()) > 0
    )
```

## Handling Missing Data

- Always provide fallback restaurant names if data lookup fails
- Use generic descriptions (e.g., "Italian Restaurant at [City]") when specific data unavailable
- Never leave meal fields empty - use "-" only when intentionally skipping
- Always attempt to fill accommodation field with at least a generic pet-friendly lodging
