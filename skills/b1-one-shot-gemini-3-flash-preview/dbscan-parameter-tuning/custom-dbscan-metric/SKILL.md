---
name: custom-dbscan-metric
description: Implementation of a custom distance metric for DBSCAN clustering using scipy and sklearn.
---

# Custom Distance Metric for DBSCAN

When using DBSCAN with a non-standard distance metric, you can either provide a callable to the `metric` parameter or precompute the distance matrix.

## Mathematical Formulation
For the Mars cloud task, the distance is defined as:
`d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)`

## Implementation using scipy.spatial.distance.cdist
Precomputing the distance matrix is often more efficient for grid searches if the metric is reused or if you want to use `sklearn.cluster.DBSCAN`.

```python
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN

def custom_metric(p1, p2, w):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)

# Vectorized version for efficiency
def precompute_custom_distance(X, w):
    # X is (N, 2)
    # Using cdist with a custom lambda can be slow, 
    # better to use vectorized numpy if possible.
    X_weighted = X * np.array([w, 2 - w])
    # Note: the formula is sqrt((w*dx)^2 + ((2-w)*dy)^2)
    # which is equivalent to standard Euclidean distance on weighted coordinates
    return cdist(X_weighted, X_weighted, metric='euclidean')

# Using DBSCAN with precomputed metric
# dist_matrix = precompute_custom_distance(X, w)
# db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
# labels = db.fit_predict(dist_matrix)
```

## Considerations
- `epsilon` in DBSCAN will be compared against the distances produced by this custom metric.
- Ensure `shape_weight` (w) is applied correctly to the coordinates before distance calculation if using standard Euclidean as a shortcut.
