---
name: geospatial-earthquake-analysis
description: Analyze earthquakes relative to tectonic plate boundaries using GeoPandas. Load earthquake and plate boundary data, identify earthquakes within specific plates, calculate distances to boundaries, and analyze spatial relationships. Use this skill when working with plate tectonics, earthquake location analysis, distance calculations to plate boundaries, or coordinate projection systems in geopandas.
---

# Geospatial Earthquake and Plate Boundary Analysis

## Overview

This skill provides a complete workflow for analyzing earthquake locations relative to tectonic plate boundaries using GeoPandas. It handles data loading, coordinate projection management, and spatial distance calculations.

## Key Concepts

### Coordinate Projections
- Earthquake data typically comes in WGS84 (EPSG:4326) - latitude/longitude
- Distance calculations require a projected coordinate system (meters/kilometers)
- Use appropriate azimuthal equidistant or equal-area projections for accurate distance measurements
- Project data before calculating distances; transform results back if needed

### Plate Boundary Data Structure
- Boundaries are typically represented as LineStrings (boundary lines)
- Plates are regions bounded by these lines
- A point is "within a plate" if it's inside the polygon formed by the plate's boundaries
- "Distance to boundary" = minimum distance from a point to any boundary line of that plate

## Workflow

### 1. Loading Earthquake Data

```python
import geopandas as gpd
import json
from shapely.geometry import Point

# Load earthquake JSON
with open('/root/earthquakes_2024.json', 'r') as f:
    earthquakes = json.load(f)

# Convert to GeoDataFrame
features = []
for eq in earthquakes['features']:
    props = eq['properties']
    geom = Point(eq['geometry']['coordinates'])
    features.append({'geometry': geom, 'id': props.get('id'), 'magnitude': props.get('mag'), ...})

earthquakes_gdf = gpd.GeoDataFrame(features, crs='EPSG:4326')
```

### 2. Loading Plate Boundary Data

```python
# Load boundaries as LineStrings
boundaries_gdf = gpd.read_file('/root/PB2002_boundaries.json')  # Has CRS info
boundaries_gdf = boundaries_gdf.to_crs('EPSG:4326')  # Ensure consistent CRS

# Load plate definitions
plates_gdf = gpd.read_file('/root/PB2002_plates.json')
plates_gdf = plates_gdf.to_crs('EPSG:4326')
```

### 3. Identifying Earthquakes Within a Specific Plate

```python
# Method: Use spatial join to find earthquakes within plate polygons
earthquakes_in_plate = gpd.sjoin(
    earthquakes_gdf,
    plates_gdf[plates_gdf['plate_name'] == 'Pacific'],
    how='inner',
    predicate='within'
)
```

### 4. Calculating Distance to Plate Boundaries

For each earthquake within the Pacific plate, calculate its minimum distance to the Pacific plate boundary:

```python
# Project to a suitable projection for distance (meters)
# Azimuthal equidistant projection centered near the Pacific
pacific_proj = 'EPSG:3832'  # Or use a custom projection

earthquakes_projected = earthquakes_gdf.to_crs(pacific_proj)
boundaries_projected = boundaries_gdf.to_crs(pacific_proj)

# Calculate distance from each earthquake point to the nearest boundary
def distance_to_boundary(point, boundary_lines):
    min_dist = float('inf')
    for line in boundary_lines.geometry:
        dist = point.distance(line)
        min_dist = min(min_dist, dist)
    return min_dist / 1000  # Convert to km

distances = []
for idx, eq in earthquakes_in_plate.iterrows():
    dist = distance_to_boundary(eq.geometry, boundaries_projected)
    distances.append(dist)

earthquakes_in_plate['distance_to_boundary_km'] = distances
```

### 5. Finding the Furthest Earthquake

```python
furthest = earthquakes_in_plate.loc[earthquakes_in_plate['distance_to_boundary_km'].idxmax()]
print(f"Furthest from boundary: {furthest['place']}, {furthest['distance_to_boundary_km']:.2f} km")
```

## Important Notes

- **CRS Consistency**: Always ensure all layers use the same CRS before spatial operations
- **Projection Selection**: Use projections appropriate for your region (azimuthal equidistant minimizes distortion)
- **Boundary Definition**: The Pacific plate boundary includes all associated trenches and ridges
- **Distance Metric**: Minimum distance accounts for complex geometry; straight-line distance is not appropriate
- **Performance**: For large datasets, use spatial indexing and consider chunking operations

## Output Format

Return earthquake details with distance information:
```python
result = {
    'id': earthquake_id,
    'place': earthquake_location,
    'time': earthquake_time_iso8601,
    'magnitude': earthquake_mag,
    'latitude': eq_lat,
    'longitude': eq_lon,
    'distance_km': distance_rounded_2dp
}
```
