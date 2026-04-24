---
name: usgs-earthquake-geojson
description: Parse and work with USGS earthquake GeoJSON data, extracting IDs, magnitudes, coordinates, times, and place descriptions.
---

# USGS Earthquake GeoJSON Parsing

## Data Structure
USGS earthquake GeoJSON follows the standard FeatureCollection format:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": 5.1,
        "place": "13 km NW of Port-Vila, Vanuatu",
        "time": 1735537742808,   // Unix timestamp in milliseconds
        "mag": 5.1,
        "magType": "mww"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [168.2183, -17.6555, 66.612]  // [lon, lat, depth_km]
      },
      "id": "us6000pgf9"
    }
  ]
}
```

## Loading into GeoDataFrame
```python
import geopandas as gpd
import json
from datetime import datetime, timezone

with open("earthquakes_2024.json") as f:
    eq_data = json.load(f)

records = []
for feat in eq_data["features"]:
    props = feat["properties"]
    coords = feat["geometry"]["coordinates"]
    time_ms = props["time"]
    time_iso = datetime.fromtimestamp(time_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    records.append({
        "id": feat["id"],
        "place": props["place"],
        "time": time_iso,
        "magnitude": props["mag"],
        "longitude": coords[0],
        "latitude": coords[1],
    })

gdf = gpd.GeoDataFrame(
    records,
    geometry=gpd.points_from_xy([r["longitude"] for r in records], [r["latitude"] for r in records]),
    crs="EPSG:4326"
)
```

## Key Notes
- `time` field is Unix timestamp in **milliseconds** (divide by 1000 for seconds)
- `geometry.coordinates` is `[longitude, latitude, depth_km]` — NOT `[lat, lon]`
- Use `datetime.fromtimestamp(ms/1000, tz=timezone.utc)` for ISO 8601 UTC formatting
