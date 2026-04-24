---
name: environment-setup
description: Procedures for setting up the environment for research projects involving Python, PyTorch, and NLP models. Use whenever environment requirements (environment.yml) are present.
---
# Environment Setup for NLP Research

When dealing with deep learning research repositories, follow these steps:

1. **Review Requirements**: Inspect `environment.yml` or `requirements.txt` to identify dependencies.
2. **Version Checks**:
   - `python -VV` to check the python version.
   - `pip freeze` to check installed packages.
3. **Environment Creation**:
   - Use `conda env update --file environment.yml` or standard pip requirements installation if conda is not available.
4. **Validation**:
   - Verify that all necessary libraries for training/evaluation are available.
   - Ensure hardware acceleration (CUDA/ROCm) is correctly configured if needed.
   - Log the final environment state.
5. **Consistency**:
   - Record the environment state to a file (e.g., `python_info.txt`) to allow for replication.
