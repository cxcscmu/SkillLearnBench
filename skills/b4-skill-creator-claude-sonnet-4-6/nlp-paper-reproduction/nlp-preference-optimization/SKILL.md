---
name: nlp-preference-optimization
description: Set up and run NLP preference optimization experiments (DPO, SimPO, CPO). Use this skill when configuring trainer environments, installing dependencies (torch, trl, transformers, peft), or running preference optimization unit tests. Triggers on: DPO, SimPO, preference optimization, trl trainer, RLHF, alignment training.
---

# NLP Preference Optimization Environment Setup

## Required Packages
```
torch==2.2.2
trl==0.9.6
transformers==4.44.2
accelerate==0.29.2
peft==0.7.1
datasets==2.18.0
numpy==1.26.4
```

## Install with pip (break-system-packages if needed)
```bash
pip3 install --break-system-packages torch==2.2.2 trl==0.9.6 transformers==4.44.2 accelerate==0.29.2 peft==0.7.1 datasets==2.18.0 numpy==1.26.4
```

## Running Unit Tests
```bash
cd /root/SimPO
python3 -m pytest unit_test/unit_test_1.py -v
# or
python3 unit_test/unit_test_1.py
```

## Common Issues

### Import conflicts
- `trl.trainer.CPOTrainer` must be importable
- Check trl version: `pip show trl`

### trl API changes
- `trl_sanitze_kwargs_for_tagging` may differ across versions
- `DPODataCollatorWithPadding` location may vary
- Check: `from trl.trainer.utils import ...`

## Logging Python Environment
```bash
python3 -VV > /root/python_info.txt
python3 -m pip freeze >> /root/python_info.txt
```
