---
name: geopandas-coordinate-projections
description: Master coordinate systems and projections in GeoPandas for accurate spatial calculations. Handle WGS84 to projected coordinate system conversions, select appropriate projections for regions, and perform distance/area calculations correctly. Use this skill when working with latitude/longitude data that needs to be converted to metric distances, or when performing spatial calculations that require specific coordinate systems.
---

# GeoPandas Coordinate Projections and Transformations

## Understanding Coordinate Systems

### Geographic vs Projected Coordinates

**Geographic Coordinates (Latitude/Longitude)**
- WGS84 (EPSG:4326) is the standard for earthquake and plate boundary data
- Degrees, not meters - distances between degrees vary by latitude
- Cannot be used directly for distance calculations
- Must be projected to a planar system for accurate metric distances

**Projected Coordinates**
- Flat 2D coordinate systems with units in meters or feet
- Preserve either distance, area, direction, or shape (no projection preserves all)
- Must match your analysis goal

### Projection Types for Plate Tectonics

| Projection | Purpose | Use Case |
|-----------|---------|----------|
| Azimuthal Equidistant | Preserves distances from center point | Distance from a specific location |
| Equal Area (Mollweide, Albers) | Preserves area relationships | Accurate area measurements |
| Mercator | Conformal (angle preserving) | Navigation, but distorts poles |
| UTM | Zone-based, good local accuracy | Local/regional analysis |

## Workflow

### 1. Check and Set CRS

```python
import geopandas as gpd

# Check current CRS
print(gdf.crs)  # Should print 'EPSG:4326' for WGS84

# Ensure WGS84 if needed
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
```

### 2. Select Appropriate Projection

For Pacific plate analysis, use an azimuthal equidistant projection centered on the Pacific:

```python
# Pacific-centered azimuthal equidistant (approximately)
# Center: ~180°E (or -180°), 0°N (Equator)
pacific_projection = 'EPSG:3832'  # Azimuthal Equidistant from Pacific
# Or use custom projection string

# Alternative: Use pyproj directly for custom projections
from pyproj import CRS
custom_crs = CRS.from_proj4('+proj=aeqd +lat_0=0 +lon_0=180 +x_0=0 +y_0=0 +datum=WGS84 +units=m')
```

### 3. Transform for Distance Calculations

```python
# Transform to projected CRS
gdf_projected = gdf.to_crs(pacific_projection)

# Now distances are in meters
# Calculate distance (example)
for idx, row in gdf_projected.iterrows():
    dist_meters = row.geometry.distance(other_geometry)
    dist_km = dist_meters / 1000
```

### 4. Transform Back to WGS84 for Output

```python
# If you need to output in geographic coordinates
gdf_result = gdf_projected.to_crs('EPSG:4326')
```

## Common Patterns

### Calculate Distance Between Points

```python
from shapely.geometry import Point

# Points in WGS84
p1 = Point(139.7, 35.6)  # Tokyo
p2 = Point(-118.2, 34.0)  # Los Angeles

# Create GeoDataFrame
gdf = gpd.GeoDataFrame([{'geometry': p1}, {'geometry': p2}], crs='EPSG:4326')

# Project and calculate
gdf_proj = gdf.to_crs('EPSG:3832')
distance_meters = gdf_proj.geometry[0].distance(gdf_proj.geometry[1])
distance_km = distance_meters / 1000
```

### Calculate Minimum Distance from Points to LineStrings

```python
# For each point in earthquakes_gdf, find minimum distance to any boundary line
def min_distance_to_features(point_geom, feature_geometries):
    """Calculate minimum distance from a point to any feature."""
    min_dist = float('inf')
    for feature in feature_geometries:
        dist = point_geom.distance(feature)
        min_dist = min(min_dist, dist)
    return min_dist

# Apply across all earthquakes
distances = []
for idx, row in earthquakes_projected.iterrows():
    dist = min_distance_to_features(row.geometry, boundaries_projected.geometry)
    distances.append(dist / 1000)  # Convert to km
```

## Projection Reference

### Common EPSG Codes for Ocean/Global Analysis

- **EPSG:3832**: Azimuthal Equidistant (Pacific-centered)
- **EPSG:4326**: WGS84 (lat/lon, DO NOT use for distances)
- **EPSG:3857**: Web Mercator (DO NOT use for scientific analysis)
- **EPSG:54034**: Equal Earth (global, area-preserving)

### Custom Projection String

```python
# Azimuthal Equidistant centered on specific location
proj_string = '+proj=aeqd +lon_0=180 +lat_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m'
```

## Troubleshooting

**Problem**: Distances come out as tiny decimals (e.g., 0.0001)
- **Cause**: Calculating in geographic coordinates (degrees)
- **Solution**: Project to a metric CRS before distance calculation

**Problem**: All distances are the same/equal area distortion
- **Cause**: Using wrong projection type
- **Solution**: Use azimuthal equidistant for distance preservation

**Problem**: CRS mismatch error
- **Cause**: Trying to combine layers with different CRS
- **Solution**: Use `.to_crs()` to harmonize CRS before spatial operations
