---
name: greedy-point-matching
description: Match clustered centroids to expert annotations using greedy nearest-neighbor matching with distance constraints. Compute F1 scores and delta metrics for clustering quality assessment.
---

## Greedy Matching Algorithm

Match predicted cluster centroids to expert annotations for a single image:

1. **Initialize:** 
   - Set of predicted centroids (from DBSCAN clustering)
   - Set of expert points (ground truth annotations)
   - Maximum allowed distance threshold = 100 pixels

2. **Greedy Loop:**
   - While there are unmatched predictions and experts:
     - Find the pair (prediction, expert) with minimum standard Euclidean distance
     - If distance > 100 pixels, stop matching
     - Mark this pair as matched and remove from consideration
     - Record the distance for this match

3. **Output:**
   - List of matched pairs and their distances
   - Count of true positives, false positives, false negatives

## F1 Score Calculation

For a single image:

```
TP = number of matched pairs
FP = number of unmatched predictions
FN = number of unmatched expert points

Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

Handle edge cases:
- If TP = 0: F1 = 0.0
- If Precision + Recall = 0: F1 = 0.0

## Delta Metric

**Delta** = average standard Euclidean distance of all matched pairs:

```
delta = mean(distances of matched pairs)
```

If no matches found for an image, delta = NaN.

## Distance Metric Note

**Important:** Always use standard Euclidean distance for matching and delta calculation:
```
euclidean(a, b) = sqrt((Δx)² + (Δy)²)
```

This is different from the custom distance metric used in DBSCAN clustering.