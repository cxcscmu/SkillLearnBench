---
name: run2_pytorch-preference-optimization
description: Environment setup and testing patterns for SimPO preference optimization with PyTorch.
---

# PyTorch Preference Optimization Environment

## Required Environment
- Python 3.10 (deadsnakes PPA on Ubuntu 24.04)
- torch==2.2.2 (CPU or CUDA)
- transformers==4.44.2
- trl==0.9.6
- accelerate==0.29.2
- peft==0.7.1
- datasets==2.18.0
- numpy==1.26.4
- rich (required by trl.trainer.utils)

## Setup Steps
```bash
# Install Python 3.10
add-apt-repository -y ppa:deadsnakes/ppa
apt-get install -y python3.10 python3.10-venv python3.10-dev

# Create venv
python3.10 -m venv /root/simpo_env
source /root/simpo_env/bin/activate

# Install packages
pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu
pip install transformers==4.44.2 accelerate==0.29.2 datasets==2.18.0 \
    trl==0.9.6 peft==0.7.1 numpy==1.26.4 rich
```

## Key Gotcha
- `trl==0.9.6` depends on `rich` but doesn't declare it as a dependency. Must install separately.

## Running Tests
```bash
cd /root/SimPO
source /root/simpo_env/bin/activate
python -m unittest unit_test.unit_test_1
```

## Logging Environment
```bash
(python -VV && echo "---" && python -m pip freeze) > /root/python_info.txt
```
