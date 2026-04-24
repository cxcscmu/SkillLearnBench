---
name: pareto-frontier-optimization
description: Identifying Pareto-optimal points in a multi-objective optimization space.
---

### Pareto Logic
A solution $(F1_a, \Delta_a)$ dominates $(F1_b, \Delta_b)$ if:
- $(F1_a \ge F1_b)$ and $(\Delta_a \le \Delta_b)$
- At least one inequality is strict.

To extract the Pareto frontier from a results list:
1.  Initialize an empty list `pareto_points`.
2.  For each candidate $A$:
    *   Check if any other candidate $B$ exists such that $B$ dominates $A$.
    *   If no $B$ dominates $A$, $A$ is on the frontier.

*Efficiency Tip:* For large search spaces, sort by $F1$ descending, then iterate through to keep only those that show a decrease in $\Delta$.