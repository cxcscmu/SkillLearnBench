---
name: parallel-grid-search
description: Parallelize hyperparameter grid searches using joblib for CPU-bound tasks like DBSCAN clustering evaluation loops.
---

# Parallel Grid Search with joblib

## Overview

`joblib` provides easy parallelism via `Parallel` and `delayed`. Ideal for embarrassingly parallel grid searches where each parameter combination is independent.

## Installation

```bash
pip install joblib
```

## Basic Pattern

```python
from joblib import Parallel, delayed
import itertools

def evaluate_params(param_combo, data):
    """Evaluate one parameter combination. Must be picklable (no lambdas)."""
    epsilon, min_samples, shape_weight = param_combo
    # ... run DBSCAN, compute metrics ...
    return {'epsilon': epsilon, 'min_samples': min_samples,
            'shape_weight': shape_weight, 'F1': f1, 'delta': delta}

# Define search space
epsilons = range(4, 25, 2)       # 4,6,8,...,24
min_samples_range = range(3, 10) # 3,4,...,9
shape_weights = [round(0.9 + 0.1*i, 1) for i in range(11)]  # 0.9..1.9

all_combos = list(itertools.product(epsilons, min_samples_range, shape_weights))

# Run in parallel (n_jobs=-1 uses all available cores)
results = Parallel(n_jobs=-1, verbose=1)(
    delayed(evaluate_params)(combo, data)
    for combo in all_combos
)

import pandas as pd
results_df = pd.DataFrame(results)
```

## Avoiding Pickling Issues

joblib pickles arguments, so avoid:
- Lambda functions as metric arguments
- Local closures with complex state

**Good:** use module-level functions or classes with `__call__`:

```python
# BAD: lambda not picklable across processes
metric = lambda a, b: np.linalg.norm(a - b)

# GOOD: named function
def euclidean(a, b):
    return np.linalg.norm(a - b)

# GOOD: class instance
class WeightedMetric:
    def __init__(self, w):
        self.w = w
    def __call__(self, a, b):
        dx, dy = a[0]-b[0], a[1]-b[1]
        return np.sqrt((self.w*dx)**2 + ((2-self.w)*dy)**2)
```

## Precomputing Shared Data

Pass shared read-only data as arguments (joblib uses copy-on-write with fork):

```python
def evaluate_one(combo, citsci_groups, expert_groups, all_images):
    eps, ms, sw = combo
    # citsci_groups and expert_groups are dicts: {file_rad -> np.array}
    ...

# Pre-group data outside parallel loop
citsci_groups = {k: v[['x','y']].values for k, v in citsci.groupby('file_rad')}
expert_groups = {k: v[['x','y']].values for k, v in expert.groupby('file_rad')}
all_images = expert['file_rad'].unique()

results = Parallel(n_jobs=-1)(
    delayed(evaluate_one)(combo, citsci_groups, expert_groups, all_images)
    for combo in all_combos
)
```

## Choosing n_jobs

- `n_jobs=-1`: use all CPU cores
- `n_jobs=-2`: use all but one core (leave one for OS)
- `n_jobs=4`: use exactly 4 cores

## Progress Tracking

```python
from joblib import Parallel, delayed
from tqdm import tqdm

# With tqdm progress bar
results = Parallel(n_jobs=-1)(
    delayed(evaluate_one)(combo, data)
    for combo in tqdm(all_combos)
)
```

## Backend Options

```python
# Default 'loky' backend: robust, works across platforms
Parallel(n_jobs=-1, backend='loky')(...)

# 'multiprocessing': use Python's multiprocessing
Parallel(n_jobs=-1, backend='multiprocessing')(...)

# 'threading': for I/O-bound tasks (GIL-free libraries like numpy)
Parallel(n_jobs=-1, backend='threading')(...)
```

## Full Grid Search Template

```python
import numpy as np
import pandas as pd
import itertools
from joblib import Parallel, delayed
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import cdist


def make_weighted_metric(w):
    class M:
        def __init__(self, w): self.w = w
        def __call__(self, a, b):
            return np.sqrt((self.w*(a[0]-b[0]))**2 + ((2-self.w)*(a[1]-b[1]))**2)
    return M(w)


def evaluate_combo(combo, citsci_groups, expert_groups, all_images):
    eps, ms, sw = combo
    metric = make_weighted_metric(sw)

    f1_list, delta_list = [], []
    for img in all_images:
        cit = citsci_groups.get(img, np.empty((0,2)))
        exp = expert_groups.get(img, np.empty((0,2)))

        if len(cit) == 0:
            f1_list.append(0.0); delta_list.append(np.nan); continue

        labels = DBSCAN(eps=eps, min_samples=ms, metric=metric).fit_predict(cit)
        unique = set(labels) - {-1}
        if not unique:
            f1_list.append(0.0); delta_list.append(np.nan); continue

        centroids = np.array([cit[labels==l].mean(axis=0) for l in unique])
        # ... compute F1 and delta via greedy matching ...
        f1_list.append(f1); delta_list.append(delta)

    avg_f1 = np.mean(f1_list)
    valid_d = [d for d in delta_list if not np.isnan(d)]
    avg_delta = np.mean(valid_d) if valid_d else np.nan
    return {'F1': avg_f1, 'delta': avg_delta, 'epsilon': eps,
            'min_samples': ms, 'shape_weight': sw}


# Run grid search
combos = list(itertools.product(range(4,25,2), range(3,10),
                                 [round(0.9+0.1*i,1) for i in range(11)]))
results = Parallel(n_jobs=-1)(
    delayed(evaluate_combo)(c, citsci_g, expert_g, images) for c in combos
)
df = pd.DataFrame(results)
df = df[df['F1'] > 0.5]
```
