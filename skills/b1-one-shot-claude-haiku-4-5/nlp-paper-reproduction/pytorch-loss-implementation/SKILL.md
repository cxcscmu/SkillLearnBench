---
name: pytorch-loss-implementation
description: Implement loss functions in PyTorch with proper tensor operations.
---

# PyTorch Loss Implementation

## Key Concepts

### 1. Tensor Operations
```python
import torch

# Sigmoid function
sigmoid_output = torch.sigmoid(input_tensor)

# Log function
log_output = torch.log(input_tensor)

# Mean reduction
mean_loss = loss.mean()

# Sum reduction
sum_loss = loss.sum()
```

### 2. Batch Processing
```python
# Batch dimension handling
batch_size = tensor.shape[0]
x = tensor[:batch_size//2]  # First half
y = tensor[batch_size//2:]  # Second half

# Ensure same device and dtype
tensor = tensor.to(device=model.device, dtype=torch.float32)
```

### 3. Numerical Stability

**Log-Sigmoid Stability**
```python
# Avoid: log(sigmoid(x)) can cause numerical issues
# Instead use:
stable_loss = torch.nn.functional.logsigmoid(x)
# Or manually:
loss = -torch.log(torch.sigmoid(x) + 1e-10)
```

**Handling Small Values**
```python
# Add epsilon to avoid log(0)
safe_log = torch.log(value + 1e-8)

# Clamp to valid range
clamped = torch.clamp(value, min=1e-10, max=1.0)
```

### 4. Device Handling
```python
# Ensure all tensors on same device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tensor = tensor.to(device)

# Or get from model
device = next(model.parameters()).device
tensor = tensor.to(device)
```

## Loss Function Pattern

```python
def compute_loss(logits, labels, temperature=1.0, margin=0.5):
    # 1. Normalize/compute rewards
    rewards = logits / (sequence_length + 1e-8)

    # 2. Compute differences
    diff = temperature * rewards[:n//2] - temperature * rewards[n//2:] - margin

    # 3. Apply objective
    loss_per_pair = -torch.log(torch.sigmoid(diff) + 1e-10)

    # 4. Reduce
    loss = loss_per_pair.mean()

    return loss
```

## Debugging Tips

1. **Check tensor shapes** at each step
2. **Use .detach()** for inspecting values without affecting gradients
3. **Verify numerical stability** with small inputs
4. **Test gradients** with `loss.backward()`
5. **Print intermediate values** for debugging

## Performance Tips

- Use in-place operations where safe: `tensor.log_()`
- Avoid unnecessary cloning/copying
- Batch operations are faster than loops
- Use PyTorch functions over custom loops
