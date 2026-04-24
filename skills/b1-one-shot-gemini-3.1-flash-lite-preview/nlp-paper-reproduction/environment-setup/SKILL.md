---
name: environment-setup
description: Procedures for setting up the python environment, installing dependencies, and verifying installations.
---

### Environment Setup
1. **Check Requirements**: Verify `environment.yml` for required packages.
2. **Setup Virtual Environment**: If not provided, create a conda or virtualenv.
3. **Install Dependencies**: `pip install -r requirements.txt` or `conda env update`.
4. **Log State**: Capture environment details with `python -VV` and `pip freeze`.

### Verification
- Ensure `import` statements in project scripts are valid.
- Run project-provided tests (e.g., `unit_test_1.py`) to confirm functional parity.
