---
name: run2_antimeridian-handling
description: Handling the antimeridian (180/-180 longitude) in geospatial analysis with GeoPandas and Shapely.
---

# Antimeridian Handling in GeoPandas

## The Problem
The Pacific plate spans the antimeridian (International Date Line at 180/-180 degrees longitude). Standard operations in EPSG:4326 may split geometries incorrectly.

## PB2002 Dataset Behavior
- The PB2002 plate polygons in GeoJSON handle the antimeridian by having bounds from -180 to 180.
- The Pacific plate polygon's bounds are `(-180, -66, 180, 60)`, meaning it wraps correctly.
- `gpd.sjoin(predicate="within")` works correctly with these polygons for point-in-polygon tests.

## Projection Solution
When computing distances, project to a CRS centered in the Pacific:
```python
# Center at 160°W (middle of Pacific Ocean)
crs = "+proj=aeqd +lat_0=0 +lon_0=-160 +datum=WGS84 +units=m"
```
This avoids antimeridian splitting because the projection center is far from the antimeridian.

## Alternative: Shift Longitudes
```python
# Shift all longitudes to [0, 360] range
def shift_lon(geom):
    from shapely.affinity import translate
    # This is complex for polygons; projection is simpler
    pass
```
Projection is generally the better approach.
