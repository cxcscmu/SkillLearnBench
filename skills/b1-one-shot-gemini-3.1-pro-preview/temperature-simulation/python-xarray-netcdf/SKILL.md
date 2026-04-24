---
name: python-xarray-netcdf
description: Reading and processing NetCDF outputs from models like GLM using Python and xarray.
---

# python-xarray-netcdf

This skill covers how to load NetCDF (.nc) files, typically output by environmental models like GLM, and process their multi-dimensional variables using xarray.

## Requirements
- `xarray`
- `netCDF4`

## Example Usage
```python
import xarray as xr

# Load the NetCDF file
ds = xr.open_dataset('output.nc')

# Access a specific variable, e.g., 'temp'
temp_data = ds['temp']

# Select a specific depth or time if indexed
# ds.sel(time='2010-01-01')

ds.close()
```