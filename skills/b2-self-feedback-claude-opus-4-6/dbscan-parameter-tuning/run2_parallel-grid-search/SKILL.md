---
name: run2_parallel-grid-search
description: Parallel DBSCAN hyperparameter grid search with joblib for Mars cloud clustering.
---

# Parallel Grid Search

## Optimization Tips
- Pre-group data by image outside the parallel loop
- Use `n_jobs=-1` for all cores
- Each evaluation function should be self-contained

```python
from joblib import Parallel, delayed
from itertools import product

params = list(product(min_samples_range, epsilon_range, shape_weight_range))

results = Parallel(n_jobs=-1)(
    delayed(evaluate_params)(ms, eps, sw) for ms, eps, sw in params
)
```

## Greedy Matching for Evaluation
- Compute Euclidean distance matrix between centroids and expert points
- Sort all pairs by distance ascending
- Greedily match closest unmatched pairs (max distance threshold = 100px)
- F1 = 2 * precision * recall / (precision + recall)
  - precision = matched / num_centroids
  - recall = matched / num_expert_points
