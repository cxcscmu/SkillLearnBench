---
name: multipart-geometry-handling
description: Work with MultiPolygon and MultiLineString geometries from real plate boundary datasets.
---

# MultiPart Geometry Handling

## Installation
```bash
pip install geopandas shapely pandas
```

## Overview
Real-world plate boundary data consists of disconnected LineString segments (MultiLineString) that need special handling for distance calculations. Similarly, plates can be represented as MultiPolygons.

## Understanding MultiPart Geometries

### MultiLineString (Plate Boundaries)
```python
from shapely.geometry import MultiLineString, LineString

# Boundaries may be stored as multiple LineString objects
boundary_geom = boundaries.geometry.unary_union
print(f"Type: {type(boundary_geom)}")  # MultiLineString

# Access individual parts
if isinstance(boundary_geom, MultiLineString):
    for i, line in enumerate(boundary_geom.geoms):
        print(f"Segment {i}: {len(line.coords)} points")
```

### MultiPolygon (Plate Regions)
```python
# Pacific plate might consist of multiple disconnected polygons
pacific_geom = pacific_plates.geometry.unary_union
print(f"Type: {type(pacific_geom)}")  # MultiPolygon

# Access individual polygons
if isinstance(pacific_geom, MultiPolygon):
    for i, poly in enumerate(pacific_geom.geoms):
        print(f"Polygon {i}: {len(poly.exterior.coords)} boundary points")
```

## Distance Calculation with MultiLineString

The Shapely `.distance()` method automatically handles MultiLineString:
- Computes distance to nearest segment
- Works efficiently with large multipart geometries

```python
# This works correctly even if boundary_geom is MultiLineString
distances = points_gdf.geometry.distance(boundary_geom)

# Find minimum distance for each point
min_distance = distances.min()  # Distance to nearest boundary segment
```

## Point-in-MultiPolygon

GeoPandas' `.within()` method also handles MultiPolygon correctly:
```python
# Find points within any part of multipolygon
within_mask = earthquakes.geometry.within(pacific_geom)
earthquakes_within = earthquakes[within_mask]

# Result: includes points in any of the disconnected polygon parts
```

## Validation: Verify Coverage

```python
import geopandas as gpd

# Sanity check: are boundaries actually on plate edges?
boundaries_gdf = boundaries.to_crs('EPSG:3857')
plate_gdf = pacific_plates.to_crs('EPSG:3857')

# Sample some boundary points
boundary_geom = boundaries_gdf.geometry.unary_union
plate_geom = plate_gdf.geometry.unary_union

# Get points along boundary
def sample_points_on_line(line, num_points=100):
    distances = [i/num_points for i in range(num_points)]
    return [line.interpolate(d, normalized=True) for d in distances]

sample_pts = sample_points_on_line(boundary_geom, 100)

# Verify most boundary points are near plate edge
# (some may be outside, some inside - this is expected for plate boundaries)
```

## Common Operations

### Flatten MultiPart to Single Collection
```python
# Get all individual parts
all_parts = list(boundary_geom.geoms)  # For MultiLineString
print(f"Total boundary segments: {len(all_parts)}")

# Recreate as single geometry (useful for visualization)
from shapely.geometry import LineString
if len(all_parts) > 1:
    flat_line = LineString([pt for line in all_parts for pt in line.coords])
```

### Measure Boundary Lengths
```python
# Total length of all boundary segments
if hasattr(boundary_geom, 'length'):
    total_length = boundary_geom.length
    print(f"Total boundary length: {total_length / 1000:.0f} km")
```

## Important Notes
- `.unary_union` automatically handles combining multiple geometries
- Distance calculations with MultiLineString return distance to nearest segment
- Point-in-polygon tests work correctly with MultiPolygon
- Shapely 2.0+ has improved performance for multipart operations
