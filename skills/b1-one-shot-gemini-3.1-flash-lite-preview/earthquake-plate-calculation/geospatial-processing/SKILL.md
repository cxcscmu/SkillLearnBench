---
name: geospatial-processing
description: Provides foundational techniques for loading, projecting, and manipulating geospatial datasets using GeoPandas.
---

# Geospatial Processing with GeoPandas

## Loading Data
Use `geopandas.read_file()` to load GeoJSON, Shapefiles, or other supported formats.
```python
import geopandas as gpd
gdf = gpd.read_file('data.json')
```

## Projections
Crucial for accurate distance calculations. Use `.to_crs()` to reproject into an equal-area projection or a projection suitable for the region of interest.
```python
# Projecting to EPSG:6933 (Cylindrical Equal Area) for global distance measurements
gdf = gdf.to_crs(epsg=6933)
```
