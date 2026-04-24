---
name: run2_simpo_loss
description: Precision implementation of SimPO (Simple Preference Optimization) loss with length-normalized rewards and configurable margin.
---

### SimPO Loss Formulation
SimPO optimizes models using a reference-free reward:
$r_\theta(x, y) = \frac{1}{|y|} \log \pi_\theta(y|x)$
The SimPO loss is:
$L_{SimPO}(\theta) = -E_{(x, y_w, y_l) \sim D} [\log \sigma(\beta(r_\theta(x, y_w) - r_\theta(x, y_l)) - \gamma)]$
where $\gamma$ is the target reward margin.

### Key Parameter Relations
In common implementations (like `SimPOTrainer`), the following relations apply:
- **Normalization**: Log probabilities MUST be averaged over tokens.
- **$\gamma$ definition**: Often expressed as $\beta \times \text{gamma\_beta\_ratio}$.
- **Loss Types**:
  - `sigmoid`: $L = - \text{logsigmoid}(\beta(r_w - r_l) - \gamma)$
  - `hinge`: $L = \max(0, \gamma - \beta(r_w - r_l))$

### Implementation Pattern
```python
import torch.nn.functional as F

def compute_simpo_loss(beta, gamma_beta_ratio, chosen_logps, rejected_logps, loss_type="sigmoid", label_smoothing=0.0):
    gamma = beta * gamma_beta_ratio
    # chosen_logps and rejected_logps should be normalized (averaged over tokens)
    logits = beta * (chosen_logps - rejected_logps) - gamma
    
    if loss_type == "sigmoid":
        losses = -F.logsigmoid(logits) * (1 - label_smoothing) - F.logsigmoid(-logits) * label_smoothing
    elif loss_type == "hinge":
        losses = torch.relu(gamma - beta * (chosen_logps - rejected_logps))
    return losses, beta * chosen_logps, beta * rejected_logps
```
