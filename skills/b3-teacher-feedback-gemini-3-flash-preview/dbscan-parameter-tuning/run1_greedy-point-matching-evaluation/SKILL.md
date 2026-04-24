---
name: greedy-point-matching-evaluation
description: Matching predicted cluster centroids to ground truth points using a greedy distance-based approach to calculate F1 score and precision/recall.
---

To evaluate clustering against expert "ground truth" points:

1.  **Centroid Calculation**: For each cluster found by DBSCAN, calculate the centroid (mean of $x$ and $y$ coordinates).
2.  **Distance Matrix**: Calculate standard Euclidean distance between all predicted centroids and all expert points for a specific image.
3.  **Greedy Matching**:
    *   Find the pair (centroid, expert point) with the smallest Euclidean distance.
    *   If distance $\le$ threshold (e.g., 100 pixels), count as a **True Positive (TP)** and remove both points from further matching for this image.
    *   Repeat until no more pairs can be matched under the threshold.
4.  **Metrics**:
    *   **TP**: Number of matched pairs.
    *   **FP** (False Positives): Number of unmatched predicted centroids.
    *   **FN** (False Negatives): Number of unmatched expert points.
    *   **F1 Score**: $2 \cdot TP / (2 \cdot TP + FP + FN)$. If $TP+FP+FN = 0$, F1 is typically 1.0 (though in this task, if no points exist/match, the requirement specifies 0.0).
    *   **Delta**: Average Euclidean distance of all matched TP pairs.