---
name: parallel-grid-search
description: >
  How to parallelize hyperparameter grid search using joblib. Use this skill
  whenever the user needs to evaluate many hyperparameter combinations
  (e.g., DBSCAN epsilon, min_samples, shape_weight) efficiently across CPU
  cores. Covers joblib.Parallel, parameter grid generation with itertools,
  and collecting results into a DataFrame.
---

# Parallel Grid Search with joblib

## Overview

`joblib.Parallel` distributes independent function calls across CPU cores.
Use it for grid search where each hyperparameter combination is independent.

## Basic Pattern

```python
import itertools
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

def evaluate_params(param_combo, data):
    """Evaluate one hyperparameter combination. Must be picklable."""
    min_samples, epsilon, shape_weight = param_combo
    # ... run DBSCAN, compute metrics ...
    return {'F1': f1, 'delta': delta,
            'min_samples': min_samples, 'epsilon': epsilon,
            'shape_weight': shape_weight}

# Define search space
min_samples_range = range(3, 10)           # 3..9
epsilon_range = range(4, 26, 2)            # 4,6,...,24
shape_weight_range = np.arange(0.9, 2.0, 0.1)  # 0.9..1.9

param_grid = list(itertools.product(
    min_samples_range, epsilon_range, shape_weight_range
))

# Run in parallel (n_jobs=-1 uses all cores)
results = Parallel(n_jobs=-1, verbose=1)(
    delayed(evaluate_params)(combo, data)
    for combo in param_grid
)

df = pd.DataFrame(results)
```

## Pickling Requirements

Functions passed to `Parallel` must be picklable. Avoid:
- Lambda functions (use `def` or `functools.partial`)
- Closures over non-picklable objects (e.g., open file handles)
- Module-level imports inside nested functions (import at top of file)

## Passing Shared Data

For large read-only datasets, pass them as arguments to avoid re-serialization
overhead. joblib uses shared memory for numpy arrays when `prefer='threads'`,
but `prefer='processes'` (default) forks the process so data is copied once.

```python
# Efficient: pass pre-grouped data dict
grouped_citsci = {img: df[df.file_rad == img][['x','y']].values
                  for img in all_images}

results = Parallel(n_jobs=-1)(
    delayed(evaluate_params)(combo, grouped_citsci, expert_grouped)
    for combo in param_grid
)
```

## Controlling Parallelism

| Parameter | Effect |
|-----------|--------|
| `n_jobs=-1` | Use all available CPU cores |
| `n_jobs=4` | Use exactly 4 cores |
| `verbose=10` | Print progress every ~10% |
| `backend='loky'` | Default; robust process-based |
| `batch_size='auto'` | Auto-tune batch size |

## Collecting and Filtering Results

```python
df = pd.DataFrame([r for r in results if r is not None])
df_filtered = df[df['F1'] > 0.5]
```

## Shape Weight Rounding

Float ranges from `np.arange` accumulate floating-point errors. Round after
generation:

```python
shape_weight_range = np.round(np.arange(0.9, 2.0, 0.1), 1)
```
