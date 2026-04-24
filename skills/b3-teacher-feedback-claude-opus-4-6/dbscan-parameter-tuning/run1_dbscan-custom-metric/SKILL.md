---
name: dbscan-custom-metric
description: How to run DBSCAN clustering with a custom weighted Euclidean distance metric, particularly using scikit-learn's DBSCAN with a precomputed distance matrix or custom metric function.
---

## DBSCAN with Custom Distance Metric

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points that are closely packed together, marking outliers as noise.

### Key Parameters
- `eps` (epsilon): Maximum distance between two points to be considered neighbors
- `min_samples`: Minimum number of points to form a dense region (core point threshold)

### Custom Metric Implementation

When using a non-standard distance metric, there are two approaches:

#### Approach 1: Precomputed Distance Matrix
```python
from sklearn.cluster import DBSCAN
import numpy as np

def custom_distance_matrix(points, shape_weight):
    """Compute pairwise distances with shape_weight (w):
    d(a, b) = sqrt((w * dx)^2 + ((2-w) * dy)^2)
    """
    w = shape_weight
    n = len(points)
    # Vectorized computation
    dx = points[:, 0][:, None] - points[:, 0][None, :]  # x differences
    dy = points[:, 1][:, None] - points[:, 1][None, :]  # y differences
    dist = np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)
    return dist

points = np.column_stack([x_values, y_values])
dist_matrix = custom_distance_matrix(points, shape_weight=1.2)
db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
labels = db.fit_predict(dist_matrix)
```

#### Approach 2: Callable Metric (slower, not recommended for large datasets)
```python
def weighted_dist(a, b, w=1.0):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)

db = DBSCAN(eps=epsilon, min_samples=min_samples, metric=weighted_dist, w=shape_weight)
```

### Computing Cluster Centroids
```python
labels = db.fit_predict(dist_matrix)
centroids = []
for label in set(labels):
    if label == -1:
        continue  # skip noise
    mask = labels == label
    centroid_x = points[mask, 0].mean()
    centroid_y = points[mask, 1].mean()
    centroids.append((centroid_x, centroid_y))
```

### Important Notes
- Label `-1` indicates noise points — exclude from centroid computation
- When `w=1`, the custom metric equals standard Euclidean distance
- When `w>1`, y-distances are attenuated (compressed); x-distances amplified
- When `w<1`, x-distances are attenuated; y-distances amplified
- The precomputed approach is much faster for repeated evaluations with the same data