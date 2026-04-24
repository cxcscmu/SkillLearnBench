---
name: greedy-matching-evaluation
description: Evaluating clustering performance using greedy matching of predicted centroids against ground truth points.
---

### Matching Algorithm
For each image:
1.  **Centroid Extraction:** Calculate the arithmetic mean of all points assigned to each cluster ID (excluding noise points labeled -1).
2.  **Greedy Matching:**
    *   Calculate a distance matrix between all cluster centroids and expert points.
    *   Iteratively pick the pair with the smallest Euclidean distance (if `< 100` pixels).
    *   Remove these points from the pool and repeat until no pairs are within 100 pixels.
3.  **Metrics:**
    *   **True Positives (TP):** Number of matches found.
    *   **False Positives (FP):** Number of unmatched clusters.
    *   **False Negatives (FN):** Number of unmatched expert points.
    *   **F1 Score:** $2 * TP / (2 * TP + FP + FN)$.
    *   **Delta:** Mean standard Euclidean distance of matched pairs.

Ensure you handle images with zero citizen science points or zero expert points correctly by returning `F1=0.0` and `delta=NaN`.