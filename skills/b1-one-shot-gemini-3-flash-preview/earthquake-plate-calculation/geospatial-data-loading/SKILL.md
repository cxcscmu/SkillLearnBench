---
name: geospatial-data-loading
description: Techniques for loading and initial processing of GeoJSON and coordinate-based datasets using GeoPandas.
---

# Geospatial Data Loading

## Overview
GeoPandas is the primary library for loading geographic data in Python. It extends pandas to allow spatial operations on geometric types.

## Loading GeoJSON
GeoJSON is a standard format for geographic data.

```python
import geopandas as gpd

# Load directly from file
gdf = gpd.read_file("data.json")

# Inspect CRS (Coordinate Reference System)
print(gdf.crs) # Usually EPSG:4326 for GeoJSON
```

## Creating GDF from Dictionary/List
If you have raw JSON or a list of dictionaries with coordinates:

```python
from shapely.geometry import Point
import geopandas as gpd

data = [
    {"id": "eq1", "lat": 10.5, "lon": 120.3},
    {"id": "eq2", "lat": -5.2, "lon": -150.8}
]

geometry = [Point(d["lon"], d["lat"]) for d in data]
gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")
```

## Handling Multi-Geometries
Some datasets might contain `MultiPolygon` or `MultiLineString`. GeoPandas handles these automatically, but you might want to "explode" them into individual parts:

```python
gdf_exploded = gdf.explode(index_parts=False)
```
