---
name: python-pandas-merge
description: Matching observations with simulated data using exact datetime and rounded depth merges in pandas.
---

# python-pandas-merge

This skill is useful when aligning observational data, such as field temperature sensors, with multi-dimensional simulated outputs from models based on exact time and rounded spatial coordinates (like depth).

## Requirements
- `pandas`
- `numpy`

## Pattern Example
```python
import pandas as pd
import numpy as np

# Suppose `obs` is a DataFrame with 'datetime' (datetime64), 'depth' (float), and 'temp_obs' (float)
# Round depth to match expected simulation bins
obs['depth_rounded'] = obs['depth'].round()

# Suppose `sim` is a DataFrame flattened from xarray, containing 'datetime', 'depth_rounded', and 'temp_sim'
# Perform exact merge
merged = pd.merge(obs, sim, on=['datetime', 'depth_rounded'], how='inner')

# Calculate Root Mean Square Error (RMSE)
rmse = np.sqrt(((merged['temp_sim'] - merged['temp_obs']) ** 2).mean())
```