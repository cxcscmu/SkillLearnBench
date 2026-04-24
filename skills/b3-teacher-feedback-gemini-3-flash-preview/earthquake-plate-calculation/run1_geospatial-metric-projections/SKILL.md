---
name: geospatial-metric-projections
description: Transform GeoPandas objects to metric projections (like World Equidistant Cylindrical) to calculate distances in meters or kilometers rather than degrees.
---

Calculations in geographic coordinates (EPSG:4326) return results in degrees, which are not suitable for distance measurements. To calculate distances in kilometers:
1. Project the GeoDataFrame to a metric CRS. For global datasets, the **World Equidistant Cylindrical** (ESRI:54002) or **World Azimuthal Equidistant** (ESRI:54032) projections are often used.
2. After projection, the `.distance()` method will return values in meters (usually the base unit for these projections).
3. Convert meters to kilometers by dividing by 1000.

```python
# Project to World Equidistant Cylindrical
metric_crs = "ESRI:54002"
points_metric = points.to_crs(metric_crs)
boundary_metric = boundary_gdf.to_crs(metric_crs)

# Distance calculation (returns meters)
distances = points_metric.distance(boundary_metric.union_all())
points['distance_km'] = distances / 1000
```