---
name: dbscan-custom-metric
description: Implementing custom distance metrics for DBSCAN in scikit-learn for specialized coordinate-based clustering.
---

### Custom Distance Logic
Standard DBSCAN in `scikit-learn` accepts a `metric` argument. To implement the specified weighted Euclidean distance:
`d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)`

You should define a function:
```python
import numpy as np

def get_custom_metric(w):
    def distance(u, v):
        # u and v are coordinate pairs [x, y]
        dx = (u[0] - v[0]) * w
        dy = (u[1] - v[1]) * (2 - w)
        return np.sqrt(dx**2 + dy**2)
    return distance
```
Pass this to the DBSCAN constructor: `DBSCAN(eps=epsilon, min_samples=min_samples, metric=get_custom_metric(shape_weight))`.

*Note:* Since `metric='precomputed'` is often faster for large datasets, consider pre-calculating the distance matrix if memory allows, or pass the callable directly if the dataset size per image is small.