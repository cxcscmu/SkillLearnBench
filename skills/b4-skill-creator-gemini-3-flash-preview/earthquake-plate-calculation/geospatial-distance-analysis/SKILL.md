---
name: geospatial-distance-analysis
description: Procedures for performing precise distance calculations between points and geometries using GeoPandas. Use this skill when calculating distances in kilometers, reprojecting GeoDataFrames, or finding the nearest features in a geospatial dataset.
---

# Geospatial Distance Analysis

This skill provides instructions for calculating distances between geospatial features accurately using GeoPandas and appropriate coordinate reference systems (CRS).

## 1. Projecting for Distance Calculations

Standard WGS84 (EPSG:4326) coordinates (latitude/longitude) are not suitable for direct distance calculations in meters or kilometers because degrees of longitude vary in length.

### Choosing a Projection
- **Equidistant Projections**: Use for accurate distance measurements.
- **World Equidistant Cylindrical (EPSG:4087)**: Good for global datasets.
- **Local UTM Zones**: Best for high precision in specific local areas.
- **Custom Azimuthal Equidistant**: Best for distances from a single point of interest.

### Implementation in GeoPandas
```python
import geopandas as gpd

# Load data in WGS84
gdf = gpd.read_file("data.json")
gdf.crs = "EPSG:4326"

# Reproject to a metric CRS (e.g., World Equidistant Cylindrical)
gdf_metric = gdf.to_crs("EPSG:4087")
```

## 2. Calculating Point-to-Geometry Distances

To find the distance from a point to the nearest part of a boundary (line or polygon):

```python
# Assuming 'points_gdf' and 'boundary_gdf' are in the same metric CRS
# 'boundary' should be a single geometry (e.g., the union of all boundary segments)
boundary_geom = boundary_gdf.union_all()

# Calculate distance for each point
points_gdf['distance_meters'] = points_gdf.geometry.distance(boundary_geom)
points_gdf['distance_km'] = points_gdf['distance_meters'] / 1000.0
```

## 3. Handling Antimeridian Issues

When working with global data (like the Pacific Plate), geometries may cross the Antimeridian (180° longitude). 

- Use `geopandas.tools.wrap_longitude` or ensure your CRS handles the wrap-around correctly.
- For calculations across the Pacific, consider a CRS centered on 180° longitude if necessary, though EPSG:4087 usually handles the coordinate range -180 to 180.

## 4. Performance Tips
- Use `.union_all()` (or `.unary_union` in older versions) to combine many boundary segments into a single geometry before calculating distances. This is much faster than iterating.
- For very large datasets, use spatial indexes (`gdf.sindex`).
