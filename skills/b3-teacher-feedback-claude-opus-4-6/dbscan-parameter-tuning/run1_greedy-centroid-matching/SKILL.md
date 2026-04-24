---
name: greedy-centroid-matching
description: How to perform greedy matching between predicted cluster centroids and ground-truth expert points using closest-pairs-first strategy with a maximum distance threshold.
---

## Greedy Matching of Centroids to Expert Points

Greedy matching pairs predicted centroids with expert annotations by repeatedly selecting the globally closest unmatched pair.

### Algorithm

1. Compute all pairwise **standard Euclidean distances** between centroids and expert points
2. Sort all pairs by distance (ascending)
3. Greedily assign matches: pick the closest pair, remove both from the pool, repeat
4. Only accept matches within a maximum distance threshold (e.g., 100 pixels)

### Implementation

```python
import numpy as np
from scipy.spatial.distance import cdist

def greedy_match(centroids, expert_points, max_dist=100.0):
    """
    Match centroids to expert points using greedy closest-first matching.
    
    Returns:
        matches: list of (centroid_idx, expert_idx, distance) tuples
    """
    if len(centroids) == 0 or len(expert_points) == 0:
        return []
    
    centroids = np.array(centroids)
    expert_points = np.array(expert_points)
    
    # Standard Euclidean distance matrix
    dist_matrix = cdist(centroids, expert_points, metric='euclidean')
    
    matches = []
    used_centroids = set()
    used_experts = set()
    
    # Get all pairs sorted by distance
    # Create list of (distance, centroid_idx, expert_idx)
    pairs = []
    for i in range(len(centroids)):
        for j in range(len(expert_points)):
            if dist_matrix[i, j] <= max_dist:
                pairs.append((dist_matrix[i, j], i, j))
    
    pairs.sort(key=lambda x: x[0])
    
    for dist, ci, ej in pairs:
        if ci not in used_centroids and ej not in used_experts:
            matches.append((ci, ej, dist))
            used_centroids.add(ci)
            used_experts.add(ej)
    
    return matches
```

### F1 Score Computation from Matches

```python
def compute_f1_delta(centroids, expert_points, max_dist=100.0):
    matches = greedy_match(centroids, expert_points, max_dist)
    
    tp = len(matches)
    fp = len(centroids) - tp    # unmatched centroids (false positives)
    fn = len(expert_points) - tp  # unmatched experts (false negatives)
    
    if tp == 0:
        f1 = 0.0
        avg_delta = float('nan')
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * precision * recall / (precision + recall)
        avg_delta = np.mean([m[2] for m in matches])
    
    return f1, avg_delta
```

### Edge Cases
- **No centroids found** (DBSCAN returns all noise): F1 = 0.0, delta = NaN
- **No expert points for an image**: This shouldn't happen if looping over expert images
- **No citizen science points for an image**: F1 = 0.0, delta = NaN
- **No matches within threshold**: F1 = 0.0, delta = NaN
- **Important**: Use standard Euclidean for matching, NOT the custom weighted metric