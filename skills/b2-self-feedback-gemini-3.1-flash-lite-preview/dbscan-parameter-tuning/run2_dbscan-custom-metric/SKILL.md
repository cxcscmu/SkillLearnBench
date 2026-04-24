---
name: run2_dbscan-custom-metric
description: Implementation of DBSCAN with custom weighted Euclidean metric, optimized for parallel execution.
---

### Implementation
1. Always define the custom distance function at the module level or ensure it is picklable if using multiprocessing.
2. For high-performance grid search, consider pre-computing the distance matrix if the data allows.
3. Keep the metric definition simple to avoid overhead.
