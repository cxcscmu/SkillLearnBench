---
name: run2_robust_env
description: Procedures for resolving environment conflicts, broken packages, and restricted system-wide access in Python.
---

### Resolving Environment Conflicts
In research environments (e.g., containers), `pip` might face restricted system-wide access or broken distributions.

1. **Handling Externally Managed Environments**:
   If `pip install` fails with "externally-managed-environment", use `--break-system-packages` cautiously or create a virtual environment (`python -m venv`).
   
2. **Fixing Broken Package Distributions**:
   - Symptoms: `OSError: cannot open shared object file` or `WARNING: Ignoring invalid distribution ~orch`.
   - Solution: Uninstall the broken distribution and reinstall.
     ```bash
     pip uninstall <pkg> -y --break-system-packages
     pip install <pkg>==<version> --break-system-packages
     ```

3. **Managing Missing Shared Objects**:
   Always verify the installation of hardware-dependent libraries like `torch` or `flash-attn` by running a basic script to import them.

### Logging System State
Use `python -VV` and `pip freeze` to ensure the runtime state is documented for reproducibility.
