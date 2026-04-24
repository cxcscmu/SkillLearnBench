---
name: environment_synchronization
description: Synchronizes the Python environment with specific dependency versions defined in project files to ensure numerical reproducibility.
---
To synchronize the environment, perform the following:
1. Verify the existence of `requirements.txt` in the root directory.
2. Execute `python -m pip install -r requirements.txt` to align installed packages with the repository's specifications.
3. Resolve dependency conflicts by uninstalling incompatible versions if `pip` reports errors.
4. Log the environment state by running `python -VV > /root/python_info.txt` followed by `python -m pip freeze >> /root/python_info.txt`.