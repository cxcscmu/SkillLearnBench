---
name: geopandas-distance-analysis
description: Calculate distances between geospatial points and boundaries using GeoPandas with proper metric projections (EPSG:4087).
---

# GeoPandas Distance Analysis

## Setup
```bash
pip install geopandas shapely
```

## Core Workflow

### 1. Load GeoJSON files
```python
import geopandas as gpd
from shapely.geometry import Point

gdf_plates = gpd.read_file("PB2002_plates.json")
gdf_boundaries = gpd.read_file("PB2002_boundaries.json")
```

### 2. Create GeoDataFrame from coordinate list
```python
geometry = [Point(lon, lat) for lon, lat in zip(lons, lats)]
gdf_points = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")
```

### 3. Spatial filtering (points within polygon)
```python
target_poly = gdf_plates[gdf_plates["Code"] == "PA"].geometry.unary_union
inside = gdf_points[gdf_points.within(target_poly)].copy()
```

### 4. Project to metric CRS before distance calculation
```python
METRIC_CRS = "EPSG:4087"  # World Equidistant Cylindrical (meters)
inside_proj = inside.to_crs(METRIC_CRS)
boundary_proj = gdf_boundaries.to_crs(METRIC_CRS).geometry.unary_union
inside["distance_km"] = inside_proj.geometry.distance(boundary_proj) / 1000.0
```

### 5. Find furthest point
```python
result = inside.nlargest(1, "distance_km").iloc[0]
print(f"ID: {result['id']}, Distance: {result['distance_km']:.2f} km")
```

## Key Rules
- **NEVER** calculate distances in EPSG:4326 (degrees != meters)
- Always project to EPSG:4087 or EPSG:3857 before `.distance()`
- Use `.unary_union` to combine multiple boundary segments into one geometry
- Use `.within()` for point-in-polygon tests (handles antimeridian better than manual checks)
- Filter boundaries by PlateA/PlateB before combining: `gdf_boundaries[(gdf_boundaries["PlateA"]=="PA") | (gdf_boundaries["PlateB"]=="PA")]`
