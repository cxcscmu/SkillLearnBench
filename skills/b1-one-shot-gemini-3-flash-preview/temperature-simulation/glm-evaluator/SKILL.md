---
name: glm-evaluator
description: A skill to process GLM NetCDF output and calculate specific RMSE metrics by merging with field observations.
---

# GLM Evaluator

## Overview
Evaluating GLM requires comparing simulated temperature profiles with field observations. The comparison must be done at the same `datetime` and `depth`.

## Key Steps
1.  **Read Observations:** Load observation data (e.g., from `field_temp_oxy.csv`). Convert timestamps to datetime and round depths if required.
2.  **Read GLM Output:** Use `netCDF4` to read `output.nc`.
3.  **Extract Data:**
    - `time`: Simulation time steps.
    - `z`: Vertical coordinates of layers (usually variable over time).
    - `temp`: Temperature in each layer.
4.  **Merge Data:** For each observation point (time, depth), find the corresponding simulated temperature.
    - **Rounding:** The task requires matching by rounded depth.
5.  **Calculate RMSE:**
    - `RMSE = sqrt(mean((obs - sim)^2))`

## Python Example (NetCDF to DataFrame)
```python
import pandas as pd
import numpy as np
from netCDF4 import Dataset

def get_simulated_temp(nc_path, obs_df):
    nc = Dataset(nc_path)
    time = nc.variables['time'][:]
    # time units like "hours since 2009-01-01 00:00:00"
    base_time = pd.to_datetime("2009-01-01 00:00:00")
    sim_times = base_time + pd.to_timedelta(time, unit='H')
    
    # temp is usually [time, depth]
    # z is usually [time, depth]
    # ... extraction logic ...
```

## Considerations
- **Depth Matching:** GLM uses a lagrangian layer approach, meaning layer thicknesses can change. To get temperature at a specific depth, find the layer that contains that depth or use the layer closest to the target depth.
- **RMSE Filters:** Apply seasonal (e.g., summer months June-Sept) or depth-based filters (e.g., depth >= 13m) before calculation.
- **Reporting:** Export final metrics to a JSON file as required by the task.
