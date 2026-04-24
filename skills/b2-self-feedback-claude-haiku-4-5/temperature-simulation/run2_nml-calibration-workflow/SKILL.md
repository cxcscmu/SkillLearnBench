---
name: run2_nml-calibration-workflow
description: Complete NML-based GLM calibration workflow with validation and verification
---

# Complete NML Calibration Workflow

## Overview
End-to-end process for calibrating GLM parameters via Fortran namelist modifications, with proper validation and quality assurance.

## Workflow Steps

### Step 1: Load Current Configuration

```python
import f90nml

nml = f90nml.read('/root/glm3.nml')

# Display all calibration parameters
calibration_params = {
    'Kw': ('light', nml['light']['Kw']),
    'coef_mix_hyp': ('mixing', nml['mixing']['coef_mix_hyp']),
    'wind_factor': ('meteorology', nml['meteorology']['wind_factor']),
    'lw_factor': ('meteorology', nml['meteorology']['lw_factor']),
    'ch': ('meteorology', nml['meteorology']['ch'])
}

print("Current calibration parameters:")
for param, (section, value) in calibration_params.items():
    print(f"  {param:20s} = {value}")
```

### Step 2: Validate Current Parameters

```python
def validate_nml_parameters(nml):
    """Ensure current parameters are within published ranges"""

    ranges = {
        'Kw': (0.1, 0.5),
        'coef_mix_hyp': (0.3, 0.7),
        'wind_factor': (0.7, 1.3),
        'lw_factor': (0.7, 1.3),
        'ch': (0.0005, 0.002)
    }

    locations = {
        'Kw': ('light', 'Kw'),
        'coef_mix_hyp': ('mixing', 'coef_mix_hyp'),
        'wind_factor': ('meteorology', 'wind_factor'),
        'lw_factor': ('meteorology', 'lw_factor'),
        'ch': ('meteorology', 'ch')
    }

    errors = []
    for param, (min_val, max_val) in ranges.items():
        section, key = locations[param]
        current = float(nml[section][key])

        if not (min_val <= current <= max_val):
            errors.append(f"{param}={current} outside [{min_val}, {max_val}]")

    if errors:
        raise ValueError("Invalid parameters: " + "; ".join(errors))
    else:
        print("✓ All parameters within published ranges")
        return True
```

### Step 3: Verify Unchanged Parameters

```python
def verify_protected_parameters(nml):
    """Confirm that parameters we're not allowed to change haven't been modified"""

    protected = {
        'sw_factor': ('meteorology', 0.95),
        'cd': ('meteorology', 0.0013),
        'ce': ('meteorology', 0.0013)
    }

    for param, (section, expected_val) in protected.items():
        actual_val = float(nml[section][param])
        if actual_val != expected_val:
            print(f"WARNING: {param} was modified to {actual_val} (expected {expected_val})")
            return False

    print("✓ Protected parameters unchanged")
    return True

# Also check initialization profile
init_depths = nml['init_profiles']['the_depths']
if init_depths != [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
    print("WARNING: Initial depths modified!")
```

### Step 4: Update Parameters

```python
def update_nml_parameters(nml_file, param_dict):
    """
    Safely update NML parameters.

    param_dict: {'param_name': new_value, ...}
    """

    nml = f90nml.read(nml_file)

    # Map parameter names to (section, nml_key)
    param_location = {
        'Kw': ('light', 'Kw'),
        'coef_mix_hyp': ('mixing', 'coef_mix_hyp'),
        'wind_factor': ('meteorology', 'wind_factor'),
        'lw_factor': ('meteorology', 'lw_factor'),
        'ch': ('meteorology', 'ch')
    }

    # Validate ranges
    ranges = {
        'Kw': (0.1, 0.5),
        'coef_mix_hyp': (0.3, 0.7),
        'wind_factor': (0.7, 1.3),
        'lw_factor': (0.7, 1.3),
        'ch': (0.0005, 0.002)
    }

    for param, new_value in param_dict.items():
        section, key = param_location[param]
        min_val, max_val = ranges[param]

        if not (min_val <= new_value <= max_val):
            raise ValueError(f"{param}={new_value} outside [{min_val}, {max_val}]")

        nml[section][key] = new_value

    # Write back
    nml.write(nml_file, force=True)

    print("✓ Parameters updated")
    return nml

# Usage:
# update_nml_parameters('/root/glm3.nml', {
#     'Kw': 0.15,
#     'coef_mix_hyp': 0.5,
#     'wind_factor': 0.9
# })
```

### Step 5: Run GLM

```python
import subprocess

def run_glm_simulation():
    """Execute GLM from /root directory"""

    print("Running GLM simulation...")
    result = subprocess.run(
        ['glm'],
        cwd='/root',
        capture_output=True,
        text=True,
        timeout=600  # 10 minute timeout
    )

    if result.returncode != 0:
        print(f"ERROR: GLM failed")
        print(f"Stdout: {result.stdout[:500]}")
        print(f"Stderr: {result.stderr[:500]}")
        return False

    print("✓ GLM completed successfully")
    return True
```

### Step 6: Evaluate Results

```python
def evaluate_simulation():
    """Compute RMSE metrics and check thresholds"""

    from glm_calibration import compute_metrics, THRESHOLDS

    print("Evaluating simulation against observations...")
    metrics = compute_metrics()

    print("\nResults:")
    all_pass = True
    for metric_name, threshold in THRESHOLDS.items():
        value = metrics[metric_name]
        status = '✓' if value < threshold else '✗'
        print(f"  {metric_name:20s}: {value:6.3f} (threshold: {threshold}) {status}")
        if value >= threshold:
            all_pass = False

    return metrics, all_pass
```

### Step 7: Save Results

```python
import json

def save_final_metrics(metrics):
    """Save metrics to JSON for verification"""

    output = {
        'overall_rmse': metrics['overall_rmse'],
        'annual_deep_rmse': metrics['annual_deep_rmse'],
        'summer_deep_rmse': metrics['summer_deep_rmse'],
        'overall_n_pairs': metrics['overall_n_pairs'],
        'annual_deep_n_pairs': metrics['annual_deep_n_pairs'],
        'summer_deep_n_pairs': metrics['summer_deep_n_pairs']
    }

    with open('/root/metrics.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✓ Metrics saved to /root/metrics.json")
    return output
```

## Complete Workflow Function

```python
def full_calibration_cycle(param_updates):
    """Complete calibration workflow for one parameter set"""

    print("="*70)
    print("GLM CALIBRATION CYCLE")
    print("="*70)

    # Load and validate
    nml = f90nml.read('/root/glm3.nml')
    validate_nml_parameters(nml)
    verify_protected_parameters(nml)

    # Update parameters
    print(f"\nUpdating parameters: {param_updates}")
    nml = update_nml_parameters('/root/glm3.nml', param_updates)

    # Run simulation
    if not run_glm_simulation():
        return None

    # Evaluate
    metrics, all_pass = evaluate_simulation()

    # Save
    save_final_metrics(metrics)

    return metrics, all_pass

# Usage:
# metrics, success = full_calibration_cycle({
#     'Kw': 0.2,
#     'coef_mix_hyp': 0.5,
#     'wind_factor': 1.0,
#     'lw_factor': 0.9,
#     'ch': 0.0016
# })
```

## Pre-Execution Checklist

Before committing parameters:
- [ ] All 5 calibration parameters are defined
- [ ] All parameters within published ranges
- [ ] Protected parameters unchanged (`sw_factor`, `cd`, `ce`)
- [ ] Initialization profile unchanged
- [ ] Force data files exist and accessible
- [ ] Output directory exists and is writable

## Post-Execution Verification

After optimization:
- [ ] GLM ran without errors
- [ ] `/root/output/output.nc` generated and contains data
- [ ] Metrics.json has correct format with all 6 fields
- [ ] All three RMSE metrics satisfy thresholds
- [ ] Parameter file contains exact values used
- [ ] No other files were modified

## Quality Assurance

```python
def final_verification():
    """Final checks before submission"""

    import os

    checks = []

    # Check file existence
    checks.append(('output.nc exists', os.path.exists('/root/output/output.nc')))
    checks.append(('metrics.json exists', os.path.exists('/root/metrics.json')))
    checks.append(('glm3.nml exists', os.path.exists('/root/glm3.nml')))

    # Check NML parameters
    nml = f90nml.read('/root/glm3.nml')
    checks.append(('Kw in range', 0.1 <= float(nml['light']['Kw']) <= 0.5))
    checks.append(('Protected sw_factor', float(nml['meteorology']['sw_factor']) == 0.95))

    # Check metrics
    import json
    with open('/root/metrics.json') as f:
        metrics = json.load(f)

    from glm_calibration import THRESHOLDS
    checks.append(('overall_rmse passes', metrics['overall_rmse'] < THRESHOLDS['overall_rmse']))
    checks.append(('annual_deep passes', metrics['annual_deep_rmse'] < THRESHOLDS['annual_deep_rmse']))
    checks.append(('summer_deep passes', metrics['summer_deep_rmse'] < THRESHOLDS['summer_deep_rmse']))

    print("\nFinal Verification:")
    all_pass = True
    for check_name, result in checks:
        status = '✓' if result else '✗'
        print(f"  {status} {check_name}")
        if not result:
            all_pass = False

    return all_pass
```
