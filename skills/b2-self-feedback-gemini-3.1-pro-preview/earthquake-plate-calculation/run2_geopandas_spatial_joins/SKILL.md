---
name: run2_geopandas_spatial_joins
description: Improved guide for performing spatial joins with GeoPandas, specifically handling antimeridian crossing polygons like the Pacific Plate.
---

# Spatial Joins and Antimeridian in GeoPandas

GeoPandas provides `sjoin` to join points and polygons based on their spatial relationship.

## Pacific Plate and the Antimeridian
The Pacific Plate spans across the 180° meridian (antimeridian). Standard WGS84 (EPSG:4326) coordinates wrap around this line.
High-quality datasets like PB2002 split tectonic plates that cross the antimeridian into `MultiPolygon` geometries. This means a standard spatial join using Euclidean intersection rules on EPSG:4326 will correctly identify points within the plate without false positives connecting -180 and 180 through Greenwich.

## Usage

```python
import geopandas as gpd

# Load points and polygons
points = gpd.read_file('points.geojson')
polygons = gpd.read_file('polygons.geojson')

# Ensure matching CRS before spatial join
if points.crs != polygons.crs:
    points = points.to_crs(polygons.crs)

# Filter polygons (e.g. Code == 'PA' for Pacific Plate)
pacific_plate = polygons[polygons['Code'] == 'PA']

# Find points within the polygon
points_in_poly = gpd.sjoin(points, pacific_plate, predicate='within')

print(f"Points inside PA plate: {len(points_in_poly)}")
```
