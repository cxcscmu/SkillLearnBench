---
name: Filter Earthquakes Within Pacific Plate
description: Use the `.within()` geometric method to identify earthquakes that are contained inside the Pacific plate polygon. Use this skill to ensure only earthquakes actually inside the Pacific plate are analyzed.
---

```python
def filter_earthquakes_within_pacific(earthquakes_gdf, plates_gdf, pacific_id, plate_name_col):
    """
    Filter earthquakes that are within the Pacific plate polygon.
    
    Args:
        earthquakes_gdf: GeoDataFrame with earthquake points
        plates_gdf: GeoDataFrame with plate polygons
        pacific_id: Identifier for the Pacific plate
        plate_name_col: Column name containing plate identifiers
        
    Returns:
        GeoDataFrame containing only earthquakes within Pacific plate
    """
    # Get Pacific plate polygon
    pacific_plate = plates_gdf[plates_gdf[plate_name_col] == pacific_id]
    
    if len(pacific_plate) == 0:
        raise ValueError(f"Pacific plate '{pacific_id}' not found in data")
    
    pacific_polygon = pacific_plate.geometry.iloc[0]
    
    # Filter earthquakes using .within()
    earthquakes_in_pacific = earthquakes_gdf[
        earthquakes_gdf.geometry.within(pacific_polygon)
    ].copy()
    
    print(f"Found {len(earthquakes_in_pacific)} earthquakes within Pacific plate")
    
    return earthquakes_in_pacific
```