---
name: calculate_max_distance_to_boundary
description: Compute the distance from each Pacific plate earthquake to the unified plate boundary.
---
After unifying the boundary geometry, perform the distance analysis:

1. Calculate the distance from each point in the earthquake GeoDataFrame to the `unary_union` geometry of the Pacific plate boundaries.
2. Ensure the calculation is performed using the projected GeoDataFrames to yield results in meters.
3. Convert the resulting distance from meters to kilometers (divide by 1000).
4. Filter for points located "within" the Pacific plate (using a spatial join or polygon containment check with the `PB2002_plates.json` polygon for the Pacific plate).
5. Identify the record with the maximum `distance_km` value and round the result to 2 decimal places.