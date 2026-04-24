---
name: mars-pareto-frontier
description: Identify Pareto-optimal solutions from Mars cloud clustering results. Use this skill when you need to find the frontier of solutions that balance multiple conflicting objectives (e.g., maximizing F1 while minimizing delta), eliminating dominated solutions and finding all trade-off points.
---

# Mars Pareto Frontier Computation

## Overview

Given a set of clustering results with F1 scores and delta values, identify the **Pareto frontier**—the subset of solutions where no solution can improve both objectives simultaneously.

## Pareto Optimality

A solution (F1, delta) is **Pareto-optimal** if:
- No other solution has higher F1 AND lower delta simultaneously
- Or equivalently: to improve F1, you must accept worse delta (higher value)

## Algorithm

```python
import numpy as np
import pandas as pd

def identify_pareto_frontier(results_df):
    """
    Identify Pareto-optimal points from clustering results.

    Parameters
    ----------
    results_df : pandas DataFrame
        Must contain columns: F1, delta, and hyperparameter columns
        (epsilon, min_samples, shape_weight)

    Returns
    -------
    pareto_df : pandas DataFrame
        Subset of results_df containing only Pareto-optimal solutions,
        sorted by F1 descending
    """
    if len(results_df) == 0:
        return pd.DataFrame()

    # Make a copy to avoid modifying original
    df = results_df.copy()

    # Initialize all points as potentially Pareto
    is_pareto = np.ones(len(df), dtype=bool)

    for i in range(len(df)):
        if not is_pareto[i]:
            continue

        f1_i = df.iloc[i]['F1']
        delta_i = df.iloc[i]['delta']

        # Check if any other point dominates point i
        for j in range(len(df)):
            if i == j or not is_pareto[j]:
                continue

            f1_j = df.iloc[j]['F1']
            delta_j = df.iloc[j]['delta']

            # Point j dominates point i if:
            # f1_j > f1_i AND delta_j < delta_i
            if (f1_j > f1_i) and (delta_j < delta_i):
                is_pareto[i] = False
                break

    # Return Pareto points sorted by F1 descending
    pareto = df[is_pareto].sort_values('F1', ascending=False).reset_index(drop=True)
    return pareto
```

## Example

```python
# Example results (F1, delta)
results = [
    {'F1': 0.8, 'delta': 10.5, 'epsilon': 5},   # Pareto-optimal
    {'F1': 0.75, 'delta': 12.0, 'epsilon': 6},  # Dominated by first
    {'F1': 0.7, 'delta': 5.0, 'epsilon': 4},    # Pareto-optimal (better delta)
    {'F1': 0.85, 'delta': 15.0, 'epsilon': 7},  # Pareto-optimal (better F1)
]

df = pd.DataFrame(results)
pareto = identify_pareto_frontier(df)
# Returns: rows 0, 2, 3 (the dominated row 1 is removed)
```

## Implementation Notes

1. **Objective directions**: Maximize F1 (higher is better), minimize delta (lower is better)
2. **Numerical precision**: Deltas may have floating-point precision differences; exact equality is rare
3. **Sorting**: Return Pareto frontier sorted by F1 descending for easy interpretation
4. **Filter before Pareto**: Apply the F1 > 0.5 filter BEFORE computing Pareto frontier
5. **All hyperparameters**: Preserve all hyperparameter columns in output

## Output Format

The Pareto frontier should be saved to CSV with columns in this order:
```
F1,delta,min_samples,epsilon,shape_weight
```

Formatting:
- F1 and delta: 5 decimal places
- shape_weight: 1 decimal place
- min_samples and epsilon: integers

```python
def format_and_save_pareto(pareto_df, output_path):
    """Format and save Pareto frontier to CSV."""
    output = pareto_df[['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight']].copy()
    output['F1'] = output['F1'].apply(lambda x: f'{x:.5f}')
    output['delta'] = output['delta'].apply(lambda x: f'{x:.5f}')
    output['shape_weight'] = output['shape_weight'].apply(lambda x: f'{x:.1f}')
    output.to_csv(output_path, index=False)
```

## Key Points

1. **Non-dominated solutions**: Every point on Pareto frontier has at least one objective better than all dominated points
2. **Trade-off frontier**: Pareto frontier represents all reasonable compromises between objectives
3. **Efficiency**: For Mars task with ~1000 results, O(n²) is fine; for larger sets consider spatial indexing
