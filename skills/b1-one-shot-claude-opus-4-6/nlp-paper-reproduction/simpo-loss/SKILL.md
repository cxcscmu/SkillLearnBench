---
name: simpo-loss
description: SimPO (Simple Preference Optimization) loss computation for LLM alignment without a reference model.
---

# SimPO Loss

## Overview
SimPO is a reference-free preference optimization algorithm. Its key innovation is using the **average log probability** of a sequence as the implicit reward, plus a **target reward margin** γ.

## Loss Formula (Eq. 6 from the paper)

```
L_SimPO = -E log σ(β/|yw| · log πθ(yw|x) - β/|yl| · log πθ(yl|x) - γ)
```

Since the log probabilities passed to `simpo_loss` are **already length-normalized** (average log prob), the loss simplifies to:

```
logits = β * policy_chosen_logps - β * policy_rejected_logps - γ
```

where `γ = gamma_beta_ratio * beta`.

## Loss Types

- **sigmoid** (default): `losses = -log σ(logits) * (1 - label_smoothing) - log σ(-logits) * label_smoothing`
- **hinge**: `losses = relu(1 - logits)`

## Rewards

- `chosen_rewards = β * policy_chosen_logps`
- `rejected_rewards = β * policy_rejected_logps`

## Default Hyperparameters
- β = 2.0
- gamma_beta_ratio = 0.25 (so γ = 0.5)
- label_smoothing = 0.0
- loss_type = "sigmoid"
