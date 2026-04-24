---
name: run2_simpo-implementation
description: Detailed SimPO implementation logic covering reward formulation and margin-based loss computation.
---

### SimPO Loss Definition
SimPO reward formulation:
1. `chosen_rewards = beta * log_prob_chosen`
2. `rejected_rewards = beta * log_prob_rejected`

Loss for sigmoid-based SimPO (Equation 6):
`loss = -log_sigmoid((chosen_rewards - rejected_rewards - gamma) / beta)`

*   Ensure `beta` is set to control the reward scale.
*   The `gamma_beta_ratio` corresponds to `gamma/beta` in the paper implementation.
---
