---
name: run2_glm-error-diagnosis
description: Diagnosing temperature profile mismatches and simulation errors in GLM outputs
---

# GLM Error Diagnosis and Debugging

## Common Issues and Diagnosis

### Issue 1: Uniform Temperature Profiles (All Depths Same Temp)

**Symptom**: Simulation shows constant temperature across all depths

**Causes**:
1. **Simulation not initialized properly**: Uniform initial conditions applied incorrectly
2. **Time step too early**: Simulation still evolving from initial state
3. **Broken forcing data**: If meteorological forcing is constant

**Diagnosis**:
```python
import netCDF4 as nc
import numpy as np

ds = nc.Dataset(output_file, 'r')
temp_data = ds.variables['temp'][0, :, 0, 0]  # First time step, first lat/lon
z_data = ds.variables['z'][0, :, 0, 0]

valid_indices = np.where(~np.isnan(temp_data))[0]
unique_temps = np.unique(temp_data[valid_indices])

print(f"Unique temperatures: {len(unique_temps)}")
print(f"All same? {len(unique_temps) == 1}")
print(f"Temperature range: {temp_data.min()}-{temp_data.max()}")
```

**Fix**: Check initialization profile in NML and verify it represents actual starting state

### Issue 2: Temperature Offset (Simulation Always Too Warm or Too Cold)

**Symptom**: RMSE constant across all depths, bias consistent (all simulated temps are X°C higher/lower)

**Diagnosis**:
```python
def analyze_temperature_bias(merged_df):
    """Compute bias in simulation"""
    diff = merged_df['sim_temp'] - merged_df['obs_temp']

    print(f"Mean bias: {diff.mean():.2f}°C")
    print(f"Std bias: {diff.std():.2f}°C")
    print(f"Bias by depth:")

    for depth in sorted(merged_df['depth_rounded'].unique()):
        depth_data = diff[merged_df['depth_rounded'] == depth]
        print(f"  Depth {depth:2d}m: {depth_data.mean():+.2f}°C")
```

**Causes**:
1. Initial conditions too warm/cold
2. All forcing data scaled wrong (`lw_factor`, `sw_factor`)
3. All forcing data systematically wrong

**Fix**:
- If too warm: Increase `ch` (heat loss), decrease `lw_factor`, or decrease `Kw`
- If too cold: Decrease `ch`, increase `lw_factor`, or increase `Kw`

### Issue 3: Stratification Wrong (Depth Variation Wrong)

**Symptom**: Mean temperature might be OK, but stratification RMSE is large

**Diagnosis**:
```python
def analyze_stratification(merged_df):
    """Check if depth gradients match"""

    for t in sorted(merged_df['datetime'].unique())[:5]:  # Check first 5 times
        at_time = merged_df[merged_df['datetime'] == t]
        at_time = at_time.sort_values('depth_rounded')

        print(f"\nTime {t}:")
        for _, row in at_time.head(15).iterrows():
            d = row['depth_rounded']
            o = row['obs_temp']
            s = row['sim_temp']
            diff = s - o
            print(f"  Depth {d:2d}m: obs={o:5.1f}  sim={s:5.1f}  diff={diff:+.1f}")
```

**Causes**:
1. `coef_mix_hyp` wrong: Too much/little deep water mixing
2. `wind_factor` wrong: Surface mixing not capturing dynamics
3. `Kw` wrong: Light penetration affects density structure

**Fix**: Adjust mixing parameters based on whether deep water is too warm or too cold

### Issue 4: Seasonal Pattern Wrong

**Symptom**: Summer RMSE >> Winter RMSE (or vice versa)

**Diagnosis**:
```python
def analyze_by_season(merged_df):
    """Decompose error by season"""
    merged_df['month'] = merged_df['datetime'].dt.month

    for season_name, months in [('Winter', [12,1,2]), ('Spring', [3,4,5]),
                                 ('Summer', [6,7,8]), ('Fall', [9,10,11])]:
        season_data = merged_df[merged_df['month'].isin(months)]
        if len(season_data) > 0:
            rmse = np.sqrt(np.mean((season_data['sim_temp'] - season_data['obs_temp'])**2))
            bias = (season_data['sim_temp'] - season_data['obs_temp']).mean()
            print(f"{season_name:6s}: RMSE={rmse:.2f}°C, bias={bias:+.2f}°C ({len(season_data)} pairs)")
```

**Common patterns**:
- **Summer too warm, winter OK**: `Kw` too high (too much light) or `coef_mix_hyp` too low (weak mixing)
- **Summer OK, winter too cold**: Initial conditions wrong or winter forcing data issue
- **Spring/Fall transitions bad**: Mixing parameters (wind_factor, coef_mix_hyp) likely wrong

### Issue 5: Deep Water Specifically Bad

**Symptom**: overall_rmse OK, annual_deep_rmse >> threshold

**Diagnosis**:
```python
def analyze_by_depth(merged_df):
    """Decompose error by depth band"""

    for depth_range in [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25)]:
        band_data = merged_df[(merged_df['depth_rounded'] >= depth_range[0]) &
                              (merged_df['depth_rounded'] < depth_range[1])]
        if len(band_data) > 0:
            rmse = np.sqrt(np.mean((band_data['sim_temp'] - band_data['obs_temp'])**2))
            print(f"Depth {depth_range[0]:2d}-{depth_range[1]:2d}m: RMSE={rmse:.2f}°C ({len(band_data):4d} pairs)")
```

**Causes**:
1. `coef_mix_hyp` controls deep mixing: Wrong value = wrong deep stratification
2. `Kw` affects light penetration to depth: Wrong value = wrong density structure

**Fix**:
- If deep water too warm: Increase `coef_mix_hyp` (more mixing brings cold water up)
- If deep water too cold: Decrease `coef_mix_hyp` (less mixing keeps it isolated)

## Data Quality Checks

### Check Observation Distribution

```python
def check_obs_distribution(obs_df):
    """Ensure observations span full lake and season"""

    print(f"Depth range: {obs_df['depth'].min()}-{obs_df['depth'].max()}m")
    print(f"Time span: {obs_df['datetime'].min()} to {obs_df['datetime'].max()}")
    print(f"Samples per depth:")

    for depth in sorted(obs_df['depth'].unique()):
        count = len(obs_df[obs_df['depth'] == depth])
        print(f"  {depth:5.1f}m: {count:3d} samples")
```

### Check Simulation Range

```python
def check_sim_range(temp_data, z_data):
    """Verify simulation outputs realistic values"""

    valid_temps = temp_data[~np.isnan(temp_data)]

    print(f"Temperature range: {valid_temps.min():.1f} to {valid_temps.max():.1f}°C")
    print(f"Mean: {valid_temps.mean():.1f}°C")

    # Most lakes should be 0-30°C
    if valid_temps.min() < -10 or valid_temps.max() > 40:
        print("WARNING: Unrealistic temperature range!")

    # Check depth range
    valid_z = z_data[~np.isnan(z_data)]
    print(f"Depth range: {valid_z.min():.1f} to {valid_z.max():.1f}m")
```

## Iterative Refinement

1. **Compute detailed metrics** - which metric fails most?
2. **Analyze spatiotemporal pattern** - which times/depths are worst?
3. **Identify primary error** - bias, stratification, seasonal, or depth-specific?
4. **Propose parameter change** - based on physical reasoning
5. **Test change** - evaluate effect on all metrics
6. **Repeat** until success

Each iteration should reduce RMSE, not increase it. If change makes things worse, revert and try different parameter.
