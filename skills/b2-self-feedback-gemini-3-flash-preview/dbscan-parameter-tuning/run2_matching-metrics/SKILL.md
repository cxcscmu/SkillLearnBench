---
name: run2_matching-metrics
description: Greedy point matching and calculation of F1 score and average distance (delta).
---

# Greedy Point Matching and Metrics

Detailed implementation of the matching process and metric calculations for image-based clustering.

## Implementation

```python
from scipy.spatial.distance import cdist
import numpy as np

def match_and_evaluate(predicted, expert, max_dist=100):
    """
    Match predicted centroids to expert points and compute metrics.
    """
    if len(predicted) == 0:
        return 0.0, np.nan
    
    if len(expert) == 0:
        return 0.0, np.nan

    # Greedy matching based on Euclidean distance
    dists = cdist(predicted, expert, metric='euclidean')
    
    # Flatten and sort pairs by distance
    pairs = []
    for i in range(dists.shape[0]):
        for j in range(dists.shape[1]):
            if dists[i, j] <= max_dist:
                pairs.append((dists[i, j], i, j))
    pairs.sort()

    matched_p = set()
    matched_e = set()
    match_distances = []
    for d, i, j in pairs:
        if i not in matched_p and j not in matched_e:
            matched_p.add(i)
            matched_e.add(j)
            match_distances.append(d)

    tp = len(match_distances)
    fp = len(predicted) - tp
    fn = len(expert) - tp
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    delta = np.mean(match_distances) if match_distances else np.nan
    return f1, delta
```
