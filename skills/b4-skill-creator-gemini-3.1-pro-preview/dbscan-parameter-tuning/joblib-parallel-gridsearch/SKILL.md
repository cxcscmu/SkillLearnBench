---
name: joblib-parallel-gridsearch
description: Perform parallel grid search using joblib. Use this skill whenever a task requires optimizing multiple hyperparameters simultaneously across CPU cores.
---

# Parallel Grid Search with Joblib

Joblib is the standard library for multiprocessing in Python data science workloads.

## Basic Usage

```python
from joblib import Parallel, delayed
import itertools

def evaluate_params(param1, param2):
    # Perform expensive computation
    score = param1 + param2
    return {'p1': param1, 'p2': param2, 'score': score}

# Define grid
param_grid = list(itertools.product([1, 2, 3], [0.1, 0.2]))

# Run in parallel
results = Parallel(n_jobs=-1, verbose=10)(
    delayed(evaluate_params)(p1, p2) for p1, p2 in param_grid
)
```

## Tips
- `n_jobs=-1` uses all available CPU cores.
- Pre-load data in the main process before spawning parallel workers to save memory.
- Pass required shared data as arguments to your delayed function.
