---
name: custom-distance-metrics
description: Define custom distance/similarity metrics for DBSCAN clustering with sklearn, using weighted Euclidean distances.
---

# Custom Distance Metrics for DBSCAN

## Overview
DBSCAN in sklearn supports custom distance metrics via `metric='precomputed'` (pass a distance matrix) or `metric=callable` with the pairwise distance function.

## Approach: Precomputed Distance Matrix
For small-to-medium datasets per image, computing a full pairwise distance matrix is efficient:

```python
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform
import numpy as np

def weighted_euclidean(points, w):
    """Compute pairwise weighted Euclidean distance.
    d(a,b) = sqrt((w*dx)^2 + ((2-w)*dy)^2)
    """
    scaled = points * [w, 2 - w]
    return squareform(pdist(scaled, metric='euclidean'))

# Usage
dist_matrix = weighted_euclidean(points_xy, shape_weight)
db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
labels = db.fit_predict(dist_matrix)
```

## Key Points
- `pdist` + `squareform` is faster than looping over pairs
- Scale the coordinates before computing standard Euclidean = same as custom weighted metric
- When w=1, this equals standard Euclidean distance
- Cluster centroids are computed from original (unscaled) coordinates
