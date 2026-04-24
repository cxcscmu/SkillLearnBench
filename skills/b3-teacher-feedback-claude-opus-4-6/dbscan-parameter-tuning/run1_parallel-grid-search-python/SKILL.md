---
name: parallel-grid-search-python
description: How to parallelize a grid search over hyperparameter combinations in Python using joblib or multiprocessing for CPU-bound tasks like DBSCAN clustering.
---

## Parallel Grid Search in Python

### Grid Construction

```python
import itertools
import numpy as np

min_samples_range = list(range(3, 10))           # 3-9: 7 values
epsilon_range = list(range(4, 25, 2))              # 4-24 step 2: 11 values
shape_weight_range = [round(0.9 + 0.1*i, 1) for i in range(11)]  # 0.9-1.9: 11 values

all_combos = list(itertools.product(min_samples_range, epsilon_range, shape_weight_range))
# Total: 7 * 11 * 11 = 847 combinations
```

### Using joblib for Parallelization

```python
from joblib import Parallel, delayed

def evaluate_params(min_samples, epsilon, shape_weight, citsci_df, expert_df):
    """Evaluate one hyperparameter combination across all images."""
    # ... run DBSCAN for each image, compute F1 and delta ...
    return {
        'min_samples': min_samples,
        'epsilon': epsilon,
        'shape_weight': shape_weight,
        'F1': avg_f1,
        'delta': avg_delta
    }

results = Parallel(n_jobs=-1, verbose=10)(
    delayed(evaluate_params)(ms, eps, sw, citsci_df, expert_df)
    for ms, eps, sw in all_combos
)
```

### Performance Tips

1. **Precompute per-image data**: Group citizen science points by `file_rad` once, outside the loop
2. **Use precomputed distance matrices**: For each image's points, compute the distance matrix inside the evaluation
3. **Avoid passing large DataFrames**: Instead, pass pre-grouped dictionaries
4. **n_jobs=-1**: Uses all available CPU cores

```python
# Pre-group data for efficiency
citsci_grouped = {}
for file_rad, group in citsci_df.groupby('file_rad'):
    citsci_grouped[file_rad] = group[['x', 'y']].values

expert_grouped = {}
for file_rad, group in expert_df.groupby('file_rad'):
    expert_grouped[file_rad] = group[['x', 'y']].values

unique_images = list(expert_grouped.keys())  # Loop over expert images
```

### Memory Considerations
- With 847 combinations and many images, memory can be an issue
- Distance matrices are O(n²) per image — but citizen science annotations per image are typically small
- Consider batching if memory is tight