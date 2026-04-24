---
name: run2_advanced-pareto
description: Efficient and robust Pareto frontier calculation for multi-objective optimization.
---

# Advanced Pareto Frontier

A robust implementation to find Pareto-optimal points where some objectives are maximized and others minimized.

## Implementation

```python
import numpy as np

def find_pareto_frontier(data, maximize=None, minimize=None):
    """
    data: np.ndarray of shape (n_samples, n_objectives)
    maximize: list of indices to maximize
    minimize: list of indices to minimize
    """
    costs = data.copy()
    if maximize:
        costs[:, maximize] = -costs[:, maximize]
    
    n_samples = costs.shape[0]
    is_efficient = np.ones(n_samples, dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            # Keep only points that are not dominated by c
            # A point p is dominated by c if p >= c in all and p > c in at least one
            # So we keep p if p < c in at least one or p == c in all
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1) | np.all(costs[is_efficient] == c, axis=1)
    return is_efficient
```
