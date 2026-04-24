---
name: earthquake-distance-calc
description: >
  Calculate geodesic distances between earthquake points and plate boundaries using
  GeoPandas projections. Use this skill when computing distances in kilometers between
  geographic points and linestring/polygon boundaries, especially for finding the
  earthquake furthest from a plate boundary. Triggers on: distance to boundary,
  furthest earthquake, geodesic distance, plate boundary distance.
---

# Earthquake Distance Calculation

## Purpose

Compute the distance (in km) from each earthquake point to the nearest point on a
plate boundary, using a proper equal-distance map projection for accuracy.

## Projection Strategy

Geographic coordinates (EPSG:4326) use degrees, not meters. To compute distances in
kilometers, project to an appropriate CRS.

### For Pacific-plate-scale analysis

Use an **Azimuthal Equidistant** projection centered on the Pacific Ocean. This
preserves distances from the center point, making it suitable for distance calculations
across the vast Pacific plate.

```python
import pyproj

# Center on the Pacific Ocean
aeqd_crs = pyproj.CRS.from_proj4(
    "+proj=aeqd +lat_0=0 +lon_0=-160 +datum=WGS84 +units=m"
)
```

Alternatively, for global-scale operations you can use a World Equidistant Cylindrical
projection (EPSG:4087), but Azimuthal Equidistant centered on the area of interest
is more accurate for distance calculations.

### Projection workflow
```python
# Project all geometries to the chosen CRS
quakes_proj = quakes_in_plate.to_crs(aeqd_crs)
boundaries_proj = pa_boundaries.to_crs(aeqd_crs)
```

## Distance Calculation

### Approach: nearest distance from point to multi-linestring boundary

1. Union all boundary segments into a single MultiLineString geometry
2. For each earthquake point, compute `point.distance(boundary_union)`
3. This gives the minimum distance in meters (divide by 1000 for km)

```python
from shapely.ops import unary_union

boundary_union = unary_union(boundaries_proj.geometry)

quakes_proj["distance_m"] = quakes_proj.geometry.distance(boundary_union)
quakes_proj["distance_km"] = quakes_proj["distance_m"] / 1000.0
```

### Find the furthest earthquake
```python
idx_max = quakes_proj["distance_km"].idxmax()
furthest = quakes_proj.loc[idx_max]
```

## Output Format

When writing results to JSON:
- Convert Unix millisecond timestamps to ISO 8601: `datetime.utcfromtimestamp(ts/1000).strftime("%Y-%m-%dT%H:%M:%SZ")`
- Round distance_km to 2 decimal places
- Include: id, place, time, magnitude, latitude, longitude, distance_km

## Performance Notes

- `unary_union` on boundary segments is the key optimization — avoids N×M distance calculations
- For 1500 earthquakes × ~50 boundary segments, this runs in seconds
- The `.distance()` method on projected geometries returns Euclidean distance in the projected CRS units (meters for AEQD)
