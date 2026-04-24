---
name: run2_plate-boundary-analysis
description: Finding earthquakes within tectonic plates and computing distances to plate boundaries using PB2002 data.
---

# Plate Boundary Analysis with PB2002

## Data Files
- **PB2002_plates.json**: GeoJSON with plate polygons. Key fields: `Code` (e.g., "PA"), `PlateName` (e.g., "Pacific").
- **PB2002_boundaries.json**: GeoJSON with boundary LineStrings. Key fields: `PlateA`, `PlateB` (two-letter plate codes).

## Step-by-Step: Finding Furthest Earthquake from Boundary

### 1. Load and filter
```python
plates = gpd.read_file("PB2002_plates.json").set_crs("EPSG:4326", allow_override=True)
boundaries = gpd.read_file("PB2002_boundaries.json").set_crs("EPSG:4326", allow_override=True)
earthquakes = gpd.read_file("earthquakes_2024.json").set_crs("EPSG:4326", allow_override=True)

pacific_plate = plates[plates["Code"] == "PA"]
pa_boundaries = boundaries[(boundaries["PlateA"] == "PA") | (boundaries["PlateB"] == "PA")]
```

### 2. Spatial join for containment
```python
eq_in_pacific = gpd.sjoin(earthquakes, pacific_plate, predicate="within")
```

### 3. Compute distances in projected CRS
```python
from shapely.ops import unary_union

crs = "+proj=aeqd +lat_0=0 +lon_0=-160 +datum=WGS84 +units=m"
pa_boundary_union = unary_union(pa_boundaries.geometry)
pa_boundary_proj = gpd.GeoSeries([pa_boundary_union], crs="EPSG:4326").to_crs(crs).iloc[0]
eq_proj = eq_in_pacific.to_crs(crs)
distances_km = eq_proj.geometry.distance(pa_boundary_proj) / 1000.0
```

### 4. Find maximum
```python
max_idx = distances_km.idxmax()
result = eq_in_pacific.loc[max_idx]
```

## USGS Earthquake Time Format
```python
from datetime import datetime, timezone
epoch_ms = result["time"]
iso = datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
```

## Expected Result
Hawaii earthquakes are typically furthest from the Pacific plate boundary (~3500+ km), as Hawaii sits in the interior of the Pacific plate.
