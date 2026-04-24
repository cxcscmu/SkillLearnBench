---
name: mars-clustering
description: How to optimize DBSCAN hyperparameters for Mars cloud clustering. Use this skill whenever performing grid search, DBSCAN clustering, or evaluating F1 and delta for Mars datasets.
---

# Mars Cloud Clustering Optimization Workflow

## 1. Data Preparation
- Load `citsci_train.csv` and `expert_train.csv` from `/root/data/`.
- Group by `file_rad` to match annotations.

## 2. DBSCAN Custom Distance Metric
Implement the custom distance function:
d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)

## 3. Evaluation Metrics
- **F1 Score**: Harmonic mean of Precision and Recall.
- **Delta**: Standard Euclidean distance between matched centroids and expert points.
- **Greedy Matching**: Match cluster centroids to expert points with max distance 100px.

## 4. Grid Search Parameters
- `min_samples`: [3, 4, 5, 6, 7, 8, 9]
- `epsilon`: [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
- `shape_weight`: [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]

## 5. Output
- Filter by mean F1 > 0.5.
- Identify Pareto-optimal frontier.
- Save to `/root/pareto_frontier.csv`.
