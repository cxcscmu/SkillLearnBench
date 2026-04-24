---
name: model-verification-unit-tests
description: Verifies model components like loss functions using unit tests and saves the results as NumPy archives.
---

# Model Verification with Unit Tests

Verifying individual components of a training pipeline, such as a loss function, ensures mathematical correctness before full-scale training.

## Running Tests

Use the `unittest` framework or `pytest`. For a script like `unit_test_1.py`:

```bash
python unit_test/unit_test_1.py
```

## Data Persistence

To allow external verification of results, save computed tensors to a `.npz` file:

```python
import numpy as np

# In the test code:
np.savez(
    "/path/to/loss.npz",
    losses=losses.detach().cpu().numpy(),
)
```

## Fixed Tensor Inputs

When verifying a loss function, use fixed tensors to ensure deterministic output:

```python
# Loading pre-computed tensors
policy_chosen_logps = torch.load("path/to/tensor.pt")
```
