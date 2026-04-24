---
name: plate-tectonics-geospatial
description: Analyze plate tectonics data using GeoPandas, identify points within plates, and calculate distances to boundaries.
---

# Plate Tectonics Geospatial Analysis

## Overview
The PB2002 (Plate Boundaries 2002) dataset provides comprehensive data on tectonic plate boundaries and plate definitions. This skill covers loading, processing, and spatial analysis of plate data.

## PB2002 Dataset Structure

### Boundary Data (PB2002_boundaries.json)
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [[lon1, lat1], [lon2, lat2], ...]
      },
      "properties": {
        "PLATE1": "Pacific",
        "PLATE2": "North American",
        "TYPE": "subduction zone",  // or "transform", "spreading", etc.
        "STEPOVER": ""
      }
    }
  ]
}
```

### Plate Data (PB2002_plates.json)
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "MultiPolygon",  // or Polygon
        "coordinates": [...]
      },
      "properties": {
        "PlateName": "Pacific",
        "PlateID": 101
      }
    }
  ]
}
```

## Loading and Processing

### Load Plate Boundaries
```python
import geopandas as gpd
import json

with open('/root/PB2002_boundaries.json', 'r') as f:
    boundaries_geojson = json.load(f)

boundaries_gdf = gpd.GeoDataFrame.from_features(
    boundaries_geojson['features'],
    crs='EPSG:4326'
)

# Filter for specific plate boundary
pacific_boundaries = boundaries_gdf[
    (boundaries_gdf['PLATE1'] == 'Pacific') |
    (boundaries_gdf['PLATE2'] == 'Pacific')
]
```

### Load Plate Polygons
```python
with open('/root/PB2002_plates.json', 'r') as f:
    plates_geojson = json.load(f)

plates_gdf = gpd.GeoDataFrame.from_features(
    plates_geojson['features'],
    crs='EPSG:4326'
)

# Get Pacific plate polygon
pacific_plate = plates_gdf[plates_gdf['PlateName'] == 'Pacific']
```

## Spatial Operations

### Identify Points Within Plate
```python
# Use spatial join to find earthquakes within Pacific plate
earthquakes_in_pacific = gpd.sjoin(
    earthquakes_gdf,
    pacific_plate,
    how='inner',
    predicate='within'
)
```

### Calculate Distance to Boundary
```python
# For each earthquake, calculate minimum distance to boundary
def min_distance_to_boundary(point, boundary_lines_gdf):
    """Calculate minimum distance from point to any boundary line"""
    min_dist = float('inf')
    for idx, boundary in boundary_lines_gdf.iterrows():
        dist = point.distance(boundary['geometry'])
        if dist < min_dist:
            min_dist = dist
    return min_dist

# Apply to all earthquakes in the plate
# First, project to projected CRS for accurate distance in km
earthquakes_projected = earthquakes_in_pacific.to_crs('EPSG:3857')
boundaries_projected = pacific_boundaries.to_crs('EPSG:3857')

earthquakes_projected['distance_to_boundary'] = earthquakes_projected.geometry.apply(
    lambda point: min_distance_to_boundary(point, boundaries_projected)
)

# Convert from meters to kilometers
earthquakes_projected['distance_km'] = earthquakes_projected['distance_to_boundary'] / 1000
```

### Find Maximum Distance
```python
# Find earthquake furthest from boundary
furthest_idx = earthquakes_projected['distance_km'].idxmax()
furthest_earthquake = earthquakes_projected.loc[furthest_idx]
```

## Important Considerations

### Polygon Validation
```python
# Ensure polygons are valid before spatial operations
if not plates_gdf.geometry.is_valid.all():
    plates_gdf['geometry'] = plates_gdf.geometry.buffer(0)

if not boundaries_gdf.geometry.is_valid.all():
    boundaries_gdf['geometry'] = boundaries_gdf.geometry.buffer(0)
```

### Handling MultiPolygons
```python
# If a plate is represented as MultiPolygon, create a union
pacific_plate_union = pacific_plate.unary_union
```

### Projection for Accurate Distances
```python
# Use Web Mercator (EPSG:3857) for global distances in meters
# Then convert to kilometers

# For regional analysis, consider UTM zones
# EPSG:32633 = UTM Zone 33N
# EPSG:32733 = UTM Zone 33S
```

## Common Pitfalls
1. **Not projecting before distance calculations** - Distances in geographic CRS are meaningless
2. **Invalid geometries** - Use `.buffer(0)` to fix self-intersecting polygons
3. **Antimeridian issues** - Points near ±180° longitude may have wrapping issues
4. **MultiPolygon confusion** - Remember that a plate may consist of multiple disconnected polygons
