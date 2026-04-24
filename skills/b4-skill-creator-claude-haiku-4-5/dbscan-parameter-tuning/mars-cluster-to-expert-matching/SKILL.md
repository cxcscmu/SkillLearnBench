---
name: mars-cluster-to-expert-matching
description: Implement greedy nearest-neighbor matching between cluster centroids and expert annotations. Use this skill when you need to match predicted cluster centers to ground-truth expert points for Mars cloud evaluation, always using standard Euclidean distance with a maximum distance threshold of 100 pixels.
---

# Mars Cluster-to-Expert Matching

## Overview

After running DBSCAN on citizen science annotations, you get cluster centroids. These must be matched to expert annotations to compute evaluation metrics. This skill implements greedy nearest-neighbor matching.

## Algorithm

Greedy matching finds 1:1 correspondences between cluster centroids and expert points:

1. Start with all cluster centroids unmatched and all expert points unmatched
2. Repeatedly:
   - Find the closest pair (centroid, expert point) from the unmatched sets
   - If distance ≤ 100 pixels: record match, remove both from unmatched sets
   - If distance > 100 pixels: stop (no more valid matches)
3. Return: list of matched (centroid, expert_point) pairs

## Implementation

```python
import numpy as np
from scipy.spatial.distance import cdist

def greedy_match_centroids_to_experts(centroids, expert_points, max_distance=100):
    """
    Match cluster centroids to expert points using greedy nearest-neighbor.

    Parameters
    ----------
    centroids : array-like, shape (n_clusters, 2)
        Cluster centroids [x, y]
    expert_points : array-like, shape (n_experts, 2)
        Expert annotations [x, y]
    max_distance : float
        Maximum Euclidean distance for a valid match (default: 100)

    Returns
    -------
    matches : list of tuples
        List of (centroid_idx, expert_idx, distance) for each match
    """
    if len(centroids) == 0 or len(expert_points) == 0:
        return []

    centroids = np.asarray(centroids)
    expert_points = np.asarray(expert_points)

    # Compute pairwise Euclidean distances (standard, not custom)
    distances = cdist(centroids, expert_points, metric='euclidean')

    unmatched_centroids = set(range(len(centroids)))
    unmatched_experts = set(range(len(expert_points)))
    matches = []

    while unmatched_centroids and unmatched_experts:
        # Find minimum distance pair from unmatched sets
        min_dist = np.inf
        best_c_idx, best_e_idx = None, None

        for c_idx in unmatched_centroids:
            for e_idx in unmatched_experts:
                dist = distances[c_idx, e_idx]
                if dist < min_dist:
                    min_dist = dist
                    best_c_idx, best_e_idx = c_idx, e_idx

        # If closest pair exceeds max_distance, stop
        if min_dist > max_distance:
            break

        # Record match
        matches.append((best_c_idx, best_e_idx, min_dist))
        unmatched_centroids.remove(best_c_idx)
        unmatched_experts.remove(best_e_idx)

    return matches
```

## Usage Example

```python
# Centroids from DBSCAN clustering
centroids = np.array([[100, 150], [200, 250]])

# Expert annotations for the same image
experts = np.array([[102, 148], [300, 300], [205, 251]])

matches = greedy_match_centroids_to_experts(centroids, experts, max_distance=100)
# matches might be: [(0, 0, 2.8), (1, 2, 5.1)]
```

## Key Points

1. **Standard Euclidean distance only**: Always use standard Euclidean (not the custom shape_weight metric)
2. **Max distance threshold**: Only accept matches within 100 pixels
3. **1:1 matching**: Each centroid matches at most one expert point, and vice versa
4. **Greedy is sufficient**: For Mars cloud data, greedy nearest-neighbor works well enough; optimal matching is not required
5. **Empty return**: If no clusters or no experts for an image, return empty list
