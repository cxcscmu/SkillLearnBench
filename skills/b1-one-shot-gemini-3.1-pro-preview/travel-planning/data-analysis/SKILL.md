---
name: data-analysis
description: Using Python and Pandas to analyze large CSV datasets and filter based on specific criteria like budget, location, and amenities.
---

# Data Analysis using Pandas

This skill covers the basic operations needed to filter and extract information from structured datasets (CSVs) using Python and Pandas.

## Key Concepts

- Loading data from CSV using `pd.read_csv()`
- Filtering data using boolean indexing (e.g., `df[df['city'] == 'Minneapolis']`)
- Selecting random or top N items from a dataset.
- Handling multiple conditions simultaneously.

## Usage Example

```python
import pandas as pd

# Load dataset
df = pd.read_csv('data/accommodations/clean_accommodations_2022.csv')

# Filter for pet-friendly accommodations in a specific city
city_hotels = df[(df['city'] == 'Cleveland') & (df['pet_friendly'] == True)]

# Select the top option
best_hotel = city_hotels.head(1)
```
