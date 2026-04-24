---
name: geopandas-spatial-filtering
description: Use GeoPandas to filter points within a specific polygon, such as finding earthquakes within a specific tectonic plate.
---

To filter points based on their location within a polygon:
1. Load the polygon data (e.g., plate geometries) and the point data (e.g., earthquakes) into GeoDataFrames.
2. Ensure both GeoDataFrames use the same Coordinate Reference System (CRS), typically WGS84 (EPSG:4326).
3. Identify the target polygon (e.g., the Pacific Plate, often abbreviated as 'PA' in PB2002 datasets).
4. Use the `.within()` predicate or a spatial join `gpd.sjoin()` to filter the points.

```python
import geopandas as gpd

# Load datasets
plates = gpd.read_file('plates.json')
points = gpd.read_file('points.json')

# Extract specific plate (e.g., Pacific Plate 'PA')
pacific_plate = plates[plates['Code'] == 'PA'].geometry.iloc[0]

# Filter points within the polygon
points_in_plate = points[points.within(pacific_plate)]
```