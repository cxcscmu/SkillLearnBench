---
name: load_and_preprocess_spatial_data
description: Load earthquake GeoJSON and plate boundary datasets, and ensure consistent projection for distance analysis.
---
To accurately calculate distances, both the earthquake points and the tectonic plate boundaries must be reprojected into an equal-area projected coordinate system (e.g., EPSG:6933 for global equal-area) to ensure distance measurements are in meters.

1. Load `earthquakes_2024.json` into a GeoDataFrame, setting the geometry from coordinates and EPSG:4326.
2. Load `PB2002_boundaries.json` and `PB2002_plates.json`.
3. Filter `PB2002_boundaries` to select only those segments that border the "Pacific" plate (checking the `LeftPlate` and `RightPlate` attributes).
4. Project all GeoDataFrames to a consistent meters-based CRS.
5. Use `unary_union` on the filtered boundary GeoSeries to create a single geometry object representing the entire Pacific plate boundary perimeter.