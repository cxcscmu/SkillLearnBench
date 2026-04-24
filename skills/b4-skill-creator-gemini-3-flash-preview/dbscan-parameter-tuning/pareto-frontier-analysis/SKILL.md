name: pareto-frontier-analysis
description: Identifying Pareto-optimal points from a set of multi-objective results. Use this when you need to find the best trade-offs between conflicting goals like maximizing F1 and minimizing error.

# Pareto Frontier Analysis

The Pareto frontier consists of all points that are not dominated by any other point.

## Dominance Definition
A point $A$ dominates point $B$ if:
1. $A$ is at least as good as $B$ in all objectives.
2. $A$ is strictly better than $B$ in at least one objective.

For the Mars cloud task:
- Objective 1: Maximize F1
- Objective 2: Minimize Delta

Point $(f1_1, d_1)$ dominates $(f1_2, d_2)$ if:
- $(f1_1 \ge f1_2)$ AND $(d_1 \le d_2)$
- AND ($(f1_1 > f1_2)$ OR $(d_1 < d_2)$)

## Algorithm to Find Pareto Frontier
1. Filter results to meet baseline criteria (e.g., F1 > 0.5).
2. For each point $P$ in the filtered set:
   - Check if any other point $P'$ dominates $P$.
   - If no such $P'$ exists, $P$ is on the Pareto frontier.

## Implementation Tip
To speed up, sort the points by one objective (e.g., descending F1). Then, as you iterate, keep track of the minimum Delta seen so far.
