---
name: pareto-frontier-computation
description: How to compute the Pareto frontier from a set of (F1, delta) optimization results where F1 is maximized and delta is minimized. Includes filtering, dominance checking, and CSV output formatting.
---

# Pareto Frontier Computation

## Overview

Given a set of solutions with multiple objectives, the Pareto frontier contains all non-dominated solutions: a solution is dominated if another solution is at least as good on all objectives and strictly better on at least one.

For this task:
- **Maximize F1** (higher is better)
- **Minimize delta** (lower is better)

## Dominance Definition

Solution A dominates solution B if:
- `A.F1 >= B.F1` AND `A.delta <= B.delta`
- AND at least one is strict: `A.F1 > B.F1` OR `A.delta < B.delta`

## Implementation

```python
import numpy as np
import pandas as pd

def compute_pareto_frontier(df):
    """
    df: DataFrame with columns [F1, delta, min_samples, epsilon, shape_weight]
    
    Returns: DataFrame of Pareto-optimal rows (non-dominated solutions).
    """
    # Work with numpy for speed
    f1 = df['F1'].values
    delta = df['delta'].values
    n = len(df)
    
    is_pareto = np.ones(n, dtype=bool)
    
    for i in range(n):
        if not is_pareto[i]:
            continue
        # Check if solution i is dominated by any other solution j
        for j in range(n):
            if i == j or not is_pareto[j]:
                continue
            # j dominates i if j is at least as good on all objectives
            # and strictly better on at least one
            j_dominates_i = (
                f1[j] >= f1[i] and delta[j] <= delta[i] and
                (f1[j] > f1[i] or delta[j] < delta[i])
            )
            if j_dominates_i:
                is_pareto[i] = False
                break
    
    return df[is_pareto].copy()


def compute_pareto_vectorized(df):
    """
    Vectorized Pareto computation — faster for large result sets.
    """
    f1 = df['F1'].values
    delta = df['delta'].values
    n = len(df)
    is_pareto = np.ones(n, dtype=bool)

    for i in range(n):
        if not is_pareto[i]:
            continue
        # All other points that are at least as good on both objectives
        # and strictly better on at least one
        dominated_by = (
            (f1 >= f1[i]) & (delta <= delta[i]) &
            ((f1 > f1[i]) | (delta < delta[i]))
        )
        dominated_by[i] = False  # Don't compare to self
        if dominated_by.any():
            is_pareto[i] = False

    return df[is_pareto].copy()
```

## Filtering and Output

```python
def filter_and_save_pareto(results, output_path):
    """
    results: list of dicts with keys [F1, delta, min_samples, epsilon, shape_weight]
    """
    df = pd.DataFrame(results, columns=['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight'])
    
    # Filter: only keep results with average F1 > 0.5
    df = df[df['F1'] > 0.5].copy()
    
    if df.empty:
        print("No solutions with F1 > 0.5 found.")
        df.to_csv(output_path, index=False)
        return df
    
    # Compute Pareto frontier
    pareto = compute_pareto_vectorized(df)
    
    # Round outputs
    pareto['F1'] = pareto['F1'].round(5)
    pareto['delta'] = pareto['delta'].round(5)
    pareto['shape_weight'] = pareto['shape_weight'].round(1)
    pareto['min_samples'] = pareto['min_samples'].astype(int)
    pareto['epsilon'] = pareto['epsilon'].astype(int)
    
    # Sort for readable output (optional but conventional)
    pareto = pareto.sort_values(['F1', 'delta'], ascending=[False, True])
    
    pareto[['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight']].to_csv(
        output_path, index=False
    )
    return pareto
```

## Notes

- After rounding, multiple parameter combinations may map to identical (F1, delta) points — all should be retained if they were non-dominated before rounding
- With only two objectives, the Pareto frontier, when sorted by F1 descending, will have delta strictly increasing (otherwise one would dominate another)