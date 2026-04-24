---
name: run2_nlp-paper-reproduction
description: Complete setup guide for reproducing NLP paper results with HuggingFace TRL/transformers on Python 3.12 - use when setting up environments for preference optimization experiments.
---

# NLP Paper Reproduction Setup Guide

## Environment Detection
```bash
# Check what Python is available
which python3 && python3 -V
which python && python -V 2>/dev/null || echo "no 'python' command"
```

## Package Installation (Python 3.12, system Python)
**Important**: Python 3.12 may require `--break-system-packages` flag for pip.

```bash
# Step 1: PyTorch (CPU version for testing, or CUDA for training)
python3 -m pip install torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu --break-system-packages

# Step 2: HuggingFace ecosystem
python3 -m pip install transformers==4.44.2 accelerate==0.29.2 datasets==2.18.0 peft==0.7.1 --break-system-packages

# Step 3: TRL (Transformer Reinforcement Learning)
python3 -m pip install trl==0.9.6 --break-system-packages

# Step 4: Missing dependencies (TRL 0.9.6 requires 'rich')
python3 -m pip install rich --break-system-packages
```

## Import Test
```python
from scripts.simpo_trainer import SimPOTrainer  # must run from project root
```

## Running Unit Tests
Unit tests import `from scripts.simpo_trainer import ...`, so they need PYTHONPATH:
```bash
# Method 1: Set PYTHONPATH to project root
PYTHONPATH=/root/SimPO python3 /root/SimPO/unit_test/unit_test_1.py

# Method 2: Run from project root with module path
cd /root/SimPO && PYTHONPATH=. python3 unit_test/unit_test_1.py

# With pytest
python3 -m pip install pytest --break-system-packages
PYTHONPATH=/root/SimPO python3 -m pytest unit_test/ -v
```

## Logging Environment for Reproducibility
```bash
python3 -VV > /root/python_info.txt
python3 -m pip freeze >> /root/python_info.txt
```

## Common Issues & Fixes

### `ModuleNotFoundError: No module named 'scripts'`
- Root cause: Working directory not set to project root
- Fix: `PYTHONPATH=/root/SimPO python3 unit_test/unit_test_1.py`

### `ModuleNotFoundError: No module named 'rich'`
- Root cause: TRL 0.9.6 requires `rich` which isn't auto-installed
- Fix: `python3 -m pip install rich --break-system-packages`

### `ERROR: This environment is externally managed`
- Root cause: Ubuntu 24.04+ restricts system pip
- Fix: Add `--break-system-packages` flag to pip commands

### PDF Reading
```bash
# Install poppler for PDF text extraction
apt-get install -y poppler-utils
pdftotext /path/to/paper.pdf /tmp/paper.txt
cat /tmp/paper.txt
```

## TRL 0.9.6 API Notes
- `from trl.trainer import CPOTrainer` — base class sometimes used
- `from trl.trainer.utils import DPODataCollatorWithPadding, disable_dropout_in_model, pad_to_length, peft_module_casting_to_bf16, trl_sanitze_kwargs_for_tagging`
- Note: `trl_sanitze_kwargs_for_tagging` (typo: "sanitze" not "sanitize") is intentional in trl source
