---
name: glm-lake-simulation
description: How to run the General Lake Model (GLM3) for lake temperature simulation, calibrate parameters in glm3.nml, read NetCDF output with Python, and compute RMSE metrics against field observations. Use this skill whenever the user mentions GLM, lake temperature simulation, glm3.nml, or wants to calibrate lake model parameters.
---

# GLM Lake Simulation Skill

## Overview

GLM (General Lake Model) simulates vertical water temperature stratification in lakes. The executable is `/usr/local/bin/glm` and must be run from the directory containing `glm3.nml`.

## Running GLM

```bash
cd /root && glm
```

GLM reads `glm3.nml` in the current directory and writes output to the path specified by `out_dir`/`out_fn` in the `&output` namelist block.

## Key Configuration File: glm3.nml

### Calibration Parameters (allowed to modify)

| Parameter | Namelist Block | Typical Range | Effect |
|-----------|---------------|---------------|--------|
| `Kw` | `&light` | 0.1–0.5 | Light extinction coefficient; higher = more surface heating |
| `coef_mix_hyp` | `&mixing` | 0.3–0.7 | Hypolimnetic mixing; higher = more deep mixing |
| `wind_factor` | `&meteorology` | 0.7–1.3 | Wind speed scaling; higher = more mixing |
| `lw_factor` | `&meteorology` | 0.7–1.3 | Longwave radiation scaling; higher = more surface heat |
| `ch` | `&meteorology` | 0.0005–0.002 | Sensible heat transfer coefficient |

### Do NOT modify
- `sw_factor`, `cd`, `ce`
- `the_depths`, `the_temps`, `the_sals` (initialization profile)
- All other settings

## Reading GLM NetCDF Output

```python
import netCDF4 as nc
import numpy as np
import pandas as pd

ds = nc.Dataset('/root/output/output.nc')

# Key variables
time_var = ds.variables['time']       # hours since simulation start
temp_var = ds.variables['temp']       # shape: (time, depth_layer)
z_var = ds.variables['z']            # elevation of each layer (m above datum)
NS_var = ds.variables['NS']          # number of active layers at each timestep

# Convert time to datetime
from netCDF4 import num2date
times = num2date(time_var[:], time_var.units)

# Extract temperature at a specific depth (meters from surface)
# Lake surface elevation varies; z gives absolute elevation
# lake_depth = crest_elev - z gives depth from surface
```

## Computing RMSE Against Observations

```python
import pandas as pd
import numpy as np
import netCDF4 as nc
from netCDF4 import num2date

def extract_glm_temps(nc_path):
    """Extract GLM temperatures as DataFrame with datetime, depth_from_surface, temp."""
    ds = nc.Dataset(nc_path)
    times = num2date(ds.variables['time'][:], ds.variables['time'].units)
    temp = ds.variables['temp'][:]      # (time, layer)
    z = ds.variables['z'][:]            # (time, layer) elevation
    NS = ds.variables['NS'][:]          # active layers per timestep

    records = []
    for i, t in enumerate(times):
        n = int(NS[i])
        dt = pd.Timestamp(t.year, t.month, t.day, t.hour, t.minute, t.second)
        for j in range(n):
            elev = float(z[i, j])
            tmp = float(temp[i, j])
            records.append({'datetime': dt, 'elev': elev, 'temp_sim': tmp})
    return pd.DataFrame(records)

def compute_rmse_metrics(obs_path, nc_path, crest_elev=258.0):
    """Compute overall, annual_deep, and summer_deep RMSE."""
    # Load observations
    obs = pd.read_csv(obs_path, parse_dates=['datetime'])
    obs['depth_round'] = obs['depth'].round()

    # Extract simulated temps
    sim_df = extract_glm_temps(nc_path)
    sim_df['depth_from_surface'] = crest_elev - sim_df['elev']
    sim_df['depth_round'] = sim_df['depth_from_surface'].round()

    # Daily average simulated temp per depth
    sim_df['date'] = sim_df['datetime'].dt.date
    sim_daily = sim_df.groupby(['date', 'depth_round'])['temp_sim'].mean().reset_index()
    sim_daily['datetime'] = pd.to_datetime(sim_daily['date'])

    # Match obs datetime to date
    obs['date'] = obs['datetime'].dt.date

    # Merge on exact datetime (date) + rounded depth
    merged = obs.merge(sim_daily, on=['date', 'depth_round'], how='inner')

    overall_rmse = np.sqrt(((merged['temp'] - merged['temp_sim'])**2).mean())

    deep = merged[merged['depth_round'] >= 13]
    annual_deep_rmse = np.sqrt(((deep['temp'] - deep['temp_sim'])**2).mean())

    summer_deep = deep[deep['datetime'].dt.month.isin([6, 7, 8, 9])]
    summer_deep_rmse = np.sqrt(((summer_deep['temp'] - summer_deep['temp_sim'])**2).mean())

    return {
        'overall_rmse': float(overall_rmse),
        'annual_deep_rmse': float(annual_deep_rmse),
        'summer_deep_rmse': float(summer_deep_rmse),
        'overall_n_pairs': int(len(merged)),
        'annual_deep_n_pairs': int(len(deep)),
        'summer_deep_n_pairs': int(len(summer_deep))
    }
```

## Calibration Strategy

1. Start with default parameters and run baseline
2. Adjust `Kw` first — it most strongly affects thermocline depth and deep-water temps
   - Lower Kw → deeper light penetration → cooler surface, warmer hypolimnion
3. Adjust `coef_mix_hyp` to control deep mixing
   - Higher → more vertical mixing → warmer deep waters
4. Adjust `wind_factor` to control surface mixing
5. Fine-tune `lw_factor` and `ch` for surface heat balance

## Workflow

```bash
# 1. Edit glm3.nml parameters
# 2. Run GLM
cd /root && glm

# 3. Evaluate metrics with Python
python3 /root/evaluate.py

# 4. Repeat until RMSE thresholds are met:
#    overall_rmse < 1.60
#    annual_deep_rmse < 1.55
#    summer_deep_rmse < 1.70
```
