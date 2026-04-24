---
name: plate-tectonics-data-processing
description: Techniques for processing tectonic plate data, specifically using the PB2002 dataset. Use this skill when filtering points within plates, identifying plate boundaries, or working with global tectonic geometries in GeoPandas.
---

# Plate Tectonics Data Processing

This skill covers the use of the PB2002 (Bird, 2003) dataset for tectonic plate analysis.

## 1. Loading PB2002 Data
The PB2002 dataset typically consists of:
- `PB2002_plates.json`: Polygons representing the extent of each tectonic plate.
- `PB2002_boundaries.json`: LineStrings representing the boundaries between plates.

### Implementation
```python
import geopandas as gpd

plates_gdf = gpd.read_file("PB2002_plates.json")
boundaries_gdf = gpd.read_file("PB2002_boundaries.json")
```

## 2. Filtering by Plate Name
The `Plate` column (or similar) in the plates dataset identifies each plate.
- **Pacific Plate**: Often identified as "PA" or "Pacific".

```python
pacific_plate = plates_gdf[plates_gdf['Plate'] == 'PA']
```

## 3. Spatial Joins and Point-in-Polygon
To find which earthquakes occurred within a specific plate:

```python
# Assuming earthquakes_gdf and plates_gdf are in the same CRS
earthquakes_in_plates = gpd.sjoin(earthquakes_gdf, plates_gdf, how="inner", predicate="within")

# Filter for a specific plate
pacific_quakes = earthquakes_in_plates[earthquakes_in_plates['Plate'] == 'PA']
```

## 4. Identifying Relevant Boundaries
Boundaries are often labeled with the names of the two plates they separate (e.g., "PA-NA" for Pacific-North America).

To get all boundaries associated with the Pacific Plate:
```python
# Search for 'PA' in the boundary name/description column
pacific_boundaries = boundaries_gdf[boundaries_gdf['Name'].str.contains('PA')]
```

## 5. Geometric Cleanup
Tectonic datasets can sometimes have minor self-intersections or gaps.
- Use `gdf.geometry = gdf.geometry.buffer(0)` to fix minor validity issues.
- Use `gdf.union_all()` to create a single geometry representing the entire plate or boundary set.
