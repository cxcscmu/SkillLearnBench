---
name: simpo-environment-setup
description: How to set up the correct Python environment for the SimPO project, specifically using Python 3.10 and resolving version conflicts. Use this when setting up the environment to run SimPO code and unit tests.
---

## SimPO Environment Setup

### Critical: Use Python 3.10

The SimPO project and its tests **require Python 3.10**. If the system has a different Python version (e.g., 3.12), you must install and use Python 3.10 explicitly.

### Step-by-step Setup

```bash
# 1. Install Python 3.10 using uv (or conda/pyenv)
uv python install 3.10

# 2. Create a virtual environment with Python 3.10
cd /root/SimPO
uv venv --python 3.10 .venv

# 3. Activate the virtual environment
source .venv/bin/activate

# 4. Verify Python version
python -VV
# Should show Python 3.10.x

# 5. Install project dependencies
# If there's a requirements.txt or setup.py:
pip install torch torchvision torchaudio
pip install transformers trl accelerate datasets
pip install numpy

# Or install from the project:
# pip install -e .

# 6. If there are conflicts with pre-installed packages (e.g., system torch for 3.12),
# the venv isolates you from those. Install everything fresh in the venv.
```

### Generate python_info.txt

```bash
# Must be run with the Python 3.10 venv activated
python -VV > /root/python_info.txt 2>&1
python -m pip freeze >> /root/python_info.txt
```

### Run the Unit Test

```bash
# With the Python 3.10 venv activated
cd /root/SimPO
python unit_test/unit_test_1.py
```

This will generate `/root/loss.npz` with key `'losses'`.

### Common Issues

1. **Wrong Python version**: If `/root/python_info.txt` shows Python 3.12, the test will fail. Always verify `python -VV` shows 3.10.
2. **Package conflicts**: If system packages conflict, create a clean venv with Python 3.10.
3. **CUDA availability**: The unit test may run on CPU. Ensure torch is installed correctly for the available hardware.
4. **uv tool**: If `uv` is available, it's the easiest way to install a specific Python version:
   ```bash
   uv python install 3.10
   uv venv --python 3.10 /root/SimPO/.venv
   ```
5. **Alternative with conda**:
   ```bash
   conda create -n simpo python=3.10 -y
   conda activate simpo
   pip install torch transformers trl accelerate datasets numpy
   ```