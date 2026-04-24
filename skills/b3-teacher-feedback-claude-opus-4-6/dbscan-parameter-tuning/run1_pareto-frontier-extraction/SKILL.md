---
name: pareto-frontier-extraction
description: How to identify Pareto-optimal solutions from a set of multi-objective optimization results, specifically maximizing one metric while minimizing another.
---

## Pareto Frontier Extraction

A solution is **Pareto-optimal** if no other solution is better in all objectives simultaneously.

### Objectives
- **Maximize F1** (higher is better)
- **Minimize delta** (lower is better)

A point `A` **dominates** point `B` if:
- `A.F1 >= B.F1` AND `A.delta <= B.delta`
- AND at least one inequality is strict

A point is Pareto-optimal if **no other point dominates it**.

### Implementation

```python
import pandas as pd
import numpy as np

def find_pareto_frontier(df, maximize_col='F1', minimize_col='delta'):
    """
    Find Pareto-optimal points.
    
    Args:
        df: DataFrame with columns for both objectives
        maximize_col: column to maximize
        minimize_col: column to minimize
    
    Returns:
        DataFrame of Pareto-optimal rows
    """
    is_pareto = np.ones(len(df), dtype=bool)
    
    values = df[[maximize_col, minimize_col]].values
    
    for i in range(len(values)):
        if not is_pareto[i]:
            continue
        for j in range(len(values)):
            if i == j or not is_pareto[j]:
                continue
            # Check if j dominates i
            # j dominates i if j.F1 >= i.F1 and j.delta <= i.delta (with at least one strict)
            if (values[j, 0] >= values[i, 0] and values[j, 1] <= values[i, 1] and
                (values[j, 0] > values[i, 0] or values[j, 1] < values[i, 1])):
                is_pareto[i] = False
                break
    
    return df[is_pareto].copy()
```

### Efficient Alternative (sort-based)

```python
def find_pareto_frontier_fast(df, maximize_col='F1', minimize_col='delta'):
    """Efficient O(n log n) for 2D Pareto frontier."""
    df_sorted = df.sort_values(maximize_col, ascending=False).reset_index(drop=True)
    
    pareto_indices = []
    min_delta_so_far = float('inf')
    
    for idx, row in df_sorted.iterrows():
        if row[minimize_col] < min_delta_so_far:
            pareto_indices.append(idx)
            min_delta_so_far = row[minimize_col]
    
    return df_sorted.loc[pareto_indices].copy()
```

**Note on ties**: The sort-based approach needs care with ties in F1. When multiple points share the same F1, only the one with the smallest delta should survive (unless it's also dominated). A safe approach:

```python
def find_pareto_frontier_safe(df, maximize_col='F1', minimize_col='delta'):
    # Sort by F1 descending, then delta ascending for tie-breaking
    df_sorted = df.sort_values(
        [maximize_col, minimize_col], 
        ascending=[False, True]
    ).reset_index(drop=True)
    
    pareto_indices = []
    min_delta_so_far = float('inf')
    
    for idx in range(len(df_sorted)):
        if df_sorted.loc[idx, minimize_col] < min_delta_so_far:
            pareto_indices.append(idx)
            min_delta_so_far = df_sorted.loc[idx, minimize_col]
    
    return df_sorted.loc[pareto_indices].copy()
```

### Filtering Before Pareto Extraction
Only include results where average F1 > 0.5 before finding the Pareto frontier.