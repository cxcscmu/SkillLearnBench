---
name: custom-distance-metrics
description: Define custom distance/similarity metrics for clustering and ML algorithms. Use when working with DBSCAN, sklearn, or scipy distance functions with application-specific metrics.
---

# Custom Distance Metrics for Clustering

## When to Use

Use this skill whenever you need a non-standard distance metric for DBSCAN, hierarchical clustering, or any sklearn/scipy algorithm that accepts a `metric` parameter. Typical cases: weighted axes, domain-specific similarity, or anisotropic distance.

## DBSCAN with Custom Metrics

DBSCAN accepts a callable metric via the `metric` parameter. The callable receives two 1-D arrays (points) and must return a scalar distance.

```python
from sklearn.cluster import DBSCAN
import numpy as np

def weighted_euclidean(a, b, w):
    """Weighted Euclidean: d = sqrt((w*dx)^2 + ((2-w)*dy)^2)"""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return np.sqrt((w * dx) ** 2 + ((2 - w) * dy) ** 2)

# Use functools.partial or a closure to bind extra parameters
from functools import partial
metric_fn = partial(weighted_euclidean, w=1.2)

db = DBSCAN(eps=10, min_samples=5, metric=metric_fn)
labels = db.fit_predict(points)  # points: array of shape (n, 2)
```

## Performance Considerations

- Custom callable metrics are slower than built-in metrics because sklearn cannot use optimized C routines.
- For large datasets, precompute the full distance matrix and pass `metric='precomputed'`:

```python
from scipy.spatial.distance import pdist, squareform

# Precompute pairwise distances
dists = pdist(points, metric=metric_fn)
dist_matrix = squareform(dists)

db = DBSCAN(eps=10, min_samples=5, metric='precomputed')
labels = db.fit_predict(dist_matrix)
```

- Precomputed matrices use O(n^2) memory but are significantly faster when DBSCAN is called repeatedly on the same data or when the custom metric is expensive.

## Extracting Cluster Centroids

After clustering, compute centroids from the original coordinates (not the distance matrix):

```python
centroids = []
for label in set(labels):
    if label == -1:
        continue  # skip noise
    mask = labels == label
    centroid = points[mask].mean(axis=0)
    centroids.append(centroid)
```
