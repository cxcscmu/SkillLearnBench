---
name: run2_pareto-optimization
description: Identifying Pareto-optimal solutions for multi-objective optimization (maximize F1, minimize delta).
---

# Pareto Frontier for Multi-Objective Optimization

## Definition
Point A dominates Point B iff:
- A.F1 >= B.F1 AND A.delta <= B.delta
- With at least one strict inequality

A point is Pareto-optimal if no other point dominates it.

## Efficient Implementation

```python
def find_pareto(results):
    """results: list of (f1, delta, ...) tuples. Maximize f1, minimize delta."""
    # Sort by F1 descending for efficiency
    indexed = sorted(enumerate(results), key=lambda x: -x[1][0])
    pareto = []
    min_delta = float('inf')

    for idx, r in indexed:
        if r[1] <= min_delta:
            pareto.append(r)
            min_delta = r[1]

    return pareto
```

This O(n log n) approach works because after sorting by F1 descending, a point is Pareto-optimal iff its delta is less than or equal to the minimum delta seen so far.
