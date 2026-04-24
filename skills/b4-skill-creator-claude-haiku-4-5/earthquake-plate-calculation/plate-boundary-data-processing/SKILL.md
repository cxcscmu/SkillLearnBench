---
name: plate-boundary-data-processing
description: Work with tectonic plate boundary datasets (PB2002 format) to identify plate regions, extract specific plate boundaries, and perform spatial filtering. Load plate boundary and plate polygon data, identify specific plates like the Pacific plate, and extract relevant boundaries. Use this skill when parsing plate tectonics datasets, identifying plate regions from boundary lines, or filtering spatial data by plate membership.
---

# Plate Boundary Data Processing

## PB2002 Dataset Overview

The PB2002 (Plate Boundaries 2002) dataset contains:
- **Boundaries file**: LineStrings representing plate boundaries (ridges, trenches, transforms)
- **Plates file**: Polygon features representing individual plate boundaries and characteristics

### Data Structure

**PB2002_boundaries.json**
- Contains LineString geometries for each plate boundary segment
- Properties typically include:
  - `type`: Boundary type (ridge, trench, transform, etc.)
  - `plate1`, `plate2`: Names of adjacent plates
  - `age`, `length`: Metadata about boundary

**PB2002_plates.json**
- Contains Polygon geometries for complete plates
- Properties typically include:
  - `plate_name`: Name of the plate (e.g., "Pacific")
  - `area`: Plate area
  - Other identifying characteristics

## Loading and Exploring Data

### Basic Loading

```python
import geopandas as gpd
import json

# Load plate boundaries
boundaries_gdf = gpd.read_file('/root/PB2002_boundaries.json')
print(f"Loaded {len(boundaries_gdf)} boundary segments")
print(boundaries_gdf.head())
print(boundaries_gdf.columns)
print(boundaries_gdf.crs)

# Load plate definitions
plates_gdf = gpd.read_file('/root/PB2002_plates.json')
print(f"Loaded {len(plates_gdf)} plates")
print(plates_gdf['plate_name'].unique())
```

### Understanding Data Types

```python
# Check geometry types
print(boundaries_gdf.geometry.type.value_counts())
# Should mostly show LineString

print(plates_gdf.geometry.type.value_counts())
# Should show Polygon
```

## Identifying the Pacific Plate

### Method 1: Extract from Plates GeoDataFrame

```python
# Find Pacific plate polygon
pacific_plate = plates_gdf[plates_gdf['plate_name'] == 'Pacific']

if len(pacific_plate) > 0:
    print(f"Found Pacific plate")
    print(f"Area: {pacific_plate.iloc[0].geometry.area}")
    pacific_boundary_polygon = pacific_plate.iloc[0].geometry
else:
    print("Pacific plate not found - check plate_name values")
    print(plates_gdf['plate_name'].unique())
```

### Method 2: Extract Boundaries Belonging to Pacific

```python
# If using plate1/plate2 columns, filter boundaries of the Pacific plate
pacific_boundaries = boundaries_gdf[
    (boundaries_gdf['plate1'] == 'Pacific') |
    (boundaries_gdf['plate2'] == 'Pacific')
]

print(f"Found {len(pacific_boundaries)} Pacific plate boundary segments")
```

## Filtering Earthquakes Within a Plate

### Using Spatial Join

```python
# Earthquake GeoDataFrame already loaded in WGS84
earthquakes_in_pacific = gpd.sjoin(
    earthquakes_gdf,
    pacific_plate,
    how='inner',
    predicate='within'
)

print(f"Found {len(earthquakes_in_pacific)} earthquakes within Pacific plate")
```

### Manual Point-in-Polygon

```python
# Alternative if spatial join has issues
pacific_polygon = pacific_plate.iloc[0].geometry

earthquakes_in_pacific = earthquakes_gdf[
    earthquakes_gdf.geometry.within(pacific_polygon)
]
```

## Extracting Boundaries for Distance Calculation

### Get All Pacific Plate Boundary Lines

```python
# Collect all boundary LineStrings for the Pacific plate
pacific_boundary_lines = boundaries_gdf[
    (boundaries_gdf['plate1'] == 'Pacific') |
    (boundaries_gdf['plate2'] == 'Pacific')
]['geometry'].tolist()

print(f"Pacific plate has {len(pacific_boundary_lines)} boundary segments")
```

### Important Consideration: Boundary vs Plate Polygon

- **Boundaries GeoDataFrame**: Individual line segments that make up the plate edge
- **Plates GeoDataFrame**: Complete polygon representing the full plate area
- For distance calculation, use boundary lines (not the polygon boundary)
- The polygon exists but distance should be to actual plate boundary data

## Handling Data Issues

### Case Sensitivity

Plate names may vary in case:

```python
# Make case-insensitive if needed
plates_gdf['plate_name_lower'] = plates_gdf['plate_name'].str.lower()
pacific = plates_gdf[plates_gdf['plate_name_lower'] == 'pacific']
```

### Missing or Inconsistent Naming

```python
# Explore actual values
print(plates_gdf.columns.tolist())
print(plates_gdf['plate_name'].value_counts())

# Check if 'Pacific' exists in plate1 or plate2 columns
if 'plate1' in boundaries_gdf.columns:
    print(boundaries_gdf['plate1'].unique())
    print(boundaries_gdf['plate2'].unique())
```

### CRS Harmonization

```python
# Ensure consistent CRS before spatial operations
if boundaries_gdf.crs != plates_gdf.crs:
    boundaries_gdf = boundaries_gdf.to_crs(plates_gdf.crs)

if earthquakes_gdf.crs != plates_gdf.crs:
    earthquakes_gdf = earthquakes_gdf.to_crs(plates_gdf.crs)
```

## Common Workflow

```python
# 1. Load all data
boundaries_gdf = gpd.read_file('/root/PB2002_boundaries.json')
plates_gdf = gpd.read_file('/root/PB2002_plates.json')
earthquakes_gdf = load_earthquake_data()  # Your function

# 2. Harmonize CRS
for gdf in [boundaries_gdf, plates_gdf, earthquakes_gdf]:
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')

# 3. Identify Pacific plate
pacific_plate = plates_gdf[plates_gdf['plate_name'] == 'Pacific']
pacific_boundaries = boundaries_gdf[
    (boundaries_gdf['plate1'] == 'Pacific') |
    (boundaries_gdf['plate2'] == 'Pacific')
]

# 4. Filter earthquakes
earthquakes_pacific = gpd.sjoin(
    earthquakes_gdf,
    pacific_plate,
    how='inner',
    predicate='within'
)

# 5. Calculate distances and find maximum
# (See geospatial-earthquake-analysis skill)
```

## Verification Checklist

- ✓ Loaded boundaries and plates with same CRS
- ✓ Located Pacific plate in plates_gdf
- ✓ Identified Pacific boundaries in boundaries_gdf
- ✓ Found earthquakes within Pacific polygon
- ✓ Boundary lines are LineStrings, not just points
- ✓ Earthquake count reasonable (not 0 or unreasonably high)
