---
name: run2_greedy-matching
description: Greedy matching of predicted centroids to expert points by closest pairs first, with max distance threshold, computing F1 and delta.
---

# Greedy Matching for Point Sets

## Algorithm

Greedy matching: enumerate all (predicted, expert) pairs, sort by standard Euclidean distance ascending, greedily assign closest pairs (each point used at most once), stop when distance exceeds max_dist.

```python
import numpy as np
from scipy.spatial.distance import cdist

def greedy_match(predicted, expert_pts, max_dist=100):
    """
    Args:
        predicted: (M, 2) array of cluster centroids
        expert_pts: (K, 2) array of expert annotations
        max_dist: maximum allowed matching distance (pixels)

    Returns:
        list of matched Euclidean distances (one per match)
    """
    if len(predicted) == 0 or len(expert_pts) == 0:
        return []

    # Standard Euclidean distance for matching
    dists = cdist(predicted, expert_pts, metric='euclidean')

    # Get all pairs sorted by distance
    pairs = [(dists[i, j], i, j)
             for i in range(len(predicted))
             for j in range(len(expert_pts))]
    pairs.sort(key=lambda x: x[0])

    matched_dists = []
    used_pred = set()
    used_expert = set()

    for dist, i, j in pairs:
        if dist > max_dist:
            break  # All remaining pairs are farther (sorted list)
        if i in used_pred or j in used_expert:
            continue
        matched_dists.append(dist)
        used_pred.add(i)
        used_expert.add(j)

    return matched_dists
```

## Computing F1 and Delta

```python
def compute_f1_delta(predicted, expert_pts, max_dist=100):
    """
    F1 = 2*TP / (2*TP + FP + FN)
      where TP = matched pairs, FP = unmatched predictions, FN = unmatched experts

    delta = mean standard Euclidean distance of matched pairs
          = NaN if no matches

    Returns: (f1, delta)
    """
    matched_dists = greedy_match(predicted, expert_pts, max_dist)

    tp = len(matched_dists)
    fp = len(predicted) - tp
    fn = len(expert_pts) - tp

    if tp == 0:
        return 0.0, np.nan

    f1 = 2 * tp / (2 * tp + fp + fn)
    delta = float(np.mean(matched_dists))
    return f1, delta
```

## Important Notes

- Use **standard Euclidean distance** for matching, NOT the custom shape-weighted metric
- max_dist = 100 pixels (as specified)
- delta = NaN when no matches (excluded from average across images)
- F1 = 0.0 when no matches (included in average across images)

## Averaging Across Images

```python
# Loop over ALL expert images
f1_list = []
delta_list = []
for file_rad in expert_images:
    f1, delta = evaluate_image(file_rad, ...)
    f1_list.append(f1)          # Always add (0.0 for bad images)
    if not np.isnan(delta):
        delta_list.append(delta)  # Only add non-NaN

avg_f1 = np.mean(f1_list)
avg_delta = np.mean(delta_list) if delta_list else np.nan
```
