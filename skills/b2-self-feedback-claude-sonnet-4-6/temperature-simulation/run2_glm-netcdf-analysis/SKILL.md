---
name: run2_glm-netcdf-analysis
description: How to read GLM3 NetCDF output (shape/dimension details verified) and extract simulated temperature profiles matched to field observations.
---

# GLM NetCDF Analysis Skill (Improved)

## Variable Structure (Verified)
```python
import netCDF4 as nc
ds = nc.Dataset('/root/output/output.nc')
# Key variables:
# - time: shape (n_timesteps,), units = "hours since YYYY-MM-DD HH:MM:SS"
# - z:    shape (n_timesteps, max_layers, 1, 1) - elevation from lake bottom (meters)
# - temp: shape (n_timesteps, max_layers, 1, 1) - temperature (°C)
# - NS:   shape (n_timesteps,) - number of active layers per timestep
```

## Depth Calculation (CRITICAL)
GLM stores `z` as **elevation from lake bottom** (not depth from surface).

```python
# For timestep i, layer j:
n = int(NS[i])  # number of active layers
z_surf = float(z[i, n-1, 0, 0])  # surface elevation above bottom
z_layer = float(z[i, j, 0, 0])   # layer elevation above bottom
depth_from_surface = z_surf - z_layer  # depth in meters from surface
```

## Building Matched Pairs

```python
import netCDF4 as nc
import numpy as np
import pandas as pd

def build_matched_pairs(nc_path, obs_path):
    obs = pd.read_csv(obs_path, parse_dates=['datetime'])
    obs['rounded_depth'] = obs['depth'].round().astype(int)

    ds = nc.Dataset(nc_path)
    time_var = ds.variables['time']
    times = nc.num2date(time_var[:], time_var.units)
    sim_times = pd.to_datetime([t.strftime('%Y-%m-%d %H:%M:%S') for t in times])

    z = ds.variables['z'][:]
    temp = ds.variables['temp'][:]
    NS = ds.variables['NS'][:]

    records = []
    for i in range(len(sim_times)):
        n = int(NS[i])
        z_surf = float(z[i, n-1, 0, 0])
        for j in range(n):
            z_layer = float(z[i, j, 0, 0])
            depth_from_surf = z_surf - z_layer
            rdepth = int(round(depth_from_surf))
            records.append({
                'datetime': sim_times[i],
                'rounded_depth': rdepth,
                'sim_temp': float(temp[i, j, 0, 0])
            })

    sim_df = pd.DataFrame(records)
    # Average if multiple layers round to same depth
    sim_df = sim_df.groupby(['datetime', 'rounded_depth'])['sim_temp'].mean().reset_index()

    # Exact datetime + rounded depth merge
    merged = obs.merge(sim_df, on=['datetime', 'rounded_depth'])
    ds.close()
    return merged
```

## Key Notes
- GLM output timestep = daily at noon (12:00:00) when `nsave=24` and `dt=3600`
- Observations also at 12:00:00, so exact datetime match works
- z dimensions have shape (n, 500, 1, 1) - note the extra singleton dims, index as `z[i, j, 0, 0]`
- Approximately 2819 matched pairs for Lake Mendota 2009-2015 dataset
