---
name: dbscan-custom-metric
description: Implements DBSCAN with a weighted Euclidean distance metric.
---

### Usage
Use this for clustering problems where directional features need attenuation.

```python
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances

def custom_distance(a, b, w):
    # d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)
    dx = (a[0] - b[0]) * w
    dy = (a[1] - b[1]) * (2 - w)
    return np.sqrt(dx**2 + dy**2)

# For DBSCAN:
# Construct a custom distance matrix or pass metric='precomputed'
```
