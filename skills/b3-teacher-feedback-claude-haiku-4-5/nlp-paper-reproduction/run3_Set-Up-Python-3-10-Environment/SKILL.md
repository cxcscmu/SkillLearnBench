---
name: Set Up Python 3.10 Environment
description: Use when you need to switch from an incompatible Python version to Python 3.10 before project setup. This ensures the correct runtime environment for dependency installation and test execution.
---

1. **Install Python 3.10 using uv**:
   ```bash
   uv python install 3.10
   ```

2. **Verify installation**:
   ```bash
   uv python list
   ```

3. **Create a virtual environment with Python 3.10**:
   ```bash
   uv venv /root/.venv310 --python 3.10
   ```

4. **Activate the Python 3.10 environment**:
   ```bash
   source /root/.venv310/bin/activate
   ```

5. **Verify the active Python version**:
   ```bash
   python --version
   python -VV
   ```

6. **Document the environment info**:
   ```bash
   python -VV > /root/python_info.txt
   python -m pip freeze >> /root/python_info.txt
   ```

**All subsequent commands must be executed within the activated Python 3.10 environment.**