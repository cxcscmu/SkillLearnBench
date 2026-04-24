---
name: run2_pareto_frontier
description: Find Pareto-optimal solutions balancing multiple conflicting objectives with rigorous verification
---

# Pareto Frontier: Multi-Objective Optimization

## Problem Definition

**Objectives**:
- Maximize F1 score (higher is better)
- Minimize delta (lower is better)

These objectives are **conflicting**: improving one typically worsens the other.

## Pareto Dominance

Solution **A dominates B** if:
1. A is **at least as good** in all objectives: F1_A ≥ F1_B AND delta_A ≤ delta_B
2. A is **strictly better** in at least one: F1_A > F1_B OR delta_A < delta_B

A solution is **Pareto-optimal** (non-dominated) if no other solution dominates it.

## Algorithm: Complete Dominance Check

```python
import numpy as np
import pandas as pd

def is_dominated(i, F1, delta):
    """
    Check if point i is dominated by any other point.
    """
    f1_i, delta_i = F1[i], delta[i]

    for j in range(len(F1)):
        if i == j:
            continue

        f1_j, delta_j = F1[j], delta[j]

        # Check if j dominates i
        if (f1_j >= f1_i and delta_j <= delta_i and
            (f1_j > f1_i or delta_j < delta_i)):
            return True  # j dominates i

    return False


def find_pareto_frontier(results_df):
    """
    Identify all Pareto-optimal solutions.

    Parameters:
    - results_df: DataFrame with columns ['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight']

    Returns:
    - pareto_df: Subset of results_df containing only Pareto-optimal points
    """
    F1 = results_df['F1'].values
    delta = results_df['delta'].values

    n = len(results_df)
    pareto_mask = np.ones(n, dtype=bool)

    for i in range(n):
        if is_dominated(i, F1, delta):
            pareto_mask[i] = False

    return results_df[pareto_mask].copy()
```

## Input Filtering: F1 > 0.5

**Before** finding the Pareto frontier, filter to meaningful solutions:

```python
# Filter by F1 > 0.5
filtered_df = results_df[results_df['F1'] > 0.5].copy()

# Then find Pareto frontier on filtered set
pareto_df = find_pareto_frontier(filtered_df)
```

**Rationale**:
- F1 ≤ 0.5 indicates poor clustering agreement with expert labels
- Threshold of 0.5 balances precision and recall below 50%, which is minimally useful
- Filtering reduces noise and focuses on practical solutions

## Output Formatting

```python
def format_pareto_output(pareto_df):
    """
    Format Pareto frontier for CSV output.
    """
    output_df = pareto_df[['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight']].copy()

    # Round according to specifications
    output_df['F1'] = output_df['F1'].round(5)
    output_df['delta'] = output_df['delta'].round(5)
    output_df['shape_weight'] = output_df['shape_weight'].round(1)

    # Integer columns stay as integers
    output_df['min_samples'] = output_df['min_samples'].astype(int)
    output_df['epsilon'] = output_df['epsilon'].astype(int)

    # Sort by delta for readability (ascending)
    output_df = output_df.sort_values('delta').reset_index(drop=True)

    return output_df


# Example
pareto_df = find_pareto_frontier(results_df[results_df['F1'] > 0.5])
output_df = format_pareto_output(pareto_df)
output_df.to_csv('pareto_frontier.csv', index=False)
```

## Properties of Pareto Frontier

### 1. Non-Dominated
Every point on the frontier is Pareto-optimal.

### 2. Ordered in Objectives
- As F1 increases, delta typically increases (trade-off)
- Frontier forms a curve balancing both objectives

### 3. Decision Support
Different stakeholders can choose based on preferences:
- **Maximize accuracy**: Choose solution with highest F1 (rightmost)
- **Minimize error**: Choose solution with lowest delta (leftmost)
- **Balanced**: Choose midpoint of frontier

## Verification Steps

```python
def verify_pareto_frontier(pareto_df, all_results_df):
    """
    Sanity checks for Pareto frontier.
    """
    F1_pareto = pareto_df['F1'].values
    delta_pareto = pareto_df['delta'].values
    F1_all = all_results_df['F1'].values
    delta_all = all_results_df['delta'].values

    # Check 1: Max F1 is on frontier
    max_f1_idx = F1_all.argmax()
    assert max_f1_idx in pareto_df.index, "Max F1 must be on frontier"

    # Check 2: Min delta is on frontier (of F1 > 0.5)
    min_delta_idx = delta_all.argmin()
    if F1_all[min_delta_idx] > 0.5:
        assert min_delta_idx in pareto_df.index, "Min delta must be on frontier"

    # Check 3: No point outside frontier dominates any frontier point
    for i in pareto_df.index:
        f1_i, delta_i = F1_all[i], delta_all[i]
        for j in range(len(all_results_df)):
            if j == i or j not in pareto_df.index:
                continue
            f1_j, delta_j = F1_all[j], delta_all[j]
            # Non-frontier point j should not dominate frontier point i
            assert not (f1_j > f1_i and delta_j < delta_i), \
                f"Non-frontier point {j} dominates frontier point {i}"

    print("✓ Pareto frontier verification passed")
```

## Edge Cases

### No Solutions with F1 > 0.5
```python
filtered_df = results_df[results_df['F1'] > 0.5]
if len(filtered_df) == 0:
    print("No solutions with F1 > 0.5")
    pareto_df = pd.DataFrame(columns=['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight'])
else:
    pareto_df = find_pareto_frontier(filtered_df)
```

### Tied Solutions (same F1 and delta)
- Both are Pareto-optimal (neither dominates the other)
- Both should appear in frontier

### NaN Values
- Exclude rows with NaN in F1 or delta before Pareto frontier computation
- (These should already be filtered during evaluation)

## Summary Statistics

```python
def pareto_summary(pareto_df):
    """Print summary of Pareto frontier."""
    print(f"Pareto frontier size: {len(pareto_df)}")
    print(f"F1 range: [{pareto_df['F1'].min():.5f}, {pareto_df['F1'].max():.5f}]")
    print(f"Delta range: [{pareto_df['delta'].min():.5f}, {pareto_df['delta'].max():.5f}]")
    print(f"Shape weight distribution:")
    print(pareto_df['shape_weight'].value_counts().sort_index())
```
