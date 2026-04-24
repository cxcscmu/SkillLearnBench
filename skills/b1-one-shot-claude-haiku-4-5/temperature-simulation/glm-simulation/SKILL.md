---
name: glm-simulation
description: Running the General Lake Model (GLM) with configuration files and parameter calibration
---

# GLM Simulation Skill

## Overview
The General Lake Model (GLM) is a 1-D hydrodynamic lake model that simulates vertical water temperature and mixing. It reads configuration from a Fortran namelist file (`.nml`) and produces NetCDF output.

## Installation & Setup

### Prerequisites
- GLM executable must be available in your PATH or current directory
- Configuration file in Fortran namelist format (`.nml`)
- Forcing data (meteorology, inflows, outflows) as CSV files

### Configuration File Structure
The GLM configuration file contains multiple namelist sections:

```fortran
&glm_setup
  sim_name = 'Lake Name'
  max_layers = 500
  min_layer_vol = 0.025
  min_layer_thick = 0.10
  max_layer_thick = 0.50
/
&light
  Kw = 0.3          ! Light extinction coefficient [0.1-0.5]
/
&mixing
  coef_mix_hyp = 0.5  ! Hypolimnetic mixing coefficient [0.3-0.7]
/
&meteorology
  wind_factor = 1.0   ! Wind speed scaling [0.7-1.3]
  lw_factor = 1.0     ! Longwave radiation scaling [0.7-1.3]
  ch = 0.0013         ! Heat transfer coefficient [0.0005-0.002]
/
&time
  start = '2009-01-01 12:00:00'
  stop = '2015-12-30 12:00:00'
  dt = 3600
/
&init_profiles
  the_depths = 0, 1, 2, ...
  the_temps = 5.1, 5.1, 5.1, ...
/
```

## Running GLM

### Basic Command
```bash
glm -f glm3.nml
```

The model reads the configuration and produces output (typically NetCDF) to the directory specified in `&output`.

### Key Parameters for Calibration

These 5 parameters can be modified within specified ranges:

1. **Kw** (light extinction): [0.1, 0.5] - affects light penetration
2. **coef_mix_hyp** (hypolimnetic mixing): [0.3, 0.7] - affects deep water mixing
3. **wind_factor**: [0.7, 1.3] - scales wind speed forcing
4. **lw_factor**: [0.7, 1.3] - scales longwave radiation
5. **ch** (heat exchange): [0.0005, 0.002] - affects surface heat transfer

### Modifying Parameters

To modify a parameter in the `.nml` file:

```python
import re

def update_nml_parameter(nml_file, section, param, value):
    """Update a parameter in a Fortran namelist file"""
    with open(nml_file, 'r') as f:
        content = f.read()

    # Find the section and update the parameter
    pattern = r'(&' + section + r'.*?)(\s+' + param + r'\s*=\s*)([^,\n]+)'
    replacement = r'\g<1>\g<2>' + str(value)
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(nml_file, 'w') as f:
        f.write(content)
```

## Validation

- Check that output files are created in the specified output directory
- Verify output is in NetCDF format if expected
- Compare simulation results to observations to evaluate model performance

## Common Issues

1. **Parameter not changing**: Ensure regex pattern matches exactly (spaces, case-sensitive)
2. **Model crash**: Check forcing data file paths and formats
3. **Poor predictions**: Indicates need for parameter calibration (RMSE optimization)
