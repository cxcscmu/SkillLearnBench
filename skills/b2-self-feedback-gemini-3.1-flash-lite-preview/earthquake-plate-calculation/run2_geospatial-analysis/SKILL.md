---
name: run2_geospatial-analysis
description: Geospatial data analysis with geopandas for distance calculations, filtering, and modern API usage.
---
# Geospatial Analysis with GeoPandas (Improved)

## Key Concepts
- **Coordinate Systems**: EPSG:4326 for storage, EPSG:4087 (metric) for distance.
- **Modern API**: As of GeoPandas 1.0+, use `unary_union` (or `union_all()` for newer versions) to combine geometries.
- **Data Conversion**: When using raw GeoJSON, extract `properties` and `geometry.coordinates` manually before GeoDataFrame creation.

## Updated Pattern
```python
import geopandas as gpd
from shapely.geometry import Point

# 1. Load data
# 2. Extract components if necessary
# 3. Project to metric CRS
METRIC_CRS = "EPSG:4087"
points_proj = gdf.to_crs(METRIC_CRS)
# 4. Combine geometries using .union_all()
boundary_geom = boundary_gdf.to_crs(METRIC_CRS).geometry.union_all()
# 5. Calculate distance
gdf["dist"] = points_proj.geometry.distance(boundary_geom)
```
