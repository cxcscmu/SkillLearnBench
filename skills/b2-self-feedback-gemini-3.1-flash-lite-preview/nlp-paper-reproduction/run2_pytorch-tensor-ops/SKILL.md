---
name: run2_pytorch-tensor-ops
description: Robust PyTorch tensor operations for implementing loss functions, including handling device placement and numerical stability.
---

### Tensor Operations
*   `torch.gather`: Useful for selecting specific log probabilities from logits: `torch.gather(log_probs, dim=-1, index=labels.unsqueeze(-1)).squeeze(-1)`.
*   `F.logsigmoid`: Stable computation of `log(sigmoid(x))`.
*   `.to(device)`: Ensure all input tensors and the trainer components are on the same device.
---
