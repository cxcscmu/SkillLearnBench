---
name: run2_pytorch-simpo-loss
description: A refined skill to implement SimPO (Simple Preference Optimization) loss in PyTorch, precisely matching the official paper implementation without a reference model.
---

# PyTorch SimPO Loss Implementation

This skill provides an implementation of the SimPO loss function as defined in the paper "SimPO: Simple Preference Optimization with a Reference-Free Reward" and matched to its official codebase.

## Mathematics
SimPO formulates preference learning by using the average log probability of the generated sequence, multiplied by a scaling factor `beta`, as the implicit reward. To encourage a margin between the chosen and rejected sequences, it uses a target reward margin `gamma`.

`reward(y|x) = beta * average_log_prob(y|x)`
`margin = reward(y_chosen|x) - reward(y_rejected|x)`

In the official codebase, the margin is computed as:
`logits = pi_logratios - gamma_beta_ratio`
`loss = -log_sigmoid(beta * logits)`

Label smoothing can also be applied.

## Code Example
```python
import torch
import torch.nn.functional as F
from typing import Tuple

def simpo_loss(
    policy_chosen_logps: torch.FloatTensor,
    policy_rejected_logps: torch.FloatTensor,
    beta: float,
    gamma_beta_ratio: float,
    label_smoothing: float = 0.0,
    loss_type: str = "sigmoid",
    device: torch.device = None,
) -> Tuple[torch.FloatTensor, torch.FloatTensor, torch.FloatTensor]:
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    if device is not None:
        pi_logratios = pi_logratios.to(device)
        
    logits = pi_logratios - gamma_beta_ratio

    if loss_type == "sigmoid":
        losses = (
            -F.logsigmoid(beta * logits) * (1 - label_smoothing)
            - F.logsigmoid(-beta * logits) * label_smoothing
        )
    elif loss_type == "hinge":
        losses = torch.relu(1 - beta * logits)
    else:
        raise ValueError(
            f"Unknown loss type: {loss_type}. Should be one of ['sigmoid', 'hinge']"
        )

    chosen_rewards = beta * policy_chosen_logps.detach()
    rejected_rewards = beta * policy_rejected_logps.detach()
    
    if device is not None:
        chosen_rewards = chosen_rewards.to(device)
        rejected_rewards = rejected_rewards.to(device)

    return losses, chosen_rewards, rejected_rewards
```
