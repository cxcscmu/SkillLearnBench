---
name: run2_glm_calibration
description: Instructions for modifying GLM parameters using regex and systematically optimizing them within physical limits.
---

# GLM Calibration (Improved)

This skill covers programmatic configuration of GLM and automated parameter tuning.

## Modifying Parameters
GLM uses a `.nml` configuration file. A robust way to edit it without dedicated Fortran namelist parsers is using Python's `re` module.
This ensures parameters with scientific notation or decimals are reliably replaced.

```python
import re
def update_nml(file_path, params):
    with open(file_path, 'r') as f:
        content = f.read()
    for k, v in params.items():
        # \b ensures exact keyword match, avoiding partial matches like 'catchrain'
        content = re.sub(rf"(\b{k}\s*=\s*)[0-9\.eE+-]+", rf"\g<1>{v}", content)
    with open(file_path, 'w') as f:
        f.write(content)
```

## Running the Model
Call the `glm` executable in the directory containing `glm3.nml`:
```bash
subprocess.run(['glm'], cwd='/path/to/project', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

## Automated Tuning
To quickly find parameters satisfying specific RMSE constraints without manual trial-and-error, you can employ `scipy.optimize.minimize` (like Nelder-Mead) over a custom objective function. 
Provide boundary lists to keep values within physically reasonable calibration ranges.
