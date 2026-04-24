---
name: run2_simpo-loss
description: Complete implementation of the SimPO (NeurIPS 2024) loss function with all variants and edge cases - use when reproducing SimPO or implementing reference-free preference optimization.
---

# SimPO Loss Function - Complete Implementation Guide

## Paper Reference
SimPO: Simple Preference Optimization with a Reference-Free Reward (NeurIPS 2024)
arXiv: 2405.14734v3 — Yu Meng, Mengzhou Xia, Danqi Chen

## Mathematical Formulation

### Length-Normalized Reward (Eq. 3-4)
```
p_θ(y|x) = 1/|y| * log π_θ(y|x) = 1/|y| * Σ log π_θ(yi|x, y<i)

r_SimPO(x, y) = β * p_θ(y|x) = β/|y| * log π_θ(y|x)
```
- `β` scales the reward difference
- Length normalization prevents bias toward longer sequences

### Bradley-Terry Objective with Target Margin (Eq. 5-6)
```
p(yw ≻ yl | x) = σ(r(x, yw) - r(x, yl) - γ)

L_SimPO(π_θ) = -E_{(x,yw,yl)} [log σ(β/|yw| * log π_θ(yw|x) - β/|yl| * log π_θ(yl|x) - γ)]
```
- `γ > 0` is the target reward margin
- `γ = β * gamma_beta_ratio` (recommended ratio: 0.0–1.0)

## Full Implementation

```python
import torch
import torch.nn.functional as F

def simpo_loss(self, policy_chosen_logps, policy_rejected_logps):
    """
    Compute SimPO loss.

    Inputs are ALREADY length-normalized (average log probability per token),
    i.e., policy_chosen_logps = 1/|yw| * log π_θ(yw|x)

    This is because get_batch_logps() is called with average_log_prob=True.
    """
    # r(x, y) = β * avg_log_prob(y)
    chosen_rewards = self.beta * policy_chosen_logps.detach()
    rejected_rewards = self.beta * policy_rejected_logps.detach()

    # logit = β*(chosen - rejected) - γ
    # Factor out β: β*(chosen - rejected - γ/β) = β*(chosen - rejected - gamma_beta_ratio)
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    gamma_logratios = self.gamma_beta_ratio  # = γ/β
    logits = pi_logratios - gamma_logratios

    if self.loss_type == "sigmoid":
        # L = -log σ(β*logits) with optional label smoothing
        losses = (
            -F.logsigmoid(self.beta * logits) * (1 - self.label_smoothing)
            - F.logsigmoid(-self.beta * logits) * self.label_smoothing
        )
    elif self.loss_type == "hinge":
        losses = torch.relu(1 - self.beta * logits)
    else:
        raise ValueError(f"Unknown loss type: {self.loss_type}")

    return losses, chosen_rewards, rejected_rewards
```

## Config Defaults
| Parameter | Default | Description |
|-----------|---------|-------------|
| beta | 2.0 | Reward scaling constant |
| gamma_beta_ratio | 0.25 | γ/β ratio → γ = 0.5 |
| loss_type | "sigmoid" | "sigmoid" or "hinge" |
| label_smoothing | 0.0 | Smoothing for sigmoid loss |

## Key Insight: Input Normalization
The trainer calls `get_batch_logps(..., average_log_prob=True)`, so inputs are:
- `policy_chosen_logps[i]` = Σ log π(token) / num_tokens for chosen sequence i
- NOT the raw log probability of the full sequence

Therefore `β * policy_chosen_logps` directly gives `r_SimPO(x, yw)` from Eq. 4.

## Numerical Check (default config)
With beta=2.0, gamma_beta_ratio=0.25, sigmoid loss, no smoothing:
- effective_logit = 2.0 * (chosen_logp - rejected_logp - 0.25)
- loss = -log(σ(effective_logit))
- When chosen=rejected: loss = -log(σ(-0.5)) ≈ 0.974
- When chosen >> rejected: loss → 0
