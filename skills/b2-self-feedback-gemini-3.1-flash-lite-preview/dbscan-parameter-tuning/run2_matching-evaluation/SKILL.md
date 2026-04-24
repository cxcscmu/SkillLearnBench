---
name: run2_matching-evaluation
description: Efficient greedy matching of cluster centroids to expert points with distance constraint.
---

### Logic
1. For each image, build a full distance matrix (N centroids x M experts).
2. Sorting the entire matrix allows for optimal greedy matching without repeated searching.
3. Ensure the distance constraint (max distance 100 pixels) is applied strictly.
