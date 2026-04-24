---
name: compute_metrics
description: Calculates RMSE between simulated and observed data using exact datetime matching and integer depth binning based on simulation start date 2009-01-01.
---

When calculating metrics, convert the model time (relative days) to `datetime` objects starting from 2009-01-01. For each `(datetime, rounded_depth)` bin, if multiple simulated values exist, calculate their mean before matching with observations.

```python
import pandas as pd
import numpy as np
import xarray as xr

def calculate_metrics(nc_path, obs_csv, lake_depth):
    ds = xr.open_dataset(nc_path)
    obs = pd.read_csv(obs_csv, parse_dates=['datetime'])
    
    # Convert GLM time to datetime
    start_date = pd.Timestamp('2009-01-01')
    ds['datetime'] = start_date + pd.to_timedelta(ds.time.values, unit='D')
    
    # Process layers: depth = lake_depth - z
    # Group by datetime and round(depth)
    # Calculate mean for bins with multiple simulated layers
    # Perform inner merge with obs on (datetime, rounded_depth)
    # Filter for annual_deep (depth >= 13) and summer_deep (month in [6,7,8,9] & depth >= 13)
```