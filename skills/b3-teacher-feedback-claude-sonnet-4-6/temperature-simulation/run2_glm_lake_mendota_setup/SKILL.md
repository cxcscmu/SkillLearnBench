---
name: glm_lake_mendota_setup
description: Use this skill to understand the GLM (General Lake Model) configuration for Lake Mendota, including how to read and modify the glm3.nml file, what parameters are allowed to change, and how the model is structured. Apply this before running or calibrating GLM.
---

# GLM Lake Mendota Setup

## Allowed Calibration Parameters
Only these five parameters may be modified in `/root/glm3.nml`:
- `Kw` — light extinction coefficient, range `[0.1, 0.5]`
- `coef_mix_hyp` — hypolimnetic mixing coefficient, range `[0.3, 0.7]`
- `wind_factor` — wind scaling factor, range `[0.7, 1.3]`
- `lw_factor` — longwave radiation scaling, range `[0.7, 1.3]`
- `ch` — bulk aerodynamic heat transfer coefficient, range `[0.0005, 0.002]`

**Do NOT change**: `sw_factor`, `cd`, `ce`, `the_depths`, `the_temps`, `the_sals`, or any other settings.

## Reading and Modifying glm3.nml

```python
import re

def read_nml_param(nml_path, param_name):
    """Read a single parameter value from the NML file."""
    with open(nml_path, 'r') as f:
        content = f.read()
    pattern = rf'^\s*{param_name}\s*=\s*([^\n,!]+)'
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        return float(match.group(1).strip())
    raise ValueError(f"Parameter {param_name} not found in {nml_path}")

def write_nml_param(nml_path, param_name, value):
    """Write a single parameter value to the NML file."""
    with open(nml_path, 'r') as f:
        content = f.read()
    pattern = rf'(^\s*{param_name}\s*=\s*)([^\n,!]+)'
    replacement = rf'\g<1>{value}'
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    if new_content == content:
        raise ValueError(f"Parameter {param_name} not found or not replaced in {nml_path}")
    with open(nml_path, 'w') as f:
        f.write(new_content)

def get_lake_depth_from_nml(nml_path):
    """Get the fixed lake depth (crest_elev - base_elev) from morphometry block."""
    with open(nml_path, 'r') as f:
        content = f.read()
    # Try lake_depth first
    m = re.search(r'^\s*lake_depth\s*=\s*([^\n,!]+)', content, re.MULTILINE)
    if m:
        return float(m.group(1).strip())
    # Fallback: crest_elev - bsn_bot or lake_depth from morphometry
    ce = re.search(r'^\s*crest_elev\s*=\s*([^\n,!]+)', content, re.MULTILINE)
    be = re.search(r'^\s*bsn_bot\s*=\s*([^\n,!]+)', content, re.MULTILINE)
    if ce and be:
        return float(ce.group(1).strip()) - float(be.group(1).strip())
    raise ValueError("Cannot determine lake_depth from NML file")
```

## Running GLM

```python
import subprocess
import os

def run_glm(glm_dir='/root'):
    """Run GLM from the given directory. Returns (returncode, stdout, stderr)."""
    result = subprocess.run(
        ['glm'],
        cwd=glm_dir,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def glm_ran_successfully(glm_dir='/root'):
    """Check that GLM ran and produced output."""
    output_path = os.path.join(glm_dir, 'output', 'output.nc')
    rc, stdout, stderr = run_glm(glm_dir)
    if rc != 0:
        print("GLM STDERR:", stderr[-2000:])
        return False
    if not os.path.exists(output_path):
        print("Output file not found:", output_path)
        return False
    return True
```