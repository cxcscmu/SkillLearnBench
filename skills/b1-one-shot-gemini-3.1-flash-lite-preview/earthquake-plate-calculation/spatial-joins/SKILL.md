---
name: spatial-joins
description: Provides techniques for performing spatial operations like joins, contains, and distance calculations to identify relations between geographic features.
---

# Spatial Operations with GeoPandas

## Point-in-Polygon
Use `geopandas.sjoin()` to identify points contained within specific polygons (e.g., plates).
```python
# Join points and polygons
joined = gpd.sjoin(points_gdf, polygons_gdf, how='inner', predicate='within')
```

## Distance Calculation
To find the distance from points to boundaries, reproject to an appropriate CRS (meters) and calculate the distance to the nearest boundary.
```python
# Find distance from each point to the nearest polygon boundary
distances = points_gdf.distance(boundaries_gdf.unary_union)
```
