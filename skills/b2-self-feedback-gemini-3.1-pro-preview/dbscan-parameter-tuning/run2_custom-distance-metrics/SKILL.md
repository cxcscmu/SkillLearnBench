---
name: run2_custom-distance-metrics
description: How to compute precomputed distance matrices for custom distance metrics in Scikit-Learn DBSCAN.
---

# Fast Custom Distance Metrics in Scikit-Learn

To effectively use custom distance metrics with DBSCAN, it is highly recommended to precompute the distance matrix. Python scalar functions passed to `metric` are typically too slow. Instead, use numpy broadcasting to compute the matrix.

## Installation
Ensure you have scikit-learn and numpy installed:
`pip install scikit-learn numpy`

## Usage
```python
import numpy as np
from sklearn.cluster import DBSCAN

def custom_dist_matrix(points, w):
    """
    Computes a distance matrix for N points.
    d(a, b) = sqrt((w * Δx)^2 + ((2 - w) * Δy)^2)
    """
    points = np.asarray(points)
    # Broadcasting to find all pairwise differences
    dx = w * (points[:, 0:1] - points[:, 0:1].T)
    dy = (2 - w) * (points[:, 1:2] - points[:, 1:2].T)
    return np.sqrt(dx**2 + dy**2)

# X is an N by 2 array of points
# dist_matrix = custom_dist_matrix(X, w=1.5)
# db = DBSCAN(eps=10, min_samples=5, metric='precomputed').fit(dist_matrix)
```
