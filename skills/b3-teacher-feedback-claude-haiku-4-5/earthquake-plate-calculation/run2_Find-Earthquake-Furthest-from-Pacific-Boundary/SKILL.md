---
name: Find Earthquake Furthest from Pacific Boundary
description: Identify the earthquake with the maximum distance to the Pacific plate boundary from the earthquakes within the Pacific plate. Use this skill to locate the target earthquake for final output.
---

```python
def find_furthest_earthquake(earthquakes_with_distance):
    """
    Find the earthquake furthest from Pacific plate boundaries.
    
    Args:
        earthquakes_with_distance: GeoDataFrame with distance_km column
        
    Returns:
        Dictionary with result earthquake data
    """
    if len(earthquakes_with_distance) == 0:
        raise ValueError("No earthquakes found within Pacific plate")
    
    # Find earthquake with maximum distance
    furthest_idx = earthquakes_with_distance['distance_km'].idxmax()
    furthest_earthquake = earthquakes_with_distance.loc[furthest_idx]
    
    # Extract coordinates (convert back to lat/lon from geometry)
    lat = furthest_earthquake.geometry.y
    lon = furthest_earthquake.geometry.x
    
    result = {
        'id': furthest_earthquake['id'],
        'place': furthest_earthquake['place'],
        'time': furthest_earthquake['time'],
        'magnitude': furthest_earthquake['magnitude'],
        'latitude': lat,
        'longitude': lon,
        'distance_km': round(furthest_earthquake['distance_km'], 2)
    }
    
    return result
```