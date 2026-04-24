---
name: run2_dbscan-custom-metric
description: DBSCAN with custom weighted Euclidean distance metric for spatial clustering of annotations.
---

# DBSCAN with Custom Distance Metrics

## Custom Metric Definition

For shape_weight `w`: `d(a, b) = sqrt((w * Δx)² + ((2-w) * Δy)²)`

```python
from sklearn.cluster import DBSCAN
import numpy as np

def custom_metric(a, b, w):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)

db = DBSCAN(eps=epsilon, min_samples=min_samples,
            metric=custom_metric, metric_params={'w': shape_weight})
labels = db.fit_predict(points_xy)
```

## Key Details
- `metric` accepts callable with signature `f(a, b, **metric_params)`
- Labels: -1 = noise, >=0 = cluster ID
- Centroids: mean of (x, y) for each cluster (excluding noise points with label -1)
- For evaluation, use standard Euclidean distance (not custom) for matching centroids to expert points
