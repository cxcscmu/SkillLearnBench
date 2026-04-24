---
name: glm-basics
description: Set up and validate the GLM environment for Lake Mendota simulation. Use this skill to verify the configuration file exists, inspect current calibration parameters, and confirm all input data (meteorological forcing, field observations, initial profile) are accessible before running calibration.
---

## Overview
Before calibrating GLM parameters, establish a baseline understanding of:
- The configuration file structure and current parameter values
- Available input data and their formats
- The observation dataset that will be used for validation

## Steps

### 1. Inspect the GLM Configuration File

```bash
head -100 /root/glm3.nml
```

Look for the `&calibration` section and note the current values of:
- `Kw`, `coef_mix_hyp`, `wind_factor`, `lw_factor`, `ch`

Also confirm that `sw_factor`, `cd`, `ce`, initialization profile (`the_depths`, `the_temps`, `the_sals`), and simulation dates are unchanged.

### 2. Read Current Calibration Parameters

Create a Python script to extract current parameter values robustly:

```python
import re

def read_current_nml_parameters(nml_path, param_names):
    """
    Extract calibration parameters from GLM .nml file.
    
    Handles:
    - Parameters at line start or after whitespace
    - Scientific notation (e.g., 1.0e-4, 1e-3)
    - Parameters with or without leading/trailing spaces
    
    Returns dict of {param: float_value}, or raises ValueError if any param missing.
    """
    pattern_template = r'{param}\s*=\s*([\d.]+(?:[eE][+-]?\d+)?)'
    
    params = {}
    with open(nml_path, 'r') as f:
        content = f.read()
    
    for param in param_names:
        pattern = pattern_template.format(param=param)
        match = re.search(pattern, content)
        if not match:
            raise ValueError(f"Parameter '{param}' not found in {nml_path}")
        params[param] = float(match.group(1))
    
    print(f"Successfully read {len(params)} parameters from {nml_path}:")
    for p, v in params.items():
        print(f"  {p} = {v}")
    
    return params

# Test extraction
current_params = read_current_nml_parameters(
    '/root/glm3.nml',
    ['Kw', 'coef_mix_hyp', 'wind_factor', 'lw_factor', 'ch']
)
```

### 3. Verify Input Data Availability

```python
import os
import pandas as pd

# Check meteorological/hydrological forcing
bcs_path = '/root/bcs/'
if os.path.isdir(bcs_path):
    files = os.listdir(bcs_path)
    print(f"Found {len(files)} forcing files in {bcs_path}")
    print(f"Files: {sorted(files)}")
else:
    raise FileNotFoundError(f"{bcs_path} not found")

# Check observation data
obs_path = '/root/field_temp_oxy.csv'
if os.path.exists(obs_path):
    obs_df = pd.read_csv(obs_path)
    print(f"\nObservation file: {obs_path}")
    print(f"Shape: {obs_df.shape}")
    print(f"Columns: {list(obs_df.columns)}")
    print(f"Date range: {obs_df.iloc[0:5]}")
else:
    raise FileNotFoundError(f"{obs_path} not found")

# Check output directory
output_dir = '/root/output'
if os.path.isdir(output_dir):
    print(f"\nOutput directory exists: {output_dir}")
else:
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")
```

### 4. Validate Calibration Parameter Ranges

```python
def validate_ranges(params, ranges):
    """
    Check that all parameters fall within published calibration ranges.
    
    Args:
        params (dict): Parameter name → value
        ranges (dict): Parameter name → (min, max) tuple
    
    Returns:
        bool: True if all params in range
    
    Raises:
        ValueError: If any param out of range
    """
    for param, value in params.items():
        if param in ranges:
            min_val, max_val = ranges[param]
            if not (min_val <= value <= max_val):
                raise ValueError(
                    f"{param}={value} is outside range [{min_val}, {max_val}]"
                )
    print("All parameters are within published calibration ranges.")
    return True

ranges = {
    'Kw': (0.1, 0.5),
    'coef_mix_hyp': (0.3, 0.7),
    'wind_factor': (0.7, 1.3),
    'lw_factor': (0.7, 1.3),
    'ch': (0.0005, 0.002)
}

validate_ranges(current_params, ranges)
```

### 5. Summary

After completing these steps, you should have:
✓ Confirmed the configuration file is readable and contains all required parameters  
✓ Extracted current calibration parameter values (with validation of scientific notation)  
✓ Verified that forcing data and observation data are accessible  
✓ Confirmed all current parameter values are within published ranges  
✓ Prepared the output directory for simulation results  

You are now ready to proceed to `glm-calibration` to adjust parameters and run the model.