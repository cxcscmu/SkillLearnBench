name: grid-search-parallel
description: Executing a grid search across multiple hyperparameters in parallel. Use this to speed up computationally intensive tasks like DBSCAN parameter sweeps.

# Parallel Grid Search

This skill covers how to efficiently iterate over a hyperparameter space using parallel processing.

## Grid Definition
Define the ranges for each parameter:
- `min_samples`: 3 to 9 (step 1)
- `epsilon`: 4 to 24 (step 2)
- `shape_weight`: 0.9 to 1.9 (step 0.1)

## Parallel Execution with Joblib
Use `joblib.Parallel` and `joblib.delayed` to distribute work.

```python
from joblib import Parallel, delayed
import itertools

def evaluate_params(params):
    min_samples, epsilon, shape_weight = params
    # ... evaluation logic ...
    return {'F1': avg_f1, 'delta': avg_delta, ...}

# Generate parameter grid
param_grid = list(itertools.product(min_samples_range, epsilon_range, shape_weight_range))

# Execute in parallel
results = Parallel(n_jobs=-1)(delayed(evaluate_params)(p) for p in param_grid)
```

## Data Management
- Pre-load data once and pass to the worker function or use global variables (if safe in the environment).
- Group annotations by image (`file_rad`) beforehand to avoid repeated filtering inside the loop.
