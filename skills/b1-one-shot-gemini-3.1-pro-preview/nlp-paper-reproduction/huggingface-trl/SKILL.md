---
name: huggingface-trl
description: Using Hugging Face TRL library for building custom trainers for Preference Optimization methods like DPO, SimPO, etc.
---

# Hugging Face TRL (Transformer Reinforcement Learning)

TRL is a library by Hugging Face that provides tools to train language models using Reinforcement Learning and Preference Optimization (like PPO, DPO, etc.).

## Custom Trainers
To implement custom loss functions like SimPO, you can subclass the `DPOTrainer` and override its specific methods (like `dpo_loss` or in this case, `simpo_loss`).

```python
from trl import DPOTrainer
import torch
import torch.nn.functional as F

class CustomTrainer(DPOTrainer):
    def custom_loss(self, policy_chosen_logps, policy_rejected_logps):
        pi_logratios = policy_chosen_logps - policy_rejected_logps
        logits = pi_logratios - self.margin
        losses = -F.logsigmoid(self.beta * logits)
        return losses
```

## Setup & Dependencies
Commonly requires `transformers`, `torch`, `trl`, and `accelerate`.
Make sure you have the matching versions as defined in the project's requirement file (e.g. `environment.yml` or `requirements.txt`).
