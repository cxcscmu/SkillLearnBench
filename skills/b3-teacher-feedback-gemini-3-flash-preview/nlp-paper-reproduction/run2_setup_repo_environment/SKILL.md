---
name: setup_repo_environment
description: Aligns the local environment with the repository's requirements by checking for dependency files, installing build-essential tools for complex packages like DeepSpeed, and logging environment metadata.
---

1. **Identify Dependencies**: Check the `/root/SimPO` directory for `environment.yml`, `requirements.txt`, or `pyproject.toml`.
2. **Align Python Version**: If a specific version is required by `environment.yml`, attempt to use that version.
3. **Install Build Tools**: Ensure the system has tools required for compiling C++/CUDA extensions (common in NLP repos for `deepspeed` or `flash-attn`):
   - `apt-get update && apt-get install -y build-essential libaio-dev`
4. **Install Packages**:
   - If `requirements.txt` exists: `pip install -r requirements.txt`.
   - Ensure `torch`, `numpy`, and `transformers` are compatible with the versions mentioned in the repo.
5. **Log Environment Info**:
   - Run `python -VV > /root/python_info.txt`
   - Run `python -m pip freeze >> /root/python_info.txt`
   - This ensures the exact state used for the loss computation is recorded for reproducibility.