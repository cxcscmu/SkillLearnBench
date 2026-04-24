---
name: glm-output-extraction
description: How to extract water temperature profiles from GLM NetCDF output files (output.nc). Use this skill when you need to read GLM simulation results, extract depth and temperature arrays, and construct a dataframe of simulated temperatures at specific depths and times.
---

## GLM NetCDF Output Structure

GLM writes output to a NetCDF file (typically `output.nc`). Key variables:

### Variables and Their Shapes
- `time`: 1D array of hours since a reference time (e.g., hours since 1904-01-01 00:00:00)
- `z`: **4D array with shape `(n_times, n_layers, 1, 1)`** — the height of each layer above the lake bottom (meters)
- `temp`: **4D array with shape `(n_times, n_layers, 1, 1)`** — water temperature (°C)
- `NS`: 1D array — number of active layers at each timestep

**CRITICAL**: `z` and `temp` are 4D, NOT 2D. You must index them as `z[t_idx, layer_idx, 0, 0]` and `temp[t_idx, layer_idx, 0, 0]`, or squeeze them first: `z_squeezed = z[:, :, 0, 0]` and `temp_squeezed = temp[:, :, 0, 0]`.

### Converting GLM Time to Datetime

```python
import netCDF4 as nc
import pandas as pd

ds = nc.Dataset('/root/output/output.nc')
time_var = ds.variables['time']
# Use netCDF4's num2date, then convert to pd.Timestamp
raw_dates = nc.num2date(time_var[:], units=time_var.units)
# CRITICAL: Convert to pd.Timestamp for exact merge compatibility
sim_times = [pd.Timestamp(d.strftime('%Y-%m-%d %H:%M:%S')) for d in raw_dates]
```

### Extracting Temperature at Specific Depths

GLM layers are counted from bottom up. The actual depth from surface is computed as:
```
depth_from_surface = lake_depth - z_height_above_bottom
```

**CRITICAL**: Read `lake_depth` dynamically from the nml file, do NOT hardcode it:
```python
import re
with open('/root/glm3.nml', 'r') as f:
    nml_text = f.read()
match = re.search(r'lake_depth\s*=\s*([\d.]+)', nml_text)
lake_depth = float(match.group(1))
```

### Full Extraction to DataFrame

```python
import numpy as np
import netCDF4 as nc
import pandas as pd

ds = nc.Dataset('/root/output/output.nc')
time_var = ds.variables['time']
raw_dates = nc.num2date(time_var[:], units=time_var.units)
sim_times = [pd.Timestamp(d.strftime('%Y-%m-%d %H:%M:%S')) for d in raw_dates]

z = ds.variables['z'][:, :, 0, 0]       # squeeze to (n_times, n_layers)
temp = ds.variables['temp'][:, :, 0, 0]  # squeeze to (n_times, n_layers)
NS = ds.variables['NS'][:]

# Read lake_depth from nml
with open('/root/glm3.nml', 'r') as f:
    nml_text = f.read()
lake_depth = float(re.search(r'lake_depth\s*=\s*([\d.]+)', nml_text).group(1))

records = []
for t_idx in range(len(sim_times)):
    n_layers = int(NS[t_idx])
    for layer_idx in range(n_layers):
        depth_from_surface = lake_depth - z[t_idx, layer_idx]
        rounded_depth = round(depth_from_surface)
        records.append({
            'datetime': sim_times[t_idx],
            'depth_rounded': rounded_depth,
            'sim_temp': temp[t_idx, layer_idx]
        })

sim_df = pd.DataFrame(records)
# If multiple layers map to the same rounded depth at the same time, average them
sim_df = sim_df.groupby(['datetime', 'depth_rounded'], as_index=False)['sim_temp'].mean()
```

### Datetime Alignment Warning

GLM typically outputs at a specific time of day (often noon 12:00:00). Observations may have different times. For an **exact datetime merge**, both sides must have identical datetime values. Check both:

```python
print("Sim times sample:", sim_df['datetime'].iloc[:3].tolist())
print("Obs times sample:", obs_df['datetime'].iloc[:3].tolist())
```

If observations are date-only (00:00:00) and simulation is at noon, you may need to normalize:
```python
# Option: normalize both to date only
sim_df['datetime'] = sim_df['datetime'].dt.normalize()
obs_df['datetime'] = pd.to_datetime(obs_df['datetime']).dt.normalize()
```

Only do this if the task allows it or if exact merge otherwise yields zero pairs.