---
name: implement-simpo-loss
description: Use this skill to implement the simpo_loss function in SimPOTrainer based on the SimPO paper. The loss combines a length-normalized reward with a margin gamma and uses BCE loss without a reference model.
---

## Implement SimPO Loss

The SimPO loss is defined in the paper as:

```
L_SimPO = -E[ log σ( (β/|y_w|) * log π(y_w|x) - (β/|y_l|) * log π(y_l|x) - γ ) ]
```

Where:
- `β` is a scaling factor
- `γ` (gamma) is a target reward margin
- `|y_w|` and `|y_l|` are the lengths of winning and losing responses
- `π(y|x)` is the policy model probability

### Implementation

```python
def simpo_loss(
    self,
    policy_chosen_logps: torch.FloatTensor,
    policy_rejected_logps: torch.FloatTensor,
    policy_chosen_logps_avg: torch.FloatTensor = None,
    policy_rejected_logps_avg: torch.FloatTensor = None,
) -> Tuple[torch.FloatTensor, torch.FloatTensor, torch.FloatTensor]:
    """Compute the SimPO loss for a batch of policy model log probabilities.
    
    Args:
        policy_chosen_logps: Log probabilities of the policy model for chosen responses.
            Shape: (batch_size,)
        policy_rejected_logps: Log probabilities of the policy model for rejected responses.
            Shape: (batch_size,)
        policy_chosen_logps_avg: Average log probabilities (per token) for chosen responses.
            Shape: (batch_size,)
        policy_rejected_logps_avg: Average log probabilities (per token) for rejected responses.
            Shape: (batch_size,)
    
    Returns:
        A tuple of three tensors: (losses, chosen_rewards, rejected_rewards)
    """
    # Use average log probs (length-normalized) as the reward signal
    # If avg logps not provided separately, they should be the per-token average
    chosen_logratios = policy_chosen_logps_avg if policy_chosen_logps_avg is not None else policy_chosen_logps
    rejected_logratios = policy_rejected_logps_avg if policy_rejected_logps_avg is not None else policy_rejected_logps

    # SimPO reward: beta * (avg_logp_chosen - avg_logp_rejected) - gamma
    # This is the length-normalized version without reference model
    pi_logratios = chosen_logratios - rejected_logratios
    
    # Apply beta scaling and subtract gamma margin
    logits = self.beta * pi_logratios - self.gamma
    
    # Compute loss: -log(sigmoid(logits))
    if self.loss_type == "sigmoid":
        losses = -F.logsigmoid(logits)
    elif self.loss_type == "hinge":
        losses = torch.relu(1 - logits)
    else:
        raise ValueError(f"Unknown loss type: {self.loss_type}")
    
    # Compute rewards for logging
    chosen_rewards = self.beta * chosen_logratios.detach()
    rejected_rewards = self.beta * rejected_logratios.detach()
    
    return losses, chosen_rewards, rejected_rewards
```

### Key Points
- **No reference model**: SimPO does not use a reference model, unlike DPO
- **Length normalization**: Uses average log probabilities (divided by sequence length)
- **Gamma margin**: Adds a target reward margin γ to encourage a gap between chosen and rejected
- **Beta scaling**: Controls the strength of the reward signal