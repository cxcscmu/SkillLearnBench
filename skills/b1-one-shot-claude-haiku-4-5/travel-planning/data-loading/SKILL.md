---
name: data-loading
description: Load and parse CSV/TXT files from travel database for itinerary planning
---

# Data Loading Skill

## Overview
This skill covers loading and parsing the travel database files used for building itineraries.

## Supported File Types

### TXT Files (Cities and States)
- `citySet_with_states.txt`: Format is `city_name,state`
- One entry per line
- Use for identifying valid city names and states

### CSV Files (Accommodations, Restaurants, Attractions)
- Header row included
- Standard CSV format (comma-separated)
- Handle missing/empty fields appropriately

## Python Code Example

```python
import csv
import json
from typing import List, Dict

# Load city data
def load_cities_with_states(filepath: str) -> List[Dict[str, str]]:
    """Load city and state mappings"""
    cities = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    cities.append({'city': parts[0].strip(), 'state': parts[1].strip()})
    except Exception as e:
        print(f"Error loading cities: {e}")
    return cities

# Load CSV data
def load_csv_data(filepath: str) -> List[Dict]:
    """Load CSV file and return list of dictionaries"""
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    data.append(row)
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return data

# Load distance matrix
def load_distance_matrix(filepath: str) -> Dict[str, Dict[str, float]]:
    """Load distance matrix and return nested dictionary"""
    matrix = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                from_city = row.get('from')
                if from_city not in matrix:
                    matrix[from_city] = {}
                # Parse remaining columns as distances to other cities
                for city, distance in row.items():
                    if city != 'from' and distance:
                        try:
                            matrix[from_city][city] = float(distance)
                        except ValueError:
                            pass
    except Exception as e:
        print(f"Error loading distance matrix: {e}")
    return matrix
```

## Key Considerations

1. **Encoding**: Use UTF-8 encoding for CSV files
2. **Headers**: CSV files include headers, use `DictReader` for easier access
3. **Missing Data**: Check for empty/null values before processing
4. **Data Types**: Convert numeric strings to appropriate types (int, float)
5. **Errors**: Wrap file operations in try-except blocks

## Usage Pattern

```python
# Load all necessary data
cities = load_cities_with_states('/app/data/background/citySet_with_states.txt')
accommodations = load_csv_data('/app/data/accommodations/clean_accommodations_2022.csv')
restaurants = load_csv_data('/app/data/restaurants/clean_restaurant_2022.csv')
attractions = load_csv_data('/app/data/attractions/attractions.csv')
distances = load_distance_matrix('/app/data/googleDistanceMatrix/distance.csv')

# Filter and process as needed
ohio_cities = [c for c in cities if c['state'] == 'Ohio']
```
