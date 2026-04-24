---
name: parallel-grid-search
description: Parallelize hyperparameter grid search using joblib for efficient multi-core execution.
---

# Parallel Grid Search

## Overview
Use joblib to parallelize expensive computations across multiple CPU cores, significantly speeding up grid search over hyperparameter combinations.

## Installation

```bash
pip install joblib scikit-learn
```

## Basic Pattern

```python
from joblib import Parallel, delayed
import itertools

def evaluate_hyperparams(hp_combination, data, evaluation_func):
    """Evaluate a single hyperparameter combination."""
    result = evaluation_func(hp_combination, data)
    return {**hp_combination, **result}

# Define hyperparameter grid
param_grid = {
    'min_samples': [3, 4, 5, 6, 7, 8, 9],
    'epsilon': [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
    'shape_weight': [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
}

# Generate all combinations
combinations = [
    {k: v for k, v in zip(param_grid.keys(), vals)}
    for vals in itertools.product(*param_grid.values())
]

# Parallel evaluation
n_jobs = -1  # Use all available cores
results = Parallel(n_jobs=n_jobs, verbose=10)(
    delayed(evaluate_hyperparams)(combo, data, eval_func)
    for combo in combinations
)
```

## Advanced: Batching and Progress

```python
from tqdm import tqdm

def parallel_grid_search_batched(param_grid, data, evaluation_func, n_jobs=-1):
    """
    Perform parallel grid search with progress tracking.

    Args:
        param_grid: Dictionary of parameter names to lists of values
        data: Dataset to evaluate on
        evaluation_func: Function that takes (hyperparams_dict, data) -> results_dict
        n_jobs: Number of parallel jobs (-1 = all cores)

    Returns:
        List of result dictionaries
    """
    # Generate all combinations
    combinations = [
        {k: v for k, v in zip(param_grid.keys(), vals)}
        for vals in itertools.product(*param_grid.values())
    ]

    # Parallel evaluation with progress bar
    results = Parallel(n_jobs=n_jobs)(
        delayed(evaluation_func)(combo, data)
        for combo in tqdm(combinations, desc="Grid Search", total=len(combinations))
    )

    return results
```

## joblib Best Practices

### Memory-Efficient Processing

```python
# Use batch_size for memory efficiency
results = Parallel(n_jobs=-1, batch_size='auto')(
    delayed(expensive_function)(item)
    for item in data
)
```

### Controlling Verbosity

```python
# verbose=10 prints progress every 10 jobs
# verbose=0 is silent, verbose=1 prints at start/end
results = Parallel(n_jobs=-1, verbose=10)(
    delayed(task)(x) for x in items
)
```

### Backend Selection

```python
# Default is 'loky' (good for most tasks)
# 'threading' is lighter but can have GIL issues
# 'processes' spawns new processes

results = Parallel(n_jobs=-1, backend='loky')(
    delayed(task)(x) for x in items
)
```

## Collecting Results into DataFrame

```python
import pandas as pd

results = Parallel(n_jobs=-1)(
    delayed(evaluate_hyperparams)(combo, data, eval_func)
    for combo in combinations
)

# Convert to DataFrame
results_df = pd.DataFrame(results)

# Filter and sort
filtered = results_df[results_df['f1'] > 0.5].sort_values('f1', ascending=False)
```

## Notes
- joblib handles pickling of functions and data automatically
- For very large datasets, consider passing data references rather than copies
- Use `n_jobs=-1` to use all cores; use `-2` to leave one core free
- Progress tracking requires `tqdm` package
