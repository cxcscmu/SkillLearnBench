---
name: run2_earthquake-analysis
description: Parse USGS GeoJSON earthquake data into GeoPandas GeoDataFrame and output structured JSON results for geospatial analysis.
---

# USGS Earthquake GeoJSON Analysis (Improved)

## Data Structure

```json
{
  "type": "FeatureCollection",
  "metadata": {"count": 1504},
  "features": [{
    "type": "Feature",
    "properties": {
      "mag": 5.1,
      "place": "13 km NW of Port-Vila, Vanuatu",
      "time": 1735537742808,  // milliseconds since Unix epoch (UTC)
      "type": "earthquake"    // could also be "quarry blast" etc.
    },
    "geometry": {
      "type": "Point",
      "coordinates": [lon, lat, depth_km]  // NOTE: lon first, then lat
    },
    "id": "us6000pgf9"
  }]
}
```

## Loading into GeoPandas

```python
import json
import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime, timezone

with open("earthquakes_2024.json") as f:
    eq_data = json.load(f)

rows = []
for feat in eq_data["features"]:
    props = feat["properties"]
    coords = feat["geometry"]["coordinates"]
    # coordinates = [longitude, latitude, depth] — lon FIRST
    rows.append({
        "id": feat["id"],
        "place": props.get("place", ""),
        "time": datetime.fromtimestamp(props["time"] / 1000, tz=timezone.utc),
        "magnitude": props.get("mag"),
        "longitude": coords[0],
        "latitude": coords[1],
    })

geometry = [Point(r["longitude"], r["latitude"]) for r in rows]
gdf_eq = gpd.GeoDataFrame(rows, geometry=geometry, crs="EPSG:4326")
```

## Key Points

- **Timestamps** are in milliseconds (not seconds) — divide by 1000 before `fromtimestamp()`
- **Coordinates** order is `[longitude, latitude, depth]` in GeoJSON (lon first!)
- **Depth** is the third coordinate element — ignore for 2D spatial analysis
- Event types may include non-earthquakes; filter if needed: `props["type"] == "earthquake"`

## Time Formatting (ISO 8601)

```python
from datetime import datetime, timezone

time_ms = 1735537742808
dt = datetime.fromtimestamp(time_ms / 1000, tz=timezone.utc)
iso_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
# => "2024-12-30T02:29:02Z"
```

## Output JSON Format

```python
import json

result = {
    "id": str(furthest["id"]),
    "place": furthest["place"],
    "time": furthest["time"].strftime("%Y-%m-%dT%H:%M:%SZ"),
    "magnitude": float(furthest["magnitude"]),
    "latitude": float(furthest["latitude"]),
    "longitude": float(furthest["longitude"]),
    "distance_km": round(float(furthest["distance_km"]), 2)
}

with open("/root/answer.json", "w") as f:
    json.dump(result, f, indent=2)
```

## Common Gotchas

| Issue | Solution |
|-------|----------|
| Unicode in place names | Python's json.dump handles it; use `ensure_ascii=False` to preserve UTF-8 |
| Timestamp in ms vs seconds | Always divide `time` by 1000 before `fromtimestamp()` |
| lon/lat order in GeoJSON | GeoJSON uses `[lon, lat]`; `Point(lon, lat)` matches this |
| float precision in output | Use `float()` cast and `round()` for clean JSON output |
