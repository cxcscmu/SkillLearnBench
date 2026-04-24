---
name: glm-calibrator
description: Calibrate GLM by adjusting key parameters to minimize RMSE. Use this skill when you need to iteratively tune model parameters to meet performance thresholds.
---

# GLM Calibrator Skill

## Calibration Strategy
1.  **Baseline Run:** Start with the original `glm3.nml` parameters.
2.  **Sensitivity Analysis:** Understand how `Kw`, `coef_mix_hyp`, `wind_factor`, `lw_factor`, and `ch` affect simulation results (e.g., `Kw` affects deep temperatures).
3.  **Iteration Loop:**
    - Adjust one or more parameters within the allowed ranges.
    - Run the simulation using `glm-runner`.
    - Evaluate performance using `glm-evaluator`.
    - Repeat until all three RMSE checks are satisfied:
        - `overall_rmse < 1.60`
        - `annual_deep_rmse < 1.55`
        - `summer_deep_rmse < 1.70`
4.  **Parameter Ranges:**
    - `Kw`: [0.1, 0.5]
    - `coef_mix_hyp`: [0.3, 0.7]
    - `wind_factor`: [0.7, 1.3]
    - `lw_factor`: [0.7, 1.3]
    - `ch`: [0.0005, 0.002]

## Key Calibration Targets
- `Kw`: Light extinction coefficient (higher `Kw` leads to cooler deep waters).
- `wind_factor`: Scaling factor for wind speed (affects surface mixing).
- `coef_mix_hyp`: Scaling factor for hypolimnetic mixing.
- `lw_factor`: Scaling factor for longwave radiation.
- `ch`: Bulk transfer coefficient for sensible heat.
