---
name: run2_netcdf-data-handling
description: This skill covers using the netCDF4 library for reading simulation outputs in Lake Mendota GLM modelling.
---
# NetCDF4 Handling Skill

## Reading NetCDF
Use `netCDF4.Dataset` to open files.
- Time conversion: Use `num2date(ds['time'][:], units=ds['time'].units, calendar='standard')`.
- Coordinate flattening: Extract variables, handle dimensions. Use masked arrays if necessary (`np.ma.is_masked`).

## Data Merging
When merging with observations, ensure types match (e.g., datetime64, rounded depths). Use pandas DataFrames for easy merging and analysis.
