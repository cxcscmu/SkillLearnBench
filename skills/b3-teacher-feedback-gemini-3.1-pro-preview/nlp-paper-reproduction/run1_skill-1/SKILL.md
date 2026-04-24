[SKILL]
---
name: simpo-preference-optimization
description: Detailed explanation and implementation guide for the SimPO (Simple Preference Optimization) loss function, which uses length-normalized log probabilities and a reference-free reward margin.
---

### SimPO (Simple Preference Optimization)

SimPO is a reference-free preference optimization algorithm that simplifies alignment compared to methods like DPO (Direct Preference Optimization). It eliminates the need for a reference model by defining the reward directly using the policy model's length-normalized log probabilities.

#### Mathematical Formulation

In SimPO, the reward $r_\theta(y)$ for a generated response $y$ given a prompt $x$ is defined as the average log probability of the response tokens, scaled by a constant $\beta$: