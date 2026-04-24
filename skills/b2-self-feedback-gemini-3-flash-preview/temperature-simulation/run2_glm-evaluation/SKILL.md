---
name: run2_glm-evaluation
description: Robust GLM evaluation methods for deep and summer water temperatures.
---

# Robust GLM Output Evaluation

Evaluation must precisely match observation times and rounded depths.

## Depth Handling in GLM Output

In GLM, layers are defined by their height `z` from the bottom. To find the temperature at a specific depth from the surface:
1.  **Surface Height:** $H_{surface}(t) = z(t, \text{num\_layers}-1)$
2.  **Layer Depths:** $D_{i}(t) = H_{surface}(t) - z_{i}(t)$
3.  **Interpolation:** Since GLM uses discrete layers, linear interpolation at the target depth $d$ within the $(D_i, T_i)$ profile provides a more accurate value than choosing the nearest layer.

## RMSE Calculation Requirements

According to task rules:
- **Overall RMSE:** Filter for available pairs across all times and depths.
- **Annual Deep RMSE:** Filter for rounded depths $\ge 13$ m.
- **Summer Deep RMSE:** Filter for months June (6) to September (9) AND rounded depths $\ge 13$ m.

Example Python snippets using `netCDF4` and `pandas`:
```python
import netCDF4
import pandas as pd
import numpy as np

def get_sim_temp_profile(nc_vars, time_idx):
    num_layers = int(nc_vars['NS'][time_idx])
    z = nc_vars['z'][time_idx, :num_layers]
    temp = nc_vars['temp'][time_idx, :num_layers]
    
    # Ensure 1D arrays and handle masking
    if hasattr(z, 'compressed'): z = z.compressed()
    if hasattr(temp, 'compressed'): temp = temp.compressed()
    
    surface_height = z[-1]
    depths = surface_height - z
    return depths, temp

def match_obs_sim(obs_csv, nc_path):
    # Load and preprocess
    obs = pd.read_csv(obs_csv)
    obs['datetime'] = pd.to_datetime(obs['datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
    obs['rounded_depth'] = obs['depth'].round().astype(int)
    
    # ... logic to apply interpolation for each observation row ...
```
Avoid nearest-time matching or alternative depth binning.
