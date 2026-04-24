---
name: pytorch-nlp-setup
description: Set up Python environments for NLP/ML projects using PyTorch, transformers, and TRL. Use this skill when installing dependencies for preference optimization, RLHF, or transformer-based training pipelines.
---

# PyTorch NLP Environment Setup

## Standard Stack for Preference Optimization Projects

```bash
pip install torch transformers datasets accelerate trl peft wandb numpy
```

## Version Compatibility Notes

- TRL (Transformer Reinforcement Learning) provides base trainers like CPOTrainer, DPOTrainer
- Older TRL versions (< 0.8) have different import paths for utilities
- Check `from trl.trainer.utils import DPODataCollatorWithPadding` availability
- For `trl_sanitze_kwargs_for_tagging` (note: typo is intentional in some versions)

## Common Issues

- If `from trl.import_utils import is_peft_available` fails, check TRL version
- Some projects pin specific transformers/TRL versions — check requirements.txt or setup.py
- CUDA availability: use `torch.device("cuda:0" if torch.cuda.is_available() else "cpu")`

## Running Unit Tests

```bash
cd /path/to/project && python -m pytest unit_test/ -v
# or
cd /path/to/project && python -m unittest unit_test.unit_test_1
```
