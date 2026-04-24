---
name: glm-runner
description: Manage GLM (General Lake Model) configuration and execution. Use this skill when modifying 'glm3.nml' or running the GLM binary to ensure simulation parameters are correctly set and the model runs successfully.
---

# GLM Runner Skill

## Configuration Management
When modifying `glm3.nml`:
- Use the `replace` tool to target specific parameters.
- Ensure only allowed parameters are modified: `Kw`, `coef_mix_hyp`, `wind_factor`, `lw_factor`, and `ch`.
- Respect calibration ranges:
    - `Kw`: [0.1, 0.5]
    - `coef_mix_hyp`: [0.3, 0.7]
    - `wind_factor`: [0.7, 1.3]
    - `lw_factor`: [0.7, 1.3]
    - `ch`: [0.0005, 0.002]
- Do not modify `sw_factor`, `cd`, `ce`, or initialization profiles (`the_depths`, `the_temps`, `the_sals`).

## Simulation Execution
- Run GLM using the `glm` command (if available) or via the provided binary.
- Ensure output paths are correctly specified in `glm3.nml` (e.g., `out_fn = 'output/output.nc'`).
- Verify that the simulation covers the requested period (e.g., 2009-01-01 to 2015-12-30).

## Verification
- Confirm `output/output.nc` is created after the run.
- Check GLM logs for any errors or warnings during execution.
