---
name: load-and-inspect-geodata
description: Load GeoJSON files with GeoPandas and inspect their structure — columns, CRS, geometry types, and sample rows. Use this before any spatial analysis to understand field names and data layout.
---

## Loading and Inspecting GeoDataFrames

```python
import geopandas as gpd
import json

def inspect_geodataframe(path, label="GeoDataFrame", n=3):
    gdf = gpd.read_file(path)
    print(f"\n=== {label} ===")
    print(f"CRS: {gdf.crs}")
    print(f"Shape: {gdf.shape}")
    print(f"Columns: {list(gdf.columns)}")
    print(f"Geometry types: {gdf.geom_type.value_counts().to_dict()}")
    print(f"\nSample rows:")
    print(gdf.head(n).to_string())
    return gdf

# Usage:
# plates = inspect_geodataframe("/root/PB2002_plates.json", "Plates")
# boundaries = inspect_geodataframe("/root/PB2002_boundaries.json", "Boundaries")
# earthquakes_raw = json.load(open("/root/earthquakes_2024.json"))
```

## Loading Earthquake JSON

```python
import json
import geopandas as gpd
from shapely.geometry import Point

def load_earthquakes(path):
    with open(path) as f:
        data = json.load(f)
    features = data["features"]
    rows = []
    for feat in features:
        props = feat["properties"]
        coords = feat["geometry"]["coordinates"]
        rows.append({
            "id": feat["id"],
            "place": props.get("place"),
            "time_ms": props.get("time"),
            "magnitude": props.get("mag"),
            "longitude": coords[0],
            "latitude": coords[1],
            "geometry": Point(coords[0], coords[1])
        })
    import pandas as pd
    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
    # Convert time from ms to ISO 8601
    gdf["time"] = pd.to_datetime(gdf["time_ms"], unit="ms", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return gdf

# earthquakes = load_earthquakes("/root/earthquakes_2024.json")
# print(earthquakes.head())
```

Key notes:
- Always print `.columns` before accessing fields — plate files often use `"Code"` not `"name"` or `"Name"`.
- Check for `PlateA`/`PlateB` in the boundaries file before filtering.
- Earthquake time is in milliseconds since epoch — convert with `pd.to_datetime(..., unit="ms", utc=True)`.