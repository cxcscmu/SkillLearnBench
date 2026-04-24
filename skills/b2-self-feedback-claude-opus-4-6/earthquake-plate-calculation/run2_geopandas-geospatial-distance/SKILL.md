---
name: run2_geopandas-geospatial-distance
description: Accurate geospatial distance calculations using GeoPandas with appropriate map projections for global-scale analysis.
---

# GeoPandas Distance Calculations with Projections

## Key Principle
Always project to a meter-based CRS before computing distances. EPSG:4326 distances are in degrees, not meters.

## Choosing a Projection
- **Azimuthal Equidistant (`+proj=aeqd`)**: Preserves distances from the center point. Best when measuring distance from a specific region.
- **Center the projection** on the area of interest to minimize distortion.
- For the Pacific plate (spans antimeridian): use `+proj=aeqd +lat_0=0 +lon_0=-160` to center in the Pacific Ocean.

## Workflow
```python
import geopandas as gpd
from shapely.ops import unary_union

# 1. Load data in EPSG:4326
gdf = gpd.read_file("data.geojson").set_crs("EPSG:4326", allow_override=True)

# 2. Define target CRS (azimuthal equidistant centered on Pacific)
target_crs = "+proj=aeqd +lat_0=0 +lon_0=-160 +x_0=0 +y_0=0 +datum=WGS84 +units=m"

# 3. Project
gdf_proj = gdf.to_crs(target_crs)

# 4. Compute distances (returns meters)
boundary_geom = unary_union(boundary_gdf_proj.geometry)
distances_m = gdf_proj.geometry.distance(boundary_geom)
distances_km = distances_m / 1000.0
```

## Caveats
- Azimuthal equidistant distorts areas/shapes far from center, but distances from center are accurate.
- For point-to-line distance, `.distance()` gives Euclidean distance in the projected CRS.
- The Pacific plate crosses the antimeridian (180/-180). The PB2002 plate polygon handles this natively in GeoJSON, but projections must be centered appropriately.
