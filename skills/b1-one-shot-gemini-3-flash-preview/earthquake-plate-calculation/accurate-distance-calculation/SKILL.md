---
name: accurate-distance-calculation
description: Using map projections to calculate real-world distances in meters or kilometers accurately.
---

# Accurate Distance Calculation

## Overview
Calculating distances in degrees (EPSG:4326) is incorrect because degrees represent different distances depending on the latitude. Always project to a metric system.

## Choosing a Projection
- **EPSG:4087**: World Equidistant Cylindrical (Good for global distance approximation).
- **UTM**: Universal Transverse Mercator (Best for local, high-accuracy areas).

## Conversion and Calculation
```python
# Project to metric (meters)
METRIC_CRS = "EPSG:4087"
gdf_projected = gdf.to_crs(METRIC_CRS)
target_geom_projected = target_gdf.to_crs(METRIC_CRS).geometry.unary_union

# Calculate distance (returns meters)
gdf['distance_meters'] = gdf_projected.distance(target_geom_projected)

# Convert to Kilometers
gdf['distance_km'] = gdf['distance_meters'] / 1000.0
```

## Finding Extremes
```python
# Furthest point
furthest = gdf.nlargest(1, 'distance_km')

# Closest point
closest = gdf.nsmallest(1, 'distance_km')
```
