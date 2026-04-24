---
name: plate-tectonics-spatial
description: Work with PB2002 plate boundary and polygon data to identify plate membership and boundary distances for earthquakes.
---

# Plate Tectonics Spatial Analysis (PB2002 Dataset)

## Data Files
- `PB2002_plates.json` — Polygons for each tectonic plate
- `PB2002_boundaries.json` — LineStrings for plate boundaries

## Plate Properties
```python
# plates.json feature properties:
{ "LAYER": "plate", "Code": "PA", "PlateName": "Pacific" }

# boundaries.json feature properties:
{ "LAYER": "plate boundary", "Name": "PA-AN", "PlateA": "PA", "PlateB": "AN", "Type": "" }
```

## Pacific Plate Boundaries
Filter boundaries where PlateA or PlateB == "PA":
```python
pacific_bounds = gdf_boundaries[
    (gdf_boundaries["PlateA"] == "PA") |
    (gdf_boundaries["PlateB"] == "PA")
]
```

Note: Some boundary names use separators like `-`, `/`, `\`. Always filter by PlateA/PlateB columns, not the Name string.

## Finding Earthquakes Within Pacific Plate
```python
pacific_poly = gdf_plates[gdf_plates["Code"] == "PA"].geometry.unary_union
eq_in_pacific = gdf_earthquakes[gdf_earthquakes.within(pacific_poly)].copy()
```

## Antimeridian Handling
The Pacific plate spans the antimeridian (±180°). GeoPandas handles this automatically when using `.within()` and `.distance()` with proper CRS. Do NOT manually shift longitudes.

## Full Analysis Pipeline
```python
import geopandas as gpd
from shapely.geometry import Point

METRIC_CRS = "EPSG:4087"

# Load data
gdf_plates = gpd.read_file("PB2002_plates.json")
gdf_bounds = gpd.read_file("PB2002_boundaries.json")

# Get Pacific plate polygon
pacific_poly = gdf_plates[gdf_plates["Code"] == "PA"].geometry.unary_union

# Filter earthquakes inside Pacific plate
eq_pacific = gdf_eq[gdf_eq.within(pacific_poly)].copy()

# Get Pacific plate boundaries
pa_bounds = gdf_bounds[
    (gdf_bounds["PlateA"] == "PA") | (gdf_bounds["PlateB"] == "PA")
].to_crs(METRIC_CRS).geometry.unary_union

# Calculate distance from each earthquake to nearest boundary
eq_proj = eq_pacific.to_crs(METRIC_CRS)
eq_pacific["distance_km"] = eq_proj.geometry.distance(pa_bounds) / 1000.0

# Find furthest earthquake from boundary
result = eq_pacific.nlargest(1, "distance_km").iloc[0]
```

## Output JSON Format
```python
import json

output = {
    "id": result["id"],
    "place": result["place"],
    "time": result["time"],  # ISO 8601: "YYYY-MM-DDTHH:MM:SSZ"
    "magnitude": result["magnitude"],
    "latitude": result["latitude"],
    "longitude": result["longitude"],
    "distance_km": round(result["distance_km"], 2)
}

with open("answer.json", "w") as f:
    json.dump(output, f, indent=2)
```
