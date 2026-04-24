---
name: earthquake-distance-analysis
description: >
  How to parse USGS GeoJSON earthquake data, filter by location relative to
  tectonic plates, and find the earthquake furthest from a plate boundary.
  Use this skill whenever the user asks to find earthquakes within a plate,
  compute distances from plate boundaries, or analyze USGS earthquake catalog
  data with GeoPandas.
---

# Earthquake Distance Analysis

## Parsing USGS GeoJSON Earthquakes

USGS earthquake data uses GeoJSON FeatureCollection format. Each feature has:
- `id`: earthquake ID string
- `properties.mag`: magnitude
- `properties.place`: location description string
- `properties.time`: Unix timestamp in milliseconds
- `geometry.coordinates`: [longitude, latitude, depth]

```python
import json
import pandas as pd
from datetime import datetime, timezone

with open("earthquakes_2024.json") as f:
    eq_data = json.load(f)

records = []
for feat in eq_data["features"]:
    props = feat["properties"]
    coords = feat["geometry"]["coordinates"]
    ts_ms = props["time"]
    iso_time = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    records.append({
        "id": feat["id"],
        "place": props["place"],
        "time": iso_time,
        "magnitude": props["mag"],
        "longitude": coords[0],
        "latitude": coords[1],
    })

df = pd.DataFrame(records)
```

## Full Workflow: Furthest Earthquake from Plate Boundary

```python
import geopandas as gpd
from shapely.ops import unary_union

# 1. Load data
plates = gpd.read_file("PB2002_plates.json")
boundaries = gpd.read_file("PB2002_boundaries.json")

# 2. Extract Pacific plate polygon and its boundaries
pacific_plate = plates[plates["Code"] == "PA"]
pa_boundaries = boundaries[boundaries["Name"].str.contains("PA")]

# 3. Choose projected CRS (Azimuthal Equidistant centered on Pacific)
CRS_PROJ = "+proj=aeqd +lat_0=0 +lon_0=-160 +units=m +datum=WGS84"

pacific_proj = pacific_plate.to_crs(CRS_PROJ)
pa_boundaries_proj = pa_boundaries.to_crs(CRS_PROJ)

# 4. Create earthquake GeoDataFrame
eq_gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
    crs="EPSG:4326"
).to_crs(CRS_PROJ)

# 5. Filter: only earthquakes inside the Pacific plate polygon
eq_in_pacific = gpd.sjoin(eq_gdf, pacific_proj[["geometry"]], how="inner", predicate="within")

# 6. Compute distance to boundary
boundary_union = unary_union(pa_boundaries_proj.geometry)
eq_in_pacific["dist_km"] = eq_in_pacific.geometry.apply(
    lambda pt: pt.distance(boundary_union) / 1000
)

# 7. Find the furthest earthquake
furthest = eq_in_pacific.loc[eq_in_pacific["dist_km"].idxmax()]
```

## Output Format

```python
import json

result = {
    "id": furthest["id"],
    "place": furthest["place"],
    "time": furthest["time"],
    "magnitude": float(furthest["magnitude"]),
    "latitude": float(furthest["latitude"]),
    "longitude": float(furthest["longitude"]),
    "distance_km": round(float(furthest["dist_km"]), 2)
}

with open("/root/answer.json", "w") as f:
    json.dump(result, f, indent=2)
```

## Common Pitfalls

- **Antimeridian wrapping**: The Pacific plate spans the date line. Some geometries
  may have issues. If `sjoin` gives unexpected results, try buffering the plate
  polygon or using a custom projection centered on the Pacific.
- **Boundary vs. plate polygon**: Use `PB2002_boundaries.json` for the boundary
  LineStrings (distance calculation), and `PB2002_plates.json` for the polygon
  (point-in-plate test).
- **Units**: After projecting to a meters-based CRS, divide by 1000 for km.
- **Duplicate index**: After `sjoin`, reset index or use `.copy()` to avoid issues.
