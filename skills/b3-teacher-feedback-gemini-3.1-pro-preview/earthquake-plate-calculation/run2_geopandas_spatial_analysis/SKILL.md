---
name: geopandas_spatial_analysis
description: How to perform spatial filtering (point-in-polygon), combine line boundaries, and accurately calculate metric distances between points and boundaries using GeoPandas.
---

# GeoPandas Spatial Analysis: Filtering and Distance Calculations

When analyzing geospatial data, you often need to find points within a specific area (spatial filtering) and determine how far those points are from a specific feature (distance calculation). 

## 1. Spatial Filtering (Point-in-Polygon)

To find which points (e.g., earthquakes) fall within a specific polygon (e.g., a tectonic plate), use spatial joins or the `.within()` / `.intersects()` methods.

```python
import geopandas as gpd

# Load data
points_gdf = gpd.read_file("points.json")
polygons_gdf = gpd.read_file("polygons.json")

# Filter for the target polygon (e.g., 'Pacific' plate)
target_polygon = polygons_gdf[polygons_gdf['PlateName'] == 'Pacific']

# Find points strictly within the target polygon
points_within = gpd.sjoin(points_gdf, target_polygon, predicate='within')
```

## 2. Combining Boundaries for Distance Calculation

When your boundary data (LineStrings/MultiLineStrings) consists of multiple segments, you must combine them into a single unified geometry before measuring distances. Otherwise, distance calculations will not work as expected across the entire boundary.

```python
# Load boundary data
boundaries_gdf = gpd.read_file("boundaries.json")

# Filter boundary segments associated with the target plate if necessary
target_boundaries = boundaries_gdf[boundaries_gdf['plate_attribute'] == 'Pacific']

# Combine all relevant boundary segments into a single geometry
combined_boundary = target_boundaries.geometry.unary_union
```

## 3. Coordinate System Projection (Crucial Step)

**Warning:** Never calculate distances directly in geographic coordinate systems like `EPSG:4326` (WGS 84). The result will be in degrees, which is completely inaccurate for distance measurements. 

Before calculating distances, you **must** project both your points and your combined boundary geometry to a metric coordinate reference system (CRS). For global, flat distance calculations, `EPSG:4087` (WGS 84 / World Equidistant Cylindrical) is a standard choice.

```python
# Project the points to EPSG:4087
points_metric = points_within.to_crs(epsg=4087)

# Project the boundary GeoDataFrame to EPSG:4087 BEFORE applying unary_union, 
# OR project the points first, then use a CRS-aware Series for the boundary.
target_boundaries_metric = target_boundaries.to_crs(epsg=4087)
combined_boundary_metric = target_boundaries_metric.geometry.unary_union
```

## 4. Distance Calculation and Unit Conversion

Once both the points and the combined boundary are in a metric CRS, use the `.distance()` method to find the shortest distance from each point to the boundary.

Metric projections calculate distance in **meters**. To obtain kilometers, divide the resulting values by 1000.

```python
# Calculate distances (in meters)
points_within['distance_m'] = points_metric.geometry.distance(combined_boundary_metric)

# Convert to kilometers
points_within['distance_km'] = points_within['distance_m'] / 1000

# Optional: Round to 2 decimal places
points_within['distance_km'] = points_within['distance_km'].round(2)
```