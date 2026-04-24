---
name: run2_geopandas_projections
description: Advanced guide on GeoPandas projections for accurate metric distance calculations without distortion using point-centric Azimuthal Equidistant CRS.
---

# Accurate Distances in GeoPandas via Custom Projections

Distance calculations in WGS84 CRS (EPSG:4326) yield meaningless degrees.
While standard projected CRSs (like UTM or Mercator) suffer from distortions away from their center or standard parallels, an **Azimuthal Equidistant** projection centered perfectly on a geometry of interest preserves the exact distance to all other geometries around it.

## The Point-Centric AEQD Strategy

To find the exact distance from a point to a boundary (such as the distance of an earthquake to a plate boundary), create a custom Azimuthal Equidistant CRS centered on the point itself.

```python
import geopandas as gpd
from shapely.geometry import Point

# Assume we have a GeoSeries or DataFrame of boundaries
boundaries_gdf = gpd.read_file('boundaries.geojson')

def get_exact_distance_km(point_geom, boundaries_gdf):
    lon, lat = point_geom.x, point_geom.y
    # Create a custom AEQD CRS centered on the point
    custom_crs = f"+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=km"
    
    # Project the boundaries to this custom CRS
    boundaries_proj = boundaries_gdf.to_crs(custom_crs)
    
    # The point itself is exactly at (0, 0) in its own AEQD projection
    center_point = Point(0, 0)
    
    # Minimum distance in kilometers
    min_dist_km = boundaries_proj.distance(center_point).min()
    return min_dist_km

# Example use:
# dist_km = get_exact_distance_km(earthquake.geometry, pa_boundaries)
```

This perfectly solves the distortion problems, even across the antimeridian (180°), because the Azimuthal Equidistant projection maps the entire globe correctly in relation to the center point.