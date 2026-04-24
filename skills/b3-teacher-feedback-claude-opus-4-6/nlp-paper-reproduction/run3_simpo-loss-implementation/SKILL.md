---
name: simpo-loss-implementation
description: How to implement the SimPO (Simple Preference Optimization) loss function based on the SimPO paper. Use this when implementing the simpo_loss method in SimPOTrainer.
---

## SimPO Loss Function

SimPO (Simple Preference Optimization) is a reference-free reward formulation for preference optimization that uses the average log probability of a sequence as the implicit reward.

### Key Formula

The SimPO loss is defined as:

```
L_SimPO = -log(sigmoid(β/|y_w| * log π_θ(y_w|x) - β/|y_l| * log π_θ(y_l|x) - γ))
```

Where:
- `β` (beta) is a scaling hyperparameter
- `γ` (gamma) is a target reward margin (the paper calls this the margin term)
- `y_w` is the winning/chosen response
- `y_l` is the losing/rejected response
- `|y_w|` and `|y_l|` are the lengths (number of tokens) of the responses
- `π_θ(y|x)` is the policy model's probability of generating y given x
- The average log probability `1/|y| * log π_θ(y|x)` serves as the implicit reward

### Implementation Details

```python
def simpo_loss(
    self,
    policy_chosen_logps: torch.FloatTensor,
    policy_rejected_logps: torch.FloatTensor,
) -> Tuple[torch.FloatTensor, torch.FloatTensor, torch.FloatTensor]:
    """Compute the SimPO loss for a batch of policy model log probabilities.
    
    Args:
        policy_chosen_logps: Average log probabilities of the policy model 
            for the chosen responses. Shape: (batch_size,)
        policy_rejected_logps: Average log probabilities of the policy model 
            for the rejected responses. Shape: (batch_size,)

    Returns:
        A tuple of three tensors: (losses, chosen_rewards, rejected_rewards).
        losses: The SimPO loss for each example in the batch.
        chosen_rewards: Reward for chosen responses (β * avg_logp).
        rejected_rewards: Reward for rejected responses (β * avg_logp).
    """
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    pi_logratios = pi_logratios.to(self.accelerator.device)
    logits = pi_logratios - self.gamma  # gamma is the margin term

    # The beta scaling is applied to the already-averaged log probs
    if self.loss_type == "sigmoid":
        losses = (
            -F.logsigmoid(self.beta * logits)
        )
    elif self.loss_type == "hinge":
        losses = torch.relu(1 - self.beta * logits)
    else:
        raise ValueError(
            f"Unknown loss type: {self.loss_type}. Should be one of ['sigmoid', 'hinge']"
        )

    chosen_rewards = self.beta * policy_chosen_logps.to(self.accelerator.device).detach()
    rejected_rewards = self.beta * policy_rejected_logps.to(self.accelerator.device).detach()

    return losses, chosen_rewards, rejected_rewards
```

### Critical Notes

1. **Average log probabilities**: The inputs `policy_chosen_logps` and `policy_rejected_logps` are ALREADY length-averaged log probabilities. The length normalization happens in the `concatenated_forward` method, not in `simpo_loss` itself. In SimPO, when computing log probabilities, they divide by the number of tokens:
   ```python
   all_logps = all_logps / size_completion  # length normalization
   ```

2. **Gamma (margin)**: The `self.gamma` parameter is subtracted from the log-ratio difference BEFORE multiplying by beta. This is the target reward margin that ensures the winning response's reward exceeds the losing response's reward by at least gamma.

3. **Beta**: The `self.beta` parameter scales the entire logit (after margin subtraction) inside the sigmoid/loss function.

4. **Loss type**: Default is "sigmoid" which uses `-log(sigmoid(β * (avg_logp_w - avg_logp_l - γ)))`.

5. **No reference model needed**: Unlike DPO, SimPO does not require a reference model. The reward is simply `β * avg_log_prob`.