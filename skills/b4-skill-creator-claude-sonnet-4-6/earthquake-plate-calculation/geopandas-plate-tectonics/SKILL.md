---
name: geopandas-plate-tectonics
description: >
  How to load, filter, and work with tectonic plate boundary and polygon data
  using GeoPandas. Use this skill whenever the user mentions plate boundaries,
  tectonic plates, PB2002 data, or needs to identify which tectonic plate a
  point belongs to, or extract boundaries for a specific plate like Pacific (PA),
  African (AF), North American (NA), etc.
---

# GeoPandas Plate Tectonics

## Data Format

PB2002 data comes in two files:
- `PB2002_plates.json`: Polygon features for each plate. Key property: `Code` (e.g. `"PA"` for Pacific).
- `PB2002_boundaries.json`: LineString features for boundaries. Key property: `Name` (e.g. `"PA-NA"` for Pacific-NorthAmerica).

## Loading Plate Data

```python
import geopandas as gpd

plates = gpd.read_file("PB2002_plates.json")
boundaries = gpd.read_file("PB2002_boundaries.json")

# Filter for a specific plate polygon
pacific_plate = plates[plates["Code"] == "PA"]

# Filter boundaries involving the Pacific plate
pa_boundaries = boundaries[boundaries["Name"].str.contains("PA")]
```

## Projecting for Distance Calculations

Always project to an equal-area or equidistant CRS before computing distances.
For global or Pacific-wide analysis, use World Azimuthal Equidistant (EPSG:4088)
or a custom Azimuthal Equidistant centered on the Pacific:

```python
# Option 1: World Azimuthal Equidistant (meters)
CRS_PROJ = "EPSG:4088"

# Option 2: Custom projection centered on Pacific centroid
import pyproj
pacific_centroid = pacific_plate.to_crs("EPSG:4326").geometry.centroid.iloc[0]
CRS_PROJ = f"+proj=aeqd +lat_0={pacific_centroid.y} +lon_0={pacific_centroid.x} +units=m"

plates_proj = plates.to_crs(CRS_PROJ)
boundaries_proj = boundaries.to_crs(CRS_PROJ)
```

## Identifying Points Inside a Plate

```python
from shapely.geometry import Point

# Create GeoDataFrame of points
points_gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
    crs="EPSG:4326"
)

# Spatial join to find points within Pacific plate
pacific_proj = pacific_plate.to_crs(CRS_PROJ)
points_proj = points_gdf.to_crs(CRS_PROJ)

points_in_pacific = gpd.sjoin(points_proj, pacific_proj[["geometry"]], how="inner", predicate="within")
```

## Computing Distance to Boundary

```python
from shapely.ops import unary_union

# Merge all Pacific boundary segments into one geometry
pa_boundary_union = unary_union(pa_boundaries_proj.geometry)

# Compute distance (in meters if projected to meters CRS)
points_in_pacific["dist_m"] = points_in_pacific.geometry.apply(
    lambda pt: pt.distance(pa_boundary_union)
)
points_in_pacific["dist_km"] = points_in_pacific["dist_m"] / 1000
```

## Notes

- Always work in projected CRS (not EPSG:4326) for distance calculations.
- The Pacific plate (PA) is very large and spans the antimeridian — watch for
  geometry wrapping issues. If geometries look wrong, try dissolving or
  using `unary_union` carefully.
- `unary_union` on all PA boundary segments gives the complete boundary as a
  single MultiLineString, which is efficient for distance queries.
