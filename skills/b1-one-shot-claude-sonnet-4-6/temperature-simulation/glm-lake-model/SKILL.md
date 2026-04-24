---
name: glm-lake-model
description: Running the General Lake Model (GLM3) for lake temperature simulation, including configuration file structure and execution.
---

# GLM Lake Model Skill

## Overview
GLM (General Lake Model) is a 1D hydrodynamic model for simulating vertical water temperature, mixing, and stratification in lakes.

## Installation
GLM binary is typically at `/usr/local/bin/glm`. Run with:
```bash
cd /path/to/simulation/dir
glm
```
GLM reads `glm3.nml` from the current directory.

## Configuration File (glm3.nml)
Key sections:
- `&glm_setup`: Basic simulation parameters
- `&light`: Light extinction (`Kw` = light attenuation coefficient, m⁻¹)
- `&mixing`: Turbulent mixing parameters
  - `coef_mix_hyp`: Hypolimnetic mixing coefficient
  - `coef_mix_conv`, `coef_wind_stir`, `coef_mix_shear`, `coef_mix_turb`, `coef_mix_KH`
- `&time`: Simulation period (`start`, `stop` in 'YYYY-MM-DD hh:mm:ss')
- `&output`: Output directory and filename
- `&meteorology`: Met forcing file and factors
  - `wind_factor`: Scale wind speed
  - `lw_factor`: Scale longwave radiation
  - `ch`: Sensible heat transfer coefficient
  - `sw_factor`, `cd`, `ce`: Do NOT change these
- `&init_profiles`: Initial temperature/salinity profiles

## Running GLM
```bash
cd /root  # Must run from directory containing glm3.nml
glm       # Reads glm3.nml, writes output per &output section
```

## Output
- NetCDF file at `output/output.nc` with variables:
  - `time`: time in days since reference
  - `z`: layer heights (m above bottom)
  - `temp`: water temperature (°C) per layer
  - `NS`: number of active layers per timestep
