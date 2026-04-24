---
name: Check Repository Dependencies
description: Use when starting a new project to verify Python version requirements declared in configuration files. This prevents version mismatches before environment setup.
---

1. **Check for requirements declaration**:
   ```bash
   cat /root/SimPO/requirements.txt 2>/dev/null || echo "No requirements.txt"
   cat /root/SimPO/environment.yml 2>/dev/null || echo "No environment.yml"
   cat /root/SimPO/pyproject.toml 2>/dev/null || echo "No pyproject.toml"
   ```

2. **Extract Python version requirement** from the output:
   - Look for `python>=X.Y` or `python==X.Y` specifications
   - Check for any `.python-version` file:
     ```bash
     cat /root/SimPO/.python-version 2>/dev/null || echo "No .python-version file"
     ```

3. **Verify the declared version matches your target** (Python 3.10):
   - If requirements specify 3.10, proceed with setup
   - If requirements specify a different version, note it for environment configuration