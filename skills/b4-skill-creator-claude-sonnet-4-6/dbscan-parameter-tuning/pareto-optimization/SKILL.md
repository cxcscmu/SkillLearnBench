---
name: pareto-optimization
description: >
  How to compute the Pareto frontier from a set of multi-objective optimization
  results using numpy or pandas. Use this skill whenever the user wants to find
  Pareto-optimal trade-off solutions, identify non-dominated points, or filter
  results where no single solution is better in all objectives simultaneously.
  Covers both minimization and maximization objectives, and mixed cases.
---

# Pareto Frontier Computation

## Concept

A solution is **Pareto-optimal** (non-dominated) if no other solution is at
least as good in all objectives AND strictly better in at least one. The set of
all Pareto-optimal solutions forms the **Pareto frontier**.

## Mixed Objectives (Maximize F1, Minimize delta)

Transform all objectives to minimization before dominance checking:
- Maximize F1 → minimize `-F1`
- Minimize delta → minimize `delta`

## Implementation

```python
import numpy as np
import pandas as pd

def pareto_frontier(df, maximize_cols, minimize_cols):
    """
    Find Pareto-optimal rows from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
    maximize_cols : list of str  — objectives to maximize
    minimize_cols : list of str  — objectives to minimize

    Returns
    -------
    pd.DataFrame of Pareto-optimal rows (subset of df)
    """
    # Build cost matrix: everything becomes "minimize"
    costs = np.zeros((len(df), len(maximize_cols) + len(minimize_cols)))
    for i, col in enumerate(maximize_cols):
        costs[:, i] = -df[col].values          # negate to convert to minimize
    for i, col in enumerate(minimize_cols):
        costs[:, len(maximize_cols) + i] = df[col].values

    is_pareto = _is_pareto_efficient(costs)
    return df[is_pareto].reset_index(drop=True)


def _is_pareto_efficient(costs):
    """
    Return boolean mask of Pareto-efficient rows.
    costs: 2D array (n_solutions, n_objectives), all minimization.
    """
    n = len(costs)
    is_efficient = np.ones(n, dtype=bool)
    for i in range(n):
        if not is_efficient[i]:
            continue
        # Row i is dominated if any other efficient row j dominates it:
        # j dominates i iff costs[j] <= costs[i] on all objectives
        # and costs[j] < costs[i] on at least one
        dominated = (
            np.all(costs[is_efficient] <= costs[i], axis=1) &
            np.any(costs[is_efficient] < costs[i], axis=1)
        )
        if np.any(dominated):
            is_efficient[i] = False
    return is_efficient
```

## Usage Example

```python
results_df = pd.DataFrame({
    'F1': [0.8, 0.7, 0.9, 0.75],
    'delta': [5.0, 3.0, 8.0, 4.0],
    'min_samples': [3, 5, 3, 4],
    'epsilon': [10, 8, 12, 10],
    'shape_weight': [1.0, 1.2, 0.9, 1.1],
})

pareto_df = pareto_frontier(
    results_df,
    maximize_cols=['F1'],
    minimize_cols=['delta'],
)
```

## Notes

- The O(n²) algorithm above is fine for grids up to ~10k solutions.
- For larger grids, sort by one objective first to reduce comparisons.
- Always filter results (e.g., F1 > 0.5) before computing Pareto frontier to
  reduce noise and improve interpretability.
