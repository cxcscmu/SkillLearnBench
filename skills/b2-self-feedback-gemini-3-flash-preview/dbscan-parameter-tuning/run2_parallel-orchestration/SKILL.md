---
name: run2_parallel-orchestration
description: Structured approach to grid search with nested loops and parallelization.
---

# Parallel Orchestration for Hyperparameter Search

A structured way to iterate through multiple hyperparameters while optimizing for performance.

## Strategy

1. Loop through `shape_weight` (most expensive since it changes the distance metric).
2. For each `shape_weight`, precompute distance matrices for all images.
3. Parallelize the evaluation of `min_samples` and `epsilon` for that `shape_weight`.

```python
from joblib import Parallel, delayed

def process_weight(w, citsci_groups, expert_groups, all_images, ms_range, eps_range):
    # Precompute dist matrices
    dist_matrices = {img: precompute_distances(citsci_groups[img], w) 
                     for img in citsci_groups if img in expert_groups}
    
    results = []
    for ms in ms_range:
        for eps in eps_range:
            f1s, deltas = [], []
            for img in all_images:
                # ... evaluation logic ...
                f1s.append(f1)
                if not np.isnan(delta): deltas.append(delta)
            results.append({'F1': np.mean(f1s), 'delta': np.mean(deltas), ...})
    return results
```
