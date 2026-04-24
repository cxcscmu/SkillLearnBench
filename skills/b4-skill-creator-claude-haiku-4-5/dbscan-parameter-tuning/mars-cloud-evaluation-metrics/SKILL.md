---
name: mars-cloud-evaluation-metrics
description: Compute F1 score and delta (average distance) metrics for Mars cloud cluster evaluation. Use this skill when evaluating DBSCAN clustering results against expert annotations, including handling edge cases like images with no clusters, no expert points, or no matches.
---

# Mars Cloud Evaluation Metrics

## Overview

Evaluation requires computing per-image F1 scores and delta (average matching distance), then averaging across all images with specific handling for edge cases.

## Metrics Definition

### F1 Score (per-image)

F1 is based on match counts:
- **True Positives (TP)**: Number of successful matches (cluster → expert)
- **False Positives (FP)**: Unmatched clusters (cluster with no expert match)
- **False Negatives (FN)**: Unmatched experts (expert with no cluster match)

```
Precision = TP / (TP + FP)     if (TP + FP) > 0 else 0
Recall = TP / (TP + FN)         if (TP + FN) > 0 else 0
F1 = 2 * (Precision * Recall) / (Precision + Recall)     if (P + R) > 0 else 0
```

### Delta (per-image)

Average standard Euclidean distance of matched pairs:

```
delta = mean([distance for (centroid, expert, distance) in matches])
```

If no matches, delta = NaN.

## Implementation

```python
import numpy as np

def compute_f1_and_delta(matches, n_clusters, n_experts):
    """
    Compute F1 score and delta for a single image.

    Parameters
    ----------
    matches : list of tuples
        List of (centroid_idx, expert_idx, distance) from greedy matching
    n_clusters : int
        Total number of cluster centroids
    n_experts : int
        Total number of expert annotations

    Returns
    -------
    f1 : float
        F1 score (0.0 to 1.0)
    delta : float
        Average distance of matched pairs, or NaN if no matches
    """
    tp = len(matches)
    fp = n_clusters - tp
    fn = n_experts - tp

    # Compute precision, recall, F1
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Compute delta
    if tp > 0:
        distances = [d for _, _, d in matches]
        delta = np.mean(distances)
    else:
        delta = np.nan

    return f1, delta
```

## Per-Hyperparameter Evaluation

After running DBSCAN on all images for a given hyperparameter set:

```python
def evaluate_hyperparameters(hyperparams, citizen_df, expert_df):
    """
    Evaluate a DBSCAN hyperparameter set across all images.

    Parameters
    ----------
    hyperparams : dict
        {epsilon, min_samples, shape_weight}
    citizen_df : pandas DataFrame
        Citizen science data (columns: file_rad, x, y)
    expert_df : pandas DataFrame
        Expert annotations (columns: file_rad, x, y)

    Returns
    -------
    f1_avg : float
        Average F1 across all images (includes 0.0 for images with no clusters)
    delta_avg : float
        Average delta across images with matches (NaN values excluded)
    """
    f1_scores = []
    deltas = []

    # Loop over ALL unique images in expert dataset
    unique_images = expert_df['file_rad'].unique()

    for image in unique_images:
        citizen_pts = citizen_df[citizen_df['file_rad'] == image][['x', 'y']].values
        expert_pts = expert_df[expert_df['file_rad'] == image][['x', 'y']].values

        # Run DBSCAN on citizen points
        if len(citizen_pts) == 0:
            # No citizen science points: F1 = 0, delta = NaN
            f1, delta = 0.0, np.nan
        else:
            # DBSCAN clustering with custom metric (implementation in separate module)
            # Returns: matches, n_clusters, centroids
            matches, centroids = cluster_and_match_image(
                citizen_pts, expert_pts, hyperparams
            )
            f1, delta = compute_f1_and_delta(matches, len(centroids), len(expert_pts))

        f1_scores.append(f1)
        if not np.isnan(delta):
            deltas.append(delta)

    # Compute averages
    f1_avg = np.mean(f1_scores) if f1_scores else 0.0
    delta_avg = np.mean(deltas) if deltas else np.nan

    return f1_avg, delta_avg
```

## Edge Cases

| Scenario | F1 | Delta |
|----------|-----|-------|
| Image has no citizen science points | 0.0 | NaN |
| DBSCAN finds no clusters (all noise) | 0.0 | NaN |
| No matches found (distances > 100 px) | 0.0 | NaN |
| Matches found | computed | computed |

## Filtering Rule

Only keep results where **average F1 > 0.5**. This ensures meaningful clustering performance.

## Key Points

1. **F1 includes zeros**: Always average F1 across ALL images, including 0.0 for images with no clusters
2. **Delta excludes NaN**: Average delta only over images where at least one match was found
3. **Loop over expert images**: Use all unique images from expert dataset, not citizen science dataset
4. **Standard distances**: All distance computations use standard Euclidean metric
