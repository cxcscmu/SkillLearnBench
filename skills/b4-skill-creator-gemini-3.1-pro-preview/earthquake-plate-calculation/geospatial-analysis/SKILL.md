---
name: geospatial-analysis
description: "How to perform geospatial analysis using GeoPandas. Use this skill whenever the user mentions maps, coordinates, geospatial distance, plate boundaries, earthquakes, or spatial data, even if they don't explicitly ask for it."
---

# Geospatial Analysis with GeoPandas

## Overview

When working with geographic data (earthquakes, plate boundaries, etc.), using `geopandas` with proper coordinate projections provides accurate distance calculations and efficient spatial operations. This guide covers best practices for geospatial analysis.

## Key Concepts

### Geographic vs Projected Coordinate Systems

| Coordinate System | Type | Units | Use Case |
|-------------------|------|-------|----------|
| EPSG:4326 (WGS84) | Geographic | Degrees (lat/lon) | Data storage, display |
| EPSG:4087 (World Equidistant Cylindrical) | Projected | Meters | Distance calculations |

**Critical Rule**: Never calculate distances directly in geographic coordinates (EPSG:4326). Always project to a metric coordinate system first.

### Why Projection Matters

```python
# ❌ INCORRECT: Calculating distance in EPSG:4326
# This treats degrees as if they were equal distances everywhere on Earth
gdf = gpd.GeoDataFrame(..., crs="EPSG:4326")
distance = point1.distance(point2)  # Wrong! Returns degrees, not meters

# ✅ CORRECT: Project to metric CRS first
gdf_projected = gdf.to_crs("EPSG:4087")
distance_meters = point1_proj.distance(point2_proj)  # Correct! Returns meters
distance_km = distance_meters / 1000.0
```

## Loading Geospatial Data

### From GeoJSON Files

```python
import geopandas as gpd

# Load GeoJSON files directly
gdf_plates = gpd.read_file("plates.json")
gdf_boundaries = gpd.read_file("boundaries.json")
```

### From Regular Data with Coordinates

```python
from shapely.geometry import Point
import geopandas as gpd

# Convert coordinate data to GeoDataFrame
data = [
    {"id": 1, "lat": 35.0, "lon": 140.0, "value": 5.5},
    {"id": 2, "lat": 36.0, "lon": 141.0, "value": 6.0},
]

geometry = [Point(row["lon"], row["lat"]) for row in data]
gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")
```

## Spatial Filtering

### Finding Points Within a Polygon

```python
# Get the polygon of interest
target_poly = gdf_plates[gdf_plates["Name"] == "Pacific"].geometry.unary_union

# Filter points that fall within the polygon
points_inside = gdf_points[gdf_points.within(target_poly)]

print(f"Found {len(points_inside)} points inside the polygon")
```

## Distance Calculations

### Point to Line/Boundary Distance

```python
# 1. Load your data
gdf_points = gpd.read_file("points.json")
gdf_boundaries = gpd.read_file("boundaries.json")

# 2. Project to metric coordinate system
METRIC_CRS = "EPSG:4087"
points_proj = gdf_points.to_crs(METRIC_CRS)
boundaries_proj = gdf_boundaries.to_crs(METRIC_CRS)

# 3. Combine boundary segments if needed
boundary_geom = boundaries_proj.geometry.unary_union

# 4. Calculate distances (returns meters)
gdf_points["distance_m"] = points_proj.geometry.distance(boundary_geom)
gdf_points["distance_km"] = gdf_points["distance_m"] / 1000.0
```

### Finding Furthest Point

```python
# Sort by distance and get the furthest point
furthest = gdf_points.nlargest(1, "distance_km").iloc[0]

print(f"Furthest point: {furthest['id']}")
print(f"Distance: {furthest['distance_km']:.2f} km")
```
