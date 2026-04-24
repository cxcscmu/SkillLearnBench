---
name: nlp-environment-management
description: Manages NLP environments, handling library dependencies like PyTorch, Transformers, and custom local packages.
---

# NLP Environment Management

Setting up an environment for NLP research requires specific versions of deep learning libraries and often custom local modules.

## Installation via Conda

If an `environment.yml` is provided:

```bash
# Update existing environment
conda env update -n base --file environment.yml
```

Or create a new one:

```bash
conda env create -f environment.yml
```

## Troubleshooting Common Conflicts

1. **Flash Attention**: Requires `flash-attn` and often specific CUDA versions. Install using:
   ```bash
   pip install flash-attn --no-build-isolation
   ```

2. **Transformers/TRL Versions**: Ensure `transformers` and `trl` versions match the codebase's expectations.

3. **Local Modules**: If a project uses local modules, ensure they are in the `PYTHONPATH`:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   ```

## Logging Environment Info

Always log the environment for reproducibility:
```bash
python -VV > python_info.txt
python -m pip freeze >> python_info.txt
```
