---
name: netcdf-obs-matching
description: >
  Extract simulated temperature from GLM NetCDF output and match against field
  observations for RMSE evaluation. Use this skill when computing RMSE metrics
  from GLM output.nc files matched against CSV observation data with datetime
  and depth columns. Covers exact datetime + rounded-depth merging.
---

# NetCDF Observation Matching for GLM Output

## GLM Output Structure

GLM writes `output.nc` with:
- `temp` variable: 2D array (time × depth_layer)
- `z` variable: 2D array of layer heights (elevation above lake bottom)
- `time` variable: hours since simulation start
- Lake depth from morphometry determines depth = max_elev - z

## Matching Algorithm (Exact Merge)

The correct procedure for matching observations to simulations:

1. **Load observations** from CSV with columns: `datetime`, `depth`, `temp`
2. **Round observation depths** to nearest integer meter
3. **Extract simulation profiles** at each unique datetime in observations
4. **Convert simulation elevations to depths**: `depth = crest_elev - z`
5. **Round simulation depths** to nearest integer meter
6. **Merge on exact datetime AND rounded depth** — no nearest-time matching, no interpolation
7. **Compute RMSE** = sqrt(mean((sim_temp - obs_temp)²))

## Python Implementation Pattern

```python
import netCDF4 as nc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load GLM output
ds = nc.Dataset('output/output.nc')
time_var = ds.variables['time']
base_time = nc.num2date(time_var[:], time_var.units)
temp = ds.variables['temp'][:]
z = ds.variables['z'][:]
crest_elev = 258  # From morphometry in glm3.nml

# Build simulation dataframe
records = []
for i, t in enumerate(base_time):
    dt_str = t.strftime('%Y-%m-%d %H:%M:%S')
    valid = ~temp[i,:].mask if hasattr(temp[i,:], 'mask') else np.ones(temp.shape[1], bool)
    for j in np.where(valid)[0]:
        depth = round(crest_elev - z[i, j])
        records.append({'datetime': dt_str, 'depth': int(depth), 'temp_sim': float(temp[i, j])})
sim_df = pd.DataFrame(records)

# Load observations
obs = pd.read_csv('field_temp_oxy.csv')
obs['depth'] = obs['depth'].round().astype(int)
obs.rename(columns={'temp': 'temp_obs'}, inplace=True)

# Merge on exact datetime + rounded depth
merged = pd.merge(obs[['datetime','depth','temp_obs']], sim_df, on=['datetime','depth'])

# Handle duplicate depths per timestamp (take mean of sim values)
merged = merged.groupby(['datetime','depth']).agg(
    temp_obs=('temp_obs','first'), temp_sim=('temp_sim','mean')
).reset_index()

# Compute RMSE
overall_rmse = np.sqrt(np.mean((merged['temp_sim'] - merged['temp_obs'])**2))
```

## Subset Definitions

- **Annual deep**: all matched pairs where rounded depth ≥ 13
- **Summer deep**: matched pairs where month in [6,7,8,9] AND rounded depth ≥ 13
- Summer months = June (6) through September (9)

## Output Format

Save to `metrics.json`:
```json
{
  "overall_rmse": 1.55,
  "annual_deep_rmse": 1.50,
  "summer_deep_rmse": 1.65,
  "overall_n_pairs": 1234,
  "annual_deep_n_pairs": 456,
  "summer_deep_n_pairs": 234
}
```
