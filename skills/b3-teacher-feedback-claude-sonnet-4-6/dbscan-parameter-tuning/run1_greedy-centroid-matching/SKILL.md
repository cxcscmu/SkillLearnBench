---
name: greedy-centroid-matching
description: How to perform greedy nearest-neighbor matching between two sets of 2D points (cluster centroids vs expert annotations) with a maximum distance threshold, returning matched pairs for F1/delta computation.
---

# Greedy Centroid-to-Expert Matching

## Overview

Given predicted cluster centroids and expert-annotated points for a single image, greedily match closest pairs (standard Euclidean distance) with a maximum distance cap of 100 pixels.

## Algorithm

1. Compute all pairwise standard Euclidean distances between centroids and expert points
2. Repeatedly pick the globally minimum distance pair
3. If distance ≤ 100, record the match; remove both points from consideration
4. If distance > 100, stop (all remaining pairs exceed threshold)
5. Count: TP = number of matches, FP = unmatched centroids, FN = unmatched expert points

## Implementation

```python
import numpy as np

def greedy_match(centroids, expert_points, max_dist=100.0):
    """
    centroids: list/array of shape (M, 2)
    expert_points: list/array of shape (K, 2)
    Returns: (tp, fp, fn, matched_distances)
      - tp: number of matched pairs
      - fp: unmatched centroids
      - fn: unmatched expert points
      - matched_distances: list of standard Euclidean distances for matched pairs
    """
    if len(centroids) == 0 and len(expert_points) == 0:
        return 0, 0, 0, []
    if len(centroids) == 0:
        return 0, 0, len(expert_points), []
    if len(expert_points) == 0:
        return 0, len(centroids), 0, []

    centroids = np.array(centroids)
    expert_points = np.array(expert_points)

    # Pairwise Euclidean distances: shape (M, K)
    diff = centroids[:, np.newaxis, :] - expert_points[np.newaxis, :, :]
    dist_matrix = np.sqrt((diff**2).sum(axis=2))

    matched_c = set()
    matched_e = set()
    matched_distances = []

    # Greedy: pick minimum distance pairs until max_dist exceeded
    while True:
        # Mask already-matched indices
        remaining = np.full(dist_matrix.shape, np.inf)
        for i in range(len(centroids)):
            for j in range(len(expert_points)):
                if i not in matched_c and j not in matched_e:
                    remaining[i, j] = dist_matrix[i, j]

        if remaining.min() > max_dist:
            break

        # Find the closest unmatched pair
        idx = np.unravel_index(np.argmin(remaining), remaining.shape)
        i, j = idx
        matched_c.add(i)
        matched_e.add(j)
        matched_distances.append(dist_matrix[i, j])

    tp = len(matched_distances)
    fp = len(centroids) - tp
    fn = len(expert_points) - tp
    return tp, fp, fn, matched_distances


def compute_f1(tp, fp, fn):
    """F1 score from TP/FP/FN counts."""
    if tp == 0:
        return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
```

## Efficient Vectorized Version

For performance in a grid search, avoid the Python loop in `remaining`:

```python
def greedy_match_fast(centroids, expert_points, max_dist=100.0):
    if len(centroids) == 0 and len(expert_points) == 0:
        return 0, 0, 0, []
    if len(centroids) == 0:
        return 0, 0, len(expert_points), []
    if len(expert_points) == 0:
        return 0, len(centroids), 0, []

    centroids = np.array(centroids, dtype=float)
    expert_points = np.array(expert_points, dtype=float)

    diff = centroids[:, np.newaxis, :] - expert_points[np.newaxis, :, :]
    dist_matrix = np.sqrt((diff**2).sum(axis=2)).copy()

    matched_distances = []
    n_c, n_e = dist_matrix.shape

    for _ in range(min(n_c, n_e)):
        min_val = dist_matrix.min()
        if min_val > max_dist:
            break
        i, j = np.unravel_index(np.argmin(dist_matrix), dist_matrix.shape)
        matched_distances.append(dist_matrix[i, j])
        # Eliminate row and column
        dist_matrix[i, :] = np.inf
        dist_matrix[:, j] = np.inf

    tp = len(matched_distances)
    fp = n_c - tp
    fn = n_e - tp
    return tp, fp, fn, matched_distances
```