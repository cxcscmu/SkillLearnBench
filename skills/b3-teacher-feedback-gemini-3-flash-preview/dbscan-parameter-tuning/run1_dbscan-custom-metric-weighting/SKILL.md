---
name: dbscan-custom-metric-weighting
description: Implementing a weighted Euclidean distance metric for DBSCAN to account for anisotropic spatial features.
---

When clustering spatial data where features (like x and y coordinates) have different importance or scales, a custom distance metric can be used with `sklearn.cluster.DBSCAN`.

The formula provided: $d(a, b) = \sqrt{(w \cdot \Delta x)^2 + ((2 - w) \cdot \Delta y)^2}$ allows for "stretching" or "compressing" the influence of horizontal vs vertical distances.

**Implementation with Scikit-Learn:**
To use this with DBSCAN, you can define a function and pass it to the `metric` parameter.

```python
from sklearn.cluster import DBSCAN
import numpy as np

def custom_dist(a, b, w):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)

# Using it in DBSCAN (note: using lambda to pass the weight)
db = DBSCAN(eps=epsilon, min_samples=min_samples, 
            metric=lambda u, v: custom_dist(u, v, weight))
clusters = db.fit_predict(points)
```

Alternatively, for performance during grid search, precomputing the distance matrix or using a vectorized function inside the metric argument is recommended.