---
name: glm-metrics
description: How to calculate and save GLM performance metrics (RMSE) to metrics.json. Use this whenever the user asks for RMSE checks or final model evaluation.
---

# GLM Performance Metrics

## Metrics to Compute
Calculate the following metrics to evaluate the model performance:
1. `overall_rmse`: Total RMSE across all matched depth/time pairs.
2. `annual_deep_rmse`: RMSE for depths >= 13 m.
3. `summer_deep_rmse`: RMSE for months June-September, depths >= 13 m.
4. `overall_n_pairs`: Number of total matches.
5. `annual_deep_n_pairs`: Number of deep matches.
6. `summer_deep_n_pairs`: Number of summer deep matches.

## Requirements
- Data: Match `/root/field_temp_oxy.csv` with simulation output `/root/output/output.nc`.
- Matching method: Exact `datetime` + rounded-depth merge.
- Do NOT use nearest-time matching, interpolation, or alternative binning.

## Output
Save the metrics as a JSON file at `/root/metrics.json` with keys named exactly as above.
