---
name: run2_dbscan-clustering
description: Efficient DBSCAN clustering with a custom parameterized distance metric using precomputed distance matrices for speed, plus centroid computation.
---

# DBSCAN with Custom Distance Metric (Efficient)

## Setup

```python
from sklearn.cluster import DBSCAN
import numpy as np
from scipy.spatial.distance import pdist, squareform
```

## Custom Weighted Distance Metric

For Mars cloud clustering:
```
d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)
```

When w=1, equals standard Euclidean. w>1 attenuates y-distances; w<1 attenuates x-distances.

## Performance: Precomputed Distance Matrix

Using a Python callable as metric in DBSCAN is **very slow** (O(N²) Python function calls).
Instead, precompute the full distance matrix and pass with `metric='precomputed'`:

```python
def compute_distance_matrix(points, shape_weight):
    """Compute the pairwise custom distance matrix for a set of points."""
    w = shape_weight
    # Use pdist with a vectorized lambda for efficiency
    def custom_metric(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)

    pairwise = pdist(points, metric=custom_metric)
    return squareform(pairwise)


def cluster_points(points, epsilon, min_samples, shape_weight):
    """
    Run DBSCAN with precomputed custom distance matrix.
    Returns: array of cluster centroids (shape M x 2), or empty if no clusters.
    """
    if len(points) < min_samples:
        return np.array([]).reshape(0, 2)

    dist_matrix = compute_distance_matrix(points, shape_weight)
    db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
    labels = db.fit_predict(dist_matrix)

    centroids = []
    for label in set(labels):
        if label == -1:  # Skip noise
            continue
        centroid = points[labels == label].mean(axis=0)
        centroids.append(centroid)

    return np.array(centroids) if centroids else np.array([]).reshape(0, 2)
```

## Notes on Behavior

- Points with fewer than `min_samples` neighbors (within `epsilon`) are labeled as noise (-1)
- Noise points are NOT included in any cluster centroid
- If ALL points are noise → returns empty array (treat as no clusters found → F1=0, delta=NaN)
- Cluster centroid = arithmetic mean of all points in that cluster

## Edge Cases

- `len(points) < min_samples`: return empty (DBSCAN requires at least min_samples points to form a core)
- Single image with 0 citizen science points: return 0.0 F1 and NaN delta immediately
- Image in expert_df but not in citsci_df: same as 0 citizen science points

## Hyperparameter Grid

```python
import numpy as np
min_samples_range = list(range(3, 10))              # 3,4,5,6,7,8,9
epsilon_range = list(range(4, 25, 2))               # 4,6,8,...,24
shape_weight_range = [round(0.9 + 0.1*i, 1) for i in range(11)]  # 0.9..1.9
```
