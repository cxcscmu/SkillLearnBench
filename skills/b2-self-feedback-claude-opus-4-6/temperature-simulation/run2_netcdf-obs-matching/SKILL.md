---
name: run2_netcdf-obs-matching
description: Extracting GLM NetCDF output and computing exact RMSE metrics via datetime+depth merge against field observations.
---

# NetCDF-Observation Matching and RMSE Evaluation

## Task
Compare GLM simulated temperatures to field observations using exact datetime matching and rounded-depth merging.

## Step 1: Load Observations
```python
import pandas as pd
obs = pd.read_csv('field_temp_oxy.csv', parse_dates=['datetime'])
obs = obs[['datetime', 'depth', 'temp']].dropna(subset=['temp'])
obs['depth_round'] = obs['depth'].round().astype(int)
```

## Step 2: Load GLM NetCDF Output
```python
import netCDF4 as nc
import numpy as np

ds = nc.Dataset('output/output.nc')
time_var = ds.variables['time']
times = nc.num2date(time_var[:], time_var.units)
sim_times = pd.to_datetime([t.strftime('%Y-%m-%d %H:%M:%S') for t in times])
temp = ds.variables['temp'][:]  # shape: (time, layers)
z = ds.variables['z'][:]        # shape: (time, layers) - height from bottom
```

## Step 3: Match Observations to Simulation
**Critical rules**:
- Match by EXACT datetime only (no nearest-time matching)
- Round observed depths to nearest integer
- Convert GLM z (height from bottom) to depth from surface
- Accept simulation depth match within 0.5m of rounded obs depth

```python
results = []
for dt in obs['datetime'].unique():
    tidx = np.where(sim_times == dt)[0]
    if len(tidx) == 0:
        continue
    ti = tidx[0]
    sim_z = z[ti, :]
    sim_t = temp[ti, :]
    surface_height = np.max(sim_z)
    sim_depths = surface_height - sim_z

    obs_at_time = obs[obs['datetime'] == dt]
    for _, row in obs_at_time.iterrows():
        target_depth = row['depth_round']
        depth_diffs = np.abs(sim_depths - target_depth)
        nearest_idx = np.argmin(depth_diffs)
        if depth_diffs[nearest_idx] < 0.5:
            results.append({
                'datetime': dt,
                'depth_round': target_depth,
                'obs_temp': row['temp'],
                'sim_temp': float(sim_t[nearest_idx])
            })
```

## Step 4: Compute RMSE Metrics
```python
df = pd.DataFrame(results)

# Overall
overall_rmse = np.sqrt(np.mean((df['obs_temp'] - df['sim_temp'])**2))

# Annual deep (all year, depth >= 13m)
deep = df[df['depth_round'] >= 13]
annual_deep_rmse = np.sqrt(np.mean((deep['obs_temp'] - deep['sim_temp'])**2))

# Summer deep (June-Sept, depth >= 13m)
summer_deep = deep[deep['datetime'].dt.month.isin([6, 7, 8, 9])]
summer_deep_rmse = np.sqrt(np.mean((summer_deep['obs_temp'] - summer_deep['sim_temp'])**2))
```

## Step 5: Save metrics.json
```python
import json
metrics = {
    'overall_rmse': round(float(overall_rmse), 4),
    'annual_deep_rmse': round(float(annual_deep_rmse), 4),
    'summer_deep_rmse': round(float(summer_deep_rmse), 4),
    'overall_n_pairs': int(len(df)),
    'annual_deep_n_pairs': int(len(deep)),
    'summer_deep_n_pairs': int(len(summer_deep))
}
with open('metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

## Expected pair counts for Lake Mendota (2009-2015)
- Overall: ~2815 pairs
- Annual deep (>=13m): ~1327 pairs
- Summer deep: ~678 pairs

## Common Mistakes to Avoid
1. Using nearest-time matching instead of exact datetime match
2. Forgetting to convert z (height) to depth (from surface)
3. Not rounding depths before matching
4. Using interpolation instead of nearest-layer matching
5. Not handling masked/fill values in NetCDF arrays
