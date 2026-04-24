---
name: simpo-loss
description: Guide on understanding and implementing the SimPO (Simple Preference Optimization) loss function for language models.
---

# SimPO Loss

SimPO (Simple Preference Optimization) is an alternative to DPO for preference learning. It optimizes the reward directly on the sequence level without requiring a reference model, using the average log probability of the generated sequence.

## Core Formula
The SimPO loss involves:
1. Calculating the average log probability per token for the chosen and rejected sequences.
2. Adding a target reward margin $\gamma$ (gamma).
3. Passing the difference through a sigmoid function (specifically, `-log(sigmoid(diff))`).

Formula:
$$L_{\text{SimPO}} = - \log \sigma \left( \beta \left( \frac{1}{|y_w|} \sum_{i} \log p(y_{w,i}|x) - \frac{1}{|y_l|} \sum_{i} \log p(y_{l,i}|x) \right) - \gamma \right)$$

where:
- $\beta$ is a scaling factor.
- $\gamma$ is the reward margin.
- $y_w$ is the chosen/winning sequence.
- $y_l$ is the rejected/losing sequence.

## Usage
In a trainer like `DPOTrainer`, this can be implemented by computing the average log probability for both policy and reference (though SimPO only needs the policy logprobs, they might be formatted similar to DPO).
