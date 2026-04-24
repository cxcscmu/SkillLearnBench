---
name: geopandas-projections
description: Using GeoPandas coordinate projections for accurate distance calculations on geospatial data.
---

# GeoPandas Projections for Distance Calculations

## Overview
When calculating distances between geographic features, you must project from geographic coordinates (lat/lon, EPSG:4326) to a projected CRS that preserves distances. Using `.distance()` on unprojected data gives degrees, not meters/km.

## Key Projections

### World Azimuthal Equidistant (ESRI:54032)
- Preserves distances from center point
- Good for measuring distances from a single point to boundaries
- Usage: `gdf.to_crs("ESRI:54032")`

### Equal Area Cylindrical (EPSG:6933)
- Preserves area, approximate distances
- Usage: `gdf.to_crs("EPSG:6933")`

### Custom Azimuthal Equidistant
- Best accuracy when measuring from a known center point
- `proj_str = f"+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m"`

## Distance Calculation Pattern

```python
import geopandas as gpd
from shapely.ops import nearest_points

# Load data in WGS84
gdf = gpd.read_file("data.geojson")  # EPSG:4326

# Project to meters-based CRS
gdf_proj = gdf.to_crs("ESRI:54032")

# Calculate distance (returns meters)
dist = gdf_proj.geometry.distance(some_geometry_proj)

# Convert to km
dist_km = dist / 1000
```

## Handling the Antimeridian (Date Line)
The Pacific plate crosses the antimeridian (±180° longitude). Standard projections may split geometries. Solutions:
1. Use a Pacific-centered projection with `+lon_0=180` or `+lon_0=-160`
2. Shift longitudes to 0-360 range before projecting
3. Use azimuthal equidistant centered on Pacific

## Point-to-LineString Distance
```python
from shapely.ops import nearest_points

# For a point to a boundary (MultiLineString)
point_proj = earthquake_point.to_crs(proj_crs)
boundary_proj = boundary.to_crs(proj_crs)
distance = point_proj.geometry.distance(boundary_proj.unary_union)
```
