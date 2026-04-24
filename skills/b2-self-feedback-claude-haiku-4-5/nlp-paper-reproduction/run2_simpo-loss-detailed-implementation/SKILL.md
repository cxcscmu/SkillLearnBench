---
name: run2_simpo-loss-detailed-implementation
description: Complete SimPO loss implementation with length-normalized rewards and target margin
---

# SimPO Loss Function - Detailed Implementation

## Mathematical Formula (SimPO Paper Equation 6)

$$L_{SimPO}(\pi_\theta) = -\mathbb{E}_{(x,y_w,y_l) \sim D} \log \sigma\left(\frac{\beta}{|y_w|}\log\pi_\theta(y_w|x) - \frac{\beta}{|y_l|}\log\pi_\theta(y_l|x) - \gamma\right)$$

## Key Design Elements

### 1. Length-Normalized Rewards
- **Input**: `policy_chosen_logps` and `policy_rejected_logps` are **already average log probabilities**
  - These are pre-computed as: $p_\theta(y|x) = \frac{1}{|y|}\log\pi_\theta(y|x)$
  - Already length-normalized when passed to the loss function
- **Processing**: Scale by $\beta$ to get the final rewards
  - $r_w = \beta \cdot p_\theta(y_w|x)$
  - $r_l = \beta \cdot p_\theta(y_l|x)$

### 2. Target Reward Margin
- Computed as: $\gamma = \beta \times \text{gamma\_beta\_ratio}$
- From SimPOConfig: `gamma_beta_ratio` (default 0.25)
- This means $\gamma = 0.25 \times \beta$ by default
- Ensures winning responses have higher rewards by at least $\gamma$

### 3. Bradley-Terry Objective with Margin
- Probability of preference: $\sigma(r_w - r_l - \gamma)$
- Loss uses negative log: $-\log\sigma(reward\_diff)$
- Equivalent to: $\log(1 + e^{-reward\_diff})$

## Implementation Details

```python
def simpo_loss(
    self,
    policy_chosen_logps: torch.FloatTensor,  # Shape: (batch_size,)
    policy_rejected_logps: torch.FloatTensor, # Shape: (batch_size,)
) -> Tuple[torch.FloatTensor, torch.FloatTensor, torch.FloatTensor]:
    """
    Compute SimPO loss for preference pairs.

    Key points:
    - Input logps are average log probabilities (length-normalized)
    - Beta and gamma come from SimPOConfig via self.args
    - F.logsigmoid is numerically stable alternative to log(sigmoid())
    - Returns per-sample losses and computed rewards
    """

    # Extract hyperparameters from config
    beta = self.args.beta                              # Default: 2.0
    gamma = beta * self.args.gamma_beta_ratio          # Default: 2.0 * 0.25 = 0.5

    # Compute scaled length-normalized rewards
    chosen_rewards = beta * policy_chosen_logps        # Shape: (batch_size,)
    rejected_rewards = beta * policy_rejected_logps    # Shape: (batch_size,)

    # Compute Bradley-Terry objective with margin
    reward_diff = chosen_rewards - rejected_rewards - gamma

    # Loss = -log(sigmoid(reward_diff)) = log(1 + exp(-reward_diff))
    # Using F.logsigmoid for numerical stability
    losses = -F.logsigmoid(reward_diff)

    return losses, chosen_rewards, rejected_rewards
```

## Numerical Stability

**Why use `F.logsigmoid(x)` instead of `torch.log(torch.sigmoid(x))`?**
- `F.logsigmoid(x) = log(1/(1 + exp(-x))) = -log(1 + exp(-x))`
- Avoids computing sigmoid (which can underflow to 0 for large x)
- Avoids log(0) when sigmoid underflows
- Automatically handles both positive and negative x values

## Unit Test Validation

The implementation produces:
- **Losses**: Positive values (range typically 0.001 to 1.6)
- **Chosen/Rejected Rewards**: Scaled versions of input logps
- **Consistency**: Fixed inputs produce identical outputs (deterministic)

### Example Output from Test
```
Losses shape: (100,)
Losses dtype: float32
Sample losses: [0.132, 0.161, 0.106, 0.114, 0.377]
Min/Max: 0.003 / 1.610
```

## Integration Notes

1. The method is called from:
   - Training loop via `compute_loss()`
   - Evaluation loop for metric computation
   - Unit tests for validation

2. Requires:
   - `self.args` to be set (via `super().__init__()` call)
   - Input tensors already on correct device
   - Input tensors already computed as average log probabilities

3. Loss can be aggregated for backpropagation:
   ```python
   batch_loss = losses.mean()  # or sum()
   batch_loss.backward()
   ```
