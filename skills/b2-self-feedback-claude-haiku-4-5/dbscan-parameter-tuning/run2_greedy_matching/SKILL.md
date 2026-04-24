---
name: run2_greedy_matching
description: Greedy one-to-one matching of cluster centroids to expert points with maximum distance constraint
---

# Greedy Matching: Cluster Centroids to Expert Points

## Problem Statement

**Input**:
- Cluster centroids from DBSCAN (variable number per image)
- Expert annotations (ground truth points)

**Goal**: Find best one-to-one matching between clusters and experts.

**Constraints**:
- Each cluster matches to at most one expert
- Each expert matches to at most one cluster
- Maximum allowed distance: 100 pixels (standard Euclidean)
- No matches beyond 100 pixels

## Algorithm: Greedy Nearest-Neighbor Matching

The greedy algorithm matches pairs in order of **increasing distance**, skipping pairs where either endpoint is already matched.

### Step-by-Step

```python
import numpy as np
from scipy.spatial.distance import cdist

def greedy_match(cluster_centroids, expert_points, max_distance=100):
    """
    Greedily match cluster centroids to expert points.

    Algorithm:
    1. Compute all pairwise Euclidean distances (standard, not custom)
    2. Create list of valid pairs (distance ≤ max_distance)
    3. Sort by distance (ascending)
    4. Iterate through sorted pairs:
       - If both endpoints unmatched: create match, mark as matched
       - Otherwise: skip (one endpoint already matched)
    5. Return all created matches and their distances

    Parameters:
    - cluster_centroids: (n_clusters, 2) array of [x, y]
    - expert_points: (n_experts, 2) array of [x, y]
    - max_distance: float, maximum Euclidean distance for valid match (default: 100)

    Returns:
    - matches: list of (centroid_idx, expert_idx) tuples
    - match_distances: list of distances for each match
    """
    # Handle empty inputs
    if len(cluster_centroids) == 0 or len(expert_points) == 0:
        return [], []

    # Compute pairwise STANDARD Euclidean distances (not custom weighted)
    distances = cdist(cluster_centroids, expert_points, metric='euclidean')

    # Track which endpoints are already matched
    unmatched_centroids = set(range(len(cluster_centroids)))
    unmatched_experts = set(range(len(expert_points)))

    # Create list of valid candidate pairs
    valid_pairs = []
    for i in range(len(cluster_centroids)):
        for j in range(len(expert_points)):
            if distances[i, j] <= max_distance:
                valid_pairs.append((distances[i, j], i, j))

    # Sort by distance (ascending)
    valid_pairs.sort()

    # Greedy matching
    matches = []
    match_distances = []
    for dist, centroid_idx, expert_idx in valid_pairs:
        # Only match if both endpoints are still unmatched
        if centroid_idx in unmatched_centroids and expert_idx in unmatched_experts:
            matches.append((centroid_idx, expert_idx))
            match_distances.append(dist)
            unmatched_centroids.remove(centroid_idx)
            unmatched_experts.remove(expert_idx)

    return matches, match_distances
```

## Why Greedy Works Well

### 1. Computational Efficiency
- O(n·m log(n·m)) sorting + O(n·m) iteration
- Fast for typical image sizes (hundreds of points)

### 2. Reasonable Quality
- Greedy on sorted distances is "locally optimal"
- Avoids blocking good matches
- Not globally optimal, but typically within 5-10% of optimal

### 3. Interpretability
- Easy to verify: check that all matches are valid
- No complex hyperparameters to tune

### 4. Stability
- Deterministic output for same input
- No randomization

## Maximum Distance Constraint: 100 Pixels

The 100-pixel threshold:
- Represents typical cloud feature size in Mars images (~1728×880 pixels)
- Prevents spurious matches far from expert annotations
- Effective false positive filtering

```python
# Example: Rejecting distant matches
if distance > 100:
    # Skip this pair, do not consider for matching
    continue
```

## Computing Cluster Centroids

```python
def get_cluster_centroids(points, labels):
    """
    Compute centroid for each cluster from DBSCAN labels.

    Parameters:
    - points: (n_points, 2) array of [x, y] coordinates
    - labels: DBSCAN labels (integer, -1 for noise points)

    Returns:
    - centroids: (n_clusters, 2) array of cluster centroids (excluding noise)
    """
    unique_labels = set(labels)

    # Remove noise label (-1)
    if -1 in unique_labels:
        unique_labels.remove(-1)

    centroids = []
    for label in sorted(unique_labels):
        # Get all points with this label
        cluster_points = points[labels == label]

        # Compute mean coordinate
        centroid = cluster_points.mean(axis=0)
        centroids.append(centroid)

    return np.array(centroids) if centroids else np.empty((0, 2))
```

## Integration with DBSCAN

```python
from sklearn.cluster import DBSCAN

def cluster_and_match(image_points, expert_points, distance_matrix, epsilon, min_samples):
    """
    Complete workflow: DBSCAN → centroids → matching.
    """
    # Run DBSCAN with custom distance matrix
    clusterer = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
    labels = clusterer.fit_predict(distance_matrix)

    # Compute centroids
    centroids = get_cluster_centroids(image_points, labels)

    # Match centroids to experts (using standard Euclidean)
    matches, match_distances = greedy_match(centroids, expert_points, max_distance=100)

    return matches, match_distances
```

## Edge Cases

### 1. No Clusters
```python
if len(centroids) == 0:
    matches = []
    match_distances = []
    # → Results in: F1 = 0.0, delta = NaN
```

### 2. No Experts
```python
if len(expert_points) == 0:
    matches = []
    # → Results in: F1 = 0.0 (recall = 0), delta = NaN
```

### 3. No Valid Pairs (all distances > 100)
```python
valid_pairs = []  # Empty after filtering by max_distance
matches = []
# → Results in: F1 = 0.0, delta = NaN
```

### 4. Single Cluster and Single Expert
```python
if len(centroids) == 1 and len(expert_points) == 1:
    distance = euclidean_distance(centroids[0], expert_points[0])
    if distance <= 100:
        matches = [(0, 0)]
        match_distances = [distance]
    else:
        matches = []
        match_distances = []
```

## Verification

```python
def verify_matching(matches, n_clusters, n_experts):
    """
    Sanity checks for matching result.
    """
    # Check 1: No duplicate centroids
    centroid_indices = [m[0] for m in matches]
    assert len(centroid_indices) == len(set(centroid_indices)), \
        "Duplicate centroid in matches"

    # Check 2: No duplicate experts
    expert_indices = [m[1] for m in matches]
    assert len(expert_indices) == len(set(expert_indices)), \
        "Duplicate expert in matches"

    # Check 3: All indices in valid range
    assert all(0 <= i < n_clusters for i in centroid_indices), \
        "Centroid index out of range"
    assert all(0 <= j < n_experts for j in expert_indices), \
        "Expert index out of range"

    # Check 4: Matches ≤ min(clusters, experts)
    assert len(matches) <= min(n_clusters, n_experts), \
        "Too many matches"

    print(f"✓ Matching verified: {len(matches)} matches")
```

## Note: Standard vs. Custom Distance

**Critical**: Always use **standard Euclidean distance** for matching, NOT the custom weighted distance:

```python
# ✓ Correct: Standard Euclidean
distances = cdist(centroids, experts, metric='euclidean')

# ✗ Wrong: Using custom weighted distance would bias matching
# based on hyperparameter choice, not actual spatial accuracy
```

The custom distance is only for **clustering** (DBSCAN), not for **evaluation** or **matching**.
