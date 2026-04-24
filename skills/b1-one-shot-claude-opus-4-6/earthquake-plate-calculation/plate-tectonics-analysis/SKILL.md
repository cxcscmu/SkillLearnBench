---
name: plate-tectonics-analysis
description: Analyzing earthquake data relative to tectonic plate boundaries using PB2002 dataset and GeoPandas.
---

# Plate Tectonics Analysis with PB2002 Dataset

## PB2002 Dataset Structure

### Plates (`PB2002_plates.json`)
- GeoJSON FeatureCollection with Polygon geometries
- Properties include `PlateName` (e.g., "PA" for Pacific)
- Each feature is a tectonic plate polygon

### Boundaries (`PB2002_boundaries.json`)
- GeoJSON FeatureCollection with LineString geometries
- Properties: `PlateA`, `PlateB` (2-letter plate codes), `Name`, `Type`
- Pacific plate code: "PA"
- Boundaries involving Pacific: PlateA == "PA" or PlateB == "PA"

### Common Plate Codes
- PA: Pacific, NA: North America, SA: South America
- EU: Eurasia, AF: Africa, AN: Antarctica
- AU: Australia, IN: India, NZ: Nazca

## Workflow: Find Earthquakes Inside a Plate

```python
import geopandas as gpd

# Load plate polygons and earthquake points
plates = gpd.read_file("PB2002_plates.json")
earthquakes = gpd.read_file("earthquakes.json")

# Get Pacific plate polygon
pacific = plates[plates["PlateName"] == "PA"]

# Spatial join: earthquakes within Pacific plate
eq_in_pacific = gpd.sjoin(earthquakes, pacific, predicate="within")
```

## Workflow: Get Plate Boundaries

```python
boundaries = gpd.read_file("PB2002_boundaries.json")

# Filter boundaries of Pacific plate
pa_bounds = boundaries[
    (boundaries["PlateA"] == "PA") | (boundaries["PlateB"] == "PA")
]

# Merge all boundary segments into one geometry
pa_boundary_union = pa_bounds.unary_union
```

## Workflow: Distance from Earthquake to Plate Boundary

```python
# Project both to a suitable CRS
proj_crs = "+proj=aeqd +lat_0=0 +lon_0=-160 +datum=WGS84 +units=m"

eq_proj = eq_in_pacific.to_crs(proj_crs)
boundary_proj = pa_bounds.to_crs(proj_crs)
boundary_union_proj = boundary_proj.unary_union

# Calculate distances
eq_proj["dist_to_boundary"] = eq_proj.geometry.distance(boundary_union_proj)
eq_proj["dist_km"] = eq_proj["dist_to_boundary"] / 1000

# Find the earthquake furthest from boundary
furthest = eq_proj.loc[eq_proj["dist_km"].idxmax()]
```
