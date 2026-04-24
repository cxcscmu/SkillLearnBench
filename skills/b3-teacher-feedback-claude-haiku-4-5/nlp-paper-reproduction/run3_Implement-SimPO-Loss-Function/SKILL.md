---
name: Implement SimPO Loss Function
description: Use when implementing the `simpo_loss` function in SimPOTrainer class. Extract loss computation logic from the paper and translate it to PyTorch code that accepts the expected tensor inputs.
---

1. **Study the SimPO loss formula in the paper**:
   - Read `/root/SimPO/paper.pdf` to understand the mathematical definition
   - Note the inputs expected (typically: logits for chosen/rejected, reference logits, or similar)
   - Identify any hyperparameters (temperature, beta, etc.)

2. **Examine the function signature in SimPOTrainer**:
   ```bash
   grep -A 10 "def simpo_loss" /root/SimPO/scripts/simpo_trainer.py
   ```

3. **Check the unit test to understand expected inputs and outputs**:
   ```bash
   cat /root/SimPO/unit_test/unit_test_1.py
   ```
   - Identify input tensor shapes and dtypes
   - Identify expected output shape and key name for `.npz` file

4. **Implement the loss function**:
   - Translate the mathematical formula to PyTorch operations
   - Handle batch dimensions correctly
   - Ensure numerical stability (use log-sum-exp tricks if needed)
   - Return losses as a 1D tensor matching batch size

5. **Verify implementation**:
   - Function accepts all required arguments from the test
   - Returns tensor with shape matching expected output
   - No undefined variables or missing imports