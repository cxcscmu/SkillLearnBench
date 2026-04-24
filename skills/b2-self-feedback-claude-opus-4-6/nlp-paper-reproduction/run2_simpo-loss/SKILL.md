---
name: run2_simpo-loss
description: Complete SimPO loss implementation with exact formula derivation from the paper.
---

# SimPO Loss Function (Equation 6 from the paper)

## Paper Reference
SimPO: Simple Preference Optimization with a Reference-Free Reward (NeurIPS 2024)

## Core Equations

### Reward (Eq. 4)
r_SimPO(x, y) = (β / |y|) * Σ log π_θ(y_i | x, y_{<i})

Since input `policy_*_logps` are **already length-normalized** (average log-probs), the reward is:
- chosen_rewards = β * policy_chosen_logps
- rejected_rewards = β * policy_rejected_logps

### Target Reward Margin (Eq. 5)
p(y_w ≻ y_l | x) = σ(r(x, y_w) - r(x, y_l) - γ)

Where γ > 0 is the target margin. In the config:
- `gamma_beta_ratio` = γ / β (default 0.25)
- So γ = gamma_beta_ratio * β

### SimPO Objective (Eq. 6)
L_SimPO = -E log σ( β * chosen_logps - β * rejected_logps - γ )

Equivalently:
```
logits = β * (policy_chosen_logps - policy_rejected_logps) - γ
```

## Loss Types

### Sigmoid (default)
With label smoothing parameter ε:
```python
losses = -F.logsigmoid(logits) * (1 - ε) - F.logsigmoid(-logits) * ε
```
When ε = 0, this simplifies to: `losses = -F.logsigmoid(logits)`

### Hinge
```python
losses = torch.relu(1 - logits)
```

## Complete Implementation
```python
def simpo_loss(self, policy_chosen_logps, policy_rejected_logps):
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    gamma = self.gamma_beta_ratio * self.beta
    logits = pi_logratios * self.beta - gamma

    chosen_rewards = self.beta * policy_chosen_logps.detach()
    rejected_rewards = self.beta * policy_rejected_logps.detach()

    if self.loss_type == "sigmoid":
        losses = (
            -F.logsigmoid(logits) * (1 - self.label_smoothing)
            - F.logsigmoid(-logits) * self.label_smoothing
        )
    elif self.loss_type == "hinge":
        losses = torch.relu(1 - logits)
    else:
        raise ValueError(f"Unknown loss type: {self.loss_type}")

    return losses, chosen_rewards, rejected_rewards
```

## Config Defaults (SimPOConfig)
- beta: 2.0
- gamma_beta_ratio: 0.25 (so γ = 0.5 by default)
- sft_weight: 0.0
- label_smoothing: 0
- loss_type: "sigmoid"
