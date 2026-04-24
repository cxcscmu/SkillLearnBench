---
name: run2_pareto-frontier
description: Computing the Pareto frontier for multi-objective optimization (maximize F1, minimize delta) with correct dominance handling and output formatting.
---

# Pareto Frontier for DBSCAN Hyperparameter Selection

## Objective

Find Pareto-optimal hyperparameter combinations that:
- **Maximize** F1 score (agreement with expert labels)
- **Minimize** delta (average distance between matched centroids and experts)

## Using paretoset Library

```python
from paretoset import paretoset
import pandas as pd

# Filter first: only keep meaningful clustering results
filtered = results_df[results_df['F1'] > 0.5].copy()

# Compute Pareto mask
# sense: 'max' for F1 (maximize), 'min' for delta (minimize)
mask = paretoset(filtered[['F1', 'delta']], sense=['max', 'min'])
pareto_df = filtered[mask].copy()
```

## Manual Pareto Frontier (fallback)

```python
import numpy as np

def pareto_mask(f1_vals, delta_vals):
    """
    A point is Pareto-optimal if no other point dominates it.
    Point j dominates point i if:
      j.F1 >= i.F1 AND j.delta <= i.delta AND (j.F1 > i.F1 OR j.delta < i.delta)
    """
    n = len(f1_vals)
    is_efficient = np.ones(n, dtype=bool)
    for i in range(n):
        if not is_efficient[i]:
            continue
        # Check if any other point dominates i
        for j in range(n):
            if i == j or not is_efficient[j]:
                continue
            if (f1_vals[j] >= f1_vals[i] and delta_vals[j] <= delta_vals[i] and
                    (f1_vals[j] > f1_vals[i] or delta_vals[j] < delta_vals[i])):
                is_efficient[i] = False
                break
    return is_efficient
```

## Output Format

```python
# Round values per spec
pareto_df['F1'] = pareto_df['F1'].round(5)
pareto_df['delta'] = pareto_df['delta'].round(5)
pareto_df['shape_weight'] = pareto_df['shape_weight'].round(1)
pareto_df['min_samples'] = pareto_df['min_samples'].astype(int)
pareto_df['epsilon'] = pareto_df['epsilon'].astype(int)

# Save CSV
cols = ['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight']
pareto_df[cols].to_csv('/root/pareto_frontier.csv', index=False)
```

## Validation

- All Pareto points should have F1 > 0.5 (filtered beforehand)
- No point in the output should be dominated by another point in the output
- Higher epsilon generally → larger clusters, fewer FP/FN, higher F1 but higher delta
- Higher min_samples → stricter clustering, fewer spurious clusters
