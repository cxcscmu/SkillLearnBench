---
name: run2_custom_distance_metrics
description: Implement weighted Euclidean distance metric for DBSCAN with shape parameter
---

# Custom Distance Metrics for Shape-Weighted Clustering

## Mathematical Foundation

### Distance Formula
The custom weighted Euclidean distance is defined as:
```
d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)
```

Where:
- `w` = shape_weight parameter (controls aspect ratio)
- `Δx` = x₁ - x₂ (horizontal difference)
- `Δy` = y₁ - y₂ (vertical difference)

### Shape Weight Interpretation
- **w = 1.0**: Standard Euclidean distance (equal weighting)
- **w > 1.0**: Attenuates y-distances (horizontal features more prominent)
- **w < 1.0**: Attenuates x-distances (vertical features more prominent)
- **w = 1.9**: Maximum y-attenuation (strongly favors horizontal clustering)
- **w = 0.9**: Maximum x-attenuation (strongly favors vertical clustering)

### Validation
Ensure w ∈ [0.9, 1.9] to maintain meaningful distance properties.

## Implementation: Precomputed Distance Matrix

For DBSCAN with precomputed distances, compute the full pairwise matrix once per image:

```python
import numpy as np
from sklearn.cluster import DBSCAN

def compute_custom_distance_matrix(points, shape_weight):
    """
    Compute pairwise custom distance matrix efficiently.

    Parameters:
    - points: (n, 2) array of [x, y] coordinates
    - shape_weight: float in [0.9, 1.9]

    Returns:
    - distances: (n, n) symmetric distance matrix
    """
    n = len(points)
    distances = np.zeros((n, n))

    # Vectorized computation
    for i in range(n):
        dx = points[i, 0] - points[:, 0]
        dy = points[i, 1] - points[:, 1]
        distances[i, :] = np.sqrt(
            (shape_weight * dx)**2 + ((2 - shape_weight) * dy)**2
        )

    return distances

# Example: Apply to citizen science points for one image
citsci_points = np.array([[100, 50], [110, 55], [200, 100]])
shape_weight = 1.2
distance_matrix = compute_custom_distance_matrix(citsci_points, shape_weight)

# Run DBSCAN with precomputed metric
clusterer = DBSCAN(eps=8, min_samples=5, metric='precomputed')
labels = clusterer.fit_predict(distance_matrix)
```

## Important Design Decisions

### 1. Precomputed vs. Callable Metric
- **Precomputed**: Compute once, reuse with multiple epsilon values ✓ **Use this**
- **Callable**: Recompute for each distance query (slower) ✗

### 2. Distance Matrix Properties
- Symmetric: d(i, j) = d(j, i)
- Non-negative: d(i, j) ≥ 0
- Identity: d(i, i) = 0
- Triangle inequality: may not hold (acceptable for DBSCAN)

### 3. Per-Image Computation
Always compute distance matrices **per image**, not globally:
```python
for image_id in unique_images:
    # Extract image-specific points
    image_points = citsci_df[citsci_df['file_rad'] == image_id][['x', 'y']].values

    # Compute distance matrix for THIS image only
    dist_matrix = compute_custom_distance_matrix(image_points, shape_weight)

    # Apply DBSCAN
    clusterer = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
    labels = clusterer.fit_predict(dist_matrix)
```

## Edge Cases and Validation

### 1. Empty Image Points
```python
if len(image_points) == 0:
    # No citizen science annotations
    # Return F1 = 0.0, delta = NaN
    return 0.0, np.nan
```

### 2. Single Point
```python
if len(image_points) == 1:
    # Distance matrix is 1x1 all zeros
    # DBSCAN typically marks as noise unless min_samples=1
    # Result: no clusters or 1 noise point
```

### 3. Shape Weight Rounding
```python
# Shape weights are rounded to 1 decimal place
shape_weights = np.round(np.arange(0.9, 2.0, 0.1), 1)
# [0.9, 1.0, 1.1, 1.2, ..., 1.9]
```

## Comparison: Custom vs. Standard Distance

```python
# Standard Euclidean
d_std = np.sqrt(dx**2 + dy**2)

# Custom (w=1.2, attenuation on y)
d_custom = np.sqrt((1.2*dx)**2 + (0.8*dy)**2)

# For dx=10, dy=10:
# d_std = 14.14
# d_custom = sqrt(144 + 64) = sqrt(208) = 14.42
# → Custom distance is slightly larger (y-difference less important)
```

## Testing Sanity Checks

```python
# Test 1: w=1.0 gives Euclidean
d_test = compute_custom_distance_matrix(
    np.array([[0, 0], [3, 4]]),
    shape_weight=1.0
)
assert d_test[0, 1] == 5.0, "w=1.0 should give standard distance 5"

# Test 2: Symmetry
d = compute_custom_distance_matrix(citsci_points, 1.2)
assert np.allclose(d, d.T), "Distance matrix must be symmetric"

# Test 3: Diagonal is zero
assert np.allclose(np.diag(d), 0), "Diagonal should be all zeros"
```

## Performance Optimization

For large images (>1000 points), precomputation is still fast:
- n=1000: ~1 million distance values
- NumPy vectorized computation: typically <100ms
- Acceptable for grid search with 847 hyperparameter combinations
