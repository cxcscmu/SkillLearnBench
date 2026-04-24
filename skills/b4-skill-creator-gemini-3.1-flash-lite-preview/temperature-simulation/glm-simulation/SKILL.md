---
name: glm-simulation
description: How to run GLM, modify calibration parameters, and manage simulation outputs. Use this whenever the user wants to run, calibrate, or troubleshoot GLM simulations.
---

# GLM Simulation Guide

## Running GLM
Run the model using the following command in the project root:
```bash
glm
```

## Configuration
The model reads `/root/glm3.nml`. 

## Calibration Parameters
Modify ONLY these parameters in `glm3.nml` within specified ranges:
- `Kw`: [0.1, 0.5]
- `coef_mix_hyp`: [0.3, 0.7]
- `wind_factor`: [0.7, 1.3]
- `lw_factor`: [0.7, 1.3]
- `ch`: [0.0005, 0.002]

## Constraints
- Do NOT change `sw_factor`, `cd`, `ce`, or the initialization profile (`the_depths`, `the_temps`, `the_sals`).
- Ensure output is saved to `/root/output/output.nc`.
