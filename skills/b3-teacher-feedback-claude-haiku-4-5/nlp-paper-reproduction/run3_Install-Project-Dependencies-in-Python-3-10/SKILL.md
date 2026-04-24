---
name: Install Project Dependencies in Python 3.10
description: Use after activating Python 3.10 environment to install project dependencies without version conflicts. This ensures all packages are compatible with the target Python version.
---

1. **Ensure Python 3.10 environment is activated**:
   ```bash
   python -VV | grep "3.10"
   ```

2. **Upgrade pip, setuptools, and wheel**:
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

3. **Install project dependencies**:
   ```bash
   cd /root/SimPO
   python -m pip install -r requirements.txt
   ```
   Or if using environment.yml:
   ```bash
   conda env update --file environment.yml --prune
   ```

4. **Verify critical packages are installed** for the project:
   ```bash
   python -c "import torch; import transformers; import numpy" && echo "Core dependencies OK"
   ```

5. **Log final environment state**:
   ```bash
   python -VV > /root/python_info.txt
   python -m pip freeze >> /root/python_info.txt
   ```