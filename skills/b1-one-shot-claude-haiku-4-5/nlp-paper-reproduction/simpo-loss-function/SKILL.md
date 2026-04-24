---
name: simpo-loss-function
description: Implement SimPO loss with length-normalized rewards and target margin.
---

# SimPO Loss Function Implementation

## Overview
SimPO (Simple Preference Optimization) implements a preference optimization objective that uses length-normalized average log probability as an implicit reward, with a target reward margin component.

## Key Formula

```
L_SimPO(πθ) = -E_(x,yw,yl)~D log σ(β/|yw| log πθ(yw|x) - β/|yl| log πθ(yl|x) - γ)
```

## Components

### 1. Length-Normalized Reward
- **Formula**: `r_SimPO(x, y) = β/|y| * log πθ(y|x)`
- **Purpose**: Average log probability per token, prevents length bias
- **Why**: Aligns training with generation metric (which uses average log likelihood for beam search)

### 2. Bradley-Terry Objective
- **Formula**: `p(yw ≻ yl | x) = σ(r(x, yw) - r(x, yl) - γ)`
- **Purpose**: Probabilistic ranking between winning and losing responses
- **Function**: σ is sigmoid function

### 3. Target Reward Margin (γ)
- **Purpose**: Ensure reward difference exceeds a target threshold
- **Effect**: Improves generalization by enforcing margin between classes
- **Typical range**: 0.5 to 1.5

## Implementation Details

### Computing Log Probabilities
```python
# log_probs shape: (batch_size, seq_len)
# Sum across sequence dimension to get total log probability
log_prob_sum = log_probs.sum(dim=1)  # (batch_size,)

# Divide by sequence length for normalization
seq_lengths = (input_ids != pad_token_id).sum(dim=1)  # (batch_size,)
avg_log_prob = log_prob_sum / seq_lengths.float()  # (batch_size,)
```

### Computing Reward Differences
```python
# Batch structure: pairs of (winning, losing) responses
batch_size = avg_log_probs.shape[0]
winning_rewards = avg_log_probs[:batch_size//2]
losing_rewards = avg_log_probs[batch_size//2:]

# Reward difference with margin
reward_diff = beta * winning_rewards - beta * losing_rewards - gamma
```

### Computing Loss
```python
# Bradley-Terry with sigmoid
import torch.nn.functional as F

sigmoid_term = torch.sigmoid(reward_diff)
loss = -torch.log(sigmoid_term).mean()
```

## Common Pitfalls

1. **Not using length normalization**: Creates bias toward longer sequences
2. **Wrong batch structure**: Ensure paired winning/losing responses
3. **Missing average in log probabilities**: Use sum/length, not just sum
4. **Gradient flow**: Ensure no detach() breaks gradients to model

## Hyperparameters
- **β**: Temperature parameter, typically 2.0-2.5
- **γ**: Target margin, typically 0.3-1.6, depends on setting
- **learning_rate**: Usually small, 1e-6 to 5e-7

## References
- SimPO Paper: Section 2.3 "The SimPO Objective"
- Length normalization: Equation (3) in paper
- Gradient analysis: Appendix F
