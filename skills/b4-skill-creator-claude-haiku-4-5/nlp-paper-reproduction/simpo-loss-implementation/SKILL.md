---
name: simpo-loss-implementation
description: Implement the SimPO loss function for preference-aligned language models. Use this skill when implementing SimPO training objectives, computing length-normalized rewards, or translating the SimPO paper's mathematical formulas into PyTorch code. Essential for LLM alignment tasks that require preference-based learning with reference-free rewards.
---

# SimPO Loss Implementation

## Overview

SimPO (Simple Preference Optimization) is a reference-free preference optimization method that trains language models using pairwise preference data. The loss function combines length-normalized rewards with a Bradley-Terry preference model.

## Core Mathematical Formulas

### 1. Length-Normalized Reward
```
r_SimPO(x, y) = (β/|y|) * log π_θ(y|x)
```

Where:
- **β**: Scaling constant (typically 2.0)
- **|y|**: Response length (number of tokens)
- **log π_θ(y|x)**: Average log probability per token (not summed)

### 2. Bradley-Terry Preference with Margin
```
p(y_w ≻ y_l | x) = σ(r(x, y_w) - r(x, y_l) - γ)
```

Where:
- **γ**: Target reward margin (calculated as γ = β * gamma_beta_ratio)
- **σ(·)**: Sigmoid function
- **y_w**: Chosen/winning response
- **y_l**: Rejected/losing response

### 3. SimPO Loss Objective
```
L_SimPO = -log(σ(reward_chosen - reward_rejected - γ))
```

This is equivalent to binary cross-entropy loss where the target is always 1.

## Implementation Pattern

### Input Parameters
```python
def simpo_loss(
    self,
    policy_chosen_logps: torch.FloatTensor,  # Shape: (batch_size,)
    policy_rejected_logps: torch.FloatTensor  # Shape: (batch_size,)
) -> Tuple[torch.FloatTensor, torch.FloatTensor, torch.FloatTensor]:
```

### Output
Returns tuple of:
- `losses`: Individual losses for each pair (batch_size,)
- `chosen_rewards`: Rewards for chosen responses (batch_size,)
- `rejected_rewards`: Rewards for rejected responses (batch_size,)

## Implementation Steps

### Step 1: Extract Configuration Values
Access `self.beta` and `gamma_beta_ratio` from the trainer's config to compute:
- `gamma = self.beta * self.config.gamma_beta_ratio`

### Step 2: Calculate Length-Normalized Rewards
For chosen responses:
```python
chosen_rewards = (self.beta / chosen_length) * policy_chosen_logps
```

For rejected responses:
```python
rejected_rewards = (self.beta / rejected_length) * policy_rejected_logps
```

**Important**: The log probabilities passed are already **averaged per token** (not summed), so division by length has already been applied. Therefore, you multiply by `beta` only:
```python
chosen_rewards = self.beta * policy_chosen_logps
rejected_rewards = self.beta * policy_rejected_logps
```

### Step 3: Compute Log Differences with Margin
```python
log_odds = chosen_rewards - rejected_rewards - gamma
```

### Step 4: Apply Sigmoid and Compute Loss
Using binary cross-entropy with logits:
```python
losses = -torch.nn.functional.logsigmoid(log_odds)
```

This computes: `-log(σ(x))` which is the negative log-likelihood that the sigmoid evaluates to 1.

## Configuration Defaults

From `SimPOConfig`:
- `beta`: 2.0 (reward scaling factor)
- `gamma_beta_ratio`: 0.25 (ratio between margin and beta)
- Default gamma: 0.5

## Key Implementation Details

1. **Log Probabilities Are Pre-Normalized**: The input `policy_chosen_logps` and `policy_rejected_logps` are already averaged log probabilities per token. No additional length normalization is needed in the loss function.

2. **No Reference Model**: Unlike DPO, SimPO uses absolute log-likelihoods, not log-ratios. This eliminates the need for a reference model.

3. **Vectorized Operations**: All operations should be vectorized across the batch dimension for efficiency.

4. **Device Consistency**: Ensure all tensors remain on the same device (CPU/GPU).

## Common Pitfalls to Avoid

1. **Double Length Normalization**: Don't divide by length again if log probs are already averaged
2. **Dimension Mismatches**: Ensure rewards and log_odds maintain shape (batch_size,)
3. **Missing Margin**: The `-gamma` term is critical; without it, the model ignores preference margins
4. **Wrong Loss Function**: Use `-logsigmoid()` not `log_sigmoid()` for negative log-likelihood

## Testing Pattern

Verify implementation by:
1. Checking output shapes match input batch sizes
2. Confirming losses are positive values
3. Validating that worse log-probability pairs produce higher losses
4. Testing with unit tests using fixed input tensors
