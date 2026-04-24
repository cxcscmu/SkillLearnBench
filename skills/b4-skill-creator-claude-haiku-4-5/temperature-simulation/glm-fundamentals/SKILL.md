---
name: glm-fundamentals
description: How to run the General Lake Model (GLM) for lake water temperature simulation. Use this skill whenever you need to execute GLM simulations, understand GLM configuration files (*.nml), interpret GLM output (NetCDF), or troubleshoot GLM execution. Essential for lake modeling and water temperature prediction tasks.
---

# GLM Fundamentals

## Overview

The General Lake Model (GLM) is a one-dimensional hydrodynamic and biogeochemical model for lakes. It simulates vertical water temperature, stratification, and mixing driven by meteorological forcing data.

## Running GLM

### Prerequisites
- GLM executable (typically `glm` or `glm.exe` in PATH)
- Configuration file: `glm3.nml` (Fortran namelist format)
- Forcing data: meteorological, inflow, outflow files referenced in config
- Output directory exists

### Basic Execution
```bash
cd /root
glm
```

GLM reads the configuration from `glm3.nml` in the current directory and produces output according to the `&output` section.

### Expected Output
- NetCDF output file (typically `output/output.nc`)
- CSV outputs if enabled (`csv_lake_fname`, `csv_point_nlevs`, etc.)

## GLM Configuration (glm3.nml)

The configuration is a Fortran namelist file with sections:

### Key Sections for Temperature Simulation

**&light** - Solar radiation and light extinction
- `Kw`: Light extinction coefficient (higher = more light absorbed)
- Default range: 0.1 to 0.5

**&mixing** - Turbulent mixing parameterization
- `coef_mix_hyp`: Hypolimnion mixing coefficient (higher = more mixing in deep water)
- Default range: 0.3 to 0.7

**&meteorology** - Atmospheric forcing and bulk transfer coefficients
- `wind_factor`: Wind speed multiplier (scales wind-driven mixing)
- `lw_factor`: Longwave radiation multiplier
- `ch`: Sensible heat transfer coefficient
- Default ranges: wind_factor [0.7, 1.3], lw_factor [0.7, 1.3], ch [0.0005, 0.002]

**&init_profiles** - Initial temperature and salinity
- `the_depths`, `the_temps`, `the_sals`: Initial conditions at start time

**&time** - Simulation period
- `start`, `stop`: Simulation dates in format 'YYYY-MM-DD HH:MM:SS'
- `dt`: Timestep in seconds (typically 3600 for hourly)

**&output** - Output configuration
- `out_dir`, `out_fn`: Output directory and filename
- `nsave`: Number of timesteps between outputs (24 = daily output for hourly timestep)

## GLM Output (NetCDF)

The NetCDF output file contains:
- **Time dimension**: Simulation timesteps
- **Depth dimension**: Lake depth layers (adaptive, varies through simulation)
- **Variables**:
  - `temp`: Water temperature (°C) at each depth and time
  - `z`: Depth of each layer
  - Other biogeochemical variables if enabled

### Reading NetCDF in Python
```python
import xarray as xr
ds = xr.open_dataset('output/output.nc')
print(ds.data_vars)  # List available variables
print(ds.temp)        # Temperature array
```

## Common Issues

**GLM doesn't run**: Verify `glm3.nml` exists in current directory and config is syntactically valid (check for missing commas, mismatched quotes).

**Output file not created**: Check the `&output` section exists and `out_dir` directory is writable.

**Unrealistic temperatures**: Usually indicates poor parameter choices. Start with defaults and adjust systematically.

## Integration with Calibration

For calibration workflows:
1. Modify only allowed parameters in `&light`, `&mixing`, `&meteorology`
2. Keep `&init_profiles`, `&time`, inflow/outflow data unchanged
3. Run GLM: `glm`
4. Extract simulated temperatures at matched observation times/depths
5. Compute RMSE against field observations
6. Adjust parameters and repeat until RMSE threshold met
