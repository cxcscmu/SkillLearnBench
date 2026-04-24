name: nlp-environment-setup
description: Steps to set up and verify a Python environment for NLP research projects. Use this skill when you need to install dependencies, resolve conflicts, and log environment information for reproducibility.

# NLP Environment Setup Guide

Setting up a robust environment is crucial for reproducibility in NLP research.

## Steps for Environment Setup

1. **Review Requirements**: Analyze `environment.yml` and `requirements.txt` to identify the needed Python version and packages.
2. **Environment Creation**: Use `conda` or `pip` as appropriate.
   - For `environment.yml`: `conda env create -f environment.yml` (if available).
   - Alternatively, install from the `pip` section directly.
3. **Handle Conflicts**: If there are version conflicts:
   - Identify the conflicting package.
   - Use `pip install <package>==<version>` to force a specific version.
   - For flash-attention or specialized packages, use appropriate flags (e.g., `--no-build-isolation`).
4. **Verification**: After installation, run `python -VV` and `python -m pip freeze` to verify the state.
5. **Logging**: Always log the verified environment state to a file (e.g., `python_info.txt`) for later reference.

## Environment Logging Script
```bash
python -VV > python_info.txt
python -m pip freeze >> python_info.txt
```

## Success Criteria
- All required packages are installed without errors.
- Python version matches the project requirement.
- Essential libraries like `torch`, `transformers`, `trl`, and `accelerate` are present.
