---
name: spatial-analysis-validation
description: Validate spatial analysis results to ensure correctness of point-in-polygon and distance calculations.
---

# Spatial Analysis Validation

## Installation
```bash
pip install geopandas shapely pandas
```

## Overview
Spatial analysis results must be validated before trusting them. This includes verifying point-in-polygon assignments, distance calculations, and identifying outliers.

## Validation Checklist

### 1. Point-in-Polygon Validation
```python
# Verify earthquakes are truly within plate
sample_earthquakes = earthquakes_within.head(10)

for idx, quake in sample_earthquakes.iterrows():
    is_within = pacific_polygon.contains(quake.geometry)
    coords = (quake.geometry.y, quake.geometry.x)
    print(f"{quake['place']}: {coords} -> within={is_within}")

    # Double-check with different method
    is_within_alt = quake.geometry.within(pacific_polygon)
    assert is_within == is_within_alt, "Inconsistent results"
```

### 2. Distance Validation
```python
# Verify distance calculations make sense
import math

# Manual distance check using Haversine formula (approximate)
def haversine_distance(lat1, lon1, lat2, lon2):
    """Approximate distance in km"""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Compare with projected distance
for idx, (calc_dist, quake) in enumerate(zip(distances_km, earthquakes_within.itertuples())):
    if idx % 20 == 0:  # Sample every 20
        # Get nearest point on boundary
        boundary_geom_wgs84 = pacific_boundaries.geometry.unary_union
        nearest_point = nearest_points(quake.geometry, boundary_geom_wgs84)[1]

        haversine_dist = haversine_distance(
            quake.geometry.y, quake.geometry.x,
            nearest_point.y, nearest_point.x
        )

        # Projected distance should be close to haversine for small distances
        diff_percent = abs(calc_dist - haversine_dist) / max(calc_dist, haversine_dist) * 100
        print(f"Quake {idx}: Projected={calc_dist:.1f}km, Haversine={haversine_dist:.1f}km, Diff={diff_percent:.1f}%")
```

### 3. Outlier Detection
```python
# Find potentially problematic results
import numpy as np

distances_array = np.array(distances_km)

# Statistical analysis
mean_dist = distances_array.mean()
std_dist = distances_array.std()
max_dist = distances_array.max()

print(f"Distance statistics:")
print(f"  Mean: {mean_dist:.1f} km")
print(f"  Std Dev: {std_dist:.1f} km")
print(f"  Max: {max_dist:.1f} km")
print(f"  Max is {(max_dist - mean_dist) / std_dist:.1f} std devs from mean")

# Verify max is reasonable (not impossible)
# For Pacific plate, distances should be within ~10,000 km
if max_dist > 12000:
    print("WARNING: Maximum distance seems unusually large")
```

### 4. Geographic Reasonableness
```python
# Verify result location makes sense
farthest_quake_coords = (farthest_quake.geometry.y, farthest_quake.geometry.x)
print(f"Farthest earthquake location: {farthest_quake['place']}")
print(f"Coordinates: {farthest_quake_coords}")

# Is this location actually in the Pacific?
expected_pacific_regions = [
    ("Hawaii", (-20, -150)),  # lat range, lon range
    ("Central Pacific", (-10, 160)),
    ("Northwest Pacific", (40, 140)),
]

# Manual check - does location make sense as Pacific earthquake?
# Pacific earthquakes typically occur at boundaries near trenches or spreading centers
```

### 5. Boundary Coverage Verification
```python
# Ensure we have all plate boundaries
print(f"Pacific boundary segments: {len(pacific_boundaries)}")
print(f"Total boundary geometry length: {boundary_geom.length / 1000:.0f} km")

# Check if boundary segments form continuous line
from shapely.geometry import MultiLineString
if isinstance(boundary_geom, MultiLineString):
    print(f"Number of boundary segments: {len(list(boundary_geom.geoms))}")

    # Analyze segment connectivity
    segments = list(boundary_geom.geoms)
    for i, seg in enumerate(segments[:5]):  # Check first 5
        print(f"  Segment {i}: {len(seg.coords)} points, "
              f"length={seg.length/1000:.0f}km")
```

### 6. Compare Different Projections
```python
# Verify result is consistent across projections
distance_3857 = distance_in_epsg_3857
distance_equal = distance_in_equal_area_projection

relative_diff = abs(distance_3857 - distance_equal) / distance_3857
print(f"Projection comparison: {relative_diff*100:.2f}% difference")

if relative_diff > 0.05:  # >5% difference is concerning
    print("WARNING: Significant difference between projections")
    print("Investigate which is more accurate for this region")
```

## Output Validation Report
```python
print("\n=== VALIDATION REPORT ===")
print(f"✓ Found {len(earthquakes_within)} earthquakes within Pacific plate")
print(f"✓ Pacific plate boundaries: {len(pacific_boundaries)} segments")
print(f"✓ Farthest earthquake: {farthest_quake['id']}")
print(f"✓ Distance: {max_distance:.2f} km")
print(f"✓ Result location: {farthest_quake['place']}")
print("✓ All validations passed")
```
