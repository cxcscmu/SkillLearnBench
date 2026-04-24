name: simpo-loss-implementation
description: Guidance on implementing the SimPO (Simple Preference Optimization) loss function in a trainer class. Use this skill when you need to implement or debug the SimPO loss, ensuring correct use of beta, gamma_beta_ratio, and average log probabilities.

# SimPO Loss Implementation Guide

SimPO is a reference-free preference optimization algorithm. The key design is using the average log probability of a sequence as the implicit reward and introducing a target reward margin.

## Reward Formulation
The implicit reward for a response $y$ given prompt $x$ is:
$$r(x, y) = \frac{\beta}{|y|} \log \pi_\theta(y | x)$$
where $|y|$ is the number of tokens in the response.

## SimPO Loss Formula
The SimPO loss for a pair of winning ($y_w$) and losing ($y_l$) responses is:
$$L_{SimPO} = -\log \sigma \left( \frac{\beta}{|y_w|} \log \pi_\theta(y_w | x) - \frac{\beta}{|y_l|} \log \pi_\theta(y_l | x) - \gamma \right)$$
In implementation, we often use `gamma = gamma_beta_ratio * beta`.

## Implementation Details
When implementing `simpo_loss` in a `SimPOTrainer` class:

1. **Input Probabilities**: Ensure `policy_chosen_logps` and `policy_rejected_logps` are the average log probabilities (log-likelihood normalized by length).
2. **Margin Calculation**: Calculate `gamma` as `self.gamma_beta_ratio * self.beta`.
3. **Logits**: Compute the logits as:
   `logits = self.beta * policy_chosen_logps - self.beta * policy_rejected_logps - gamma`
4. **Loss Types**:
   - **Sigmoid**: `losses = -F.logsigmoid(logits)`
   - **Hinge**: `losses = torch.relu(1 - logits)`
5. **Rewards**: Return the rewards for logging:
   - `chosen_rewards = self.beta * policy_chosen_logps`
   - `rejected_rewards = self.beta * policy_rejected_logps`

## Example Snippet
```python
def simpo_loss(self, policy_chosen_logps, policy_rejected_logps):
    gamma = self.gamma_beta_ratio * self.beta
    logits = self.beta * policy_chosen_logps - self.beta * policy_rejected_logps - gamma

    if self.loss_type == "sigmoid":
        losses = -F.logsigmoid(logits)
    elif self.loss_type == "hinge":
        losses = torch.relu(1 - logits)
    else:
        raise ValueError(f"Unknown loss type: {self.loss_type}")

    chosen_rewards = self.beta * policy_chosen_logps
    rejected_rewards = self.beta * policy_rejected_logps

    return losses, chosen_rewards, rejected_rewards
```
