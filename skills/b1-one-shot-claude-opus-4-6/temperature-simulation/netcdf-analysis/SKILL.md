---
name: netcdf-analysis
description: Reading and analyzing GLM NetCDF output with Python netCDF4 and pandas for RMSE evaluation.
---

# NetCDF Analysis for GLM Output

## Reading GLM Output
```python
import netCDF4 as nc
import numpy as np
import pandas as pd

ds = nc.Dataset('output/output.nc')
temp = ds.variables['temp'][:]  # masked array [time, layers]
z = ds.variables['z'][:]        # height above bottom [time, layers]
time_var = ds.variables['time']
times = nc.num2date(time_var[:], time_var.units)
```

## Extracting Temperature at Specific Depths
GLM uses variable layer heights. For each timestep:
```python
lake_depth = 25  # from morphometry (crest_elev - min(H))
for t in range(len(times)):
    valid = ~temp[t].mask if hasattr(temp[t], 'mask') else np.ones(temp.shape[1], bool)
    depths_from_surface = lake_depth - z[t, valid]
    temps = temp[t, valid]
    # Interpolate to desired depth
```

## RMSE Calculation
```python
# Merge on exact datetime and rounded depth
# rmse = sqrt(mean((obs - sim) ** 2))
```

## Key Notes
- GLM z is height from lake bottom; depth = lake_depth - z
- Round depths to nearest integer for matching
- Use exact datetime matching (no nearest-time)
