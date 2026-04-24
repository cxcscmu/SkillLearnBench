---
name: geopandas-point-in-polygon
description: How to determine which points fall inside a specific polygon using GeoPandas.
---

# Point in Polygon with GeoPandas

This skill demonstrates how to filter a set of points (like earthquakes or cities) to find only those that fall within a specific polygon (like a country or tectonic plate) using GeoPandas.

## Prerequisites

```bash
pip install geopandas shapely
```

## Basic Usage

When you have a set of points and a polygon, you can use the `.within()` spatial predicate to filter the points.

```python
import geopandas as gpd
from shapely.geometry import Point

# 1. Load the polygon data
polygons_gdf = gpd.read_file('polygons.geojson')

# 2. Extract the specific polygon you want to test against
# Example: Get the polygon for a specific region
target_polygon = polygons_gdf[polygons_gdf['name'] == 'Target Region'].geometry.unary_union

# 3. Create or load your points data
points_data = [
    {'id': 1, 'lat': 34.0, 'lon': -118.2},
    {'id': 2, 'lat': 40.7, 'lon': -74.0}
]
# Convert to GeoDataFrame
geometry = [Point(xy['lon'], xy['lat']) for xy in points_data]
points_gdf = gpd.GeoDataFrame(points_data, geometry=geometry, crs="EPSG:4326")

# 4. Perform the spatial filter
# This creates a boolean mask of points that are within the target polygon
points_inside = points_gdf[points_gdf.geometry.within(target_polygon)]

print(f"Found {len(points_inside)} points inside the polygon.")
```

## Tips

- Always ensure both the points and the polygon share the same Coordinate Reference System (CRS) before doing spatial operations.
- Using `.unary_union` on the filtered polygon GeoDataFrame is useful if the target region consists of multiple polygon geometries (like a multipolygon).
