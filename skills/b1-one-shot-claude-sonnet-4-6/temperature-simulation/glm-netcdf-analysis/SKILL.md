---
name: glm-netcdf-analysis
description: Extracting and analyzing GLM NetCDF output to compute RMSE against field observations using exact datetime+depth matching.
---

# GLM NetCDF Analysis Skill

## Reading GLM NetCDF Output
```python
import netCDF4 as nc
import numpy as np
import pandas as pd

ds = nc.Dataset('/root/output/output.nc')
# Key variables
time_raw = ds.variables['time'][:]       # days since some reference
temp = ds.variables['temp'][:]           # shape: (ntimes, nlayers)
z = ds.variables['z'][:]                 # layer heights (m above bottom), shape: (ntimes, nlayers)
NS = ds.variables['NS'][:]               # number of active layers per timestep

# Get time units and convert
time_units = ds.variables['time'].units  # e.g., "hours since 1900-01-01 00:00:00"
import cftime
times = nc.num2date(time_raw, time_units)
```

## Converting Heights to Depths
```python
# z is height above bottom; lake_depth converts to depth from surface
lake_depth = 25.0  # from glm3.nml init_profiles lake_depth
# depth from surface = lake_depth - height_above_bottom
depths = lake_depth - z  # array of depths for each layer, each timestep
```

## Exact Datetime + Rounded Depth Merge
```python
obs = pd.read_csv('/root/field_temp_oxy.csv', parse_dates=['datetime'])
obs['depth_round'] = obs['depth'].round(0).astype(int)

# Build simulation dataframe
sim_rows = []
for i, t in enumerate(times):
    n = int(NS[i])
    dt = pd.Timestamp(t.year, t.month, t.day, t.hour, t.minute, t.second)
    for j in range(n):
        h = float(z[i, j])
        d = lake_depth - h
        d_round = round(d)
        sim_rows.append({'datetime': dt, 'depth_round': d_round, 'sim_temp': float(temp[i, j])})

sim_df = pd.DataFrame(sim_rows)
# Keep one sim value per datetime+depth (if duplicates, take mean or last)
sim_df = sim_df.groupby(['datetime', 'depth_round'])['sim_temp'].mean().reset_index()

merged = obs.merge(sim_df, on=['datetime', 'depth_round'], how='inner')
```

## Computing RMSE Metrics
```python
import json

def rmse(df):
    return float(np.sqrt(np.mean((df['temp'] - df['sim_temp'])**2)))

overall_rmse = rmse(merged)

deep = merged[merged['depth_round'] >= 13]
annual_deep_rmse = rmse(deep)

summer_deep = deep[deep['datetime'].dt.month.isin([6, 7, 8, 9])]
summer_deep_rmse = rmse(summer_deep)

metrics = {
    'overall_rmse': overall_rmse,
    'annual_deep_rmse': annual_deep_rmse,
    'summer_deep_rmse': summer_deep_rmse,
    'overall_n_pairs': len(merged),
    'annual_deep_n_pairs': len(deep),
    'summer_deep_n_pairs': len(summer_deep)
}

with open('/root/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```
