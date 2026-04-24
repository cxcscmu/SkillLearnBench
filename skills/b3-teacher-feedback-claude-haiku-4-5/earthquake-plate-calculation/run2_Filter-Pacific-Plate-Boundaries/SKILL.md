---
name: Filter Pacific Plate Boundaries
description: Filter the boundary dataset to include only boundaries relevant to the Pacific plate (where PlateA or PlateB equals the Pacific plate identifier). Use this skill to exclude irrelevant boundaries before distance calculations.
---

```python
def filter_pacific_boundaries(boundaries_gdf, pacific_id):
    """
    Filter boundaries to only those involving the Pacific plate.
    
    Args:
        boundaries_gdf: GeoDataFrame with all plate boundaries
        pacific_id: Identifier for the Pacific plate
        
    Returns:
        GeoDataFrame containing only Pacific plate boundaries
    """
    # Filter where PlateA or PlateB equals Pacific identifier
    pacific_boundaries = boundaries_gdf[
        (boundaries_gdf['PlateA'] == pacific_id) | 
        (boundaries_gdf['PlateB'] == pacific_id)
    ].copy()
    
    print(f"Found {len(pacific_boundaries)} boundaries involving Pacific plate")
    
    return pacific_boundaries
```