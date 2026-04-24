---
name: nlp-project-setup
description: Set up Python environment for NLP and preference optimization projects.
---

# NLP Project Environment Setup

## Environment Requirements for SimPO

### Core Dependencies
- **PyTorch**: Deep learning framework (torch, torchvision, torchaudio)
- **Transformers**: Hugging Face library for LLMs
- **NumPy**: Numerical computing
- **SciPy**: Scientific computing utilities
- **tqdm**: Progress bars for training loops

### Optional but Recommended
- **wandb**: Experiment tracking
- **accelerate**: Distributed training
- **bitsandbytes**: 8-bit optimization
- **Flash-Attn**: Efficient attention

## Installation Steps

### 1. Check Python Version
```bash
python --version  # Should be 3.8+
python -VV        # Detailed version info
```

### 2. Create Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Core Dependencies
```bash
# PyTorch (CUDA 12.1 example)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Transformers
pip install transformers

# Other essentials
pip install numpy scipy tqdm
```

### 4. Verify Installation
```bash
python -c "import torch; print(torch.__version__)"
python -c "import transformers; print(transformers.__version__)"
```

## Dependency Version Considerations

### For SimPO Specifically
- **transformers** >= 4.30.0 (for AutoTokenizer, model loading)
- **torch** >= 1.13.0 (for modern PyTorch features)
- **numpy** (for .npz file saving)

### Compatibility Notes
- Different CUDA versions may require different torch builds
- GPU memory requirements: typically 10-20GB for 7B models
- CPU-only mode works but is much slower

## Requirements File
Create `requirements.txt`:
```
torch>=1.13.0
transformers>=4.30.0
numpy
scipy
tqdm
accelerate>=0.20.0
```

Then install:
```bash
pip install -r requirements.txt
```

## Logging Installed Packages
```bash
# Save package list
python -m pip freeze > /root/python_info.txt

# Or capture with version info
python -VV >> /root/python_info.txt
python -m pip freeze >> /root/python_info.txt
```

## Troubleshooting

### CUDA/GPU Issues
```bash
# Check if CUDA available
python -c "import torch; print(torch.cuda.is_available())"

# Find CUDA version
nvidia-smi  # Shows CUDA version

# Match PyTorch to CUDA version
# Visit: https://pytorch.org/get-started/locally/
```

### Missing Dependencies
```bash
# Install specific package
pip install <package_name>

# Or reinstall all from requirements
pip install --force-reinstall -r requirements.txt
```

### Version Conflicts
```bash
# Show package version
pip show <package_name>

# Check compatibility
pip check
```
