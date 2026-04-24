---
name: implement_simpo_loss
description: Implements the SimPO (Simple Preference Optimization) loss function with length normalization and reward margin as specified in the research paper.
---

1. **Implement the Logic**: In `SimPOTrainer.simpo_loss` within `/root/SimPO/scripts/simpo_trainer.py`, implement the following mathematical steps:
   - Calculate the log probabilities for the winning (chosen) and losing (rejected) responses.
   - **Length Normalization**: Divide the log probabilities of each sequence by its length ($L$): $p_{norm} = \frac{1}{L} \log \pi(x, y)$.
   - **Reward Calculation**: Calculate rewards as $R = \beta \cdot p_{norm}$.
   - **SimPO Loss**: Use the formula:
     $\mathcal{L}_{SimPO} = -\mathbb{E}_{(x, y_w, y_l)} [\log \sigma(\beta p_{norm}(y_w|x) - \beta p_{norm}(y_l|x) - \gamma)]$
     where $\gamma$ is the target reward margin and $\beta$ is the scale.
2. **Verification**:
   - Import the required libraries (torch, numpy).
   - Ensure the function returns the loss tensor in the format expected by the trainer.