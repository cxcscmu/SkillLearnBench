---
name: dbscan-anisotropic-distance
description: Efficiently computing DBSCAN with a custom weighted (anisotropic) distance metric using coordinate scaling, avoiding the overhead of slow custom distance functions.
---

# Efficient Anisotropic Distance for DBSCAN

When using scikit-learn's `DBSCAN`, passing a custom Python function to the `metric` argument forces the algorithm to bypass highly optimized C/Cython code, making it run extremely slowly (or requiring precomputing massive $N \times N$ distance matrices).

If your custom distance metric takes the form:
$d(a, b) = \sqrt{(w_x \cdot \Delta x)^2 + (w_y \cdot \Delta y)^2}$

This is mathematically identical to performing a standard Euclidean distance search on **scaled coordinates**. By temporarily transforming the dataset, you can use the default `metric='euclidean'` in `DBSCAN` at full C-optimized speeds.

### Implementation

```python
import numpy as np
from sklearn.cluster import DBSCAN

def get_cluster_centroids_weighted(df_points, min_samples, epsilon, shape_weight):
    if len(df_points) == 0:
        return []
    
    # 1. Extract coordinates
    X = df_points[['x', 'y']].values.astype(float)
    
    # 2. Scale coordinates to represent the weighted Euclidean distance
    # Example: d = sqrt((w * dx)^2 + ((2-w) * dy)^2)
    # We multiply the x column by w, and the y column by (2 - w)
    X_scaled = X.copy()
    X_scaled[:, 0] *= shape_weight
    X_scaled[:, 1] *= (2 - shape_weight)
    
    # 3. Run DBSCAN using standard Euclidean distance on the scaled data
    db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='euclidean')
    labels = db.fit_predict(X_scaled)
    
    # 4. Compute centroids using the ORIGINAL (unscaled) coordinates
    centroids = []
    for k in set(labels):
        if k == -1:
            continue # Skip noise points
        
        cluster_mask = (labels == k)
        # Always return the real-world spatial coordinates for the centroid!
        cluster_centroid = X[cluster_mask].mean(axis=0)
        centroids.append(cluster_centroid)
        
    return np.array(centroids)
```