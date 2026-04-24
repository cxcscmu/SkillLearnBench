---
name: simpo-loss
description: Implement the SimPO (Simple Preference Optimization) loss function for LLM alignment. Use this skill whenever implementing SimPO training objectives, reference-free reward optimization, or Bradley-Terry preference loss with target reward margin. Triggers on: SimPO, preference optimization loss, average log probability reward, gamma margin.
---

# SimPO Loss Implementation

## Paper Reference
"SimPO: Simple Preference Optimization with a Reference-Free Reward" (Meng et al., 2024)

## Core Formula

The SimPO objective (Eq. 6 from paper):

```
L_SimPO(π_θ) = -E[(x,yw,yl)~D] [log σ(β/|yw| * log π_θ(yw|x) - β/|yl| * log π_θ(yl|x) - γ)]
```

Where:
- `β` (beta): scaling factor for rewards
- `γ` (gamma): target reward margin = `gamma_beta_ratio * beta`
- `|yw|`, `|yl|`: sequence lengths of winning/losing responses (used for length normalization)
- `σ`: sigmoid function

## Key Design: Length-Normalized Reward

The implicit reward is the **average log probability** (not sum):
```
r(x, y) = β/|y| * log π_θ(y|x) = β * avg_log_prob(y)
```

This aligns with the generation metric (average log-likelihood).

## Implementation

```python
def simpo_loss(self, policy_chosen_logps, policy_rejected_logps):
    """
    Args:
        policy_chosen_logps: Average log probs for chosen. Shape: (batch_size,)
        policy_rejected_logps: Average log probs for rejected. Shape: (batch_size,)

    Note: inputs are already length-normalized (average_log_prob=True upstream)
    """
    # Compute rewards (beta * avg_log_prob)
    chosen_rewards = self.beta * policy_chosen_logps
    rejected_rewards = self.beta * policy_rejected_logps

    # gamma = gamma_beta_ratio * beta
    gamma = self.gamma_beta_ratio * self.beta

    # Reward difference with target margin
    logits = chosen_rewards - rejected_rewards - gamma

    if self.loss_type == "sigmoid":
        # With optional label smoothing
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

## Config Parameters

From `SimPOConfig`:
- `beta: float = 2.0` - reward scaling
- `gamma_beta_ratio: float = 0.25` - γ/β ratio, so γ = 0.25 * 2.0 = 0.5 by default
- `label_smoothing: float = 0` - smoothing for sigmoid loss
- `loss_type: Literal["sigmoid", "hinge"] = "sigmoid"`

## Notes

- `gamma_beta_ratio` represents γ/β, so actual gamma = `gamma_beta_ratio * beta`
- The logps passed in are already averaged (from `get_batch_logps` with `average_log_prob=True`)
- Rewards are beta-scaled average log probabilities
- No reference model needed (reference-free)
