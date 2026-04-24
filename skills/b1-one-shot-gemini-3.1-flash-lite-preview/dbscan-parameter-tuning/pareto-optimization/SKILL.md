---
name: pareto-optimization
description: Identifying the Pareto frontier in multi-objective optimization.
---

### Logic
A point is Pareto-optimal if no other point dominates it. In this context, we want to maximize F1 and minimize delta. Point A dominates point B if F1_A >= F1_B and Delta_A <= Delta_B (with at least one inequality strict).

```python
def get_pareto_frontier(points):
    # points: list of (f1, delta, ...)
    # Return points that are not dominated
    pareto = []
    for i, p1 in enumerate(points):
        is_dominated = False
        for j, p2 in enumerate(points):
            if i == j: continue
            # Check if p2 dominates p1 (p2 has better or equal f1, lower or equal delta)
            if p2[0] >= p1[0] and p2[1] <= p1[1]:
                # If they are strictly better in one dimension, it dominates
                if p2[0] > p1[0] or p2[1] < p1[1]:
                    is_dominated = True
                    break
        if not is_dominated:
            pareto.append(p1)
    return pareto
```
