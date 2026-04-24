---
name: dbscan-custom-distance-clustering
description: Implement DBSCAN clustering with a custom weighted Euclidean distance metric controlled by shape_weight parameter. Use this skill to cluster citizen science point annotations on Mars cloud images.
---

## Overview

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) is a clustering algorithm that groups points based on density. This implementation uses a **custom distance metric** that weights x and y dimensions asymmetrically.

## Custom Distance Metric

The distance between points `a` and `b` is:

```
d(a, b) = sqrt((w * Δx)² + ((2 - w) * Δy)²)
```

Where:
- `w` = `shape_weight` parameter (0.9–1.9)
- `Δx` = difference in x-coordinates
- `Δy` = difference in y-coordinates

**Interpretation:**
- When `w = 1.0`: Standard Euclidean distance
- When `w > 1.0`: y-distances are attenuated (points closer in y-direction are grouped together more easily)
- When `w < 1.0`: x-distances are attenuated (points closer in x-direction are grouped together more easily)

## DBSCAN Parameters

- **epsilon** (eps): Maximum distance between two points for them to be in the same neighborhood
- **min_samples**: Minimum number of points in a neighborhood for a point to be considered a core point

## Implementation Notes

1. Use scikit-learn's DBSCAN with a custom metric function or distance matrix
2. Compute cluster centroids as the mean (x, y) of all points in each cluster
3. Ignore noise points (label = -1) when computing centroids
4. Return only valid clusters (at least 1 cluster found)