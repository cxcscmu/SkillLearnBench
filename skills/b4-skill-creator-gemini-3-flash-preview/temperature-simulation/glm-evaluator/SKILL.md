---
name: glm-evaluator
description: Evaluate GLM simulation results using field observations and RMSE metrics. Use this skill when you need to merge simulation results with field observations and calculate RMSE values for different conditions (overall, annual_deep, summer_deep).
---

# GLM Evaluator Skill

## Data Requirements
- Observations: `field_temp_oxy.csv` (contains depth, temp, oxygen, and datetime).
- Simulation Results: `output/output.nc` (contains water temperature profiles).

## Evaluation Methodology
1.  **Preprocessing Observations:**
    - Parse `datetime`.
    - Extract `depth` and `temp`.
2.  **Preprocessing Simulation:**
    - Extract `temp` profiles and `time`.
    - Map simulation depths to observation depths.
3.  **Merging:**
    - Perform an exact `datetime` + rounded-depth merge.
    - Do not use nearest-time matching or interpolation.
4.  **Metric Definitions:**
    - `overall_rmse`: RMSE of all matched pairs.
    - `annual_deep_rmse`: RMSE for depths >= 13 m.
    - `summer_deep_rmse`: RMSE for depths >= 13 m and months June to September.
5.  **Reporting:**
    - Save results to `metrics.json` with keys: `overall_rmse`, `annual_deep_rmse`, `summer_deep_rmse`, `overall_n_pairs`, `annual_deep_n_pairs`, and `summer_deep_n_pairs`.

## Python Libraries
Use `pandas` for data manipulation, `netCDF4` or `xarray` to read `.nc` files, and `numpy` for calculations.
