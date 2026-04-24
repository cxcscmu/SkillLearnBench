---
name: parallel-processing
description: Parallel processing with joblib for grid search and batch computations. Use when speeding up computationally intensive tasks across multiple CPU cores.
---

# Parallel Processing with joblib

## When to Use

Use this skill when you need to parallelize independent computations — grid search evaluations, batch processing, cross-validation folds, or any embarrassingly parallel workload.

## Basic Pattern

```python
from joblib import Parallel, delayed

def evaluate(param1, param2):
    """Single evaluation — must be a pure function."""
    # ... computation ...
    return result

# Generate all parameter combinations
from itertools import product
params = list(product(range_1, range_2))

# Run in parallel
results = Parallel(n_jobs=-1, verbose=1)(
    delayed(evaluate)(p1, p2) for p1, p2 in params
)
```

## Key Parameters

- `n_jobs=-1`: Use all available cores
- `n_jobs=-2`: Use all cores minus one
- `verbose=1`: Show progress bar
- `backend='loky'` (default): Process-based, best for CPU-bound work
- `prefer='threads'`: Thread-based, better for I/O-bound or when sharing large read-only data

## Sharing Read-Only Data

For large datasets shared across workers, avoid copying by passing data outside the delayed call:

```python
import numpy as np

# Large shared data — read by all workers
big_array = np.load('data.npy')

def process(idx, data=big_array):
    # data is shared, not copied (with loky backend)
    return data[idx].sum()

results = Parallel(n_jobs=-1)(delayed(process)(i) for i in range(1000))
```

## Grid Search Pattern

```python
from itertools import product

param_grid = {
    'eps': [4, 6, 8, 10],
    'min_samples': [3, 5, 7],
    'weight': [0.9, 1.0, 1.1]
}

combos = list(product(*param_grid.values()))

def evaluate_combo(combo):
    eps, min_samples, weight = combo
    # ... run clustering, compute metrics ...
    return {'eps': eps, 'min_samples': min_samples, 'weight': weight, 'score': score}

results = Parallel(n_jobs=-1, verbose=5)(
    delayed(evaluate_combo)(c) for c in combos
)

import pandas as pd
results_df = pd.DataFrame(results)
```
