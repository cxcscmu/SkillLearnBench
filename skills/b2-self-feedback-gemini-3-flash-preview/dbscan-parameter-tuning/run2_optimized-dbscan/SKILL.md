---
name: run2_optimized-dbscan
description: Efficient DBSCAN implementation by caching distance matrices for repeated hyperparameter evaluations.
---

# Optimized DBSCAN for Grid Search

When performing grid search over `eps` and `min_samples` while keeping the distance metric (and its parameters like `shape_weight`) constant, it is much faster to precompute the distance matrix once.

## Caching Strategy

```python
import numpy as np
from sklearn.cluster import DBSCAN

def precompute_distances(points, w):
    """Precompute distance matrix for a specific shape_weight."""
    x, y = points[:, 0], points[:, 1]
    dx = x[:, np.newaxis] - x[np.newaxis, :]
    dy = y[:, np.newaxis] - y[np.newaxis, :]
    return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)

def cluster_with_precomputed(dist_matrix, points, eps, min_samples):
    """Cluster using precomputed distances and return centroids."""
    if len(points) < min_samples:
        return np.array([])
    
    db = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
    labels = db.fit_predict(dist_matrix)
    
    unique_labels = set(labels) - {-1}
    if not unique_labels:
        return np.array([])
    
    centroids = [np.mean(points[labels == l], axis=0) for l in unique_labels]
    return np.array(centroids)
```
