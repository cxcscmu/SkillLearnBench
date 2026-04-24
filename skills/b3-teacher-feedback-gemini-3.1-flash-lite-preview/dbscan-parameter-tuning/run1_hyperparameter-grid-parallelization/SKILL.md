---
name: hyperparameter-grid-parallelization
description: Efficiently executing grid search over massive parameter spaces using Python multiprocessing.
---

### Parallel Execution
Use `multiprocessing.Pool` to distribute image-level processing. Since you are performing a grid search:
1.  **Outer Loop:** Define the product of hyperparameter combinations:
    ```python
    import itertools
    params = list(itertools.product(min_samples_range, epsilon_range, shape_weight_range))
    ```
2.  **Mapping:** Use `pool.starmap` to pass a function that performs the loop over `unique(file_rad)` for each parameter set.
3.  **Memory Management:** Ensure that individual worker processes clean up memory (DBSCAN structures) to prevent OOM errors, as the grid space involves hundreds of combinations.