---
name: pareto-optimization
description: Multi-objective optimization with Pareto frontiers. Use when optimizing multiple conflicting objectives simultaneously, finding trade-off solutions, or computing Pareto-optimal points.
---

# Pareto Frontier Computation

## When to Use

Use this skill whenever you need to find the set of non-dominated solutions from multi-objective optimization results — e.g., balancing accuracy vs. cost, F1 vs. distance, precision vs. recall.

## Core Algorithm

A solution is Pareto-optimal if no other solution is better on all objectives simultaneously.

```python
import numpy as np

def pareto_frontier(objectives, maximize=None):
    """
    Find Pareto-optimal points.

    Args:
        objectives: array of shape (n, k) where k is the number of objectives
        maximize: list of bools, True = maximize that objective, False = minimize
                  Default: all maximize

    Returns:
        Boolean mask of Pareto-optimal points
    """
    n = len(objectives)
    if maximize is None:
        maximize = [True] * objectives.shape[1]

    # Flip sign for objectives to maximize (so we can treat all as minimize)
    obj = objectives.copy().astype(float)
    for i, m in enumerate(maximize):
        if m:
            obj[:, i] = -obj[:, i]

    is_pareto = np.ones(n, dtype=bool)
    for i in range(n):
        if not is_pareto[i]:
            continue
        # A point dominates i if it's <= on all objectives and < on at least one
        for j in range(n):
            if i == j or not is_pareto[j]:
                continue
            if np.all(obj[j] <= obj[i]) and np.any(obj[j] < obj[i]):
                is_pareto[i] = False
                break
    return is_pareto
```

## Usage Pattern for Grid Search Results

```python
import pandas as pd

# results_df has columns: F1, delta, param1, param2, ...
# Maximize F1, minimize delta
objectives = results_df[['F1', 'delta']].values
mask = pareto_frontier(objectives, maximize=[True, False])
pareto_df = results_df[mask]
```

## Notes

- Filter out invalid/unwanted results before computing the frontier
- The frontier is sensitive to objective scales — normalization isn't needed for finding Pareto points but matters for visualization
- For two objectives, sorting by one and scanning for improvements in the other gives O(n log n) performance
