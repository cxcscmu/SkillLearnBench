---
name: geopandas-distance-calculation
description: How to calculate distance between points and other geometries (like lines or polygons) in metric units using GeoPandas.
---

# Distance Calculation with GeoPandas

This skill demonstrates how to calculate the distance between geographic features (like points and lines) accurately. The crucial step is projecting geographic coordinates (degrees) into a projected coordinate system (meters).

## Prerequisites

```bash
pip install geopandas shapely
```

## Basic Usage

When calculating distances on the Earth's surface, you **must not** calculate distance directly in `EPSG:4326` (which uses degrees). Instead, you project the data into a metric coordinate system like `EPSG:4087` (World Equidistant Cylindrical) or `EPSG:3857` (Web Mercator, though it distorts distance). `EPSG:4087` or `EPSG:6933` (Cylindrical Equal Area) are common for global calculations, or a local UTM zone. `EPSG:4087` provides distances in meters.

```python
import geopandas as gpd
from shapely.geometry import Point

# 1. Load data
points_gdf = gpd.read_file('points.geojson')
lines_gdf = gpd.read_file('lines.geojson')

# 2. Define a metric CRS (e.g., EPSG:4087 for World Equidistant Cylindrical)
METRIC_CRS = "EPSG:4087"

# 3. Project both datasets to the metric CRS
points_proj = points_gdf.to_crs(METRIC_CRS)
lines_proj = lines_gdf.to_crs(METRIC_CRS)

# 4. Optional: If you want distance to any part of the lines network, combine them
network_geometry = lines_proj.geometry.unary_union

# 5. Calculate distance (the result will be in meters because of the CRS)
points_gdf['distance_m'] = points_proj.geometry.distance(network_geometry)

# 6. Convert to kilometers
points_gdf['distance_km'] = points_gdf['distance_m'] / 1000.0

# 7. Find the point furthest away
furthest_point = points_gdf.nlargest(1, 'distance_km').iloc[0]

print(f"Furthest point distance: {furthest_point['distance_km']:.2f} km")
```

## Tips
- Always verify your metric CRS when doing distance calculations. `EPSG:4326` will return distances in degrees.
- Combining features with `.unary_union` before calling `.distance()` is significantly faster than calculating distances to each feature individually.
