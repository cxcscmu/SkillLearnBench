---
name: glm-observation-merge-rmse
description: How to merge GLM simulation output with field observations and compute RMSE metrics for Lake Mendota calibration. Use this when computing overall RMSE, annual deep RMSE, and summer deep RMSE from matched observation-simulation pairs.
---

## Loading Field Observations

The observation file (`/root/field_temp_oxy.csv`) typically has columns for datetime, depth, and temperature:

```python
import pandas as pd

obs_df = pd.read_csv('/root/field_temp_oxy.csv')
# Identify columns — common names: datetime, depth, temp or similar
print(obs_df.columns.tolist())
print(obs_df.head())
```

Prepare observations:
```python
# Adjust column names as needed based on actual file
# Typical columns might be: 'datetime' or 'date', 'Depth' or 'depth', 'Temp' or 'temp'
obs_df['datetime'] = pd.to_datetime(obs_df['datetime'])  # adjust column name as needed
obs_df['depth_rounded'] = obs_df['depth'].round(0).astype(int)  # round depth to nearest integer
# Rename temperature column to 'obs_temp' for clarity
obs_df = obs_df.rename(columns={'temp': 'obs_temp'})  # adjust source column name
```

## Exact Merge on datetime + rounded depth

```python
merged = pd.merge(
    obs_df[['datetime', 'depth_rounded', 'obs_temp']],
    sim_df[['datetime', 'depth_rounded', 'sim_temp']],
    on=['datetime', 'depth_rounded'],
    how='inner'
)
print(f"Total matched pairs: {len(merged)}")
```

**If zero matches**: Check datetime formats and times-of-day on both sides. See the datetime alignment warning in the extraction skill.

## Computing the Three RMSE Metrics

```python
import numpy as np

# 1. Overall RMSE
overall_rmse = np.sqrt(np.mean((merged['sim_temp'] - merged['obs_temp'])**2))

# 2. Annual deep RMSE (depths >= 13 m)
deep = merged[merged['depth_rounded'] >= 13]
annual_deep_rmse = np.sqrt(np.mean((deep['sim_temp'] - deep['obs_temp'])**2))

# 3. Summer deep RMSE (June-September, depths >= 13 m)
summer_deep = deep[deep['datetime'].dt.month.isin([6, 7, 8, 9])]
summer_deep_rmse = np.sqrt(np.mean((summer_deep['sim_temp'] - summer_deep['obs_temp'])**2))

print(f"Overall RMSE: {overall_rmse:.4f} (n={len(merged)})")
print(f"Annual deep RMSE: {annual_deep_rmse:.4f} (n={len(deep)})")
print(f"Summer deep RMSE: {summer_deep_rmse:.4f} (n={len(summer_deep)})")
```

## Saving Metrics

```python
import json

metrics = {
    'overall_rmse': round(float(overall_rmse), 4),
    'annual_deep_rmse': round(float(annual_deep_rmse), 4),
    'summer_deep_rmse': round(float(summer_deep_rmse), 4),
    'overall_n_pairs': int(len(merged)),
    'annual_deep_n_pairs': int(len(deep)),
    'summer_deep_n_pairs': int(len(summer_deep))
}
with open('/root/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
```

## Target Thresholds
- `overall_rmse < 1.60`
- `annual_deep_rmse < 1.55`
- `summer_deep_rmse < 1.70`