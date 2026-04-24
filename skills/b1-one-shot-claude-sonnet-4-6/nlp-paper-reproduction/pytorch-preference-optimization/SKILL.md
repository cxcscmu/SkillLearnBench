---
name: pytorch-preference-optimization
description: Guide for implementing preference optimization methods (DPO, SimPO, IPO) in PyTorch. Use when implementing loss functions for RLHF-style training.
---

# PyTorch Preference Optimization

## Common Pattern
All preference optimization methods take:
- `policy_chosen_logps`: log probs for preferred responses
- `policy_rejected_logps`: log probs for rejected responses

## DPO Loss
```python
# Requires reference model log probs
logits = (policy_chosen_logps - ref_chosen_logps) - (policy_rejected_logps - ref_rejected_logps)
losses = -F.logsigmoid(beta * logits)
```

## SimPO Loss (Reference-Free)
```python
# No reference model needed - uses length-normalized log probs
pi_logratios = policy_chosen_logps - policy_rejected_logps  # already avg'd per token
logits = pi_logratios - gamma_beta_ratio  # gamma_beta_ratio = gamma/beta
losses = -F.logsigmoid(beta * logits)
```

## Tips
- `F.logsigmoid(x)` is numerically more stable than `torch.log(torch.sigmoid(x))`
- For label smoothing: `loss = -logsigmoid(logits)*(1-ls) - logsigmoid(-logits)*ls`
- Hinge loss: `torch.relu(1 - beta * logits)`
- Always `.detach()` reward tensors to prevent gradient flow through them
