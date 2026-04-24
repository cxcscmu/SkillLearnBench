---
name: trl-setup
description: Setup and installation of TRL (Transformer Reinforcement Learning) library with compatible torch/transformers versions. Use when setting up preference optimization training environments.
---

# TRL Setup

## Installation
```bash
pip install torch transformers trl accelerate peft datasets --break-system-packages
```

## Compatibility Notes
- TRL imports from `trl.trainer.utils`: `DPODataCollatorWithPadding`, `pad_to_length`, etc.
- Some imports may change across TRL versions (e.g., `trl_sanitze_kwargs_for_tagging` vs `trl_sanitize_kwargs_for_tagging`)
- If running in externally-managed Python (Debian), use `--break-system-packages` flag

## Common Import Errors
- `trl_sanitze_kwargs_for_tagging` not found → check trl version, may be renamed or removed
- Missing `CPOTrainer` → upgrade trl: `pip install --upgrade trl`

## Running Tests from Project Root
```bash
cd /root/SimPO && python -m pytest unit_test/unit_test_1.py -v
# or
cd /root/SimPO && python unit_test/unit_test_1.py
```

## Key TRL Trainer Utilities
- `DPODataCollatorWithPadding`: handles padding for preference pairs
- `pad_to_length`: pads tensor to specified length
- `disable_dropout_in_model`: disables dropout during eval
