---
name: run2_project_alignment
description: Procedures for aligning a project-specific environment to its `environment.yml` and project-root structure.
---

### Aligning Project Environment
When a project provides an `environment.yml` but `conda` is unavailable, align the project manually using `pip`.

1. **Extracting Pip Dependencies**:
   Extract all `pip:` entries from the `environment.yml` and install them.
   
2. **Managing PYTHONPATH**:
   Ensure the project root is in the `PYTHONPATH` to correctly resolve local imports.
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   ```

3. **Verifying with Unit Tests**:
   Run unit tests from the project root and ensure they use the correct trainer/config classes by referencing them as `scripts.<module>` or similar.

4. **Saving Results for Reproductivity**:
   Always use fixed output files like `/root/loss.npz` and document system versions in `/root/python_info.txt` to help others reproduce results exactly.
