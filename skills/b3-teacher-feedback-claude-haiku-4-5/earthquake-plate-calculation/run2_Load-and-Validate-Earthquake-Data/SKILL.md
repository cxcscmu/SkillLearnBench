---
name: Load and Validate Earthquake Data
description: Load earthquake data from GeoJSON format and validate that it contains required fields (id, time, magnitude, latitude, longitude, place). Use this skill when initializing the analysis to ensure data integrity before processing.
---

```python
import json
import geopandas as gpd
from shapely.geometry import Point

def load_earthquake_data(filepath):
    """
    Load earthquake data from GeoJSON and convert to GeoDataFrame.
    
    Args:
        filepath: Path to earthquakes_2024.json
        
    Returns:
        GeoDataFrame with earthquake points and attributes
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    earthquakes = []
    for feature in data['features']:
        props = feature['properties']
        coords = feature['geometry']['coordinates']
        
        # Validate required fields
        required = ['id', 'time', 'mag', 'place']
        if not all(k in props for k in required):
            continue
            
        earthquakes.append({
            'id': props['id'],
            'time': props['time'],
            'magnitude': props['mag'],
            'place': props['place'],
            'geometry': Point(coords[0], coords[1])
        })
    
    gdf = gpd.GeoDataFrame(earthquakes, crs='EPSG:4326')
    return gdf
```