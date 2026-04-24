---
name: run2_antimeridian_handling
description: Techniques for handling geometries that cross the 180/-180 degree longitude line.
---

# Handling the Anti-meridian in Geospatial Analysis

When working with data spanning the Pacific, geometries often cross the anti-meridian. Standard projections centered at 0° longitude will "rip" these geometries.

## Techniques

### 1. Shift Coordinates to 0-360
You can shift the longitude of all geometries to be in the [0, 360) range.
```python
def shift_lon(geom):
    from shapely.affinity import translate
    # This is complex for polygons that cross the line. 
    # Better to use a specific CRS.
    pass
```

### 2. Use a Pacific-Centered CRS
The most robust way is to use a CRS centered on the Pacific (e.g., 150°E or 180°).
```python
# Custom Equidistant Cylindrical centered at 150E
pacific_crs = "+proj=eqc +lat_ts=0 +lat_0=0 +lon_0=150 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
gdf_pacific = gdf.to_crs(pacific_crs)
```
When reprojecting to a Pacific-centered CRS, GeoPandas/PyProj handles the wrap-around correctly for points. For polygons, they might need to be "unwrapped" first if they were originally defined in [-180, 180].

### 3. Using `dateline_fix` (if available)
Some libraries have tools to split or join geometries at the dateline.
