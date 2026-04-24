---
name: spatial-distance-to-boundary
description: Calculate the shortest distance between points (earthquakes) and a complex line geometry (plate boundaries).
---

To find the distance from points to a boundary:
1. Isolate the boundary geometry. This can be the boundary of a plate polygon (`plate_gdf.geometry.boundary`) or a separate LineString dataset.
2. If the boundary consists of multiple segments, use `.union_all()` (in GeoPandas 1.0+) or `.unary_union` to create a single geometry object for comparison.
3. Use the `.distance()` method on the points GeoDataFrame against the unified boundary geometry.
4. To find the point furthest from the boundary, use `.loc[gdf['distance_col'].idxmax()]`.

```python
# Create a single geometry representing the boundary
boundary_geom = boundaries_gdf.union_all()

# Calculate distance for each row
gdf['dist_to_boundary'] = gdf.geometry.distance(boundary_geom)

# Find the record with the maximum distance
furthest_record = gdf.loc[gdf['dist_to_boundary'].idxmax()]
```