---
name: simpo-loss-implementation
description: Guidelines for implementing the SimPO (Simple Preference Optimization) loss function for NLP model training. Use this skill when modifying trainers or implementing preference-based loss functions in transformer projects.
---
# SimPO Loss Implementation

The SimPO loss is designed to optimize language models based on preference data without a separate reward model.

## Implementation Principles
1. **Mathematical correctness**: Implement the log-likelihood difference with the margin, normalized by the length of the sequences.
2. **Numerical stability**: Use log-sum-exp or similar techniques if necessary to avoid overflow.
3. **Loss formula**:
   - For a sequence pair (chosen, rejected) $y_w, y_l$:
   - Reward $r(x, y) = \beta \log P_\theta(y|x)$ (simplified, check paper for exact implementation details).
   - SimPO Loss = $-\log \sigma (\beta(\log P_\theta(y_w|x) - \log P_\theta(y_l|x)) - \gamma)$
   - $\gamma$ is the target margin.

## Checklist
- [ ] Ensure `logits` are masked properly for padding tokens.
- [ ] Calculate `log_probs` using the model's output and target labels.
- [ ] Normalize the `log_probs` by length if the paper requires it.
- [ ] Ensure the margin $\gamma$ is configurable.
- [ ] Verify the loss is averaged over the batch.
