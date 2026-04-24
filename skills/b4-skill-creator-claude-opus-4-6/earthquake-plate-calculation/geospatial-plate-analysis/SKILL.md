---
name: geospatial-plate-analysis
description: >
  Analyze tectonic plate geometries using GeoPandas with proper coordinate projections.
  Use this skill whenever working with PB2002 plate boundary/plate polygon data,
  filtering points by plate membership, or extracting plate-specific boundaries.
  Triggers on: plate tectonics, tectonic plates, plate boundaries, PB2002 dataset.
---

# Geospatial Plate Analysis

## Purpose

Load and process PB2002 tectonic plate data (boundaries and plate polygons) using GeoPandas,
then perform spatial operations like point-in-polygon tests and boundary extraction.

## Data Format

### PB2002_plates.json
- GeoJSON FeatureCollection with plate polygons
- Properties: `Code` (e.g., "PA"), `PlateName` (e.g., "Pacific")
- Geometry: Polygon or MultiPolygon (lon/lat, EPSG:4326)
- The Pacific plate ("PA") is a **MultiPolygon** that crosses the antimeridian (±180°)

### PB2002_boundaries.json
- GeoJSON FeatureCollection with plate boundary LineStrings
- Properties: `PlateA`, `PlateB` (two-letter plate codes), `Name`, `Type`
- To get all boundaries of a plate (e.g., "PA"), filter where `PlateA == "PA"` OR `PlateB == "PA"`

### Earthquake GeoJSON (USGS format)
- Features with Point geometry: `[longitude, latitude, depth]`
- Properties include: `mag`, `place`, `time` (Unix ms), `type`
- Feature `id` field contains the earthquake ID

## Workflow

### 1. Load data
```python
import geopandas as gpd

plates = gpd.read_file("PB2002_plates.json")
boundaries = gpd.read_file("PB2002_boundaries.json")
earthquakes = gpd.read_file("earthquakes_2024.json")
```

All data loads in EPSG:4326 (WGS84 lon/lat).

### 2. Extract a specific plate polygon
```python
pacific_plate = plates[plates["Code"] == "PA"]
```

### 3. Filter points inside a plate
Use a spatial join or `within` test:
```python
quakes_in_plate = gpd.sjoin(earthquakes, pacific_plate, predicate="within")
```

### 4. Extract plate boundaries
Filter boundaries where the plate code appears in either PlateA or PlateB:
```python
pa_boundaries = boundaries[
    (boundaries["PlateA"] == "PA") | (boundaries["PlateB"] == "PA")
]
```

## Antimeridian Handling

The Pacific plate crosses the ±180° meridian. GeoPandas handles MultiPolygon geometries
natively, so `sjoin` with `predicate="within"` works correctly for point-in-polygon tests
as long as the plate polygon is properly defined (which PB2002 data is).

## Key Libraries
- `geopandas` — spatial data frames, spatial joins
- `shapely` — geometry operations (union, distance, nearest_points)
- `pyproj` — CRS transformations
