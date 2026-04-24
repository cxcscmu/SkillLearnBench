---
name: dbscan-custom-metric
description: Run DBSCAN clustering with a custom distance metric using sklearn, including how to define weighted Euclidean metrics and extract cluster centroids.
---

# DBSCAN with Custom Distance Metrics

## Overview

scikit-learn's DBSCAN accepts a `metric` parameter that can be a callable Python function. When using a custom metric, set `algorithm='ball_tree'` or `algorithm='brute'` (default `'auto'` may not support custom callables).

## Installation

```bash
pip install scikit-learn numpy
```

## Custom Metric Definition

A custom metric must accept two 1D arrays and return a scalar distance.

```python
import numpy as np

def weighted_euclidean(a, b, w=1.0):
    """
    Weighted Euclidean distance:
      d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)

    When w=1: standard Euclidean distance.
    w>1: attenuates y-distances (stretches x influence).
    w<1: attenuates x-distances (stretches y influence).
    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)
```

## Using with DBSCAN

DBSCAN requires a metric with a fixed signature `(a, b) -> float`. Use `functools.partial` or a closure to bind parameters:

```python
from sklearn.cluster import DBSCAN
from functools import partial
import numpy as np

def make_metric(shape_weight):
    def metric(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return np.sqrt((shape_weight * dx)**2 + ((2 - shape_weight) * dy)**2)
    return metric

# Run DBSCAN
points = np.array([[x1, y1], [x2, y2], ...])  # shape (N, 2)
dbscan = DBSCAN(eps=epsilon, min_samples=min_samples, metric=make_metric(1.2))
labels = dbscan.fit_predict(points)
```

**Important:** When using a custom callable metric, sklearn uses `algorithm='brute'` internally. You do NOT need to pass a precomputed distance matrix — just pass the raw points array.

## Extracting Cluster Centroids

```python
import numpy as np

def get_cluster_centroids(points, labels):
    """
    Returns array of centroids for each cluster (excluding noise label -1).
    points: np.array of shape (N, 2)
    labels: np.array of cluster labels from DBSCAN
    """
    unique_labels = set(labels) - {-1}  # exclude noise
    centroids = []
    for label in unique_labels:
        mask = labels == label
        centroid = points[mask].mean(axis=0)
        centroids.append(centroid)
    return np.array(centroids) if centroids else np.empty((0, 2))
```

## Greedy Matching of Centroids to Expert Points

Match predicted cluster centroids to expert annotations using greedy closest-pair matching with a max distance threshold:

```python
from scipy.spatial.distance import cdist

def greedy_match(pred_centroids, expert_points, max_dist=100):
    """
    Greedily match predicted centroids to expert points.
    Returns (matched_pred, matched_expert) index pairs and distances.
    Uses standard Euclidean distance (not custom metric).
    """
    if len(pred_centroids) == 0 or len(expert_points) == 0:
        return [], []

    dist_matrix = cdist(pred_centroids, expert_points, metric='euclidean')

    matched_pred = []
    matched_expert = []
    used_pred = set()
    used_expert = set()

    # Flatten and sort all pairs by distance
    pairs = sorted(
        [(dist_matrix[i, j], i, j)
         for i in range(len(pred_centroids))
         for j in range(len(expert_points))],
        key=lambda x: x[0]
    )

    for dist, i, j in pairs:
        if dist > max_dist:
            break
        if i not in used_pred and j not in used_expert:
            matched_pred.append(i)
            matched_expert.append(j)
            used_pred.add(i)
            used_expert.add(j)

    return matched_pred, matched_expert

def compute_f1_delta(pred_centroids, expert_points, max_dist=100):
    """
    Compute F1 score and average delta for one image.
    Returns (f1, delta) where delta is NaN if no matches found.
    """
    if len(pred_centroids) == 0 or len(expert_points) == 0:
        return 0.0, float('nan')

    dist_matrix = cdist(pred_centroids, expert_points, metric='euclidean')
    matched_pred, matched_expert = greedy_match(pred_centroids, expert_points, max_dist)

    tp = len(matched_pred)
    fp = len(pred_centroids) - tp
    fn = len(expert_points) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    if tp == 0:
        delta = float('nan')
    else:
        deltas = [dist_matrix[matched_pred[k], matched_expert[k]] for k in range(tp)]
        delta = np.mean(deltas)

    return f1, delta
```

## Full Pipeline Example

```python
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

citsci = pd.read_csv('citsci_train.csv')
expert = pd.read_csv('expert_train.csv')

all_images = expert['file_rad'].unique()

f1_scores, deltas = [], []
for img in all_images:
    cit_pts = citsci[citsci['file_rad'] == img][['x', 'y']].values
    exp_pts = expert[expert['file_rad'] == img][['x', 'y']].values

    if len(cit_pts) < min_samples:
        f1_scores.append(0.0)
        deltas.append(float('nan'))
        continue

    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples, metric=make_metric(shape_weight))
    labels = dbscan.fit_predict(cit_pts)
    centroids = get_cluster_centroids(cit_pts, labels)

    f1, delta = compute_f1_delta(centroids, exp_pts)
    f1_scores.append(f1)
    deltas.append(delta)

avg_f1 = np.mean(f1_scores)
valid_deltas = [d for d in deltas if not np.isnan(d)]
avg_delta = np.mean(valid_deltas) if valid_deltas else float('nan')
```
