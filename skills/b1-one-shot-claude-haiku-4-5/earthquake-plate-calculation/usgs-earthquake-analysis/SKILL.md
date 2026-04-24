---
name: usgs-earthquake-analysis
description: Load, parse, and process USGS earthquake data in GeoJSON or JSON formats.
---

# USGS Earthquake Data Analysis

## Overview
USGS earthquake data is typically provided in GeoJSON format or as JSON with earthquake features. Understanding the data structure is essential for filtering, processing, and analysis.

## Standard USGS Data Format

### GeoJSON Structure
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "us1000abc1",
      "geometry": {
        "type": "Point",
        "coordinates": [longitude, latitude, depth]
      },
      "properties": {
        "mag": 4.5,
        "place": "12 km E of somewhere",
        "time": 1632000000000,
        "updated": 1632100000000,
        "url": "https://...",
        "detail": "https://...",
        "felt": null,
        "cdi": null,
        "mmi": null,
        "alert": null,
        "status": "reviewed",
        "tsunami": 0,
        "sig": 350,
        "net": "us",
        "code": "1000abc1",
        "ids": ",us1000abc1,",
        "sources": ",us,",
        "types": ",origin,phase-data,"
      }
    }
  ]
}
```

## Key Fields
- `geometry.coordinates`: [longitude, latitude, depth]
- `properties.mag`: Magnitude
- `properties.place`: Location description
- `properties.time`: Unix timestamp in milliseconds
- `properties.id`: Unique earthquake identifier

## Loading and Processing

### From GeoJSON
```python
import json
import geopandas as gpd
from datetime import datetime

with open('/root/earthquakes_2024.json', 'r') as f:
    data = json.load(f)

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(data['features'], crs='EPSG:4326')

# Convert timestamp (milliseconds to seconds, then to ISO format)
gdf['time'] = pd.to_datetime(gdf['time'], unit='ms').dt.strftime('%Y-%m-%dT%H:%M:%SZ')
gdf['magnitude'] = gdf['mag']
```

### From Custom JSON Structure
```python
import pandas as pd

# If data is a simple list of earthquakes
earthquakes_list = json.load(open('/root/earthquakes_2024.json'))
df = pd.DataFrame(earthquakes_list)

# Ensure required fields
df['longitude'] = df['lon']
df['latitude'] = df['lat']
df['magnitude'] = df['mag']
```

## Data Validation

### Common Issues
- **Null magnitudes**: Some events may not have reliable magnitude estimates
- **Depth as third coordinate**: USGS includes depth in coordinates [lon, lat, depth]
- **Timestamp format**: Always in milliseconds since Unix epoch for USGS data

### Validation Checks
```python
# Check for required fields
required_fields = ['id', 'magnitude', 'latitude', 'longitude', 'place', 'time']
for field in required_fields:
    assert field in gdf.columns, f"Missing field: {field}"

# Verify coordinates are in valid range
assert gdf['longitude'].between(-180, 180).all()
assert gdf['latitude'].between(-90, 90).all()

# Check for null values in critical fields
assert not gdf[['id', 'magnitude', 'latitude', 'longitude']].isnull().any().any()
```

## Common Operations

### Filter by Region
```python
# Earthquakes within lat/lon bounds
pacific = gdf[(gdf['latitude'] > -60) & (gdf['latitude'] < 70) &
              (gdf['longitude'] > 100) | (gdf['longitude'] < -80)]
```

### Filter by Magnitude
```python
significant = gdf[gdf['magnitude'] >= 4.0]
```

### Convert Time to ISO Format
```python
def unix_ms_to_iso(timestamp_ms):
    return pd.to_datetime(timestamp_ms, unit='ms').strftime('%Y-%m-%dT%H:%M:%SZ')

gdf['iso_time'] = gdf['time'].apply(unix_ms_to_iso)
```
