---
name: pareto-frontier-identification
description: Identifying the set of non-dominated solutions in a multi-objective optimization problem.
---

In multi-objective optimization (e.g., maximizing F1 while minimizing Delta), a solution is **Pareto optimal** if no other solution is better in both metrics.

**Algorithm to find Pareto Frontier:**
1.  Start with a list of candidate points (after filtering for `F1 > 0.5`).
2.  A point $A$ is "dominated" by point $B$ if:
    *   $F1_B \ge F1_A$ AND $Delta_B \le Delta_A$
    *   AND at least one inequality is strict.
3.  The Pareto frontier consists of all points that are not dominated by any other point in the set.

**Implementation Tip:**
Sort the candidates by one objective (e.g., F1 descending) first. This simplifies the comparison logic as you iterate through the list to check for dominance.