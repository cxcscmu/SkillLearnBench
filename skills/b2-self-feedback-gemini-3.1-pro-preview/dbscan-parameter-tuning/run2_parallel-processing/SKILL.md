---
name: run2_parallel-processing
description: Advanced usage of joblib for parallel execution of grid search tasks, including result flattening.
---

# Parallel Processing with Joblib (Advanced)

When running grid searches where each worker computes multiple results, Joblib returns a list of lists. You can easily flatten this to create a DataFrame.

## Installation
Ensure you have joblib and pandas installed:
`pip install joblib pandas`

## Usage
```python
import pandas as pd
from joblib import Parallel, delayed
import itertools

def evaluate_subset(param_group):
    # param_group might evaluate multiple things internally
    results = []
    for param in param_group:
        results.append({'param': param, 'score': param * 2})
    return results

param_groups = [[1, 2], [3, 4], [5, 6]]

# Returns list of lists
all_results = Parallel(n_jobs=-1)(
    delayed(evaluate_subset)(group) for group in param_groups
)

# Flatten results
flat_results = [item for sublist in all_results for item in sublist]

# Convert to DataFrame
df = pd.DataFrame(flat_results)
```
