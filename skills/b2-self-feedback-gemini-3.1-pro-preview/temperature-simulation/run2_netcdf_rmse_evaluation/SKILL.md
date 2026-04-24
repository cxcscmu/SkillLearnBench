---
name: run2_netcdf_rmse_evaluation
description: Instructions for safely parsing GLM NetCDF output with netCDF4 and correctly executing an exact datetime + rounded-depth merge.
---

# GLM Evaluation (Improved)

This skill describes how to correctly open and extract depth and temperature from GLM `output.nc` without coordinate conflict errors, and how to compute exact match RMSE against field data.

## Loading and Interpolating
Using `xarray` to open `output.nc` will likely result in a `MissingDimensionsError` because GLM defines a `z` variable with a dimension that shares its name. 
Instead, rely on the `netCDF4` library natively.

```python
import netCDF4 as nc
import pandas as pd
import numpy as np

# Load simulation
ds = nc.Dataset('output.nc')
times = nc.num2date(ds.variables['time'][:], ds.variables['time'].units)
datetimes = pd.to_datetime([t.strftime('%Y-%m-%d %H:%M:%S') for t in times])

z = ds.variables['z'][:, :, 0, 0]
temp = ds.variables['temp'][:, :, 0, 0]
ns = ds.variables['NS'][:] # Number of simulated layers at each time step
```

## Depth Extraction
GLM saves `z` as distance from the lake bottom. The distance from the surface down (which field data typically uses) is dynamically derived using `surface_z - z`:
```python
depths = np.array([z[i, ns[i]-1] - z[i, :ns[i]] if ns[i] > 0 else [] for i in range(len(ns))])
```

## Creating Paired Dataset
To perform the *exact `datetime` and rounded-depth merge*:
1. Construct a flat `sim_df` of valid datetime, rounded depth, and simulated temperature pairs.
2. Format `obs` datetime to match, and generate its `depth_rounded`.
3. Perform an explicit merge `pd.merge(obs, sim_df, on=['datetime', 'depth_rounded'])`.
Avoid "alternative depth binning" (like `groupby().mean()`) unless explicitly instructed; GLM layers matching the same rounded integer will create multiple paired rows.
