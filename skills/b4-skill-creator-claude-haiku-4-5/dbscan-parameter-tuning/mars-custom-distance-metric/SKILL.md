---
name: mars-custom-distance-metric
description: Implement weighted custom distance metric for DBSCAN clustering. Use this skill when working with DBSCAN on Mars cloud data where distances need to be weighted differently across x and y axes using a shape_weight parameter (w). The custom metric is d(a,b) = sqrt((w*Δx)² + ((2-w)*Δy)²), controlling whether x-distances or y-distances are attenuated.
---

# Mars Custom Distance Metric for DBSCAN

## Overview

The Mars cloud clustering task requires a custom distance metric that lets you control the relative weight of x-distances vs y-distances:

```
d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)
```

Where `w` (shape_weight) ranges from 0.9 to 1.9:
- w = 1.0: Standard Euclidean distance
- w > 1.0: Attenuates y-distances (prioritizes x-variation)
- w < 1.0: Attenuates x-distances (prioritizes y-variation)

## Implementation with scipy.spatial.distance

Use `scipy.spatial.distance.cdist` with a custom callable metric:

```python
from scipy.spatial.distance import cdist
import numpy as np

def shape_weighted_distance(u, v, w):
    """
    Compute shape-weighted distance between two points.

    u, v: 1D arrays of coordinates [x, y]
    w: shape_weight parameter (0.9 to 1.9)
    """
    dx = (w * (u[0] - v[0]))**2
    dy = ((2 - w) * (u[1] - v[1]))**2
    return np.sqrt(dx + dy)

# For use with scipy cdist (requires callable metric):
from functools import partial

metric = partial(shape_weighted_distance, w=shape_weight_value)
distance_matrix = cdist(points, points, metric=metric)
```

## Using with DBSCAN

sklearn's DBSCAN accepts a precomputed distance matrix:

```python
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform
from functools import partial

def shape_weighted_distance(u, v, w):
    dx = (w * (u[0] - v[0]))**2
    dy = ((2 - w) * (u[1] - v[1]))**2
    return np.sqrt(dx + dy)

# Compute full distance matrix with custom metric
metric_func = partial(shape_weighted_distance, w=shape_weight)
distance_matrix = cdist(points, points, metric=metric_func)

# Run DBSCAN with precomputed metric
clustering = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
labels = clustering.fit_predict(distance_matrix)
```

## Key Points

1. **Two-point vs pairwise distances**: Use `cdist` for pairwise distances (all points vs all points), not `shape_weighted_distance` directly on individual pairs
2. **DBSCAN precomputed mode**: Pass `metric='precomputed'` to DBSCAN and provide the full distance matrix
3. **Standard Euclidean for matching**: When matching cluster centroids to expert points later, always use standard Euclidean distance (w=1.0), not the custom metric
4. **Parameter range**: shape_weight typically ranges 0.9–1.9 in grid search
