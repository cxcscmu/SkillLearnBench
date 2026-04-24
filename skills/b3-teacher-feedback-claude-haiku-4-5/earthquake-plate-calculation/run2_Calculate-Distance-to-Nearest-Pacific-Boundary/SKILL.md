---
name: Calculate Distance to Nearest Pacific Boundary
description: Combine all Pacific plate boundary geometries using `.unary_union` and calculate the distance from each earthquake to this combined boundary geometry. Returns the minimum distance in kilometers for each earthquake.
---

```python
def calculate_distances_to_boundary(earthquakes_proj, boundaries_proj):
    """
    Calculate distance from each earthquake to the nearest Pacific boundary.
    
    Args:
        earthquakes_proj: GeoDataFrame with earthquakes in EPSG:4087
        boundaries_proj: GeoDataFrame with Pacific boundaries in EPSG:4087
        
    Returns:
        GeoDataFrame with added 'distance_km' column
    """
    # Combine all boundary geometries into single geometry
    combined_boundaries = boundaries_proj.geometry.unary_union
    
    # Calculate distance from each earthquake to combined boundary
    # EPSG:4087 uses meters, so divide by 1000 for kilometers
    earthquakes_proj['distance_km'] = earthquakes_proj.geometry.distance(
        combined_boundaries
    ) / 1000
    
    return earthquakes_proj
```