---
name: geopandas-projection-tools
description: >
  Handles CRS transformations and distance calculations in kilometers.
  Use this for converting between geographic coordinates (WGS84) and 
  equal-area projections (like Lambert Azimuthal Equal Area centered 
  on the Pacific region) for accurate distance measurements.
---

# Geopandas Projection Tools

## CRS Transformation
For accurate distance measurement in km, always transform to an appropriate
local projected coordinate system (e.g., EPSG:6933 for equal-area or 
custom projections centered on the region of interest).

## Distance Calculation
1. Set the GeoDataFrame CRS to EPSG:4326.
2. Reproject to a meters-based projection (e.g., EPSG:3857 for simplicity or
   a custom equal-area projection for scientific accuracy).
3. Use `.distance()` to calculate distances.
4. Convert result to km (divide by 1000).
