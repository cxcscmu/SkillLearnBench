---
name: geojson-processing
description: Loading and processing GeoJSON earthquake and plate boundary data with GeoPandas for spatial analysis.
---

# GeoJSON Processing with GeoPandas

## Loading GeoJSON Files

```python
import geopandas as gpd

# Standard GeoJSON
gdf = gpd.read_file("file.geojson")

# USGS Earthquake GeoJSON specifics:
# - Coordinates are [longitude, latitude, depth]
# - Time is in milliseconds since epoch
# - Properties include: mag, place, time, type, id
```

## USGS Earthquake Time Conversion

```python
import pandas as pd
from datetime import datetime, timezone

# Convert epoch ms to ISO 8601
timestamp_ms = 1735537742808
dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
iso_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
```

## Extracting Coordinates from GeoJSON Points

```python
# After loading with GeoPandas
gdf["longitude"] = gdf.geometry.x
gdf["latitude"] = gdf.geometry.y
```

## Writing Results to JSON

```python
import json

result = {
    "id": "us6000pgf9",
    "place": "13 km NW of Port-Vila, Vanuatu",
    "time": "2024-12-30T03:29:02Z",
    "magnitude": 5.1,
    "latitude": -17.6555,
    "longitude": 168.2183,
    "distance_km": 1234.56
}

with open("answer.json", "w") as f:
    json.dump(result, f, indent=2)
```
