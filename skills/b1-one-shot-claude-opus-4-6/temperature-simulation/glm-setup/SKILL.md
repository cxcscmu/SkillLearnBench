---
name: glm-setup
description: Running the General Lake Model (GLM) and understanding its NML configuration file format.
---

# GLM Setup and Configuration

## Running GLM
GLM is run from the directory containing `glm3.nml`:
```bash
cd /path/to/sim && glm
```

## Key NML Sections
- `&glm_setup`: Layer configuration
- `&light`: Light attenuation (`Kw` = light extinction coefficient)
- `&mixing`: Mixing parameters (`coef_mix_hyp` = hypolimnetic mixing)
- `&meteorology`: Met forcing adjustments (`wind_factor`, `sw_factor`, `lw_factor`, `cd`, `ce`, `ch`)
- `&time`: Simulation period (`start`, `stop`, `dt`)
- `&output`: Output directory and file naming
- `&init_profiles`: Initial temperature/salinity profiles
- `&morphometry`: Lake bathymetry
- `&inflow`/`&outflow`: Hydrological boundary conditions

## Output
- NetCDF file at `<out_dir>/<out_fn>.nc`
- Contains variables: `temp` (temperature), `salt`, etc.
- Dimensions: time × depth (layers vary per timestep)
- `z` variable gives height above bottom; convert to depth = lake_depth - z

## NML Editing
Fortran namelist format. Parameters are `key = value` pairs within `&section ... /` blocks.
