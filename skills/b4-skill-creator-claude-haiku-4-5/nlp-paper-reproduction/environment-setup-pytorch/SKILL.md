---
name: environment-setup-pytorch
description: Set up Python environment for PyTorch-based NLP projects with transformers and alignment training. Use this skill when initializing project environments, managing dependencies from environment.yml files, installing required packages, and ensuring CUDA/device compatibility. Essential for reproducible machine learning research requiring specific package versions.
---

# Environment Setup for PyTorch Projects

## Overview

This skill covers setting up a complete Python environment for PyTorch-based NLP and language model alignment training, including dependency management and device verification.

## Environment Setup Workflow

### Step 1: Identify Environment Configuration Files

Check for conda/pip configuration files:
- `environment.yml` - Conda environment specification
- `requirements.txt` - Pip requirements
- `setup.py` - Package setup configuration
- `pyproject.toml` - Modern Python project config

### Step 2: Choose Installation Method

#### Option A: Conda Environment
```bash
# Create environment from YAML
conda env create -f environment.yml

# Activate environment
conda activate <env_name>
```

Benefits:
- Manages both Python and system dependencies
- Consistent across platforms
- Handles CUDA toolkit versions

#### Option B: Pip with Virtual Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt
```

#### Option C: Direct Pip Installation
```bash
# Install specific packages
pip install torch torchvision torchaudio
pip install transformers datasets accelerate peft
```

### Step 3: Verify Python Version and Packages

Get detailed environment information:
```bash
python -VV                      # Detailed Python version
python -m pip freeze           # All installed packages with versions
python -m pip show torch       # Specific package info
python -c "import torch; print(torch.__version__)"
```

### Step 4: Check CUDA/Device Availability

Verify GPU access for training:
```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"
```

### Step 5: Install Project in Development Mode

For local project development:
```bash
pip install -e .
# or for projects with setup.py
python setup.py develop
```

## Common Packages for Alignment Training

### Core PyTorch Stack
- `torch`: Deep learning framework
- `torchvision`: Computer vision utilities
- `torchaudio`: Audio processing
- `pytorch-cuda`: CUDA runtime (if using conda)

### NLP and Transformers
- `transformers`: Hugging Face models and utilities
- `tokenizers`: Fast tokenizer library
- `datasets`: Dataset loading and processing
- `accelerate`: Multi-GPU/device training utilities

### Alignment and Training
- `peft`: Parameter-Efficient Fine-Tuning (LoRA, etc.)
- `trl`: Transformers Reinforcement Learning
- `bitsandbytes`: 8-bit optimization utilities
- `flash-attn`: Optimized attention (optional, for efficiency)

### Development Tools
- `numpy`: Numerical computing
- `scipy`: Scientific computing
- `scikit-learn`: Machine learning utilities
- `wandb`: Weights & Biases experiment tracking (optional)

## Dependency Conflict Resolution

### Check for Conflicts
```bash
pip check
```

### Resolve Common Issues

#### PyTorch Version Mismatch
```bash
# Reinstall PyTorch with specific CUDA version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# For CPU-only
pip install torch torchvision torchaudio
```

#### Package Incompatibilities
```bash
# Use environment solver
conda install --solver=libmamba  # Faster solver
# or
pip install --upgrade --upgrade-strategy eager <package>
```

#### Remove Conflicting Packages
```bash
pip uninstall -y <package_name>
pip install <package_name>==<specific_version>
```

### Conda Environment from File
When using conda with environment.yml, sometimes recreating helps:
```bash
# Backup current environment
conda env export > backup_env.yml

# Remove and recreate
conda env remove --name <env_name>
conda env create -f environment.yml
```

## Reproducibility Best Practices

### 1. Lock Dependency Versions
```bash
pip freeze > requirements-lock.txt
conda env export > env-lock.yml
```

### 2. Document Environment Information
Always log:
- Python version and build (`python -VV`)
- Key package versions (torch, transformers, cuda)
- Hardware details (GPU model, CPU)

```bash
# Create comprehensive environment log
{
    echo "=== Python Version ==="
    python -VV
    echo
    echo "=== Package Freeze ==="
    python -m pip freeze
    echo
    echo "=== PyTorch Info ==="
    python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
} > environment_info.txt
```

### 3. Test Critical Imports
```python
import torch
import transformers
from datasets import load_dataset
from peft import get_peft_model
print("All critical imports successful!")
```

## Environment Variables

### CUDA Configuration
```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3  # Specify GPUs
export CUDA_LAUNCH_BLOCKING=1         # Synchronous GPU operations (for debugging)
```

### Training Configuration
```bash
export HF_DATASETS_CACHE=/path/to/cache  # Hugging Face cache
export TRANSFORMERS_CACHE=/path/to/cache
export TOKENIZERS_PARALLELISM=false      # Avoid warnings
```

### Debugging
```bash
export PYTHONUNBUFFERED=1  # Real-time output
export PYTHONBREAKPOINT=ipdb.set_trace  # Use ipdb for breakpoints
```

## Troubleshooting

### Import Errors
```bash
# Reinstall with no cache
pip install --no-cache-dir --force-reinstall <package>

# Check installation location
python -c "import <module>; print(<module>.__file__)"
```

### CUDA/Device Errors
```bash
# Verify CUDA installation
python -c "import torch; torch.cuda.is_available()"

# Check CUDA version
nvcc --version

# Match PyTorch CUDA version to installed CUDA
```

### Memory Issues
```bash
# Install CPU-only version for testing
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Project-Specific Setup

For SimPO and similar training projects:

1. Check `environment.yml` for required versions
2. Create conda environment if file exists
3. Verify transformers and torch compatibility
4. Confirm CUDA/device availability
5. Install project in dev mode if setup.py exists
6. Log all environment details for reproducibility
