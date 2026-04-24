---
name: pytorch-preference-optimization
description: PyTorch patterns for implementing preference optimization losses (DPO, SimPO, etc.) for LLM training.
---

# PyTorch Preference Optimization Patterns

## Key Functions

- `torch.nn.functional.logsigmoid(x)`: Numerically stable log-sigmoid, used in Bradley-Terry losses.
- `torch.relu(x)`: Used for hinge-loss variants.
- `torch.FloatTensor`: Common type for log probability tensors.

## Implementation Pattern

```python
import torch
import torch.nn.functional as F

def preference_loss(chosen_logps, rejected_logps, beta, gamma, label_smoothing=0.0, loss_type="sigmoid"):
    logits = beta * (chosen_logps - rejected_logps) - gamma

    if loss_type == "sigmoid":
        losses = -F.logsigmoid(logits) * (1 - label_smoothing) - F.logsigmoid(-logits) * label_smoothing
    elif loss_type == "hinge":
        losses = torch.relu(1 - logits)

    chosen_rewards = beta * chosen_logps.detach()
    rejected_rewards = beta * rejected_logps.detach()

    return losses, chosen_rewards, rejected_rewards
```

## Environment Setup
- trl==0.9.6 is needed for compatibility with older SimPO codebases (CPOTrainer import).
- PyTorch CPU is sufficient for loss computation testing.
