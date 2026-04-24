---
name: run2_pareto-optimization
description: Finding the Pareto frontier for multi-objective optimization using dominance conditions.
---

# Pareto Optimization (Dominance Condition)

When you need to optimize multiple conflicting objectives (e.g., maximizing F1, minimizing error), you can identify the Pareto frontier by explicitly checking if a point is "dominated" by another point.

## Installation
Ensure you have numpy and pandas installed:
`pip install numpy pandas`

## Usage
```python
import numpy as np
import pandas as pd

def get_pareto_frontier(df, obj_max_cols, obj_min_cols):
    """
    Finds non-dominated rows in a DataFrame.
    """
    pareto_mask = np.ones(len(df), dtype=bool)
    
    for i in range(len(df)):
        # Assume self is not dominated unless proven otherwise
        row_i = df.iloc[i]
        
        # Check against all other rows
        better_or_equal = np.ones(len(df), dtype=bool)
        strictly_better = np.zeros(len(df), dtype=bool)
        
        for col in obj_max_cols:
            better_or_equal &= (df[col] >= row_i[col])
            strictly_better |= (df[col] > row_i[col])
            
        for col in obj_min_cols:
            better_or_equal &= (df[col] <= row_i[col])
            strictly_better |= (df[col] < row_i[col])
            
        # If any other point is better or equal in all, AND strictly better in at least one
        if np.any(better_or_equal & strictly_better):
            pareto_mask[i] = False
            
    return df[pareto_mask]

# pareto_df = get_pareto_frontier(results_df, ['F1'], ['delta'])
```
