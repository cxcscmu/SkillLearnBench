---
name: netcdf-processing
description: Reading, processing, and analyzing NetCDF output from lake simulation models
---

# NetCDF Processing Skill

## Overview
NetCDF (Network Common Data Form) is a self-describing binary format commonly used for scientific data. GLM outputs simulation results in NetCDF format containing temperature, mixing, and other variables across time and depth.

## Installation & Setup

### Required Libraries
```bash
pip install netCDF4 numpy pandas
```

### Basic Reading

```python
import netCDF4 as nc
import pandas as pd

# Open NetCDF file
ds = nc.Dataset('/path/to/output.nc', 'r')

# List variables
print(ds.variables.keys())

# List dimensions
print(ds.dimensions.keys())

# Read a variable
temp = ds.variables['temp'][:]  # Returns numpy array
time = ds.variables['time'][:]
z = ds.variables['z'][:]  # depth dimension
```

## GLM-Specific Output Structure

Typical GLM NetCDF output contains:

- **time**: Time index (often hours since simulation start)
- **z**: Depth levels (m)
- **temp**: Temperature (°C) with shape [time, depth]
- Other variables: salinity, mixing rates, etc.

## Data Extraction Example

```python
import netCDF4 as nc
import pandas as pd

def extract_glm_temperatures(nc_file, start_date='2009-01-01'):
    """Extract temperature time series from GLM NetCDF output"""
    ds = nc.Dataset(nc_file)

    # Get data
    temp = ds.variables['temp'][:]  # [time, depth]
    z = ds.variables['z'][:]        # depth
    time = ds.variables['time'][:]  # time since reference

    # Get reference date from time variable
    time_var = ds.variables['time']
    units = time_var.units  # e.g., "seconds since 2009-01-01 00:00:00"

    # Convert time to datetime
    from netCDF4 import num2date
    dates = num2date(time, units)

    ds.close()

    return temp, z, dates
```

## Key Operations

### Subsetting Data
```python
# Get temperature at specific depth
depth_idx = 5  # 5m depth
temp_5m = temp[:, depth_idx]

# Get temperature at specific time
time_idx = 100  # Time step 100
temp_at_time = temp[time_idx, :]
```

### Time Operations
```python
from netCDF4 import num2date
from datetime import datetime

# Convert netCDF time to datetime
dates = num2date(time_values, time_units)

# Filter to specific date range
start = datetime(2009, 1, 1)
end = datetime(2015, 12, 31)
mask = (dates >= start) & (dates <= end)
filtered_temp = temp[mask, :]
```

### Handling Dimensions
```python
# Interpolate to standard depths
from scipy.interpolate import interp1d

# Get simulated temps at exact depths
standard_depths = [0, 5, 10, 15, 20]
interpolator = interp1d(z, temp[time_idx, :], kind='linear')
interp_temps = interpolator(standard_depths)
```

## Common Patterns

1. **Read entire temperature field**: Straightforward numpy array indexing
2. **Match observations**: Use time and depth to find nearest simulation values
3. **Compare profiles**: Extract vertical temperature profile at specific times
4. **Time series analysis**: Extract temperature at single depth over time

## Performance Notes

- Reading entire large NetCDF files into memory is usually fine for lake models
- Use slicing (e.g., `temp[:, idx]`) to avoid unnecessary I/O
- Close datasets after use: `ds.close()`
