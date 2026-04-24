---
name: glm-runner
description: A skill to execute the GLM binary and manage its simulation output.
---

# GLM Runner

## Overview
The GLM model is typically a standalone binary executable. Running it involves ensuring all input files (namelist, forcing, initialization) are correctly linked and accessible.

## Setup
Ensure the `glm` binary is in your PATH. 
Check its version with:
```bash
glm --version
```

## Running the Simulation
GLM is usually run from the directory containing `glm3.nml`.
```bash
# Execute GLM
glm
```

## Output Monitoring
GLM logs progress to standard output. Success is usually indicated by the model finishing its time steps.
Output is typically written to a NetCDF file, e.g., `output.nc`.

## Troubleshooting
- **Input Error:** Check that all CSV forcing files (e.g., in `bcs/`) have the columns specified in `glm3.nml`.
- **Config Error:** Namelist errors in `glm3.nml` (like typos or missing parameters) will cause GLM to crash or use default values.
- **Range Error:** Some parameters have physical limits. If GLM crashes early, check your parameter values.
