---
name: install-simpo-dependencies-python310
description: Use this skill to install all required packages for the SimPO project using Python 3.10 specifically. Installs torch, transformers, trl, and other dependencies into the python3.10 environment.
---

## Install SimPO Dependencies Under Python 3.10

### Step 1: Upgrade pip for python3.10

```bash
python3.10 -m pip install --upgrade pip
```

### Step 2: Install core dependencies

```bash
python3.10 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
python3.10 -m pip install transformers datasets accelerate
python3.10 -m pip install trl peft
python3.10 -m pip install numpy scipy
```

### Step 3: Install any project-specific requirements

```bash
# Check if requirements.txt exists
if [ -f /root/SimPO/requirements.txt ]; then
    python3.10 -m pip install -r /root/SimPO/requirements.txt
fi
```

### Step 4: Verify key imports

```bash
python3.10 -c "import torch; import transformers; import numpy; print('All imports OK')"
```