---
name: glm-config-optimization
description: Manage and calibrate General Lake Model (GLM) configuration files (glm3.nml) within specified parameter constraints and physical ranges.
---

1. **Parameter Constraints**: Only modify the permitted calibration parameters: `Kw`, `coef_mix_hyp`, `wind_factor`, `lw_factor`, and `ch`. Do not alter `sw_factor`, `cd`, `ce`, or initialization profiles (`the_depths`, `the_temps`, `the_sals`).
2. **Range Validation**: Ensure all final values remain within the published calibration ranges:
   - `Kw`: [0.1, 0.5]
   - `coef_mix_hyp`: [0.3, 0.7]
   - `wind_factor`: [0.7, 1.3]
   - `lw_factor`: [0.7, 1.3]
   - `ch`: [0.0005, 0.002]
3. **Setup Verification**: Ensure the `&glm_setup` section correctly defines the simulation period (e.g., `2009-01-01` to `2015-12-30`) to align with required output timestamps.
4. **Consistency**: Verify that `the_depths` in `&init_profiles` are correctly interpreted as distance from the surface (depth) while the model internal coordinates (z) are height from the bottom.