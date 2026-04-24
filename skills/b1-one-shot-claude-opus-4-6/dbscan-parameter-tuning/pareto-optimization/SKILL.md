---
name: pareto-optimization
description: Multi-objective optimization with Pareto frontiers for finding trade-off solutions between conflicting objectives.
---

# Pareto Frontier Computation

## Definition
A point is Pareto-optimal if no other point is better in ALL objectives simultaneously.

## For Maximize F1, Minimize Delta

```python
import numpy as np

def pareto_frontier(results):
    """Find Pareto-optimal points.
    results: list of (f1, delta, ...) tuples
    Maximize f1, minimize delta.
    """
    arr = np.array([(r[0], r[1]) for r in results])
    is_pareto = np.ones(len(arr), dtype=bool)
    for i in range(len(arr)):
        if not is_pareto[i]:
            continue
        for j in range(len(arr)):
            if i == j or not is_pareto[j]:
                continue
            # j dominates i if j has >= f1 AND <= delta, with at least one strict
            if arr[j, 0] >= arr[i, 0] and arr[j, 1] <= arr[i, 1]:
                if arr[j, 0] > arr[i, 0] or arr[j, 1] < arr[i, 1]:
                    is_pareto[i] = False
                    break
    return [r for r, p in zip(results, is_pareto) if p]
```

## Key Points
- Point A dominates B if A is at least as good in all objectives and strictly better in at least one
- Pareto frontier = set of all non-dominated points
- For maximize F1 + minimize delta: A dominates B if A.f1 >= B.f1 AND A.delta <= B.delta (with at least one strict inequality)
