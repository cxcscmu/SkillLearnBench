---
name: optimal-projection-selection
description: Select appropriate projected CRS based on geographic region for accurate distance calculations.
---

# Optimal Projection Selection for Regional Analysis

## Installation
```bash
pip install geopandas pyproj shapely
```

## Overview
Distance calculations in projected coordinate systems must account for distortion patterns. Different regions require different projections to minimize error.

## Projection Selection Guide

### Global Analysis
- **EPSG:3857 (Web Mercator)**: Distorts toward poles, OK for equatorial regions
- **EPSG:3395 (World Mercator)**: Similar properties, different formulation
- **EPSG:54008 (Sinusoidal)**: Equal-area, preserves area but distorts shape

### Pacific Ocean Region
- **EPSG:3832 (Web Mercator Auxiliary Sphere)**: Web standard but with distortion
- **EPSG:3857**: Web Mercator (distortion increases away from equator)
- **Custom approach**: Split analysis by region (North/South Pacific separately)

### Better Approach: Use Azimuthal Equidistant
```python
# Azimuthal Equidistant centered on Pacific
# Creates accurate distances from a central point
# For Pacific plate, could use various centers

# Create center point (e.g., Pacific plate centroid)
center_geom = pacific_polygon.centroid
print(f"Pacific plate center: {center_geom}")
```

## Validation: Compare Distance Methods

```python
import geopandas as gpd
from shapely.geometry import Point
import math

# Method 1: Projected CRS (EPSG:3857)
gdf_3857 = gdf.to_crs('EPSG:3857')
dist_3857 = gdf_3857.geometry.distance(boundary_3857).max()

# Method 2: Projected CRS (equal-area)
gdf_equal = gdf.to_crs('EPSG:54008')  # Sinusoidal
dist_equal = gdf_equal.geometry.distance(boundary_equal).max()

# Verify consistency
print(f"Distance (Web Mercator): {dist_3857 / 1000:.2f} km")
print(f"Distance (Equal-area): {dist_equal / 1000:.2f} km")

# If results differ significantly, investigate
if abs(dist_3857 - dist_equal) / max(dist_3857, dist_equal) > 0.1:
    print("WARNING: Significant difference between projections")
```

## Important Considerations

1. **Distortion Pattern**: Each projection has strengths and weaknesses
2. **Distance Consistency**: For Pacific-wide analysis, use projection that minimizes global distortion
3. **Multiple Validation**: Cross-check with different projections for critical results
4. **Units**: Ensure understanding of output units (usually meters for standard projections)
5. **Boundary Geometry**: Ensure boundary is also in same projection before calculating distance

## Recommended Approach for Pacific
```python
# Use World Mercator (EPSG:3857) as primary
# For verification, also check with Mollweide (EPSG:54009)
earthquakes_proj = earthquakes.to_crs('EPSG:3857')
boundaries_proj = boundaries.to_crs('EPSG:3857')

# Convert distance in meters to kilometers
distance_km = earthquakes_proj.geometry.distance(boundaries_proj).max() / 1000
```
