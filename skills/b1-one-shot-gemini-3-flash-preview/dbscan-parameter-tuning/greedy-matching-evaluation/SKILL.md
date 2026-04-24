---
name: greedy-matching-evaluation
description: Greedy matching algorithm to pair predicted cluster centroids with ground truth points for F1 and distance metrics.
---

# Greedy Matching for Clustering Evaluation

To evaluate clustering performance against ground truth (expert) points, we need to match predicted centroids to expert points.

## Algorithm
1. Compute all pairwise standard Euclidean distances between predicted centroids and expert points.
2. Filter pairs with distance > `max_dist` (e.g., 100 pixels).
3. Sort remaining pairs by distance (closest first).
4. Iteratively pick the closest pair, ensuring each centroid and each expert point is matched at most once.

## F1 Score Calculation
- **True Positives (TP)**: Number of matched pairs.
- **False Positives (FP)**: Number of unmatched predicted centroids.
- **False Negatives (FN)**: Number of unmatched expert points.
- `Precision = TP / (TP + FP)`
- `Recall = TP / (TP + FN)`
- `F1 = 2 * (Precision * Recall) / (Precision + Recall)` (Handle division by zero)

## Python Implementation
```python
import numpy as np
from scipy.spatial.distance import cdist

def evaluate_clustering(centroids, experts, max_dist=100):
    if len(centroids) == 0:
        return 0.0, np.nan
    if len(experts) == 0:
        return 0.0, np.nan

    distances = cdist(centroids, experts, metric='euclidean')
    
    # Greedy matching
    indices = np.where(distances <= max_dist)
    pairs = sorted(zip(indices[0], indices[1]), key=lambda x: distances[x[0], x[1]])
    
    matched_centroids = set()
    matched_experts = set()
    match_distances = []
    
    for c_idx, e_idx in pairs:
        if c_idx not in matched_centroids and e_idx not in matched_experts:
            matched_centroids.add(c_idx)
            matched_experts.add(e_idx)
            match_distances.append(distances[c_idx, e_idx])
            
    tp = len(matched_centroids)
    fp = len(centroids) - tp
    fn = len(experts) - tp
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    avg_delta = np.mean(match_distances) if len(match_distances) > 0 else np.nan
    
    return f1, avg_delta
```
