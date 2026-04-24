---
name: pareto-optimization
description: Algorithm to identify Pareto-optimal points from a set of multi-objective evaluations.
---

# Pareto Optimization

When evaluating multiple conflicting objectives (e.g., maximize F1 score, minimize distance), a point is Pareto optimal if no other point is better in all objectives.

## Usage
```python
import numpy as np

def is_pareto_efficient(costs, maximize=[True, False]):
    ""\"
    Find the pareto-efficient points
    costs: An (n_points, n_costs) array
    maximize: Boolean array indicating if the corresponding objective should be maximized
    ""\"
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    
    # Adjust costs so we can simply look for points that are strictly "less than or equal"
    # For objectives we want to maximize, we negate them.
    adjusted_costs = np.copy(costs)
    for i, max_obj in enumerate(maximize):
        if max_obj:
            adjusted_costs[:, i] = -adjusted_costs[:, i]
            
    for i, c in enumerate(adjusted_costs):
        if is_efficient[i]:
            # Keep any point with a lower cost or not strictly dominated
            # A point is strictly dominated if it's >= in all dimensions and > in at least one
            is_efficient[is_efficient] = np.any(adjusted_costs[is_efficient] < c, axis=1) | np.all(adjusted_costs[is_efficient] == c, axis=1)
            is_efficient[i] = True  # And keep self
    return is_efficient
```
