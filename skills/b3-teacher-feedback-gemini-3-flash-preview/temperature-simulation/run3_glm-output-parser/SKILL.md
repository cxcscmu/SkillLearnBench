---
name: glm-output-parser
description: Extract and transform water temperature data from GLM NetCDF files, handling dynamic layering, masked arrays, and temporal alignment.
---

1. **Time Alignment**:
   - Extract the `time` variable from the NetCDF file.
   - Use the `units` attribute (e.g., "hours since 2009-01-01 00:00:00") and the `&glm_setup` start time to convert numeric time values into standard `datetime` objects.
   - Ensure the resolution (e.g., daily noon) is consistent for comparison with observations.

2. **Dynamic Depth Calculation**:
   - For every timestep, retrieve the vertical height array `z` and the temperature array `temp`.
   - Identify valid (non-masked) layers.
   - Calculate the surface height ($H_{max}$) for that specific timestep as the maximum value of `z`.
   - Calculate the depth for each layer: $Depth = H_{max} - z$.

3. **Handling Masked Arrays**:
   - GLM output often contains masked or fill values for inactive layers. Explicitly filter out these values from both `z` and `temp` before processing to avoid inclusion of invalid data in means or comparisons.

4. **Data Structuring**:
   - Store processed data in a format suitable for merging (e.g., a DataFrame) containing columns for `datetime`, `depth`, and `temp`.