---
name: glm-metric-validator
description: Calculate specific RMSE metrics by merging simulation and observation data using exact datetime and rounded-depth matching.
---

1. **Data Preparation**:
   - Load field observations from `field_temp_oxy.csv`.
   - Ensure observation `datetime` values are truncated or aligned to match the simulation's temporal resolution (e.g., setting minutes/seconds to zero if the simulation outputs daily/hourly values).

2. **Merge Logic**:
   - Apply `round().astype(int)` to the `depth` values of both the simulation and observation datasets to ensure integer-based depth matching.
   - Perform an inner join on the `datetime` and `rounded_depth` columns. No interpolation or nearest-neighbor matching is permitted for the final evaluation.

3. **Metric Calculation**:
   - **Overall RMSE**: Calculate the Root Mean Square Error for all matched pairs.
   - **Annual Deep RMSE**: Calculate RMSE for all matched pairs where `rounded_depth` $\ge 13$.
   - **Summer Deep RMSE**: Calculate RMSE for matched pairs where `rounded_depth` $\ge 13$ and the month is June, July, August, or September (6-9).

4. **Reporting**:
   - Save the results to `/root/metrics.json` using the keys: `overall_rmse`, `annual_deep_rmse`, `summer_deep_rmse`, `overall_n_pairs`, `annual_deep_n_pairs`, and `summer_deep_n_pairs`.