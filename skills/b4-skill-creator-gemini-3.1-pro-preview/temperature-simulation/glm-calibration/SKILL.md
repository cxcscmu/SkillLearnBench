---
name: glm-calibration
description: Use this skill to learn how to calibrate the General Lake Model (GLM) by adjusting specific parameters like Kw, coef_mix_hyp, wind_factor, lw_factor, and ch to match observed water temperatures and improve overall, annual deep, and summer deep RMSE metrics.
---

# GLM Calibration

## Objective
Calibrate the General Lake Model (GLM) by modifying allowed parameters to achieve target RMSE metrics for simulated vs. observed water temperatures.

## Allowed Parameters and Ranges
Modify only these parameters in `glm3.nml` to keep within the published ranges:
- `Kw` (light attenuation): `[0.1, 0.5]`
- `coef_mix_hyp` (hypolimnetic mixing efficiency): `[0.3, 0.7]`
- `wind_factor` (wind speed scaling factor): `[0.7, 1.3]`
- `lw_factor` (longwave radiation scaling factor): `[0.7, 1.3]`
- `ch` (bulk aerodynamic coefficient for sensible heat): `[0.0005, 0.002]`

## Process
1. Parse the simulation output from `output/output.nc`.
2. Match simulated temperatures to field observations based on exact datetime and rounded depth. Do not use nearest-time matching, interpolation, or alternative depth binning.
3. Compute metrics:
   - `overall_rmse`: RMSE across all matched pairs.
   - `annual_deep_rmse`: RMSE for all matched pairs at rounded depths >= 13 m.
   - `summer_deep_rmse`: RMSE for months June-September and rounded depths >= 13 m.
4. Iteratively adjust parameters to reduce RMSE values until thresholds are met.
