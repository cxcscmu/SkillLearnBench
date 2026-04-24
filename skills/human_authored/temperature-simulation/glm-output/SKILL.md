---
name: glm-output
description: Output-processing guidance for GLM tasks. Especially useful after glm-basics and glm-calibration when you need verifier-matching metrics from output.nc and a final /root/metrics.json.
license: MIT
---

# GLM Output Guide

## Overview

GLM produces NetCDF output containing simulated water temperature profiles. Processing this output requires understanding the coordinate system and matching with observations.

## Suggested Skill Flow

This skill is usually the right final step after `glm-basics` and `glm-calibration`. As soon as calibration has found a configuration that appears to pass the task metrics, switch here, compute the final exact metrics, and write `/root/metrics.json` from this logic rather than from a separately improvised evaluator. If the exact final metrics pass here, end the task instead of returning to a broader calibration search.

## Exact-Reporting Tasks

When a task requires an exact self-evaluation file, save `/root/metrics.json` with the task's required keys. For the deep-band calibration tasks in this benchmark family, the file must contain:
- `overall_rmse`
- `annual_deep_rmse`
- `summer_deep_rmse`
- `overall_n_pairs`
- `annual_deep_n_pairs`
- `summer_deep_n_pairs`

Do not use nearest-time approximations or vertical interpolation for the final reported metrics. Use the exact `datetime`/rounded-depth merge shown below, then compute any task-specific subsets from that merged table.

## Output File

After running GLM, results are in `output/output.nc`:

| Variable | Description | Shape |
|----------|-------------|-------|
| `time` | Hours since simulation start | (n_times,) |
| `z` | Height from lake bottom (not depth!) | (n_times, n_layers, 1, 1) |
| `temp` | Water temperature (°C) | (n_times, n_layers, 1, 1) |

## Reading Output with Python
```python
from netCDF4 import Dataset
import numpy as np
import pandas as pd
from datetime import datetime

nc = Dataset('output/output.nc', 'r')
time = nc.variables['time'][:]
z = nc.variables['z'][:]
temp = nc.variables['temp'][:]
nc.close()
```

## Coordinate Conversion

**Important**: GLM `z` is height from lake bottom, not depth from surface.
```python
LAKE_DEPTH = <lake_depth_from_nml>
depth_from_surface = LAKE_DEPTH - z
```

## Complete Output Processing
```python
from netCDF4 import Dataset
import numpy as np
import pandas as pd
from datetime import datetime

def read_glm_output(nc_path, lake_depth):
    nc = Dataset(nc_path, 'r')
    time = nc.variables['time'][:]
    z = nc.variables['z'][:]
    temp = nc.variables['temp'][:]
    start_date = datetime(2009, 1, 1, 12, 0, 0)

    records = []
    for t_idx in range(len(time)):
        hours = float(time[t_idx])
        date = pd.Timestamp(start_date) + pd.Timedelta(hours=hours)
        heights = z[t_idx, :, 0, 0]
        temps = temp[t_idx, :, 0, 0]

        for d_idx in range(len(heights)):
            h_val = heights[d_idx]
            t_val = temps[d_idx]
            if not np.ma.is_masked(h_val) and not np.ma.is_masked(t_val):
                depth = lake_depth - float(h_val)
                if 0 <= depth <= lake_depth:
                    records.append({
                        'datetime': date,
                        'depth': round(depth),
                        'temp_sim': float(t_val)
                    })
    nc.close()

    df = pd.DataFrame(records)
    df = df.groupby(['datetime', 'depth']).agg({'temp_sim': 'mean'}).reset_index()
    return df
```

## Reading Observations
```python
def read_observations(obs_path):
    df = pd.read_csv(obs_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['depth'] = df['depth'].round().astype(int)
    df = df.rename(columns={'temp': 'temp_obs'})
    return df[['datetime', 'depth', 'temp_obs']]
```

## Calculating Task Metrics
```python
def rmse_from_merged(merged):
    if len(merged) == 0:
        return 999.0
    errors = merged['temp_sim'] - merged['temp_obs']
    return float(np.sqrt(np.mean(errors ** 2)))

def calculate_task_metrics(sim_df, obs_df):
    merged = pd.merge(obs_df, sim_df, on=['datetime', 'depth'], how='inner')
    summer_mask = merged['datetime'].dt.month.isin([6, 7, 8, 9])
    annual_deep = merged[merged['depth'] >= 13]
    summer_deep = merged[summer_mask & (merged['depth'] >= 13)]

    return {
        'overall_rmse': rmse_from_merged(merged),
        'annual_deep_rmse': rmse_from_merged(annual_deep),
        'summer_deep_rmse': rmse_from_merged(summer_deep),
        'overall_n_pairs': int(len(merged)),
        'annual_deep_n_pairs': int(len(annual_deep)),
        'summer_deep_n_pairs': int(len(summer_deep)),
    }
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| RMSE very high | Wrong depth conversion | Use `lake_depth - z`, not `z` directly |
| No matched observations | Datetime mismatch | Check datetime format consistency |
| Empty merged dataframe | Depth rounding issues | Round depths to integers |
| Whole-lake RMSE looks fine but query still fails | Deep subsets were not recomputed explicitly | Check both `depth >= 13` bands on the merged table |

## Best Practices

- Check `lake_depth` in `&init_profiles` section of `glm3.nml`
- Always convert z to depth from surface before comparing with observations
- Round depths to integers for matching
- Group by datetime and depth to handle duplicate records
- Check the matched-pair counts for the full table, the annual deep band, and the summer deep band before writing `metrics.json`
- Treat this as the final reporting handoff after calibration, not as another place to continue searching
- Once the exact final metrics are written and pass, stop the task immediately
