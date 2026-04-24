---
name: run2_glm-rmse-metrics
description: Exact RMSE metric computation for GLM lake temperature evaluation - verified matching procedure with correct threshold values.
---

# GLM RMSE Metrics Skill (Improved)

## Metric Definitions
- **overall_rmse**: RMSE over ALL matched pairs
- **annual_deep_rmse**: RMSE for `rounded_depth >= 13`, all months
- **summer_deep_rmse**: RMSE for `rounded_depth >= 13` AND `month in [6,7,8,9]`

## RMSE Thresholds (Lake Mendota)
- `overall_rmse < 1.60`
- `annual_deep_rmse < 1.55`
- `summer_deep_rmse < 1.70`

## Complete Evaluation Script

```python
import netCDF4 as nc
import numpy as np
import pandas as pd
import json

def evaluate_and_save(nc_path='/root/output/output.nc',
                       obs_path='/root/field_temp_oxy.csv',
                       metrics_path='/root/metrics.json'):
    # Build matched pairs
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
            rdepth = int(round(z_surf - z_layer))
            records.append({'datetime': sim_times[i], 'rounded_depth': rdepth,
                             'sim_temp': float(temp[i, j, 0, 0])})

    sim_df = pd.DataFrame(records)
    sim_df = sim_df.groupby(['datetime', 'rounded_depth'])['sim_temp'].mean().reset_index()
    merged = obs.merge(sim_df, on=['datetime', 'rounded_depth'])
    ds.close()

    # Compute metrics
    residuals = merged['sim_temp'] - merged['temp']
    overall_rmse = float(np.sqrt(np.mean(residuals**2)))

    deep = merged[merged['rounded_depth'] >= 13]
    annual_deep_rmse = float(np.sqrt(np.mean((deep['sim_temp'] - deep['temp'])**2)))

    summer_deep = deep[deep['datetime'].dt.month.isin([6, 7, 8, 9])]
    summer_deep_rmse = float(np.sqrt(np.mean((summer_deep['sim_temp'] - summer_deep['temp'])**2)))

    metrics = {
        'overall_rmse': overall_rmse,
        'annual_deep_rmse': annual_deep_rmse,
        'summer_deep_rmse': summer_deep_rmse,
        'overall_n_pairs': int(len(merged)),
        'annual_deep_n_pairs': int(len(deep)),
        'summer_deep_n_pairs': int(len(summer_deep))
    }

    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    return metrics
```

## Verified Results (Lake Mendota, best parameters)
```json
{
  "overall_rmse": 1.3662,
  "annual_deep_rmse": 1.3468,
  "summer_deep_rmse": 1.4713,
  "overall_n_pairs": 2819,
  "annual_deep_n_pairs": 1327,
  "summer_deep_n_pairs": 678
}
```

## Common Pitfalls
- Do NOT use nearest-time matching or interpolation
- Do NOT use alternative depth binning (only round to nearest integer)
- Merge must be exact on both `datetime` AND `rounded_depth`
- Use `.groupby().mean()` on sim_df before merging to handle duplicate rounded depths
