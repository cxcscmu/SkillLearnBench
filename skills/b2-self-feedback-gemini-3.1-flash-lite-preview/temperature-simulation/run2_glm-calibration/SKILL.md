---
name: run2_glm-calibration
description: This skill covers the process of calibrating GLM by iterating through parameters within allowed bounds and verifying metrics against observations.
---
# GLM Calibration Process

## Parameters
Modify the following in `glm3.nml`:
- `Kw`: 0.1 - 0.5
- `coef_mix_hyp`: 0.3 - 0.7
- `wind_factor`: 0.7 - 1.3
- `lw_factor`: 0.7 - 1.3
- `ch`: 0.0005 - 0.002

## Calibration Loop
1. Generate parameter set within bounds.
2. Update `glm3.nml`.
3. Run `glm --nml glm3.nml --quiet`.
4. Calculate RMSE metrics using observation comparison script.
5. Record metrics in `metrics.json`.
