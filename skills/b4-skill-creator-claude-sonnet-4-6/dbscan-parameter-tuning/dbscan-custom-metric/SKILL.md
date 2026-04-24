---
name: dbscan-custom-metric
description: >
  How to run DBSCAN clustering with a custom anisotropic distance metric using
  sklearn and scipy. Use this skill whenever the user needs to cluster spatial
  points with a weighted or shape-adjusted distance, such as attenuating x vs y
  distances differently, or when DBSCAN needs a non-Euclidean metric defined as
  a callable. Covers cluster centroid computation and noise-point handling.
---

# DBSCAN with Custom Distance Metric

## Overview

`sklearn.cluster.DBSCAN` accepts `metric='precomputed'` or a callable. For
runtime-efficient custom metrics, use `metric='precomputed'` with a
precomputed distance matrix, or pass a Python callable directly.

## Custom Anisotropic Metric

For the shape-weighted metric `d(a, b) = sqrt((w*Δx)² + ((2-w)*Δy)²)`:

```python
import numpy as np
from sklearn.cluster import DBSCAN

def make_metric(shape_weight):
    w = shape_weight
    def metric(a, b):
        dx = w * (a[0] - b[0])
        dy = (2 - w) * (a[1] - b[1])
        return np.sqrt(dx*dx + dy*dy)
    return metric

def run_dbscan(points_xy, epsilon, min_samples, shape_weight):
    """points_xy: np.ndarray of shape (N, 2)"""
    if len(points_xy) < min_samples:
        return np.array([])  # no clusters possible

    metric = make_metric(shape_weight)
    db = DBSCAN(eps=epsilon, min_samples=min_samples, metric=metric)
    labels = db.fit_predict(points_xy)
    return labels
```

## Computing Cluster Centroids

After fitting, compute the mean (x, y) of each non-noise cluster:

```python
def compute_centroids(points_xy, labels):
    """Returns list of (cx, cy) for each unique cluster label >= 0."""
    unique_labels = set(labels) - {-1}
    centroids = []
    for lbl in sorted(unique_labels):
        mask = labels == lbl
        cx = points_xy[mask, 0].mean()
        cy = points_xy[mask, 1].mean()
        centroids.append((cx, cy))
    return centroids  # list of (x, y) tuples
```

## Performance Notes

- For large datasets, prefer `metric='precomputed'` with scipy's `cdist`:
  ```python
  from scipy.spatial.distance import cdist
  D = cdist(points_xy, points_xy, metric=metric)
  db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
  labels = db.fit_predict(D)
  ```
- For grid search parallelism, pass the metric as a closure (not a lambda
  that captures mutable state).

## Edge Cases

- If fewer than `min_samples` points exist: return no clusters (empty labels).
- If all points are labeled `-1` (noise): no clusters found.
- Empty `points_xy` array: skip DBSCAN, return empty centroids.
