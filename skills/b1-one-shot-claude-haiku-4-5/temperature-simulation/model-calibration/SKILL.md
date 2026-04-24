---
name: model-calibration
description: Calculating RMSE metrics and parameter calibration for lake model validation
---

# Model Calibration Skill

## Overview
Model calibration involves adjusting parameters to minimize differences between simulations and observations. RMSE (Root Mean Squared Error) is a standard metric for measuring model performance.

## RMSE Calculation

### Basic Formula
```
RMSE = sqrt(mean((simulated - observed)^2))
```

### Implementation

```python
import numpy as np
import pandas as pd

def calculate_rmse(simulated, observed):
    """Calculate RMSE between matched pairs"""
    if len(simulated) == 0:
        return np.nan
    residuals = simulated - observed
    rmse = np.sqrt(np.mean(residuals**2))
    return rmse

def calculate_metrics(sim_temps, obs_temps, depths=None, dates=None):
    """
    Calculate multiple RMSE metrics

    Parameters:
    - sim_temps: matched simulated temperatures
    - obs_temps: matched observed temperatures
    - depths: depth of each match (for deep water filtering)
    - dates: datetime of each match (for seasonal filtering)

    Returns:
    - overall_rmse: RMSE of all matched pairs
    - annual_deep_rmse: RMSE of pairs at depths >= 13m
    - summer_deep_rmse: RMSE of summer (Jun-Sep) pairs at depths >= 13m
    """

    overall_rmse = calculate_rmse(sim_temps, obs_temps)

    # Annual deep water (depths >= 13m)
    if depths is not None:
        deep_mask = np.array(depths) >= 13
        annual_deep_rmse = calculate_rmse(
            sim_temps[deep_mask],
            obs_temps[deep_mask]
        )
    else:
        annual_deep_rmse = np.nan

    # Summer deep water (Jun-Sep, depths >= 13m)
    if dates is not None and depths is not None:
        summer_mask = (np.array([d.month for d in dates]) >= 6) & \
                     (np.array([d.month for d in dates]) <= 9)
        deep_mask = np.array(depths) >= 13
        combined_mask = summer_mask & deep_mask
        summer_deep_rmse = calculate_rmse(
            sim_temps[combined_mask],
            obs_temps[combined_mask]
        )
    else:
        summer_deep_rmse = np.nan

    return {
        'overall_rmse': overall_rmse,
        'annual_deep_rmse': annual_deep_rmse,
        'summer_deep_rmse': summer_deep_rmse
    }
```

## Matching Observations to Simulation

Critical: Use exact datetime + rounded-depth matching (no interpolation)

```python
def match_obs_to_sim(obs_df, sim_temps, sim_z, sim_dates, round_depth=1):
    """
    Match observations to simulation output

    obs_df: DataFrame with columns [datetime, depth, temp]
    sim_temps: [time, depth] array
    sim_z: depth values
    sim_dates: datetime for each time step
    round_depth: rounding for depth matching

    Returns: matched simulation temps, observed temps, and metadata
    """
    import pandas as pd

    obs_df['depth_rounded'] = (obs_df['depth'] / round_depth).round() * round_depth

    matched_sim = []
    matched_obs = []
    matched_depths = []
    matched_dates = []

    for idx, row in obs_df.iterrows():
        obs_datetime = pd.Timestamp(row['datetime'])
        obs_depth = row['depth_rounded']
        obs_temp = row['temp']

        # Find exact datetime match
        time_matches = [i for i, d in enumerate(sim_dates)
                       if d == obs_datetime]

        # Find exact depth match
        depth_matches = [i for i, z in enumerate(sim_z)
                        if z == obs_depth]

        # Need both to match
        if time_matches and depth_matches:
            t_idx = time_matches[0]
            z_idx = depth_matches[0]
            sim_temp = sim_temps[t_idx, z_idx]

            matched_sim.append(sim_temp)
            matched_obs.append(obs_temp)
            matched_depths.append(obs_depth)
            matched_dates.append(obs_datetime)

    return (np.array(matched_sim), np.array(matched_obs),
            matched_depths, matched_dates)
```

## Parameter Tuning Strategy

### 1. Sensitivity Analysis
Run model with one parameter varied at a time to identify most influential parameters.

### 2. Systematic Search
For 5 parameters with small ranges, can do grid search:
- Test 3-5 values per parameter
- Evaluate all combinations
- Select best performers

### 3. Iterative Refinement
- Start with literature values
- Adjust parameters that have largest impact on target RMSE
- Focus on worst-performing seasonal/depth bins

### 4. Constraint Checking
Always verify final parameters are within published ranges:
```python
def validate_parameters(params):
    ranges = {
        'Kw': (0.1, 0.5),
        'coef_mix_hyp': (0.3, 0.7),
        'wind_factor': (0.7, 1.3),
        'lw_factor': (0.7, 1.3),
        'ch': (0.0005, 0.002)
    }
    for param, (min_val, max_val) in ranges.items():
        if not (min_val <= params[param] <= max_val):
            raise ValueError(f"{param} out of range: {params[param]}")
    return True
```

## Evaluation Thresholds

For Lake Mendota:
- Overall RMSE < 1.60°C
- Annual deep (≥13m) RMSE < 1.55°C
- Summer deep (Jun-Sep, ≥13m) RMSE < 1.70°C

Model is successful when ALL three thresholds are met.
