---
name: pareto-frontier
description: Identify Pareto-optimal points from a set of multi-objective solutions.
---

# Pareto Frontier Identification

A point is Pareto-optimal if no other point is better in all objectives. For this task, we want to maximize F1 and minimize Delta.

## Logic
A solution `A` dominates `B` if:
1. `A.F1 >= B.F1` AND `A.Delta <= B.Delta`
2. At least one inequality is strict.

## Python Implementation
```python
def is_pareto_efficient(costs):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array where costs are to be MINIMIZED.
    :return: A boolean array of length n_points indicating efficiency.
    """
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            # Keep any point that is better than 'c' in at least one attribute
            # OR equal in all attributes (to handle duplicates)
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1) | \
                                          np.all(costs[is_efficient] == c, axis=1)
            is_efficient[i] = True  # And keep self
    return is_efficient

# For Max F1 and Min Delta, transform F1:
# costs = np.array([[-f1, delta] for f1, delta in results])
# efficient_mask = is_pareto_efficient(costs)
```
