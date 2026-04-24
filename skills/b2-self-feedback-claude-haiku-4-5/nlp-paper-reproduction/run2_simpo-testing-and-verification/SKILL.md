---
name: run2_simpo-testing-and-verification
description: Testing SimPO loss function with fixed tensors and output verification
---

# SimPO Testing and Verification Framework

## Fixed-Input Unit Testing

The SimPO implementation uses **pre-computed fixed tensors** for deterministic testing:

### Test Structure
```python
# Load pre-computed tensors
policy_chosen_logps = torch.load("unit_test/tensors/policy_chosen_logps.pt")
policy_rejected_logps = torch.load("unit_test/tensors/policy_rejected_logps.pt")

# Create trainer instance
config = SimPOConfig(output_dir="./simpo_output")
trainer = SimPOTrainer(model="sshleifer/tiny-gpt2", args=config)

# Run loss function
losses, chosen_rewards, rejected_rewards = trainer.simpo_loss(
    policy_chosen_logps,
    policy_rejected_logps,
)

# Verify and save
assert losses.shape == (100,)  # Batch size 100
np.savez("/root/loss.npz", losses=losses.detach().cpu().numpy())
```

### Why Fixed Tensors?
1. **Reproducibility**: Same input → Same output every time
2. **Verification**: Can compare against expected values
3. **Debugging**: Fixed values make it easy to trace issues
4. **CI/CD**: Automated testing of implementation correctness

## Expected Output Characteristics

### Tensor Shapes
- `losses`: (batch_size,) - one loss per sample
- `chosen_rewards`: (batch_size,) - one reward per chosen response
- `rejected_rewards`: (batch_size,) - one reward per rejected response

### Value Ranges
Based on unit test with 100 samples:
- **Losses**: [0.003, 1.610] with mean ≈ 0.5
- **Chosen rewards**: Varies with input logps and beta
- **Rejected rewards**: Varies with input logps and beta

### Numerical Properties
- All losses should be positive (range: [0, ∞))
- No NaN or Inf values
- Gradients should flow properly for backprop

## Verification Steps

### 1. Output File Validation
```python
import numpy as np

data = np.load('/root/loss.npz')
assert 'losses' in data, "Missing 'losses' key"
losses = data['losses']

assert losses.dtype in [np.float32, np.float64], f"Wrong dtype: {losses.dtype}"
assert losses.shape == (100,), f"Wrong shape: {losses.shape}"
assert np.all(losses > 0), "Negative losses found!"
assert not np.isnan(losses).any(), "NaN values found!"
assert not np.isinf(losses).any(), "Inf values found!"

print("✓ All validations passed!")
```

### 2. Loss Computation Verification
```python
# Manually compute loss for first sample
beta = 2.0
gamma = beta * 0.25  # default gamma_beta_ratio
chosen_logp = policy_chosen_logps[0].item()
rejected_logp = policy_rejected_logps[0].item()

chosen_reward = beta * chosen_logp
rejected_reward = beta * rejected_logp
reward_diff = chosen_reward - rejected_reward - gamma

expected_loss = -np.log(1 / (1 + np.exp(-reward_diff)))
computed_loss = losses[0].item()

assert np.isclose(expected_loss, computed_loss, rtol=1e-5), \
    f"Loss mismatch: {expected_loss} vs {computed_loss}"
```

### 3. Environment Reproducibility
Save Python environment information:
```bash
python -VV > python_info.txt
python -m pip freeze >> python_info.txt
```

This allows exact reproduction of the test:
- Python version: 3.12.3
- PyTorch: 2.2.2+cpu
- Transformers: 4.44.2
- NumPy: 1.26.4

## Running the Test

### Using unittest
```bash
cd /root/SimPO
python3 -m unittest unit_test.unit_test_1.TestModelOutputs.test_random_pairs -v
```

### Manual Test
```python
python3 << 'EOF'
from unit_test.unit_test_1 import TestModelOutputs
import unittest

# Create test suite
suite = unittest.TestSuite()
suite.addTest(TestModelOutputs('test_random_pairs'))

# Run with verbose output
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Check result
if result.wasSuccessful():
    print("\n✓ Test passed successfully!")
else:
    print("\n✗ Test failed!")
    for error in result.errors:
        print(f"Error: {error[1]}")
EOF
```

## Troubleshooting

### Issue: ImportError for torch/transformers
**Solution**: Install packages
```bash
pip install torch transformers trl numpy
```

### Issue: Model loading fails
**Solution**: Use tiny-gpt2 for testing (small, fast to load)
```python
model = "sshleifer/tiny-gpt2"  # ~10MB, trains instantly
```

### Issue: Loss values seem wrong
**Verification**: Check formula
```
loss = -log(sigmoid(chosen_reward - rejected_reward - gamma))
```
Should be positive, typically 0.01 to 2.0 range.

### Issue: Numerical instability
**Cause**: Using `log(sigmoid())` directly
**Solution**: Already fixed in implementation via `F.logsigmoid()`
