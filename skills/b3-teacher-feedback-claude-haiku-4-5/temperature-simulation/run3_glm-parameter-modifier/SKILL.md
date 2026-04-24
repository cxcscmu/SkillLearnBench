---
name: glm-parameter-modifier
description: Safely modify specific calibration parameters in the GLM configuration file. Use this skill when you need to update Kw, coef_mix_hyp, wind_factor, lw_factor, or ch while preserving all other settings and respecting published calibration ranges.
---

## Overview
This skill handles the technical task of modifying only the allowed calibration parameters in `/root/glm3.nml`. It includes robust regex patterns that handle scientific notation and careful validation before and after writing.

## Implementation

### Modify NML Parameters Function

```python
import re

def modify_nml_parameters(nml_path, new_params, ranges):
    """
    Update specific calibration parameters in GLM .nml file.
    
    Handles:
    - Parameters at line start or after whitespace/section markers
    - Scientific notation in both old and new values
    - Validation against published ranges
    - Backup of original file
    
    Args:
        nml_path (str): Path to glm3.nml
        new_params (dict): {param_name: new_value}
        ranges (dict): {param_name: (min, max)} for validation
    
    Raises:
        ValueError: If any new parameter is out of range
        RuntimeError: If modification fails
    """
    # Validate all new parameters are in range
    for param, value in new_params.items():
        if param in ranges:
            min_val, max_val = ranges[param]
            if not (min_val <= value <= max_val):
                raise ValueError(
                    f"Cannot set {param}={value}: outside range [{min_val}, {max_val}]"
                )
    
    # Read original content
    with open(nml_path, 'r') as f:
        content = f.read()
    
    # Create backup
    backup_path = nml_path + '.backup'
    with open(backup_path, 'w') as f:
        f.write(content)
    print(f"Backup created: {backup_path}")
    
    # Pattern: parameter name = optional whitespace = number (with optional scientific notation)
    # Matches: `Kw = 0.3`, `coef_mix_hyp=1.0e-4`, etc.
    pattern_template = r'({param}\s*=\s*)([\d.]+(?:[eE][+-]?\d+)?)'
    
    modified_content = content
    for param, new_value in new_params.items():
        pattern = pattern_template.format(param=param)
        replacement = rf'\g<1>{new_value}'
        
        # Check if parameter exists
        if not re.search(pattern, modified_content):
            raise RuntimeError(f"Parameter '{param}' not found in {nml_path}")
        
        # Replace all occurrences (typically one, but be safe)
        modified_content = re.sub(pattern, replacement, modified_content)
        print(f"Updated {param} → {new_value}")
    
    # Write modified content
    with open(nml_path, 'w') as f:
        f.write(modified_content)
    
    print(f"\nModified configuration saved to {nml_path}")
    return True


def verify_nml_modification(nml_path, expected_params):
    """
    Verify that parameters were written correctly.
    
    Args:
        nml_path (str): Path to modified glm3.nml
        expected_params (dict): {param_name: expected_value}
    
    Returns:
        bool: True if all parameters match expected values
    
    Raises:
        AssertionError: If any parameter doesn't match
    """
    pattern_template = r'{param}\s*=\s*([\d.]+(?:[eE][+-]?\d+)?)'
    
    with open(nml_path, 'r') as f:
        content = f.read()
    
    print("Verification of modified parameters:")
    for param, expected_value in expected_params.items():
        pattern = pattern_template.format(param=param)
        match = re.search(pattern, content)
        assert match, f"Parameter '{param}' not found after modification"
        
        actual_value = float(match.group(1))
        assert abs(actual_value - expected_value) < 1e-10, \
            f"{param}: expected {expected_value}, got {actual_value}"
        print(f"  ✓ {param} = {actual_value}")
    
    return True
```

### Usage Example

```python
# Define ranges (from task specification)
ranges = {
    'Kw': (0.1, 0.5),
    'coef_mix_hyp': (0.3, 0.7),
    'wind_factor': (0.7, 1.3),
    'lw_factor': (0.7, 1.3),
    'ch': (0.0005, 0.002)
}

# Propose new parameter set
new_params = {
    'Kw': 0.35,
    'coef_mix_hyp': 0.5,
    'wind_factor': 1.0,
    'lw_factor': 1.0,
    'ch': 0.001
}

# Modify the configuration
modify_nml_parameters('/root/glm3.nml', new_params, ranges)

# Verify the modification
verify_nml_modification('/root/glm3.nml', new_params)
```

## Important Notes

- **Always validate ranges before modifying**: The `modify_nml_parameters()` function enforces this.
- **Backup is automatic**: A `.backup` file is created before any modification.
- **Scientific notation is handled**: Both reading and writing support formats like `1.0e-4`.
- **Only allowed parameters**: The function will only modify the five calibration parameters listed in the task; all others remain unchanged.

Use this skill in conjunction with `glm-calibration` to iterate on parameter values based on model performance metrics.