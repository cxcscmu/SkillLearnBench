---
name: data-matching
description: Greedy matching of centroid points to expert annotations based on standard Euclidean distance.
---

### Logic
Greedy matching for two point sets.

```python
import numpy as np
from scipy.spatial.distance import cdist

def match_points(centroids, expert_points, max_dist=100.0):
    if len(centroids) == 0 or len(expert_points) == 0:
        return 0, 0, 0 # TP, FN, FP
    
    dist_matrix = cdist(centroids, expert_points, 'euclidean')
    # Find all pairs within distance
    matches = []
    for i in range(len(centroids)):
        for j in range(len(expert_points)):
            if dist_matrix[i, j] <= max_dist:
                matches.append((dist_matrix[i, j], i, j))
    
    matches.sort(key=lambda x: x[0]) # Closest first
    
    used_centroids = set()
    used_experts = set()
    total_dist = 0
    num_matches = 0
    
    for dist, i, j in matches:
        if i not in used_centroids and j not in used_experts:
            used_centroids.add(i)
            used_experts.add(j)
            total_dist += dist
            num_matches += 1
            
    # TP: num_matches
    # FN: len(expert_points) - num_matches
    # FP: len(centroids) - num_matches
    return num_matches, len(expert_points) - num_matches, len(centroids) - num_matches, total_dist
```
