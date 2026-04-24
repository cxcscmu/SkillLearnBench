---
name: glm-simulation
description: This skill covers running the General Lake Model (GLM) and modifying its configuration file (glm3.nml).
---

# GLM Simulation Skill

## Running GLM
Ensure the `glm` executable is in your PATH. Run the simulation using:
`glm`

The model expects `glm3.nml` to be in the current working directory.

## Modifying Configuration
Use `sed` or Python to update calibration parameters in `glm3.nml`.
Allowed parameters:
- `Kw`: [0.1, 0.5]
- `coef_mix_hyp`: [0.3, 0.7]
- `wind_factor`: [0.7, 1.3]
- `lw_factor`: [0.7, 1.3]
- `ch`: [0.0005, 0.002]

Example (updating Kw):
`sed -i 's/Kw = .*/Kw = 0.2/' glm3.nml`
