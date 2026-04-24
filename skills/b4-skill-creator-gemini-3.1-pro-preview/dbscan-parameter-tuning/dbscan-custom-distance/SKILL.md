---
name: dbscan-custom-distance
description: Define custom distance metrics for DBSCAN clustering. Use this skill whenever a task requires clustering points with unequal weighting or application-specific distances.
---

# DBSCAN Custom Distance Metrics

This skill shows how to define and use custom distance metrics with scikit-learn's DBSCAN.

## Parameterized Distance Functions

To use a distance function with configurable parameters (like variable feature weights), use a factory function:

```python
import numpy as np
from sklearn.cluster import DBSCAN

def create_weighted_distance(weight_x, weight_y):
    """Create a distance function with specific weights."""
    def distance(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return np.sqrt((weight_x * dx)**2 + (weight_y * dy)**2)
    return distance

# Create a distance function instance
dist_metric = create_weighted_distance(1.5, 0.5)

# Pass it to DBSCAN
db = DBSCAN(eps=10, min_samples=5, metric=dist_metric)
labels = db.fit_predict(points)
```

## Performance Notes
- Custom Python metrics are slower than built-in scikit-learn metrics.
- Vectorized operations using `scipy.spatial.distance.pdist` or `cdist` are faster, but DBSCAN handles the metric parameter elegantly via a callable.
