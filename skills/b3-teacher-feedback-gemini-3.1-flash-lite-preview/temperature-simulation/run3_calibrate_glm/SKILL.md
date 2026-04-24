---
name: calibrate_glm
description: Performs efficient parameter optimization using a heuristic search or scipy.optimize to satisfy RMSE constraints within fixed parameter ranges.
---

Since a full grid search is computationally expensive, implement an optimization routine (e.g., `scipy.optimize.minimize` with bounds) to minimize the `overall_rmse`. Ensure all parameters stay within defined constraints: `Kw` [0.1, 0.5], `coef_mix_hyp` [0.3, 0.7], `wind_factor` [0.7, 1.3], `lw_factor` [0.7, 1.3], `ch` [0.0005, 0.002].

```python
from scipy.optimize import minimize

def objective_function(x):
    params = {'Kw': x[0], 'coef_mix_hyp': x[1], 'wind_factor': x[2], 'lw_factor': x[3], 'ch': x[4]}
    update_glm_parameters(params)
    run_simulation()
    metrics = calculate_metrics(...)
    return metrics['overall_rmse']

# Use Bounds to enforce calibration ranges
bounds = [(0.1, 0.5), (0.3, 0.7), (0.7, 1.3), (0.7, 1.3), (0.0005, 0.002)]
```