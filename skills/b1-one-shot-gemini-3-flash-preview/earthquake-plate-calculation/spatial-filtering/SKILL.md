---
name: spatial-filtering
description: Methods for filtering GeoDataFrames based on spatial relationships like containment and intersection.
---

# Spatial Filtering

## Overview
Spatial filtering allows you to select features based on their location relative to other features.

## Point-in-Polygon
To find points that lie inside a specific polygon:

```python
# Assuming gdf_points and gdf_polygons are GeoDataFrames
# 1. Get a specific polygon geometry
pacific_poly = gdf_polygons[gdf_polygons['Code'] == 'PA'].geometry.unary_union

# 2. Filter points
points_in_pacific = gdf_points[gdf_points.within(pacific_poly)]
```

## Spatial Joins
Alternatively, use `sjoin` for batch processing:

```python
joined = gpd.sjoin(gdf_points, gdf_polygons, predicate='within')
```

## Attribute-based Spatial Selection
Often you need to combine attribute filters with spatial operations:

```python
# Find boundaries associated with the Pacific plate (PA)
pacific_boundaries = gdf_boundaries[
    (gdf_boundaries['PlateA'] == 'PA') | (gdf_boundaries['PlateB'] == 'PA')
]
```
