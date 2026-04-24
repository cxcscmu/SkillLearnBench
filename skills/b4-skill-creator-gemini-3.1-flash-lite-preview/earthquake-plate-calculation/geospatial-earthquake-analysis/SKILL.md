---
name: geospatial-earthquake-analysis
description: >
  Handles loading and processing of earthquake and plate boundary data.
  Use this for reading, filtering, and joining geospatial datasets
  related to tectonics (plates, boundaries, earthquake points).
---

# Geospatial Earthquake Analysis

## Data Loading
Use `geopandas.read_file()` to load JSON datasets like `earthquakes_2024.json`, `PB2002_boundaries.json`, and `PB2002_plates.json`.

## Processing Workflow
1. Load datasets into GeoDataFrames.
2. Ensure consistent CRS (e.g., EPSG:4326 for WGS84).
3. Filter plates to identify the Pacific plate.
4. Perform spatial queries (e.g., `sjoin` or custom distance calculations) between earthquake locations and boundary features.
