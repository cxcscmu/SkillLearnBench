name: mars-cloud-clustering
description: Clustering Mars cloud annotations using DBSCAN with a custom distance metric and evaluating against expert labels. Use this skill when processing citizen science data that needs to be matched to ground truth points.

# Mars Cloud Clustering Logic

This skill covers the implementation of DBSCAN with a custom distance metric and the evaluation of clusters against expert annotations.

## Custom Distance Metric
DBSCAN should use a custom distance metric defined as:
`d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)`
where `w` is the `shape_weight`.

Implementation in Python:
```python
import numpy as np
from sklearn.cluster import DBSCAN

def custom_metric(a, b, w):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return np.sqrt((w * dx)**2 + ((2 - w) * dy)**2)

# For use in DBSCAN (precompute or use a callable)
# metric=lambda u, v: custom_metric(u, v, w)
```

## Evaluation Workflow
For each image:
1. **Clustering**: Run DBSCAN on citizen science points.
2. **Centroids**: Compute the mean (x, y) for each cluster found.
3. **Greedy Matching**: 
   - Match centroids to expert points using standard Euclidean distance.
   - Use a greedy approach: match the closest pair first, then the next closest, etc.
   - Max distance threshold: 100 pixels.
4. **Metrics**:
   - **True Positives (TP)**: Number of matches.
   - **False Positives (FP)**: Number of clusters - TP.
   - **False Negatives (FN)**: Number of expert points - TP.
   - **F1 Score**: `2 * TP / (2 * TP + FP + FN)`
   - **Delta**: Average Euclidean distance of matched pairs.

## Averaging Across Images
- Include all expert images in the F1 average.
- If no points/clusters/matches, `F1 = 0.0` and `delta = NaN`.
- `avg_F1 = mean(all_F1s)`
- `avg_delta = mean(all_deltas excluding NaN)`
