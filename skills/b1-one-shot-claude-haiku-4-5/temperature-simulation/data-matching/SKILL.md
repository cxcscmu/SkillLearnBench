---
name: data-matching
description: Matching observation data to simulation output with exact datetime and depth binning
---

# Data Matching Skill

## Overview
Successfully matching observations to simulations requires careful handling of datetime and depth coordinates. The matching must use exact values with proper rounding—no interpolation or nearest-neighbor approximation.

## Observation Data Format

CSV with columns:
```
datetime,depth,temp,OXY_oxy
2009-01-21 12:00:00,0,0.1,16.3
2009-01-21 12:00:00,1,0.7,16.3
...
```

- **datetime**: ISO format timestamp
- **depth**: Measured depth in meters
- **temp**: Water temperature in °C
- **OXY_oxy**: Oxygen (not used for temperature RMSE)

## Simulation Output Characteristics

GLM output:
- **Time dimension**: Regular hourly intervals from simulation start
- **Depth dimension**: Variable number of layers based on model dynamics
- **Temperature**: Simulated at each time step and depth layer

## Exact Matching Algorithm

### Step 1: Load Observations
```python
import pandas as pd

obs_df = pd.read_csv('/root/field_temp_oxy.csv')
obs_df['datetime'] = pd.to_datetime(obs_df['datetime'])
```

### Step 2: Round Depths
Round observation depths to nearest meter (standard practice):
```python
obs_df['depth_rounded'] = obs_df['depth'].round(0)
```

### Step 3: Extract Simulation Data
```python
import netCDF4 as nc
from netCDF4 import num2date

ds = nc.Dataset('/root/output/output.nc')
temp_sim = ds.variables['temp'][:]      # [time, depth]
z_sim = ds.variables['z'][:]            # depth coordinates
time_sim = ds.variables['time'][:]      # time values

# Convert time to datetime
time_var = ds.variables['time']
dates_sim = num2date(time_sim, time_var.units)

ds.close()
```

### Step 4: Exact Matching
```python
def exact_match(obs_df, temp_sim, z_sim, dates_sim):
    """
    Match observations to simulation using exact datetime and rounded-depth

    Returns: aligned arrays of simulated temps, observed temps,
             and metadata for filtering
    """
    import numpy as np

    matched = {
        'sim_temp': [],
        'obs_temp': [],
        'depth': [],
        'datetime': [],
        'obs_idx': []
    }

    for idx, row in obs_df.iterrows():
        obs_date = row['datetime']
        obs_depth = row['depth_rounded']
        obs_temp = row['temp']

        # Find time index: exact datetime match
        time_idx = None
        for i, sim_date in enumerate(dates_sim):
            if sim_date == obs_date:
                time_idx = i
                break

        if time_idx is None:
            continue  # No exact datetime match

        # Find depth index: exact depth match
        depth_idx = None
        for j, sim_z in enumerate(z_sim):
            if np.isclose(sim_z, obs_depth, atol=0.01):
                depth_idx = j
                break

        if depth_idx is None:
            continue  # No exact depth match

        # Record match
        matched['sim_temp'].append(temp_sim[time_idx, depth_idx])
        matched['obs_temp'].append(obs_temp)
        matched['depth'].append(obs_depth)
        matched['datetime'].append(obs_date)
        matched['obs_idx'].append(idx)

    return matched
```

## Quality Checks

### Missing Matches
```python
# Check what percentage of observations were matched
total_obs = len(obs_df)
matched_count = len(matched['sim_temp'])
match_fraction = matched_count / total_obs
print(f"Matched {matched_count}/{total_obs} observations ({100*match_fraction:.1f}%)")
```

### Temporal Coverage
```python
# Check date range of matches
import pandas as pd
match_dates = pd.DataFrame(matched['datetime'])
print(f"Match date range: {match_dates.min()} to {match_dates.max()}")
```

### Depth Distribution
```python
# Check which depths are represented
import numpy as np
matched_depths = np.array(matched['depth'])
unique_depths = np.unique(matched_depths)
print(f"Matched depths: {sorted(unique_depths)}")
```

## Filtering for Metrics

After exact matching, apply semantic filters:

```python
import numpy as np

matched_sim = np.array(matched['sim_temp'])
matched_obs = np.array(matched['obs_temp'])
matched_depths = np.array(matched['depth'])
matched_dates = np.array(matched['datetime'])

# Overall RMSE: all matches
overall_mask = np.ones(len(matched_sim), dtype=bool)

# Annual deep (depths >= 13m)
annual_deep_mask = matched_depths >= 13

# Summer deep (June-Sept, depths >= 13m)
summer_mask = np.array([d.month in [6, 7, 8, 9]
                        for d in matched_dates])
summer_deep_mask = summer_mask & (matched_depths >= 13)

# Calculate RMSE for each category
from numpy import sqrt, mean
overall_rmse = sqrt(mean((matched_sim - matched_obs)**2))
annual_deep_rmse = sqrt(mean((matched_sim[annual_deep_mask] -
                              matched_obs[annual_deep_mask])**2))
summer_deep_rmse = sqrt(mean((matched_sim[summer_deep_mask] -
                              matched_obs[summer_deep_mask])**2))
```

## Common Pitfalls

1. **Rounding inconsistency**: Always round observation depths the same way
2. **Timezone issues**: Ensure times are in same timezone before comparison
3. **Nearest-neighbor fallback**: Must use exact matches only
4. **Interpolation**: Do NOT interpolate simulation to observation depths/times
