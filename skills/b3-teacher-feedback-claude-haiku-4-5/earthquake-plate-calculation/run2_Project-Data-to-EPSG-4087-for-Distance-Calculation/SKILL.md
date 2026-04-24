---
name: Project Data to EPSG:4087 for Distance Calculation
description: Reproject earthquake points and boundary geometries to EPSG:4087 (World Equidistant Cylindrical) before calculating distances. Use this skill to ensure accurate distance measurements in kilometers.
---

```python
def project_for_distance_calculation(earthquakes_gdf, boundaries_gdf):
    """
    Reproject both datasets to EPSG:4087 for accurate distance calculation.
    
    Args:
        earthquakes_gdf: GeoDataFrame with earthquake points (EPSG:4326)
        boundaries_gdf: GeoDataFrame with boundaries (EPSG:4326)
        
    Returns:
        Tuple of (reprojected_earthquakes, reprojected_boundaries)
    """
    # Reproject to EPSG:4087 (World Equidistant Cylindrical)
    earthquakes_proj = earthquakes_gdf.to_crs('EPSG:4087')
    boundaries_proj = boundaries_gdf.to_crs('EPSG:4087')
    
    return earthquakes_proj, boundaries_proj
```