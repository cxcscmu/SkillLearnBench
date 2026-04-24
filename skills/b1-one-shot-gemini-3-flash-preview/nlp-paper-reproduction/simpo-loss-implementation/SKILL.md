---
name: simpo-loss-implementation
description: Implements the Simple Preference Optimization (SimPO) loss function in PyTorch, focusing on length-normalized log probabilities and target reward margins.
---

# SimPO Loss Implementation

SimPO is a reference-free preference optimization algorithm that uses length-normalized log probabilities as rewards and incorporates a target reward margin.

## Mathematical Formulation

The SimPO loss is defined as:
$$L_{SimPO}(\pi_\theta) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta r_\theta(x, y_w) - \beta r_\theta(x, y_l) - \gamma \right) \right]$$

Where:
- $r_\theta(x, y) = \frac{1}{|y|} \log \pi_\theta(y|x)$ is the length-normalized log probability.
- $\beta$ is a scaling factor.
- $\gamma$ is the target reward margin.

## PyTorch Implementation

```python
import torch
import torch.nn.functional as F

def simpo_loss(
    policy_chosen_logps: torch.FloatTensor,
    policy_rejected_logps: torch.FloatTensor,
    beta: float,
    gamma: float,
    label_smoothing: float = 0.0,
    loss_type: str = "sigmoid"
):
    """
    Args:
        policy_chosen_logps: Average log probabilities of the chosen responses. (batch_size,)
        policy_rejected_logps: Average log probabilities of the rejected responses. (batch_size,)
        beta: Scaling factor for rewards.
        gamma: Target reward margin.
        label_smoothing: Label smoothing factor.
        loss_type: Type of loss ("sigmoid" or "hinge").
    """
    # rewards are beta * average logps
    chosen_rewards = beta * policy_chosen_logps
    rejected_rewards = beta * policy_rejected_logps

    logits = chosen_rewards - rejected_rewards - gamma

    if loss_type == "sigmoid":
        losses = (
            -F.logsigmoid(logits) * (1 - label_smoothing)
            - F.logsigmoid(-logits) * label_smoothing
        )
    elif loss_type == "hinge":
        losses = torch.relu(1 - logits)
    else:
        raise ValueError(f"Unknown loss type: {loss_type}")

    return losses, chosen_rewards, rejected_rewards
```

## Usage in Trainer

In a trainer class, ensure that `policy_chosen_logps` and `policy_rejected_logps` are already length-normalized (divided by the number of non-padded tokens).
