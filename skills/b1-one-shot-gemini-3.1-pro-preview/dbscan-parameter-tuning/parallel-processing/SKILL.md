---
name: parallel-processing
description: Parallel processing with joblib to speed up computationally intensive parameter grid searches.
---

# Parallel Processing with joblib

`joblib` is highly optimized for Python parallel processing, especially for numpy arrays and independent tasks like grid search.

## Setup
```bash
pip install joblib
```

## Usage
```python
from joblib import Parallel, delayed

def evaluate_params(param1, param2):
    # Intensive computation
    return param1 + param2, param1 * param2

params_list = [(1, 2), (3, 4), (5, 6)]

results = Parallel(n_jobs=-1)(
    delayed(evaluate_params)(p1, p2) for p1, p2 in params_list
)
```
This pattern perfectly fits hyperparameter grid searches.
