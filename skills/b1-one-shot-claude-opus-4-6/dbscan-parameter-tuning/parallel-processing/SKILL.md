---
name: parallel-processing
description: Parallel processing with joblib for grid search and batch computations across multiple CPU cores.
---

# Parallel Processing with joblib

## Grid Search Parallelization

```python
from joblib import Parallel, delayed
import itertools

def evaluate_params(min_samples, epsilon, shape_weight, citsci_grouped, expert_grouped, all_images):
    # ... evaluate one hyperparameter combination
    return f1_avg, delta_avg, min_samples, epsilon, shape_weight

param_grid = list(itertools.product(
    range(3, 10),           # min_samples
    range(4, 25, 2),        # epsilon
    [round(0.9 + i*0.1, 1) for i in range(11)]  # shape_weight
))

results = Parallel(n_jobs=-1)(
    delayed(evaluate_params)(ms, eps, sw, citsci_grouped, expert_grouped, all_images)
    for ms, eps, sw in param_grid
)
```

## Key Points
- `n_jobs=-1` uses all available cores
- `delayed()` wraps the function for lazy evaluation
- Each call should be independent (no shared mutable state)
- Pass pre-grouped DataFrames to avoid redundant groupby in each worker
