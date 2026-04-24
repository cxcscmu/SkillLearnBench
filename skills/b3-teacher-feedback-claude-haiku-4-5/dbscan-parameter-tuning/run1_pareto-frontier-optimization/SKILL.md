---
name: pareto-frontier-optimization
description: Execute grid search over DBSCAN hyperparameters, evaluate each combination across all images, filter by F1 threshold, and identify Pareto-optimal solutions balancing F1 score and delta metric.
---

## Grid Search Space

Create all combinations of:

| Parameter | Range | Values |
|-----------|-------|--------|
| `min_samples` | 3–9 | [3, 4, 5, 6, 7, 8, 9] |
| `epsilon` | 4–24 (step 2) | [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24] |
| `shape_weight` | 0.9–1.9 (step 0.1) | [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9] |

**Total combinations:** 7 × 11 × 11 = 847

## Evaluation Pipeline

For each hyperparameter combination (min_samples, epsilon, shape_weight):

1. **Loop over all unique images** from expert dataset (using `file_rad`)
2. **For each image:**
   - Extract citizen science points for this image
   - If no citizen science points exist:
     - Set F1 = 0.0, delta = NaN
     - Continue to next image
   - Run DBSCAN with current hyperparameters on citizen science points
   - If no clusters found (all points noise or single cluster with < min_samples):
     - Set F1 = 0.0, delta = NaN
     - Continue to next image
   - Compute cluster centroids
   - Extract expert points for this image
   - Perform greedy matching of centroids to expert points
   - Compute F1 score and delta metric for this image

3. **Aggregate across images:**
   - Average F1: Include all F1 values (including 0.0)
   - Average delta: Only include non-NaN values
   - If all delta values are NaN (no matches found in any image), set average delta = NaN

4. **Filter results:**
   - Keep only results where average F1 > 0.5

## Pareto Frontier

Identify Pareto-optimal solutions:

A solution is **Pareto-optimal** if:
- No other solution has **both** higher F1 **and** lower delta
- It is not dominated on both objectives

**Optimization goals:**
- **Maximize** F1 score (higher is better)
- **Minimize** delta (lower is better)

## Parallelization

Recommended approach:
- Use `multiprocessing.Pool` or `joblib.Parallel` to evaluate hyperparameter combinations in parallel
- Each worker processes one or more complete combinations (all images for one hyperparameter set)
- Collect results and apply filtering/Pareto frontier detection on main process