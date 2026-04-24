---
name: fixed-tensor-testing
description: Test ML functions with fixed input tensors for reproducibility.
---

# Testing with Fixed Input Tensors

## Purpose
Fixed tensor testing ensures deterministic, reproducible results for loss functions and model outputs. Enables verification without training dependencies.

## Creating Fixed Tensors

### 1. Deterministic Seeding
```python
import torch
import numpy as np

# Set all random seeds
torch.manual_seed(42)
np.random.seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)
```

### 2. Creating Test Tensors
```python
# Fixed log probabilities (typically negative)
log_probs = torch.randn(batch_size, seq_len)
# Ensure reasonable log prob range (e.g., -2 to 0)
log_probs = torch.clamp(log_probs, min=-5.0, max=0.0)

# Fixed sequence lengths
seq_lengths = torch.randint(10, 100, (batch_size,))

# Fixed input IDs (for masking)
input_ids = torch.randint(0, vocab_size, (batch_size, seq_len))
```

### 3. Example Test Setup
```python
batch_size = 4
seq_len = 10

# Generate fixed tensors
torch.manual_seed(123)
log_probs = torch.randn(batch_size, seq_len)
log_probs = torch.clamp(log_probs, -5.0, 0.0)

# Create mask (e.g., padding)
mask = torch.ones(batch_size, seq_len, dtype=torch.bool)
mask[:, seq_len-2:] = False  # Last 2 tokens are padding

# Lengths accounting for mask
seq_lengths = mask.sum(dim=1).float()
```

## Saving Test Results

### Save as .npz (NumPy Compressed)
```python
import numpy as np

results = {
    'losses': loss.cpu().detach().numpy(),
    'log_probs': log_probs.cpu().detach().numpy(),
}

np.savez_compressed('/path/to/results.npz', **results)
```

### Load .npz Files
```python
data = np.load('/path/to/results.npz')
losses = data['losses']
print(f"Shape: {losses.shape}, dtype: {losses.dtype}")
```

## Assertions and Validation

### Basic Checks
```python
# Loss should be finite and positive
assert torch.isfinite(loss).all(), "Loss contains NaN or Inf"
assert loss.item() > 0, "Loss should be positive"

# Shape validation
assert loss.shape == expected_shape, f"Shape mismatch: {loss.shape}"

# Range checks
assert loss.item() < 100, "Loss unreasonably large"
assert log_probs.min() >= -6.0, "Log probs too small"
```

### Reproducibility Checks
```python
# Run computation twice, should get same result
loss1 = compute_loss(fixed_tensors)
loss2 = compute_loss(fixed_tensors)
assert torch.allclose(loss1, loss2), "Loss not reproducible"
```

## Common Test Patterns

### 1. Unit Test for Loss Function
```python
def test_simpo_loss():
    # Setup fixed inputs
    batch_size = 8
    torch.manual_seed(42)

    log_probs = torch.randn(batch_size, 20)
    seq_lengths = torch.full((batch_size,), 20.0)

    # Compute loss
    beta = 2.0
    gamma = 1.0

    loss = compute_simpo_loss(log_probs, seq_lengths, beta, gamma)

    # Assertions
    assert loss.shape == torch.Size([])
    assert torch.isfinite(loss)
    assert loss.item() > 0

    return loss.item()
```

### 2. Gradient Flow Test
```python
# Ensure gradients can backpropagate
x = torch.randn(5, 10, requires_grad=True)
loss = some_loss_function(x)
loss.backward()
assert x.grad is not None
assert not torch.allclose(x.grad, torch.zeros_like(x.grad))
```

### 3. Numerical Stability Test
```python
# Test with extreme values
extreme_inputs = [
    torch.full((5,), -100.0),  # Very negative log probs
    torch.full((5,), 0.0),      # Zero log probs
    torch.zeros(5),             # All zeros
]

for inp in extreme_inputs:
    try:
        loss = compute_loss(inp)
        assert torch.isfinite(loss), f"Loss not finite for {inp}"
    except Exception as e:
        print(f"Failed with input {inp}: {e}")
```

## Best Practices

1. **Use consistent seeds** across test runs
2. **Document expected outputs** for regression testing
3. **Test edge cases** (empty batches, single samples, extreme values)
4. **Validate shapes** before and after operations
5. **Check numerical stability** with both typical and extreme inputs
6. **Save results** in standard formats (.npz, .pt, .json)

## Debugging Fixed Tensor Tests

```python
# Print intermediate values
def debug_loss(log_probs, seq_lengths, beta, gamma):
    rewards = beta * log_probs / seq_lengths.unsqueeze(1)
    print(f"Rewards shape: {rewards.shape}, min: {rewards.min():.4f}, max: {rewards.max():.4f}")

    # ... rest of computation

    print(f"Final loss: {loss.item():.6f}")
    return loss
```
