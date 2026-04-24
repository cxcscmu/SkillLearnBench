---
name: data-processing
description: Filter CSV data (restaurants, accommodations, attractions) based on criteria like city, cuisine, budget, and pet-friendliness.
---
# Data Processing

Use Pandas to filter travel datasets efficiently.

## Example Usage

```python
import pandas as pd

def filter_restaurants(df, city, cuisines):
    # Filter by city
    city_df = df[df['City'].str.lower() == city.lower()]
    # Filter by cuisines (assuming Cuisines is a string like "American, Italian")
    pattern = '|'.join(cuisines)
    return city_df[city_df['Cuisines'].str.contains(pattern, case=False, na=False)]

def filter_accommodations(df, city, budget_per_night, pet_friendly=True):
    city_df = df[df['city'].str.lower() == city.lower()]
    if pet_friendly:
        # Assuming pet-friendly means 'No pets' is NOT in house_rules
        city_df = city_df[~city_df['house_rules'].str.contains('No pets', case=False, na=False)]
    return city_df[city_df['price'] <= budget_per_night]
```
