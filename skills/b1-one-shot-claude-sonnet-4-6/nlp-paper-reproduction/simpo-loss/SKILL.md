---
name: simpo-loss
description: Implements the SimPO (Simple Preference Optimization) loss function from the paper "SimPO: Simple Preference Optimization with a Reference-Free Reward". Use this when implementing or understanding SimPO training objectives.
---

# SimPO Loss Implementation

## Overview
SimPO (Simple Preference Optimization) is a reference-free preference optimization method that:
1. Uses length-normalized log probability as the implicit reward (aligns with generation metric)
2. Introduces a target reward margin γ to separate winning/losing responses
3. Eliminates the need for a reference model (unlike DPO)

## Loss Formula (from paper Eq. 6)
```
LSimPO(πθ) = −E(x,yw,yl)∼D [ log σ( β/|yw| * log πθ(yw|x) - β/|yl| * log πθ(yl|x) - γ ) ]
```

Where:
- β: scaling factor (default: 2.0)
- γ: target reward margin (default: gamma_beta_ratio * β = 0.25 * 2.0 = 0.5)
- |yw|, |yl|: lengths of winning/losing responses
- policy_chosen_logps, policy_rejected_logps: AVERAGE log probabilities per token

## Key Notes
- `policy_chosen_logps` = average log prob per token = (1/|yw|) * log πθ(yw|x)
- So `β * policy_chosen_logps` = `β/|yw| * log πθ(yw|x)` (already normalized)
- gamma_beta_ratio = γ/β, so γ = gamma_beta_ratio * β

## Implementation

```python
def simpo_loss(
    self,
    policy_chosen_logps: torch.FloatTensor,
    policy_rejected_logps: torch.FloatTensor,
) -> Tuple[torch.FloatTensor, torch.FloatTensor, torch.FloatTensor]:
    # Length-normalized log prob difference
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    # Subtract gamma/beta ratio (equivalent to subtracting gamma from beta*logratios)
    gamma_logratios = self.gamma_beta_ratio
    logits = pi_logratios - gamma_logratios

    if self.loss_type == "sigmoid":
        losses = (
            -F.logsigmoid(self.beta * logits) * (1 - self.label_smoothing)
            - F.logsigmoid(-self.beta * logits) * self.label_smoothing
        )
    elif self.loss_type == "hinge":
        losses = torch.relu(1 - self.beta * logits)
    else:
        raise ValueError(f"Unknown loss type: {self.loss_type}")

    # Rewards (scaled average log probs)
    chosen_rewards = self.beta * policy_chosen_logps.detach()
    rejected_rewards = self.beta * policy_rejected_logps.detach()

    return losses, chosen_rewards, rejected_rewards
```

## Config Parameters (SimPOConfig)
- `beta`: float = 2.0
- `gamma_beta_ratio`: float = 0.25 (γ/β ratio)
- `label_smoothing`: float = 0
- `loss_type`: "sigmoid" | "hinge" = "sigmoid"
