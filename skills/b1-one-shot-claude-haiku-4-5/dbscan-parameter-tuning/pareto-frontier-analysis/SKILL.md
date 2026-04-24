---
name: pareto-frontier-analysis
description: Identify Pareto-optimal solutions from multi-objective optimization results.
---

# Pareto Frontier Analysis

## Overview
The Pareto frontier identifies non-dominated solutions where you cannot improve one objective without worsening another. For this task: maximize F1 score and minimize delta distance.

## Key Concepts

- **Dominated**: A solution is dominated if another solution has both better F1 AND better (lower) delta
- **Pareto-optimal**: A solution is not dominated by any other solution in the set
- **Pareto frontier**: The set of all Pareto-optimal solutions

## Implementation

```python
import numpy as np
import pandas as pd

def compute_pareto_frontier(results_df):
    """
    Find Pareto-optimal solutions from results.

    Args:
        results_df: DataFrame with columns 'f1' and 'delta'

    Returns:
        pareto_indices: Boolean array marking Pareto-optimal solutions
    """
    f1_scores = results_df['f1'].values
    deltas = results_df['delta'].values

    n = len(results_df)
    is_pareto = np.ones(n, dtype=bool)

    for i in range(n):
        # Check if solution i is dominated
        for j in range(n):
            if i == j:
                continue

            # Solution j dominates solution i if:
            # - j has better F1 (higher) AND
            # - j has better delta (lower)
            if f1_scores[j] > f1_scores[i] and deltas[j] < deltas[i]:
                is_pareto[i] = False
                break

    return is_pareto
```

## Alternative: Faster Implementation with NumPy

```python
def compute_pareto_frontier_fast(f1_scores, deltas):
    """Fast vectorized computation of Pareto frontier."""
    n = len(f1_scores)
    is_pareto = np.ones(n, dtype=bool)

    # For each solution, check if any other solution dominates it
    for i in range(n):
        dominated = (f1_scores > f1_scores[i]) & (deltas < deltas[i])
        if np.any(dominated):
            is_pareto[i] = False

    return is_pareto
```

## Visualization (Optional)

```python
import matplotlib.pyplot as plt

def plot_pareto_frontier(results_df, pareto_mask):
    """Visualize the Pareto frontier."""
    plt.figure(figsize=(10, 6))

    # Plot all points
    plt.scatter(results_df[~pareto_mask]['delta'],
                results_df[~pareto_mask]['f1'],
                alpha=0.3, label='Dominated', s=30)

    # Plot Pareto points
    pareto_df = results_df[pareto_mask]
    plt.scatter(pareto_df['delta'], pareto_df['f1'],
                color='red', label='Pareto-optimal', s=100, marker='*')

    plt.xlabel('Delta (Average Distance)')
    plt.ylabel('F1 Score')
    plt.title('Pareto Frontier')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
```

## Notes
- Handle NaN values in delta carefully (exclude from comparison or handle explicitly)
- The Pareto frontier typically forms a curved boundary in multi-objective space
- Points on the frontier represent trade-off solutions
