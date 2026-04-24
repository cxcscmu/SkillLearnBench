---
name: simpo-implementation
description: Guidelines for implementing the SimPO loss function as per the SimPO paper.
---

### SimPO Loss Implementation
The SimPO loss is designed to optimize language models by maximizing the gap between positive and negative response log-probabilities, normalized by the length of the response.

### Mathematical Formulation
The SimPO loss $L_{SimPO}$ is defined as:
$L_{SimPO} = -\mathbb{E}_{(x, y_w, y_l) \sim D} \left[ \log \sigma \left( \beta \left( \frac{1}{|y_w|} \log \pi_\theta(y_w|x) - \frac{1}{|y_l|} \log \pi_\theta(y_l|x) - \gamma \right) \right) \right]$

Where:
- $y_w$ is the winning response.
- $y_l$ is the losing response.
- $\beta$ is the reward margin scale.
- $\gamma$ is the reward margin threshold.
- $\pi_\theta(y|x)$ is the model's likelihood for sequence $y$ given $x$.

### Implementation Steps
1. **Calculate Log Probabilities**: Use the model to compute the log-likelihood of tokens in $y_w$ and $y_l$.
2. **Sum Log Probabilities**: Sum the log-likelihoods over the generated sequence.
3. **Normalize**: Divide the sum by the sequence length (or use a length-normalized log-prob implementation).
4. **Compute Margin**: Calculate the difference between normalized log-probs of $y_w$ and $y_l$, then subtract $\gamma$.
5. **Apply Sigmoid and Log**: Apply the sigmoid function to $\beta \times \text{margin}$, take the negative log, and compute the mean over the batch.
