---
name: run2_geopandas-plate-tectonics
description: Load and work with PB2002 tectonic plate boundary data using GeoPandas for spatial filtering and distance calculations, with antimeridian awareness.
---

# GeoPandas Plate Tectonics Analysis (Improved)

## Setup

```python
import geopandas as gpd
from shapely.geometry import Point
```

## PB2002 Data Structure

### Plates file (PB2002_plates.json)
- `Code`: 2-letter plate code (e.g., "PA" for Pacific, "NA" for North America)
- `PlateName`: Full plate name
- Geometry: Polygon (may be MultiPolygon for plates crossing antimeridian)

### Boundaries file (PB2002_boundaries.json)
- `PlateA`, `PlateB`: 2-letter codes for plates on each side
- `Name`: Mixed-separator combined name (e.g., "PA-AN", "NA/PA", "AU\\PA")
- Geometry: LineString segments

## Loading Data

```python
gdf_plates = gpd.read_file("PB2002_plates.json")   # CRS: EPSG:4326
gdf_boundaries = gpd.read_file("PB2002_boundaries.json")  # CRS: EPSG:4326
```

## Antimeridian Handling

The Pacific plate spans the antimeridian (180°/-180° line). GeoPandas/Shapely
represents this as a **MultiPolygon** with separate polygons on each side:
- Eastern Pacific: bounds roughly (-180, -66) to (-102, 60)
- Western Pacific: bounds roughly (138, -65) to (180, 55)
- Southern Pacific: bounds roughly (157, -65) to (180, -37)

The `.within()` spatial predicate works correctly with MultiPolygon — no manual
longitude adjustment needed.

## Filtering Pacific Plate

```python
# Get Pacific plate polygon (MultiPolygon due to antimeridian split)
pacific_poly = gdf_plates[gdf_plates["Code"] == "PA"].geometry.union_all()

# Get all Pacific plate boundaries — filter by PlateA/PlateB, NOT Name
# (Name field uses mixed separators: -, /, \)
pa_boundaries = gdf_boundaries[
    (gdf_boundaries["PlateA"] == "PA") | (gdf_boundaries["PlateB"] == "PA")
]
```

## Distance Calculation (Metric CRS)

```python
METRIC_CRS = "EPSG:4087"  # World Equidistant Cylindrical (meters)

# Project boundaries to metric and combine
boundary_union = pa_boundaries.to_crs(METRIC_CRS).geometry.union_all()

# Project points and calculate distances
eq_proj = gdf_eq_in_pacific.to_crs(METRIC_CRS)
distances_km = eq_proj.geometry.distance(boundary_union) / 1000.0
```

## Note: use union_all() not unary_union

`unary_union` is deprecated in newer geopandas. Use `union_all()` instead:

```python
# ❌ Deprecated
boundary_geom = gdf.geometry.unary_union

# ✅ Current
boundary_geom = gdf.geometry.union_all()
```

## Complete Workflow

```python
import json, geopandas as gpd
from shapely.geometry import Point
from datetime import datetime, timezone

# Load
gdf_plates = gpd.read_file("PB2002_plates.json")
gdf_boundaries = gpd.read_file("PB2002_boundaries.json")

# Pacific plate polygon
pacific_poly = gdf_plates[gdf_plates["Code"] == "PA"].geometry.union_all()

# Pacific boundaries
pa_bounds = gdf_boundaries[
    (gdf_boundaries["PlateA"] == "PA") | (gdf_boundaries["PlateB"] == "PA")
]

# Spatial filter
eq_in_pacific = gdf_eq[gdf_eq.geometry.within(pacific_poly)].copy()

# Distance in metric CRS
METRIC = "EPSG:4087"
boundary_union = pa_bounds.to_crs(METRIC).geometry.union_all()
eq_proj = eq_in_pacific.to_crs(METRIC)
eq_in_pacific["distance_km"] = eq_proj.geometry.distance(boundary_union) / 1000.0

# Furthest
furthest = eq_in_pacific.nlargest(1, "distance_km").iloc[0]
```
