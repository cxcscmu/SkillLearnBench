---
name: greedy-bipartite-matching
description: Implement greedy bipartite matching for pairing cluster centroids with expert annotations.
---

# Greedy Bipartite Matching

## Overview
Greedy matching finds pairs between two sets of points by iteratively selecting the closest unmatched pair until no more matches are possible below a distance threshold.

## Algorithm

1. Compute pairwise distances between cluster centroids and expert points
2. Repeatedly find the closest pair (centroid, expert point) below max_distance
3. Mark both as matched and remove from consideration
4. Continue until no more valid pairs can be found

## Implementation

```python
import numpy as np

def greedy_match(centroids, expert_points, max_distance=100):
    """
    Match centroids to expert points using greedy algorithm.

    Args:
        centroids: (n, 2) array of cluster centroids
        expert_points: (m, 2) array of expert annotations
        max_distance: Maximum distance for a valid match

    Returns:
        matched_pairs: List of (centroid_idx, expert_idx, distance) tuples
    """
    centroids = np.asarray(centroids)
    expert_points = np.asarray(expert_points)

    if len(centroids) == 0 or len(expert_points) == 0:
        return []

    # Compute Euclidean distances (always standard Euclidean for matching)
    distances = np.linalg.norm(
        centroids[:, np.newaxis, :] - expert_points[np.newaxis, :, :],
        axis=2
    )

    matched_pairs = []
    unmatched_centroids = set(range(len(centroids)))
    unmatched_experts = set(range(len(expert_points)))

    while unmatched_centroids and unmatched_experts:
        # Find closest unmatched pair
        min_dist = np.inf
        best_c_idx = None
        best_e_idx = None

        for c_idx in unmatched_centroids:
            for e_idx in unmatched_experts:
                dist = distances[c_idx, e_idx]
                if dist < min_dist:
                    min_dist = dist
                    best_c_idx = c_idx
                    best_e_idx = e_idx

        # If distance exceeds threshold, stop
        if min_dist > max_distance:
            break

        # Record match and remove from unmatched sets
        matched_pairs.append((best_c_idx, best_e_idx, min_dist))
        unmatched_centroids.remove(best_c_idx)
        unmatched_experts.remove(best_e_idx)

    return matched_pairs
```

## Computing Metrics from Matches

```python
def compute_f1_and_delta(matched_pairs, num_centroids, num_expert_points):
    """
    Compute F1 score and average delta from matched pairs.

    Returns:
        f1: Precision-recall harmonic mean
        avg_delta: Average distance of matched pairs
    """
    if len(matched_pairs) == 0:
        return 0.0, np.nan

    # True positives = number of matches
    tp = len(matched_pairs)

    # False positives = unmatched centroids
    fp = num_centroids - tp

    # False negatives = unmatched expert points
    fn = num_expert_points - tp

    # Precision and recall
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    # F1 score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Average delta (distance)
    avg_delta = np.mean([dist for _, _, dist in matched_pairs])

    return f1, avg_delta
```

## Notes
- Always use standard Euclidean distance for matching, not the custom clustering metric
- The greedy approach is O(n*m) per iteration, overall O(n² * m²) worst case
- For larger datasets, consider Hungarian algorithm for optimal matching
