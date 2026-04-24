---
name: custom-distance-metrics
description: Custom distance metric implementation for use with clustering algorithms like DBSCAN.
---

# Custom Distance Metrics for Scikit-Learn

When clustering spatial data, you often want to weigh dimensions differently or apply a non-standard metric.

## Usage

You can implement custom metrics in `sklearn` or `scipy`. Scikit-learn's `DBSCAN` allows a custom distance metric passed as a callable.

Example:
```python
import numpy as np
from sklearn.cluster import DBSCAN

def custom_metric(x, y, weight=1.0):
    dx = x[0] - y[0]
    dy = x[1] - y[1]
    return np.sqrt((weight * dx)**2 + ((2 - weight) * dy)**2)

# Usage in DBSCAN
dbscan = DBSCAN(eps=5, min_samples=3, metric=custom_metric, metric_params={'weight': 1.5})
clusters = dbscan.fit_predict(data)
```
Alternatively, for performance, precompute the distance matrix or use `cdist`/`pdist` with custom metrics if needed, but the callable approach is simplest.
