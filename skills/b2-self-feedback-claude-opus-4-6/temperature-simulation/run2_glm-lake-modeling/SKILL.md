---
name: run2_glm-lake-modeling
description: Complete guide to setting up, running, and configuring the General Lake Model (GLM) for 1D lake temperature simulation.
---

# General Lake Model (GLM) - Setup and Configuration

## What is GLM?
GLM is a 1D hydrodynamic model that simulates vertical temperature, salinity, and density profiles in lakes and reservoirs. It solves energy and mass balance equations layer-by-layer.

## Prerequisites
- `glm` binary installed (check with `which glm`)
- Configuration file `glm3.nml` in working directory
- Meteorological forcing CSV (`bcs/meteo.csv`)
- Inflow/outflow CSVs
- Output directory must exist (`mkdir -p output`)

## Configuration File Structure (glm3.nml)
The file uses Fortran namelist format with `&section ... /` blocks:

| Section | Key Parameters | Notes |
|---------|---------------|-------|
| `&glm_setup` | max_layers, layer thickness | Layer resolution |
| `&light` | **Kw** (extinction coeff) | Controls light penetration depth |
| `&mixing` | **coef_mix_hyp**, coef_mix_conv, etc. | Vertical mixing strengths |
| `&morphometry` | H, A arrays | Lake bathymetry (elevation-area) |
| `&time` | start, stop, dt | Simulation period and timestep |
| `&output` | out_dir, out_fn, nsave | NetCDF output control |
| `&init_profiles` | the_depths, the_temps | Initial conditions |
| `&meteorology` | **wind_factor**, **lw_factor**, **ch**, cd, ce, sw_factor | Met scaling and bulk transfer |
| `&inflow`/`&outflow` | inflow_fl, outflow_fl | Hydrological boundary conditions |
| `&sediment` | sed_temp_mean, sed_heat_Ksoil | Bottom boundary condition |

## Running GLM
```bash
cd /path/to/config/dir
mkdir -p output
glm   # reads glm3.nml, writes output/output.nc
```
GLM exits silently on success. Check for `output/output.nc` existence.

## Output Structure (NetCDF)
- `temp[time, z]` - water temperature (°C)
- `z[time, z]` - height from lake bottom (m) - NOT depth from surface
- `time` - time coordinate with units attribute for `num2date` conversion

### Converting height to depth
```python
surface_height = np.max(z[time_idx, :])
depth_from_surface = surface_height - z[time_idx, :]
```

## Parameter Sensitivity for Lake Mendota
From calibration experiments:
1. **Kw** (0.1-0.5): Most impactful. Higher values reduce deep heating, improve thermocline.
2. **wind_factor** (0.7-1.3): Controls wind-driven mixing intensity. Lower = stronger stratification.
3. **lw_factor** (0.7-1.3): Scales longwave radiation. Values < 1 cool the lake.
4. **coef_mix_hyp** (0.3-0.7): Hypolimnetic mixing. Moderate values (0.4-0.5) balance deep temperature.
5. **ch** (0.0005-0.002): Sensible heat transfer. Lower = less surface heat exchange.

## Common Pitfalls
- Forgetting to create output directory before running
- Not preserving the exact nml format when editing (Fortran is picky)
- Confusing z (height from bottom) with depth from surface
- The `ch` parameter regex can match `catchrain` if not careful - use `\bch\s*=` or match line context
