---
name: pytorch-testing-logging
description: Run PyTorch unit tests, save results to NumPy files, and log environment information for reproducibility. Use this skill when executing test suites for neural network functions, validating loss computations, saving tensor outputs for verification, and creating reproducibility logs with Python/package versions.
---

# PyTorch Testing and Results Logging

## Overview

This skill covers running unit tests for PyTorch functions, verifying outputs, saving results in standardized formats (NumPy .npz), and logging environment information for complete reproducibility of machine learning experiments.

## Unit Test Execution

### Running PyTorch Unit Tests

#### Basic Test Execution
```bash
# Run all tests in a file
python -m pytest unit_test/unit_test_1.py -v

# Run with unittest framework
python -m unittest unit_test.unit_test_1 -v

# Run directly
python unit_test/unit_test_1.py
```

#### Test Output Flags
```bash
# Verbose output
-v or --verbose

# Show print statements
-s or --capture=no

# Stop on first failure
-x or --exitfirst

# Show local variables in tracebacks
-l or --showlocals
```

#### Running Specific Tests
```bash
# Run single test method
python -m pytest unit_test/unit_test_1.py::TestModelOutputs::test_random_pairs -v

# Run by pattern matching
python -m pytest unit_test/ -k "test_loss" -v
```

### Handling Test Issues

#### ImportError - Module Not Found
```bash
# Ensure test directory is in Python path
export PYTHONPATH=/path/to/project:$PYTHONPATH
python unit_test/unit_test_1.py

# Or run from project root
cd /root/SimPO
python -m pytest unit_test/unit_test_1.py
```

#### Device/CUDA Issues in Tests
```python
# Test automatically selects device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Verify device placement
tensor = tensor.to(device)
```

#### File Path Resolution
Tests often use relative paths. Run from:
- Project root directory
- Or ensure test adjusts paths with `Path(__file__).resolve().parent`

## Saving Results to NumPy Format

### NPZ File Format (Recommended for Multi-Array Storage)

#### Writing Results
```python
import numpy as np
import torch

# Single array save
losses = torch.tensor([0.5, 0.3, 0.7])
np.savez(
    "/root/loss.npz",
    losses=losses.detach().cpu().numpy()
)

# Multiple arrays save
np.savez(
    "/root/results.npz",
    losses=losses.detach().cpu().numpy(),
    rewards_chosen=chosen_rewards.detach().cpu().numpy(),
    rewards_rejected=rejected_rewards.detach().cpu().numpy()
)
```

#### Reading Saved Results
```python
import numpy as np

# Load single file
data = np.load("/root/loss.npz")
losses = data['losses']

# Load all arrays
data = np.load("/root/results.npz")
losses = data['losses']
chosen_rewards = data['rewards_chosen']

# List all keys
print(data.keys())  # dict_keys(['losses', 'rewards_chosen', ...])
```

### Converting PyTorch Tensors to NumPy

#### Device-Agnostic Conversion
```python
# Correct pattern
numpy_array = tensor.detach().cpu().numpy()

# Breakdown:
# .detach() - remove gradient tracking
# .cpu() - move to CPU memory
# .numpy() - convert to NumPy array

# For GPU tensors
gpu_tensor = torch.randn(10, device="cuda")
numpy_array = gpu_tensor.detach().cpu().numpy()

# Direct method (if already on CPU)
tensor_cpu = tensor.cpu()
numpy_array = tensor_cpu.numpy()
```

#### Preserving Precision
```python
# Default: float32
numpy_array = tensor.numpy()

# Explicit dtype control
numpy_array = tensor.detach().cpu().numpy().astype(np.float32)
numpy_array = tensor.detach().cpu().numpy().astype(np.float64)
```

## Environment Logging for Reproducibility

### Comprehensive Environment Information

#### Python Version and Build
```bash
# Detailed Python version
python -VV

# Output format:
# Python 3.10.12 (main, Sep 11 2024, 14:17:37) [GCC 11.4.0]
```

#### Package Freeze
```bash
# All installed packages with versions
python -m pip freeze

# Save to file
python -m pip freeze > environment_info.txt

# Or with timestamp
{
    echo "=== Environment Log - $(date) ==="
    echo
    echo "=== Python Version ==="
    python -VV
    echo
    echo "=== Installed Packages ==="
    python -m pip freeze
    echo
    echo "=== Key Package Versions ==="
    python -c "import torch; print(f'torch: {torch.__version__}')"
    python -c "import transformers; print(f'transformers: {transformers.__version__}')"
} > /root/python_info.txt
```

#### Creating Reproducibility Log

```bash
# Single command to create comprehensive log
{
    echo "=== Environment Information ==="
    echo "Timestamp: $(date)"
    echo "Hostname: $(hostname)"
    echo "Platform: $(python -c 'import platform; print(platform.platform())')"
    echo
    echo "=== Python Version ==="
    python -VV
    echo
    echo "=== All Installed Packages ==="
    python -m pip freeze
    echo
    echo "=== CUDA/Device Info ==="
    python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"
} > /root/python_info.txt
```

### Logging During Test Execution

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# In test
logger.info(f"Test started with device: {device}")
logger.info(f"Input shapes: chosen={chosen_logps.shape}, rejected={rejected_logps.shape}")
logger.info(f"Loss computation completed")
```

## Complete Test-to-Save Workflow

### Pattern for Loss Function Testing

```python
import torch
import numpy as np
import unittest
from pathlib import Path

class TestLossFunction(unittest.TestCase):
    def setUp(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # Load or create test data
        self.chosen_logps = torch.load("unit_test/tensors/policy_chosen_logps.pt").to(self.device)
        self.rejected_logps = torch.load("unit_test/tensors/policy_rejected_logps.pt").to(self.device)

    def test_loss_computation(self):
        # Initialize model/trainer
        loss_fn = YourLossFunction()

        # Compute losses
        losses, chosen_rewards, rejected_rewards = loss_fn(
            self.chosen_logps,
            self.rejected_logps
        )

        # Verify outputs
        self.assertEqual(losses.shape, (len(self.chosen_logps),))
        self.assertTrue(torch.all(losses >= 0))

        # Save results
        np.savez(
            "/root/loss.npz",
            losses=losses.detach().cpu().numpy(),
            chosen_rewards=chosen_rewards.detach().cpu().numpy(),
            rejected_rewards=rejected_rewards.detach().cpu().numpy()
        )
        print("Results saved to /root/loss.npz")

if __name__ == "__main__":
    unittest.main()
```

## Verification Checklist

After running tests and saving results:

1. **Check Output File**
   ```bash
   ls -lh /root/loss.npz
   ```

2. **Verify File Contents**
   ```python
   import numpy as np
   data = np.load("/root/loss.npz")
   print(f"Keys: {list(data.keys())}")
   print(f"Losses shape: {data['losses'].shape}")
   print(f"Loss values sample: {data['losses'][:5]}")
   ```

3. **Validate Loss Properties**
   ```python
   losses = data['losses']
   print(f"Min loss: {losses.min()}, Max loss: {losses.max()}")
   print(f"Mean loss: {losses.mean()}, Std: {losses.std()}")
   print(f"No NaN values: {not np.any(np.isnan(losses))}")
   print(f"No Inf values: {not np.any(np.isinf(losses))}")
   ```

4. **Check Environment Log**
   ```bash
   head -20 /root/python_info.txt
   ```

## Common Issues and Solutions

### Issue: ImportError in Test
**Solution**: Ensure Python path includes project root
```bash
cd /root/SimPO
export PYTHONPATH=/root/SimPO:$PYTHONPATH
python -m pytest unit_test/unit_test_1.py -v
```

### Issue: Tensor on Wrong Device
**Solution**: Check device placement
```python
if self.device.type == 'cuda':
    tensor = tensor.cuda()
else:
    tensor = tensor.cpu()
```

### Issue: NPZ File Not Created
**Solution**: Verify directory exists and is writable
```bash
touch /root/test.npz  # Test write permission
ls -l /root/
```

### Issue: NumPy Conversion from GPU Tensor
**Solution**: Always detach and move to CPU
```python
# WRONG
numpy_array = tensor.numpy()  # Fails for GPU tensors

# CORRECT
numpy_array = tensor.detach().cpu().numpy()
```
