---
name: simpo-loss
description: Implement the SimPO (Simple Preference Optimization) loss function from the NeurIPS 2024 paper. Use this skill whenever implementing SimPO, preference optimization losses, or DPO variants that use length-normalized rewards and reward margins.
---

# SimPO Loss Implementation

## Core Formula (Eq. 6 from the paper)

The SimPO objective:

```
L_SimPO(πθ) = -E log σ( (β/|yw|) log πθ(yw|x) - (β/|yl|) log πθ(yl|x) - γ )
```

Where:
- `β` (beta): scaling factor for reward difference (default: 2.0)
- `γ` (gamma): target reward margin, computed as `gamma_beta_ratio * beta` (default ratio: 0.25)
- `|yw|`, `|yl|`: lengths of winning/losing responses
- `σ`: sigmoid function

## Key Design Decisions

1. **Length-normalized reward**: `r(x,y) = (β/|y|) * log πθ(y|x)` — the average log probability scaled by β
2. **Target reward margin γ**: ensures winning response reward exceeds losing by at least γ
3. **No reference model needed** — unlike DPO

## Implementation Pattern

Given `policy_chosen_logps` and `policy_rejected_logps` (already length-normalized average log probs):

```python
pi_logratios = policy_chosen_logps - policy_rejected_logps
gamma = self.gamma_beta_ratio * self.beta
logits = pi_logratios * self.beta - gamma

# Sigmoid loss (with optional label smoothing)
losses = (
    -F.logsigmoid(logits) * (1 - self.label_smoothing)
    - F.logsigmoid(-logits) * self.label_smoothing
)

# Hinge loss variant
# losses = torch.relu(1 - logits)

chosen_rewards = self.beta * policy_chosen_logps.detach()
rejected_rewards = self.beta * policy_rejected_logps.detach()
```

## Config Parameters (SimPOConfig)

| Parameter | Default | Description |
|-----------|---------|-------------|
| beta | 2.0 | Reward scaling factor |
| gamma_beta_ratio | 0.25 | γ/β ratio |
| label_smoothing | 0.0 | Label smoothing factor |
| loss_type | "sigmoid" | "sigmoid" or "hinge" |
| sft_weight | 0.0 | Optional SFT loss weight |

## Returns

Tuple of `(losses, chosen_rewards, rejected_rewards)` — all tensors of shape `(batch_size,)`.
