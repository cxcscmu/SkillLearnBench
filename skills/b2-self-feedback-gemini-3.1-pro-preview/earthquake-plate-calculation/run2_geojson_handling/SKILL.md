---
name: run2_geojson_handling
description: Advanced handling of GeoJSON files in GeoPandas, emphasizing correct geometry formats and time processing to ISO 8601 standard.
---

# GeoJSON and Time Formatting

GeoPandas natively reads GeoJSON files into a `GeoDataFrame`.
Properties like Unix timestamps in JSON are often stored in milliseconds, and must be correctly formatted to ISO 8601 string representations (e.g. `YYYY-MM-DDTHH:MM:SSZ`) for external consistency.

## Usage

```python
import geopandas as gpd
from datetime import datetime, timezone

# Load points
gdf = gpd.read_file('features.json')

# Attributes are Pandas columns
print(gdf['mag'].max())

# Spatial properties
lon = gdf.geometry.x
lat = gdf.geometry.y

# Format Time to ISO 8601 (without fractional seconds)
def format_iso_time(ms_timestamp):
    dt = datetime.fromtimestamp(ms_timestamp / 1000.0, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

print(format_iso_time(1735537742808))
# Outputs: '2024-12-30T04:02:22Z'
```
