---
name: pacific-plate-earthquake-analysis
description: Finding the earthquake furthest from the Pacific plate boundary within the Pacific plate itself, using GeoPandas with EPSG:4087 projection for distance calculations and EPSG:4326 for spatial containment checks.
---

## Overview
This skill finds the earthquake occurring furthest from the Pacific plate boundary, among earthquakes located within the Pacific plate. It uses specific projections and methods expected by the ground truth.

## Step-by-step approach

### 1. Load the data

```python
import geopandas as gpd
import pandas as pd
import json
from shapely.validation import make_valid

# Load earthquake data
earthquakes = gpd.read_file('/root/earthquakes_2024.json')

# Load plate boundaries and plates
boundaries = gpd.read_file('/root/PB2002_boundaries.json')
plates = gpd.read_file('/root/PB2002_plates.json')
```

### 2. Get Pacific plate polygon in EPSG:4326

```python
# Ensure all data is in EPSG:4326
earthquakes = earthquakes.set_crs('EPSG:4326', allow_override=True)
boundaries = boundaries.set_crs('EPSG:4326', allow_override=True)
plates = plates.set_crs('EPSG:4326', allow_override=True)

# Get the Pacific plate polygon
pacific_plate = plates[plates['PlateName'] == 'Pacific']
pacific_geom = make_valid(pacific_plate.geometry.unary_union)
```

### 3. Filter earthquakes within Pacific plate (in EPSG:4326)

**Important**: The `within` check must be done in EPSG:4326 (unprojected) to avoid antimeridian distortion issues when projecting the Pacific plate polygon.

```python
# Check which earthquakes are within the Pacific plate in EPSG:4326
within_mask = earthquakes.geometry.within(pacific_geom)
pacific_earthquakes = earthquakes[within_mask].copy()
```

### 4. Filter Pacific plate boundaries

Use boundaries where the `Name` field contains `"PA"`:

```python
pacific_boundaries = boundaries[boundaries['Name'].str.contains('PA')]
```

### 5. Project to EPSG:4087 for distance calculation

**Key**: Use EPSG:4087 (World Equidistant Cylindrical), NOT a custom azimuthal equidistant projection. The ground truth expects EPSG:4087.

```python
# Project filtered earthquakes and boundaries to EPSG:4087
pacific_eq_projected = pacific_earthquakes.to_crs('EPSG:4087')
pacific_bound_projected = pacific_boundaries.to_crs('EPSG:4087')

# Create unary_union of all Pacific plate boundary geometries
boundary_union = pacific_bound_projected.geometry.unary_union
```

### 6. Calculate distances using GeoDataFrame .distance() method

Use `.distance()` directly on the GeoDataFrame against the unary_union, rather than iterating point-by-point:

```python
# Calculate distance from each earthquake to the Pacific plate boundary union
pacific_eq_projected['distance_m'] = pacific_eq_projected.geometry.distance(boundary_union)
pacific_eq_projected['distance_km'] = pacific_eq_projected['distance_m'] / 1000.0
```

### 7. Find the earthquake with the maximum distance

```python
max_idx = pacific_eq_projected['distance_km'].idxmax()
result_row = pacific_eq_projected.loc[max_idx]

# Also get original (unprojected) data for lat/lon
orig_row = pacific_earthquakes.loc[max_idx]
```

### 8. Format and output the result

```python
# Convert time to ISO 8601 format
time_val = pd.Timestamp(result_row['time'], unit='ms').strftime('%Y-%m-%dT%H:%M:%SZ') if isinstance(result_row['time'], (int, float)) else str(result_row['time'])

# If time is already in ms epoch, convert:
# time_val = pd.to_datetime(result_row['time'], unit='ms').strftime('%Y-%m-%dT%H:%M:%SZ')

answer = {
    "id": str(result_row['id']),
    "place": str(result_row['place']),
    "time": time_val,
    "magnitude": float(result_row['mag']),
    "latitude": float(orig_row.geometry.y),
    "longitude": float(orig_row.geometry.x),
    "distance_km": round(float(result_row['distance_km']), 2)
}

with open('/root/answer.json', 'w') as f:
    json.dump(answer, f, indent=2)
```

## Critical details

- **EPSG:4326 for containment**: The `within` check MUST be done in EPSG:4326 to avoid Pacific plate polygon distortion at the antimeridian
- **EPSG:4087 for distances**: Use World Equidistant Cylindrical, not custom aeqd
- **Boundary filtering**: Use `boundaries['Name'].str.contains('PA')` to get Pacific plate boundaries
- **Unary union**: Use `.unary_union` on projected boundaries before computing distances
- **Distance method**: Use GeoDataFrame `.distance()` directly, not point-by-point iteration
- **Rounding**: `round(value, 2)` for distance_km
- **Time field handling**: The earthquake time may be in epoch milliseconds — convert with `pd.to_datetime(val, unit='ms')`
- **Magnitude field**: The field name in earthquake GeoJSON is typically `mag`, not `magnitude`
- **make_valid**: Apply `make_valid` to the Pacific plate geometry before the containment check