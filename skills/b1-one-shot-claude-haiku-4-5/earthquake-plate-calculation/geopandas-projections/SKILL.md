---
name: geopandas-projections
description: Use GeoPandas with coordinate projections to perform accurate spatial calculations and transformations.
---

# GeoPandas Spatial Projections

## Overview
GeoPandas is built on top of Shapely and Fiona, enabling geographic data manipulation with proper coordinate reference systems (CRS). Using correct projections is critical for accurate distance calculations and spatial operations.

## Installation
```bash
pip install geopandas shapely fiona pyproj
```

## Key Concepts

### Coordinate Reference Systems (CRS)
- **EPSG:4326**: WGS84 (lat/lon), commonly used for geographic data but NOT suitable for distance calculations
- **EPSG:3857**: Web Mercator, used for web mapping
- **Regional Projected CRS**: For accurate local distance calculations (e.g., UTM zones)

### Distance Calculations
Always project to a projected CRS before calculating distances. Geographic CRS (like EPSG:4326) measure in degrees, not kilometers.

## Code Examples

### Creating GeoDataFrames from Points
```python
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

# From earthquake data
earthquakes_df = pd.read_json('/root/earthquakes_2024.json')
geometry = [Point(xy) for xy in zip(earthquakes_df['longitude'], earthquakes_df['latitude'])]
gdf = gpd.GeoDataFrame(earthquakes_df, geometry=geometry, crs='EPSG:4326')
```

### Loading GeoJSON with Boundaries
```python
import json

# Load GeoJSON and convert to GeoDataFrame
with open('/root/PB2002_boundaries.json', 'r') as f:
    geojson_data = json.load(f)
boundaries_gdf = gpd.GeoDataFrame.from_features(geojson_data['features'], crs='EPSG:4326')
```

### Projecting to Projected CRS
```python
# Project to a suitable CRS for distance calculations
# Example: project to Mercator for global analysis
gdf_projected = gdf.to_crs('EPSG:3857')
boundaries_projected = boundaries_gdf.to_crs('EPSG:3857')

# Or use a specific UTM zone for a region
# EPSG:32633 is UTM zone 33N
```

### Spatial Filtering (Point in Polygon)
```python
# Check if points fall within polygons
earthquakes_in_plate = gpd.sjoin(gdf, plate_polygons, how='inner', predicate='within')
```

### Distance to Nearest Geometry
```python
# Calculate distance from each point to nearest boundary
def min_distance_to_boundary(row, boundary_geom):
    return row['geometry'].distance(boundary_geom)

# Distance in projected CRS (meters) or geographic CRS (degrees)
gdf['distance'] = gdf.geometry.distance(boundary_geometry)
```

## Common Pitfalls
1. **Calculating distances in geographic CRS** - Use projected CRS for kilometers
2. **Mixing CRS** - Always ensure geometries have the same CRS before operations
3. **Not checking polygon orientation** - Invalid/reversed rings can cause issues

## Best Practices
1. Always set CRS explicitly when creating GeoDataFrames
2. Project to appropriate CRS before distance calculations
3. Use `gdf.to_crs()` to transform, not `gdf.crs = new_crs`
4. Validate geometries: `gdf.is_valid.all()`
