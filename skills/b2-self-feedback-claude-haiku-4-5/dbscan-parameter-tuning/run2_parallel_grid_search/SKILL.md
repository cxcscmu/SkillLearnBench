---
name: run2_parallel_grid_search
description: Efficient parallel hyperparameter grid search using joblib with 847 combinations
---

# Parallel Grid Search Optimization

## Grid Search Space

For Mars cloud clustering, evaluate all combinations of:
- **min_samples**: 3, 4, 5, 6, 7, 8, 9 (7 values)
- **epsilon**: 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24 (11 values)
- **shape_weight**: 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9 (11 values)

Total combinations: 7 × 11 × 11 = **847**

## Parallelization with joblib

### Setup

```python
from joblib import Parallel, delayed
import pandas as pd
import numpy as np

# Define hyperparameter ranges
min_samples_vals = list(range(3, 10))
epsilon_vals = list(range(4, 26, 2))
shape_weight_vals = list(np.round(np.arange(0.9, 2.0, 0.1), 1))

# Generate all combinations
hp_list = []
for ms in min_samples_vals:
    for eps in epsilon_vals:
        for sw in shape_weight_vals:
            hp_list.append((ms, eps, sw))

print(f"Total combinations: {len(hp_list)}")  # Should be 847
```

### Evaluation Function

Each worker evaluates one hyperparameter combination:

```python
def evaluate_hyperparams(min_samples, epsilon, shape_weight, citsci_df, expert_df, expert_images):
    """
    Evaluate one hyperparameter combination across all expert images.

    Returns: (F1_avg, delta_avg, min_samples, epsilon, shape_weight)
    """
    f1_scores = []
    delta_scores = []

    for image_id in expert_images:
        f1, delta = evaluate_image(image_id, citsci_df, expert_df,
                                    min_samples, epsilon, shape_weight)
        f1_scores.append(f1)
        if not np.isnan(delta):
            delta_scores.append(delta)

    avg_f1 = np.mean(f1_scores) if f1_scores else 0.0
    avg_delta = np.mean(delta_scores) if delta_scores else np.nan

    return avg_f1, avg_delta, min_samples, epsilon, shape_weight
```

### Parallel Execution

```python
# Load data once, before parallelization
citsci_df = pd.read_csv('/root/data/citsci_train.csv')
expert_df = pd.read_csv('/root/data/expert_train.csv')
expert_images = sorted(expert_df['file_rad'].unique())

# Evaluate all combinations in parallel
results = Parallel(n_jobs=-1, verbose=1)(
    delayed(evaluate_hyperparams)(ms, eps, sw, citsci_df, expert_df, expert_images)
    for ms, eps, sw in hp_list
)

# Convert results to DataFrame
results_df = pd.DataFrame(results,
    columns=['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight'])
```

## Joblib Parameters

### n_jobs=-1
Uses all available CPU cores. For typical 22-core machines:
- ~22 parallel workers
- 847 combinations ÷ 22 ≈ 39 tasks per worker
- Total time: ~1.7 minutes (vs. ~60+ minutes sequentially)

### verbose=1
Prints progress:
```
[Parallel(n_jobs=-1)]: Done   6 tasks      | elapsed:    3.0s
[Parallel(n_jobs=-1)]: Done 156 tasks      | elapsed:   20.7s
[Parallel(n_jobs=-1)]: Done 847 out of 847 | elapsed:  1.7min finished
```

## Memory Efficiency

### Data Sharing
Using Unix fork (default for Loky backend):
- Data loaded once in parent process
- Child processes inherit via copy-on-write
- No duplication overhead

### Per-Evaluation Memory
Each worker needs:
- DBSCAN per image: O(n²) for distance matrix (n = points per image)
- Typical image: 50-100 points → 3KB-10KB distance matrix
- All workers combined: reasonable memory usage

```python
# Load data BEFORE parallel section
citsci_df = pd.read_csv('/root/data/citsci_train.csv')
expert_df = pd.read_csv('/root/data/expert_train.csv')
expert_images = sorted(expert_df['file_rad'].unique())

# Pass as parameters (more efficient than loading in each worker)
results = Parallel(n_jobs=-1)(
    delayed(evaluate_hyperparams)(ms, eps, sw,
                                   citsci_df, expert_df, expert_images)
    for ms, eps, sw in hp_list
)
```

## Progress Tracking Alternatives

### Option 1: joblib verbose
```python
results = Parallel(n_jobs=-1, verbose=10)(
    delayed(fn)(args) for args in arguments
)
# verbose levels: 1=minimal, 5=moderate, 10=detailed
```

### Option 2: tqdm progress bar
```python
from tqdm import tqdm

results = Parallel(n_jobs=-1)(
    delayed(fn)(args)
    for args in tqdm(arguments, total=len(arguments))
)
```

### Option 3: Custom progress tracking
```python
from joblib import Parallel, delayed, parallel_backend

def progress_callback(n_tasks):
    """Called every n_tasks completed."""
    print(f"Progress: {n_tasks} tasks completed")

results = Parallel(n_jobs=-1)(
    delayed(fn)(args) for args in arguments
)
```

## Results Aggregation

```python
# All results collected after parallel section completes
results_df = pd.DataFrame(results,
    columns=['F1', 'delta', 'min_samples', 'epsilon', 'shape_weight'])

# Verify completeness
assert len(results_df) == 847, "Missing results"

# Analyze
print(f"F1 range: [{results_df['F1'].min():.5f}, {results_df['F1'].max():.5f}]")
print(f"Delta range: [{results_df['delta'].min():.5f}, {results_df['delta'].max():.5f}]")
print(f"Solutions with F1 > 0.5: {(results_df['F1'] > 0.5).sum()}")
```

## Error Handling

### Timeout Protection
```python
# Set timeout for long-running tasks
results = Parallel(n_jobs=-1, timeout=300)(  # 5 minutes per task
    delayed(evaluate_hyperparams)(ms, eps, sw, citsci_df, expert_df, expert_images)
    for ms, eps, sw in hp_list
)
```

### Worker Crash Recovery
```python
# If a worker crashes, task fails and exception propagates
# Typical causes:
# - Out of memory
# - Segmentation fault
# - Infinite loop (timeout helps)

# Recovery: Increase memory, reduce n_jobs, or fix underlying issue
```

## Performance Optimization

### Batch Size
```python
# Parallel can batch tasks for efficiency
results = Parallel(n_jobs=-1, batch_size='auto')(
    delayed(fn)(args) for args in arguments
)
```

### Backend Selection
```python
from joblib import parallel_backend

# Loky backend (default, most robust)
with parallel_backend('loky', n_jobs=-1):
    results = Parallel()(delayed(fn)(args) for args in arguments)

# Threading backend (for I/O-bound tasks, lower overhead)
with parallel_backend('threading', n_jobs=-1):
    results = Parallel()(delayed(fn)(args) for args in arguments)
```

## Reproducibility

```python
# Set random seed for reproducibility
import numpy as np
np.random.seed(42)

# Note: DBSCAN is deterministic (no randomness)
# Parallelization doesn't affect results (only speed)
```

## Typical Performance

For 847 DBSCAN evaluations across 369 images:

| Configuration | Time |
|---|---|
| Sequential (1 core) | ~60-90 minutes |
| Parallel (22 cores) | ~1.5-2 minutes |
| Speedup | ~40-45× |

## Debugging Parallel Code

```python
# Test single evaluation first
result = evaluate_hyperparams(3, 4, 0.9, citsci_df, expert_df, expert_images)
print(result)

# Then enable parallelization
results = Parallel(n_jobs=-1, verbose=10)(
    delayed(evaluate_hyperparams)(ms, eps, sw, citsci_df, expert_df, expert_images)
    for ms, eps, sw in hp_list[:10]  # Test on subset first
)

# Finally, full grid search
results = Parallel(n_jobs=-1, verbose=1)(
    delayed(evaluate_hyperparams)(ms, eps, sw, citsci_df, expert_df, expert_images)
    for ms, eps, sw in hp_list
)
```

## Key Takeaways

1. **Load data before parallelization**: Avoids redundant I/O in each worker
2. **Return simple types**: Tuples faster than dictionaries or objects
3. **Use n_jobs=-1**: Automatic CPU count detection and full utilization
4. **Monitor progress**: verbose=1 or tqdm for user feedback
5. **Test sequentially first**: Easier debugging before parallel execution
6. **Check results completeness**: Verify all 847 combinations evaluated
