---
name: run2_advanced_projections
description: Selecting optimal projections for distance calculations in the Pacific.
---

# Optimal Projections for Pacific Distance Analysis

Calculating distances across the entire Pacific plate requires a projection that minimizes distortion.

## Recommended Projections

### 1. World Equidistant Cylindrical (EPSG:4087)
- **Pros**: Distances along meridians are accurate.
- **Cons**: Distances along parallels are distorted as you move away from the equator.

### 2. Custom Azimuthal Equidistant (AEQD)
- **Pros**: Distances from the *center point* to any other point are perfectly accurate.
- **Usage**: Center it on the approximate centroid of the Pacific plate.
```python
# Centered on Hawaii (approx center of Pacific plate)
aeqd_crs = "+proj=aeqd +lat_0=20 +lon_0=-155 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
gdf_projected = gdf.to_crs(aeqd_crs)
```

### 3. Geodesic Distance (Haverine/Vincenty)
For the highest accuracy without projections, use geodesic distance calculations directly on the sphere/ellipsoid.
```python
# Use geopy or scipy for geodesic distance
# Or use the 'geodesic' methods in some libraries.
```
However, calculating distance from a point to a complex *line* geodesically is computationally intensive. Projecting to a local AEQD or a centered Equidistant Cylindrical is usually sufficient for "GeoPandas projections" requirement.
