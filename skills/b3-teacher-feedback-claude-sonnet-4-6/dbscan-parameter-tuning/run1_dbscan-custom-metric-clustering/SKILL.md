---
name: dbscan-custom-metric-clustering
description: How to run DBSCAN with a custom anisotropic distance metric using sklearn, including defining callable metrics and computing cluster centroids from labeled output.
---

# DBSCAN with Custom Distance Metric

## Overview

`sklearn.cluster.DBSCAN` accepts a `metric` parameter that can be a callable. This enables custom distance functions beyond standard Euclidean distance.

## Custom Anisotropic Metric

The shape-weighted distance is:

```
d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)
```

Where `w = shape_weight`. When `w=1`, this is standard Euclidean distance.

## Implementation

```python
import numpy as np
from sklearn.cluster import DBSCAN

def make_metric(shape_weight):
    w = shape_weight
    def metric(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)
    return metric

def run_dbscan(points, epsilon, min_samples, shape_weight):
    """
    points: np.ndarray of shape (N, 2), columns [x, y]
    Returns: cluster labels array (length N), -1 = noise
    """
    if len(points) == 0:
        return np.array([])
    
    metric = make_metric(shape_weight)
    db = DBSCAN(eps=epsilon, min_samples=min_samples, metric=metric)
    labels = db.fit_predict(points)
    return labels

def compute_centroids(points, labels):
    """
    Compute centroids for each cluster (excluding noise label -1).
    Returns: list of (cx, cy) tuples
    """
    centroids = []
    unique_labels = set(labels) - {-1}
    for label in unique_labels:
        mask = labels == label
        centroid = points[mask].mean(axis=0)
        centroids.append(centroid)
    return centroids  # list of np.array([cx, cy])
```

## Key Notes

- `metric='precomputed'` with a distance matrix is an alternative but slower for large grids
- Using a callable metric disables the ball-tree/kd-tree optimization; DBSCAN uses brute force — acceptable for moderate N
- Noise points (label `-1`) are excluded from centroid computation
- If all points are noise or input is empty, `centroids` is an empty list