---
name: dbscan-custom-metrics
description: Implement DBSCAN clustering with custom distance metrics using scikit-learn's pairwise_distances.
---

# DBSCAN with Custom Distance Metrics

## Overview
DBSCAN can use custom distance metrics by computing a precomputed distance matrix or using `pairwise_distances` with a custom metric function.

## Key Concepts

### Custom Metric Function
A custom metric function takes two 1D arrays (two points) and returns a scalar distance:

```python
def custom_metric(u, v, shape_weight):
    """Compute weighted distance between two points."""
    dx = u[0] - v[0]
    dy = u[1] - v[1]
    return np.sqrt((shape_weight * dx)**2 + ((2 - shape_weight) * dy)**2)
```

### Using with scikit-learn

For DBSCAN with a custom metric, use `metric='precomputed'` and pass a precomputed distance matrix:

```python
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import DBSCAN

# Compute precomputed distance matrix
distances = pairwise_distances(
    points,
    metric=custom_metric,
    metric_params={'shape_weight': w}
)

# Run DBSCAN with precomputed distances
clusterer = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
labels = clusterer.fit_predict(distances)
```

## Implementation Pattern

```python
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import DBSCAN

def shape_weighted_distance(u, v, shape_weight):
    """Distance metric with shape weighting."""
    dx = u[0] - v[0]
    dy = u[1] - v[1]
    return np.sqrt((shape_weight * dx)**2 + ((2 - shape_weight) * dy)**2)

def cluster_with_custom_metric(points, epsilon, min_samples, shape_weight):
    """Cluster points using DBSCAN with custom distance metric."""
    if len(points) == 0:
        return np.array([], dtype=int)

    # Compute distance matrix
    distances = pairwise_distances(
        points,
        metric=shape_weighted_distance,
        metric_params={'shape_weight': shape_weight}
    )

    # Run DBSCAN
    clusterer = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
    labels = clusterer.fit_predict(distances)

    return labels
```

## Notes
- Distance metrics must be symmetric: d(a, b) = d(b, a)
- When shape_weight=1, the formula reduces to standard Euclidean distance
- Consider caching distance matrices for repeated use on same data
