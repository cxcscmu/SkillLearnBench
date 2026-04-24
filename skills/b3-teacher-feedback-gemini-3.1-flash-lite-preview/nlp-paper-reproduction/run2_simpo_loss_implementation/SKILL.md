---
name: simpo_loss_implementation
description: Implements the SimPO loss function using stable log-probability operations in the specified trainer file.
---
1. Open `/root/SimPO/scripts/simpo_trainer.py`.
2. Locate the `simpo_loss` method within the `SimPOTrainer` class.
3. Implement the formula: $L_{SimPO} = -\log(\sigma(\beta(\log \pi_\theta(y_w|x) - \log \pi_\theta(y_l|x)) - \gamma))$.
4. Ensure all tensor operations explicitly cast inputs to `torch.float32` to maintain precision parity with the unit test's fixed tensors.
5. Use `torch.nn.functional.logsigmoid` or stable subtraction to prevent overflow during exponentiation.