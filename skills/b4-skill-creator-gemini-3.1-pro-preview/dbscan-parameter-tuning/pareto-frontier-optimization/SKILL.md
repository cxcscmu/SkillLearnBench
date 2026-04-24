---
name: pareto-frontier-optimization
description: Compute the Pareto frontier for multi-objective optimization. Use this skill whenever a task requires finding optimal trade-offs between conflicting metrics (e.g., maximize F1, minimize distance).
---

# Pareto Frontier Computation

The Pareto frontier consists of the non-dominated solutions in a multi-objective optimization problem.

## Manual Implementation

Here is a simple, robust manual implementation to filter a list of results (e.g. dictionaries) for Pareto optimality:

```python
def get_pareto_frontier(results, maximize_keys, minimize_keys):
    """
    results: list of dicts
    maximize_keys: list of strings (keys to maximize)
    minimize_keys: list of strings (keys to minimize)
    """
    pareto_optimal = []
    
    for i, candidate in enumerate(results):
        dominated = False
        for j, other in enumerate(results):
            if i == j: continue
            
            # Check if 'other' dominates 'candidate'
            # 'other' dominates if it is at least as good in ALL metrics, 
            # and strictly better in AT LEAST ONE.
            
            at_least_as_good = True
            strictly_better = False
            
            for key in maximize_keys:
                if other[key] < candidate[key]:
                    at_least_as_good = False
                    break
                if other[key] > candidate[key]:
                    strictly_better = True
                    
            if not at_least_as_good:
                continue
                
            for key in minimize_keys:
                if other[key] > candidate[key]:
                    at_least_as_good = False
                    break
                if other[key] < candidate[key]:
                    strictly_better = True
                    
            if at_least_as_good and strictly_better:
                dominated = True
                break
                
        if not dominated:
            pareto_optimal.append(candidate)
            
    return pareto_optimal
```
