---
name: pareto-optimization
description: Compute Pareto-optimal frontiers from multi-objective optimization results, including dominance checking and frontier extraction.
---

# Pareto Optimization

## Overview

A solution is **Pareto-optimal** if no other solution dominates it — i.e., no other solution is at least as good on all objectives and strictly better on at least one.

## When to Use

- Multi-objective optimization with conflicting goals
- Finding trade-off solutions (e.g., maximize F1 vs minimize error)
- Grid search results where you want the best trade-off set

## Core Implementation

```python
import numpy as np
import pandas as pd

def is_pareto_dominated(costs, i):
    """
    Check if solution i is dominated by any other solution.
    costs: 2D array where each row is [obj1_to_minimize, obj2_to_minimize, ...]
    Returns True if solution i is dominated.
    """
    for j in range(len(costs)):
        if j == i:
            continue
        # j dominates i if j is <= i on all objectives and < i on at least one
        if all(costs[j] <= costs[i]) and any(costs[j] < costs[i]):
            return True
    return False

def get_pareto_frontier(df, objectives):
    """
    Extract Pareto-optimal rows from a DataFrame.

    Args:
        df: pandas DataFrame with results
        objectives: dict mapping column names to 'min' or 'max'
                    e.g., {'F1': 'max', 'delta': 'min'}

    Returns:
        DataFrame with only Pareto-optimal rows
    """
    # Convert to minimization: negate 'max' objectives
    costs = np.zeros((len(df), len(objectives)))
    for k, (col, direction) in enumerate(objectives.items()):
        if direction == 'max':
            costs[:, k] = -df[col].values
        else:
            costs[:, k] = df[col].values

    pareto_mask = np.zeros(len(df), dtype=bool)
    for i in range(len(df)):
        if not is_pareto_dominated(costs, i):
            pareto_mask[i] = True

    return df[pareto_mask].copy()
```

## Vectorized (Faster) Implementation

```python
def get_pareto_frontier_fast(df, objectives):
    """Vectorized Pareto frontier extraction — O(n²) but with numpy."""
    costs = np.zeros((len(df), len(objectives)))
    for k, (col, direction) in enumerate(objectives.items()):
        costs[:, k] = -df[col].values if direction == 'max' else df[col].values

    n = len(costs)
    is_pareto = np.ones(n, dtype=bool)

    for i in range(n):
        if not is_pareto[i]:
            continue
        # Check if any other solution dominates i
        # dominates[j] = True if j dominates i
        dominated_by = np.all(costs <= costs[i], axis=1) & np.any(costs < costs[i], axis=1)
        dominated_by[i] = False  # don't compare with self
        if np.any(dominated_by):
            is_pareto[i] = False

    return df[is_pareto].copy()
```

## Efficient Implementation (O(n log n))

```python
def pareto_frontier_efficient(df, objectives):
    """
    Efficient Pareto frontier using sort + sweep.
    Works best when objectives is a 2-element dict.
    """
    cols = list(objectives.keys())
    directions = list(objectives.values())

    # Work on a copy with normalized costs
    work = df.copy()
    sort_col = cols[0]

    # Sort by first objective (descending if maximize)
    ascending = directions[0] == 'min'
    work = work.sort_values(sort_col, ascending=ascending).reset_index(drop=True)

    pareto_rows = []
    best_second = None  # track best value of second objective seen so far

    for _, row in work.iterrows():
        second_val = row[cols[1]]
        better = directions[1] == 'min'

        if best_second is None:
            pareto_rows.append(row)
            best_second = second_val
        else:
            if better:  # minimize second objective
                if second_val < best_second:
                    pareto_rows.append(row)
                    best_second = second_val
            else:  # maximize second objective
                if second_val > best_second:
                    pareto_rows.append(row)
                    best_second = second_val

    return pd.DataFrame(pareto_rows)
```

## Usage Example

```python
import pandas as pd

# Grid search results
results = pd.DataFrame({
    'F1': [0.7, 0.8, 0.75, 0.6, 0.85],
    'delta': [5.0, 8.0, 6.0, 3.0, 12.0],
    'epsilon': [4, 6, 5, 4, 8],
    'min_samples': [3, 3, 4, 5, 3],
    'shape_weight': [1.0, 1.1, 1.0, 0.9, 1.2]
})

# Filter to meaningful results
results = results[results['F1'] > 0.5]

# Get Pareto frontier (maximize F1, minimize delta)
pareto = get_pareto_frontier_fast(results, {'F1': 'max', 'delta': 'min'})
print(pareto.sort_values('F1'))
```

## Validation

A Pareto frontier should satisfy:
- No two points in the frontier where one dominates the other
- Every non-frontier point is dominated by at least one frontier point

```python
def validate_pareto(frontier_df, all_results_df, objectives):
    """Assert frontier validity."""
    # Check no frontier point dominates another
    costs_frontier = ...  # compute cost matrix for frontier
    for i in range(len(frontier_df)):
        for j in range(len(frontier_df)):
            if i != j:
                assert not dominates(costs_frontier[j], costs_frontier[i]), \
                    f"Frontier point {j} dominates frontier point {i}"
```
