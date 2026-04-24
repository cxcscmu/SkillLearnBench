---
name: Run Unit Test in Python 3.10 Environment
description: Use to execute the unit test within the Python 3.10 virtual environment after implementing the loss function. This validates the implementation against fixed input tensors.
---

1. **Ensure Python 3.10 environment is active**:
   ```bash
   source /root/.venv310/bin/activate
   python -VV
   ```

2. **Navigate to project root**:
   ```bash
   cd /root/SimPO
   ```

3. **Run the unit test**:
   ```bash
   python unit_test/unit_test_1.py
   ```

4. **Verify output file was created**:
   ```bash
   ls -lh /root/loss.npz
   ```

5. **Inspect the saved loss values** (optional verification):
   ```bash
   python -c "import numpy as np; data = np.load('/root/loss.npz'); print(data['losses'])"
   ```

6. **Check for any error messages**:
   - If test fails, review error traceback
   - Verify tensor shapes match test expectations
   - Confirm loss computation logic against paper formula