---
name: simpo-unit-test-execution
description: How to correctly run the SimPO unit test to generate the loss.npz output file with reproducible results. Use when executing the unit test after implementing the loss function.
---

## Running the SimPO Unit Test

### Prerequisites
- Python 3.10 environment is active
- `simpo_loss` function is correctly implemented in `/root/SimPO/scripts/simpo_trainer.py`
- All dependencies (torch, transformers, trl, accelerate, etc.) are installed

### Execution Steps

```bash
# 1. Ensure correct Python
source /root/SimPO/.venv/bin/activate  # or however the venv is activated
python -VV  # Must show Python 3.10.x

# 2. Run the unit test (DO NOT modify unit_test_1.py)
cd /root/SimPO
python unit_test/unit_test_1.py

# 3. Verify output exists
python -c "import numpy as np; data = np.load('/root/loss.npz'); print('losses:', data['losses'])"

# 4. Generate the python info file
python -VV > /root/python_info.txt 2>&1
python -m pip freeze >> /root/python_info.txt
```

### What the Unit Test Does

The unit test:
1. Creates fixed input tensors for `policy_chosen_logps` and `policy_rejected_logps`
2. Creates a SimPOTrainer (or mock) with specific `beta` and `gamma` values
3. Calls `simpo_loss()` with those fixed inputs
4. Saves the resulting losses to `/root/loss.npz` with key `'losses'`

### Verifying Correctness

The SimPO loss with sigmoid loss type should compute:
```
losses = -log(sigmoid(beta * (chosen_avg_logps - rejected_avg_logps - gamma)))
```

If the test provides specific beta and gamma values, you can manually verify:
```python
import torch
import torch.nn.functional as F

# Example verification
logits = policy_chosen_logps - policy_rejected_logps - gamma
losses = -F.logsigmoid(beta * logits)
```

### Important Notes

- Do NOT modify `unit_test_1.py` — it has fixed inputs for reproducibility
- The loss output must be deterministic (no randomness involved)
- Make sure `self.accelerator.device` is handled correctly; the unit test may mock or provide this
- If the unit test creates a minimal/mock trainer, ensure your `simpo_loss` method works with it