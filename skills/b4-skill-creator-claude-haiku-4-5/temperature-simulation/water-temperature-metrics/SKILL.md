---
name: water-temperature-metrics
description: Computing RMSE (Root Mean Squared Error) and other metrics for water temperature model validation. Use this skill whenever you need to match simulated temperatures with field observations, compute RMSE by depth categories, calculate annual/seasonal subsets, or prepare model evaluation metrics. Essential for lake model calibration and validation workflows.
---

# Water Temperature Metrics for Lake Models

## Overview

Validating lake temperature models requires matching simulated output with field observations, then computing error metrics. The critical challenge is properly aligning observations and simulations in time and depth.

## Exact Datetime + Rounded Depth Matching

For GLM calibration, use **exact datetime matching with rounded depth**:

1. **Load field observations**: DataFrame with `datetime`, `depth`, `temp`
2. **Load simulated output**: NetCDF with temperature at times and depths
3. **Round depths** in both datasets to nearest integer meter (e.g., 0.4m → 0, 1.6m → 2)
4. **Merge** on exact datetime AND rounded depth
5. **Compute errors** from matched pairs only

### Why Exact Datetime?
- Simulations output at fixed intervals (e.g., daily snapshots)
- Observations often fall exactly on simulation output times
- Exact matching avoids interpolation bias

### Why Rounded Depth?
- Simulated layers are adaptive and vary over time
- Rounding to integer meters groups observations near same layer
- More robust than interpolation to exact observation depth

## RMSE Computation

### Overall RMSE
```
overall_rmse = sqrt(mean((sim - obs)^2))
```
Computed across all matched pairs.

### Annual Deep RMSE
- Subset: All matched pairs at rounded depth ≥ 13 m
- Includes all times (Jan-Dec)
- Captures deeper mixing errors

### Summer Deep RMSE
- Subset: Matched pairs in June-September (months 6-9)
- Rounded depth ≥ 13 m
- Captures summer stratification errors in deep water

## Implementation Strategy

### Step 1: Load Data
```python
import pandas as pd
import xarray as xr
import numpy as np

# Load observations
obs_df = pd.read_csv('field_temp_oxy.csv', parse_dates=['datetime'])

# Load simulation
ds = xr.open_dataset('output/output.nc')
sim_time = pd.to_datetime(ds.time.values)
sim_z = ds.z.values  # depth dimension
sim_temp = ds.temp.values  # (time, depth) array
```

### Step 2: Round Depths
```python
obs_df['depth_rounded'] = np.round(obs_df['depth']).astype(int)
```

### Step 3: Extract Simulated Temps at Observation Times
For each observation datetime, find matching simulation time. If exact match exists:
```python
# For each row in obs_df:
# 1. Find sim time matching obs datetime exactly
# 2. At that time, interpolate simulated depth profile to round(obs_depth)
# 3. Extract temperature
```

### Step 4: Merge and Compute RMSE
```python
# Create matched pairs
merged = obs_with_sim[obs_with_sim['sim_temp'].notna()]

# Overall RMSE
overall_rmse = np.sqrt(((merged['sim_temp'] - merged['temp'])**2).mean())

# Annual deep (depth >= 13m)
annual_deep = merged[merged['depth_rounded'] >= 13]
annual_deep_rmse = np.sqrt(((annual_deep['sim_temp'] - annual_deep['temp'])**2).mean())

# Summer deep (months 6-9, depth >= 13m)
merged['month'] = merged['datetime'].dt.month
summer_deep = merged[(merged['month'].isin([6,7,8,9])) & (merged['depth_rounded'] >= 13)]
summer_deep_rmse = np.sqrt(((summer_deep['sim_temp'] - summer_deep['temp'])**2).mean())
```

### Step 5: Count Matched Pairs
Track `n_pairs` for each category to ensure sufficient sample sizes.

## Depth Interpolation at Simulation Times

When simulated output has adaptive layers:

1. At each simulation time, simulated temps are at specific depths (z-coordinates)
2. For observation at depth d_obs: interpolate temperature to d_obs using linear interpolation
3. Use rounded depth d_rounded for matching
4. Report temp at d_obs for RMSE

Alternative: Use nearest simulated layer depth to d_rounded. Simpler but less accurate.

## JSON Output Format

Save metrics to file:
```json
{
  "overall_rmse": 1.45,
  "annual_deep_rmse": 1.50,
  "summer_deep_rmse": 1.65,
  "overall_n_pairs": 3200,
  "annual_deep_n_pairs": 1100,
  "summer_deep_n_pairs": 450
}
```

## Thresholds for GLM Lake Mendota Calibration

- overall_rmse < 1.60 °C
- annual_deep_rmse < 1.55 °C
- summer_deep_rmse < 1.70 °C

These thresholds are based on typical lake model accuracy benchmarks and field measurement precision.
