---
name: travel-data-query
description: Query and filter travel CSV datasets (restaurants, accommodations, attractions, distances) using Python. Use this skill whenever you need to extract specific records from the travel database files, check pet policies, filter by cuisine, look up driving times, or validate that a city exists in the dataset.
---

# Travel Data Query

## Dataset Schema

### `data/restaurants/clean_restaurant_2022.csv`
| Column | Type | Notes |
|---|---|---|
| (index) | int | Row number |
| Name | str | Restaurant name |
| City | str | City name |
| Cuisines | str | Comma-separated list |
| Average Cost | int | Cost per meal (USD) |
| Aggregate Rating | float | 0.0–5.0 |

### `data/accommodations/clean_accommodations_2022.csv`
| Column | Type | Notes |
|---|---|---|
| (index) | int | Row number |
| NAME | str | Property name |
| room type | str | Private room / Entire home/apt / Shared room |
| price | float | Per night (USD) |
| minimum nights | float | Min booking nights |
| review rate number | float | 1–5 |
| house_rules | str | Restrictions (e.g. "No pets & No smoking") |
| maximum occupancy | int | Max guests |
| city | str | City name (lowercase key) |

### `data/attractions/attractions.csv`
| Column | Type | Notes |
|---|---|---|
| Name | str | Attraction name |
| Latitude | float | |
| Longitude | float | |
| Address | str | |
| Phone | str | |
| Website | str | |
| City | str | City name |

### `data/googleDistanceMatrix/distance.csv`
| Column | Type | Notes |
|---|---|---|
| origin | str | Departure city |
| destination | str | Arrival city |
| cost | str | Usually empty |
| duration | str | e.g. "2 hours 8 mins" |
| distance | str | e.g. "228 km" |

### `data/background/citySet_with_states.txt`
Tab-separated: `CityName\tStateName`

## Common Query Patterns

### Find pet-friendly accommodations
```python
import csv
with open('data/accommodations/clean_accommodations_2022.csv') as f:
    reader = csv.DictReader(f)
    results = [r for r in reader
               if r['city'] == 'Cleveland'
               and 'No pets' not in r['house_rules']
               and float(r['minimum nights']) <= 2]
```

### Find restaurants by cuisine
```python
import csv
with open('data/restaurants/clean_restaurant_2022.csv') as f:
    reader = csv.DictReader(f)
    results = [r for r in reader
               if r['City'] == 'Columbus'
               and any(c in r['Cuisines'] for c in ['American', 'Italian'])]
```

### Look up driving distance
```python
import csv
with open('data/googleDistanceMatrix/distance.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['origin'] == 'Minneapolis' and row['destination'] == 'Cleveland':
            print(row['duration'], row['distance'])
```

### Verify city exists
```python
with open('data/background/citySet_with_states.txt') as f:
    cities = [line.strip().split('\t') for line in f]
    ohio_cities = [c[0] for c in cities if len(c) > 1 and c[1] == 'Ohio']
```

## Tips
- `house_rules` uses `" & "` as separator; check with `'No pets' not in row['house_rules']`
- `Cuisines` is comma+space separated; simple substring search works
- Distance matrix is not symmetric — always check both directions if needed
- Some accommodations have `minimum nights` > 7; always filter for the planned stay length
