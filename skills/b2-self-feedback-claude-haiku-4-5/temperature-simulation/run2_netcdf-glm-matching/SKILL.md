---
name: run2_netcdf-glm-matching
description: Advanced matching of time-varying GLM simulation depths with observation data
---

# Time-Varying Depth Matching for GLM Netcdf

## Problem
GLM simulations output time-varying depth coordinates (z variable). The water column structure changes with time due to mixing and stratification. Naive depth matching fails because:
- Depths aren't fixed - they evolve with simulation
- Multiple simulation layers may round to the same integer depth
- Some time steps have many active layers, others have few
- Masked/NaN values need careful handling

## Solution: Temporal Matching

### Load Data with Proper Type Handling

```python
import netCDF4 as nc
import numpy as np
import pandas as pd

ds = nc.Dataset(output_file, 'r')

# Convert masked arrays to regular arrays with NaN for missing values
def safe_load(var):
    data = var[:]
    if hasattr(data, 'mask'):
        return np.ma.filled(data, np.nan)
    return np.array(data)

temp_data = safe_load(ds.variables['temp'])  # Shape: (time, z, lat, lon)
z_data = safe_load(ds.variables['z'])        # Shape: (time, z, lat, lon) - TIME VARYING!
time_data = safe_load(ds.variables['time'])

ds.close()
```

### Convert Time to Datetime

```python
# Get time units from netCDF attributes
ds = nc.Dataset(output_file, 'r')
units_str = ds.variables['time'].units  # e.g., "hours since 2009-01-01 12:00:00"
ds.close()

# Parse reference date and convert
ref_date_str = units_str.replace('hours since ', '')
ref_date = pd.to_datetime(ref_date_str)
time_datetime = ref_date + pd.to_timedelta(time_data, unit='h')
```

### Efficient Temporal Matching

```python
def match_observations_to_simulation(obs_df, temp_data, z_data, time_datetime):
    """
    Match observations to simulation by exact datetime and rounded depth.

    obs_df: DataFrame with columns [datetime, depth, obs_temp] (at least)
    z_data: (time, z_layers, lat, lon) - time-varying depths
    temp_data: (time, z_layers, lat, lon) - simulation temperatures
    time_datetime: datetime array for time dimension
    """

    # Ensure observations have required columns
    obs_df['depth_rounded'] = obs_df['depth'].round().astype(int)

    # Get unique observation times to avoid processing unnecessary timesteps
    obs_times_set = set(obs_df['datetime'].unique())

    matched_records = []

    for t_idx, t_val in enumerate(time_datetime):
        # Skip if no observations at this time
        if t_val not in obs_times_set:
            continue

        # Get observations at this time
        obs_at_time = obs_df[obs_df['datetime'] == t_val]

        # Extract profiles at this timestep (assuming single lat/lon)
        z_profile = z_data[t_idx, :, 0, 0]      # Shape: (z_layers,)
        temp_profile = temp_data[t_idx, :, 0, 0]  # Shape: (z_layers,)

        # Round depths for matching
        z_rounded = np.round(z_profile).astype(int)

        # For each observation at this time
        for _, obs_row in obs_at_time.iterrows():
            obs_depth_rounded = obs_row['depth_rounded']
            obs_temp = obs_row['obs_temp']

            # Find simulation layers at this rounded depth
            matching_indices = np.where(z_rounded == obs_depth_rounded)[0]

            # Use first valid match (could also use closest actual depth)
            for z_idx in matching_indices:
                sim_temp = temp_profile[z_idx]

                # Only include if temperature is valid (not NaN)
                if not np.isnan(sim_temp):
                    matched_records.append({
                        'datetime': t_val,
                        'depth_rounded': obs_depth_rounded,
                        'obs_temp': float(obs_temp),
                        'sim_temp': float(sim_temp),
                        'z_actual': float(z_profile[z_idx]),
                        'z_idx': z_idx
                    })
                    break  # Use first match, don't double-count

    return pd.DataFrame(matched_records)
```

## Quality Checks

### Verify Coverage

```python
def check_matching_coverage(merged_df):
    """Ensure adequate data coverage for metrics"""

    print(f"Total matched pairs: {len(merged_df)}")
    print(f"Unique datetimes: {merged_df['datetime'].nunique()}")
    print(f"Unique depths: {sorted(merged_df['depth_rounded'].unique())}")

    # Check for sufficient deep samples
    deep = merged_df[merged_df['depth_rounded'] >= 13]
    print(f"\nDeep water (≥13m): {len(deep)} pairs")

    # Check for sufficient summer samples
    merged_df['month'] = merged_df['datetime'].dt.month
    summer = merged_df[(merged_df['month'] >= 6) & (merged_df['month'] <= 9)]
    print(f"Summer (Jun-Sep): {len(summer)} pairs")

    summer_deep = summer[summer['depth_rounded'] >= 13]
    print(f"Summer deep: {len(summer_deep)} pairs")

    if len(deep) < 500:
        print("WARNING: Limited deep samples for reliable annual_deep metric")
    if len(summer_deep) < 200:
        print("WARNING: Limited summer deep samples")
```

## Handle Edge Cases

### Multiple Matching Layers

```python
# When multiple sim layers round to same integer depth,
# options include:
# 1. Use first match (current approach)
# 2. Use closest actual depth
# 3. Average matching layers

# Option 2: Use closest actual depth to observation
matching_indices = np.where(z_rounded == obs_depth_rounded)[0]
if len(matching_indices) > 0:
    # Find which one is closest to obs depth
    actual_depths = z_profile[matching_indices]
    closest_idx = matching_indices[np.argmin(np.abs(actual_depths - obs_depth_rounded))]
    sim_temp = temp_profile[closest_idx]
```

### Handling NaN Values

```python
# After matching, before RMSE computation:
# Remove any remaining invalid pairs
merged = merged.dropna(subset=['obs_temp', 'sim_temp'])

# Verify no NaN values remain
if merged['sim_temp'].isna().any() or merged['obs_temp'].isna().any():
    print(f"WARNING: {merged['obs_temp'].isna().sum()} NaN obs, {merged['sim_temp'].isna().sum()} NaN sim")
```

## Key Differences from Simple Matching

- **Temporal iteration**: Process one timestep at a time, skip unused times
- **Depth time-variance**: Use z_data[t_idx] for each time, not a constant depth array
- **Memory efficiency**: Don't create full (time × depth) cartesian product
- **Quality control**: Explicit checks for sufficient data coverage
