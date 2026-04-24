---
name: run2_clustering_metrics
description: Compute and aggregate F1 score and delta from clustering evaluation across images
---

# Clustering Evaluation Metrics: F1 and Delta

## Metric 1: F1 Score (Per Image)

### Definition
F1 score measures balance between precision and recall for cluster-to-expert matching:

```
Precision = (# matched clusters) / (# clusters found)
Recall = (# matched clusters) / (# expert annotations)
F1 = 2 · (Precision · Recall) / (Precision + Recall)
```

**Interpretation**:
- F1 = 1.0: Perfect clusters matching all experts with no false positives
- F1 = 0.5: Balanced precision and recall at 50%
- F1 = 0.0: No clusters, no matches, or no clusters found

### Computation

```python
def compute_f1_score(n_clusters, n_experts, n_matches):
    """
    Compute F1 score from cluster-expert matching counts.

    Parameters:
    - n_clusters: int, number of clusters found by DBSCAN
    - n_experts: int, number of expert annotations in image
    - n_matches: int, number of successful cluster-expert matches

    Returns:
    - f1: float in [0.0, 1.0]
    """
    # Edge case: no clusters found
    if n_clusters == 0:
        return 0.0

    # Edge case: no expert annotations (degenerate)
    if n_experts == 0:
        return 0.0 if n_matches == 0 else 0.0

    # Compute precision and recall
    precision = n_matches / n_clusters
    recall = n_matches / n_experts

    # Compute F1
    denominator = precision + recall
    if denominator == 0:
        return 0.0

    f1 = 2 * precision * recall / denominator
    return f1
```

### Example Calculations

| n_clusters | n_experts | n_matches | Precision | Recall | F1 |
|------------|-----------|-----------|-----------|--------|-----|
| 3          | 3         | 3         | 1.00      | 1.00   | 1.00 |
| 5          | 3         | 3         | 0.60      | 1.00   | 0.75 |
| 3          | 5         | 3         | 1.00      | 0.60   | 0.75 |
| 4          | 5         | 2         | 0.50      | 0.40   | 0.44 |
| 0          | 3         | 0         | —         | 0.00   | 0.00 |

## Metric 2: Delta (Per Image)

### Definition
Delta is the average standard Euclidean distance between matched cluster centroids and their matched expert points:

```
delta = mean([distance(centroid_i, expert_j) for each match (i, j)])
```

**Interpretation**:
- delta ≈ 0: Clusters perfectly positioned at expert annotations
- delta ≈ 50: Clusters typically 50 pixels away from experts
- delta = NaN: No matches found (cannot compute average)

### Computation

```python
import numpy as np

def compute_delta(match_distances):
    """
    Compute average distance for matched pairs.

    Parameters:
    - match_distances: list or array of float distances for each match

    Returns:
    - delta: float (mean distance) or np.nan if no matches
    """
    if len(match_distances) == 0:
        return np.nan

    return np.mean(match_distances)


# Example
match_distances = [5.3, 8.2, 6.1]
delta = compute_delta(match_distances)
# delta = 6.53
```

## Aggregation: Across All Images

### Per-Image Loop

For each image in the **expert dataset** (including images with no citizen science data):

```python
def evaluate_all_images(citsci_df, expert_df, min_samples, epsilon, shape_weight):
    """
    Evaluate hyperparameters across all unique images from expert dataset.

    This loop is critical:
    - Iterates over ALL expert images (not just images with citizen science data)
    - If image has no citsci data: F1 = 0.0, delta = NaN
    - Includes F1 = 0.0 in average (all images contribute to F1 average)
    - Excludes delta = NaN from average (only images with matches counted)

    Returns:
    - avg_f1: average F1 across all expert images
    - avg_delta: average delta across images where matches were found
    """
    # Get ALL unique images from expert dataset
    expert_images = sorted(expert_df['file_rad'].unique())

    f1_scores = []
    delta_scores = []

    for image_id in expert_images:
        # Evaluate this image (handles case of no citizen science data)
        f1, delta = evaluate_image(
            image_id, citsci_df, expert_df,
            min_samples, epsilon, shape_weight
        )

        # IMPORTANT: Always include F1 in average
        f1_scores.append(f1)

        # IMPORTANT: Only include valid delta values
        if not np.isnan(delta):
            delta_scores.append(delta)

    # Aggregate
    avg_f1 = np.mean(f1_scores) if f1_scores else 0.0
    avg_delta = np.mean(delta_scores) if delta_scores else np.nan

    return avg_f1, avg_delta
```

### Key Aggregation Rules

**Rule 1: F1 Averaging**
- Include **all** images (even those with F1 = 0.0)
- Example: 369 images, 50 with F1 = 0.0, 319 with F1 > 0
- avg_F1 = (sum of all F1 values) / 369

**Rule 2: Delta Averaging**
- **Exclude** NaN values (use `np.nanmean` or conditional mean)
- Example: 369 images, 200 with valid delta, 169 with delta = NaN
- avg_delta = (sum of valid delta values) / 200

```python
# Correct delta averaging (exclude NaN)
avg_delta = np.nanmean([delta_scores]) if delta_scores else np.nan
# Equivalently:
avg_delta = np.mean([d for d in delta_scores if not np.isnan(d)])
```

### Cases Leading to delta = NaN

1. **No citizen science points**: DBSCAN finds no clusters
2. **No clusters found**: All points marked as noise by DBSCAN
3. **No matches**: All clusters > 100 pixels from expert points
4. **No expert points**: (rare, but handled gracefully)

## Complete Evaluation Loop

```python
def evaluate_single_hyperparams(min_samples, epsilon, shape_weight, citsci_df, expert_df):
    """
    Evaluate one hyperparameter combination.

    Returns: (F1_avg, delta_avg, min_samples, epsilon, shape_weight)
    """
    # Get all unique images from expert dataset
    expert_images = sorted(expert_df['file_rad'].unique())

    f1_scores = []
    delta_scores = []

    for image_id in expert_images:
        # Extract image-specific points
        citsci_points = citsci_df[citsci_df['file_rad'] == image_id][['x', 'y']].values
        expert_points = expert_df[expert_df['file_rad'] == image_id][['x', 'y']].values

        # If no citizen science data
        if len(citsci_points) == 0:
            f1_scores.append(0.0)
            # delta remains NaN
            continue

        # Compute custom distance matrix
        from skills.custom_distance_metrics import compute_custom_distance_matrix
        distances = compute_custom_distance_matrix(citsci_points, shape_weight)

        # Run DBSCAN
        from sklearn.cluster import DBSCAN
        clusterer = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
        labels = clusterer.fit_predict(distances)

        # Get centroids and match
        from skills.greedy_matching import get_cluster_centroids, greedy_match
        centroids = get_cluster_centroids(citsci_points, labels)
        matches, match_distances = greedy_match(centroids, expert_points, max_distance=100)

        # Compute metrics
        f1 = compute_f1_score(len(centroids), len(expert_points), len(matches))
        delta = compute_delta(match_distances)

        f1_scores.append(f1)
        if not np.isnan(delta):
            delta_scores.append(delta)

    # Aggregate across all images
    avg_f1 = np.mean(f1_scores)
    avg_delta = np.mean(delta_scores) if delta_scores else np.nan

    return avg_f1, avg_delta, min_samples, epsilon, shape_weight
```

## Filtering Results

After evaluating all hyperparameter combinations:

```python
import pandas as pd

# Create results DataFrame
results_df = pd.DataFrame(results_list,
    columns=['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight'])

# Filter to meaningful solutions (F1 > 0.5)
filtered_df = results_df[results_df['F1'] > 0.5].copy()

# Format output
output_df = filtered_df[['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight']].copy()
output_df['F1'] = output_df['F1'].round(5)
output_df['delta'] = output_df['delta'].round(5)
output_df['shape_weight'] = output_df['shape_weight'].round(1)

print(f"Total results: {len(results_df)}")
print(f"After filtering (F1 > 0.5): {len(output_df)}")
print(f"F1 range: [{output_df['F1'].min():.5f}, {output_df['F1'].max():.5f}]")
print(f"Delta range: [{output_df['delta'].min():.5f}, {output_df['delta'].max():.5f}]")
```

## Handling Special Cases

### Image with Expert Points but No Citizen Science
```python
if len(citsci_points) == 0:
    f1 = 0.0  # No clusters detected
    delta = np.nan  # Cannot compute distance
```

### Image with Citizen Science but No Expert Points
```python
if len(expert_points) == 0:
    # Clusters exist but no ground truth to match to
    # F1 = 0.0 (recall = 0)
    # delta = NaN
    f1 = 0.0
    delta = np.nan
```

### Multiple Images with delta = NaN
```python
# All f1_scores contribute to average (including 0.0)
avg_f1 = np.mean(f1_scores)  # ✓ Correct

# Only non-NaN delta values contribute
avg_delta = np.nanmean(delta_scores)  # ✓ Correct
# or
avg_delta = np.mean([d for d in delta_scores if not np.isnan(d)])
```
