---
name: grid-search-parallelization
description: Running a multi-parameter grid search efficiently using parallel processing to find optimal hyperparameters.
---

When searching a large hyperparameter space (like combinations of `min_samples`, `epsilon`, and `shape_weight`), `joblib` or `multiprocessing` can significantly reduce execution time.

**Workflow:**
1.  Generate a list of all parameter combinations using `itertools.product`.
2.  Define a worker function that takes one combination, processes all images, and returns the average metrics.
3.  Use a parallel map to distribute the combinations across CPU cores.

```python
from itertools import product
from joblib import Parallel, delayed

def evaluate_params(params):
    min_s, eps, w = params
    # ... logic to group images, cluster, match, and calculate averages ...
    return {'F1': avg_f1, 'delta': avg_delta, 'min_samples': min_s, 'epsilon': eps, 'shape_weight': w}

# Define ranges
space = list(product(range(3, 10), range(4, 25, 2), np.arange(0.9, 2.0, 0.1)))
results = Parallel(n_jobs=-1)(delayed(evaluate_params)(p) for p in space)
```