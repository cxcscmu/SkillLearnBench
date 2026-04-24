---
name: glm-config-management
description: Managing and modifying GLM configuration files (glm3.nml) for calibration. Use this skill whenever you need to safely update GLM parameters, preserve non-calibration settings, validate configuration syntax, or manage multiple parameter sets. Essential for iterative calibration workflows where parameters must change reliably without corrupting the config.
---

# GLM Configuration File Management

## Configuration File Format

GLM uses Fortran namelist format (`.nml` files). Structure:
```
&section_name
  parameter1 = value1
  parameter2 = value2
/
```

Key rules:
- Sections delimited by `&section_name` (start) and `/` (end)
- Each parameter on its own line
- Values must match Fortran types (reals for decimals, integers for ints, strings in quotes, logicals .true./.false.)
- Commas optional but allow consistency
- Comments not allowed in namelist sections

## Calibration-Safe Parameter Updates

### Parameters You CAN Modify

In `&light`:
- `Kw`: Real number, currently ~0.3

In `&mixing`:
- `coef_mix_hyp`: Real number, currently ~0.5

In `&meteorology`:
- `wind_factor`: Real number, currently ~1.0
- `lw_factor`: Real number, currently ~1.0
- `ch`: Real number, currently ~0.0013

### Parameters You MUST NOT MODIFY

**&meteorology:**
- `sw_factor` (solar shortwave multiplier)
- `cd` (drag coefficient)
- `ce` (evaporation coefficient)

**&init_profiles:**
- `the_depths` (initial depth levels)
- `the_temps` (initial temperatures)
- `the_sals` (initial salinities)

**All other sections:**
- Time period, morphometry, inflows, outflows, etc.

## Safe Update Procedure

### Python Method (Recommended)

```python
import re

def update_glm_parameter(nml_file, section, param, value):
    """
    Update a single parameter in GLM config, preserving all else.

    Args:
        nml_file: Path to glm3.nml
        section: Section name (e.g., 'light', 'mixing', 'meteorology')
        param: Parameter name (e.g., 'Kw', 'wind_factor')
        value: New value (will be formatted appropriately)
    """
    with open(nml_file, 'r') as f:
        content = f.read()

    # Build regex pattern for the parameter line
    # Matches: param = value (with possible whitespace, commas)
    pattern = rf'({param}\s*=\s*)[-+]?\d*\.?\d+([eE][-+]?\d+)?'

    # Format value
    if isinstance(value, float):
        replacement = rf'\g<1>{value}'
    else:
        replacement = rf'\g<1>{value}'

    # Replace only first occurrence (assumes one per section)
    content_new = re.sub(pattern, replacement, content, count=1)

    # Verify replacement happened
    if content == content_new:
        raise ValueError(f"Parameter {param} not found in &{section}")

    # Write back
    with open(nml_file, 'w') as f:
        f.write(content_new)

    print(f"Updated {section}.{param} to {value}")

# Usage:
update_glm_parameter('/root/glm3.nml', 'light', 'Kw', 0.35)
update_glm_parameter('/root/glm3.nml', 'mixing', 'coef_mix_hyp', 0.45)
```

### Bash Method (Using sed)

```bash
# Update Kw in &light section
sed -i 's/Kw = [0-9.e]*/Kw = 0.35/' /root/glm3.nml

# Verify update
grep -A 5 '&light' /root/glm3.nml | grep Kw
```

**Warning**: Bash sed is fragile with Fortran format. Use Python for safety.

## Validation Procedures

### Syntax Check (Python)
```python
import f90wrap  # or similar parser
# Can validate Fortran namelist format
# OR simply run: glm --help (if supported)
```

### Functional Check
```bash
cd /root
glm  # Will fail with clear error if config is invalid
# If GLM runs without error, config is OK
```

### Diff Before/After
```bash
diff -u glm3.nml.backup glm3.nml
```

## Parameter Ranges and Defaults

| Parameter | Section | Min | Default | Max | Type |
|-----------|---------|-----|---------|-----|------|
| Kw | light | 0.1 | 0.3 | 0.5 | real |
| coef_mix_hyp | mixing | 0.3 | 0.5 | 0.7 | real |
| wind_factor | meteorology | 0.7 | 1.0 | 1.3 | real |
| lw_factor | meteorology | 0.7 | 1.0 | 1.3 | real |
| ch | meteorology | 0.0005 | 0.0013 | 0.002 | real |
| sw_factor | meteorology | - | 0.95 | - | (locked) |
| cd | meteorology | - | 0.0013 | - | (locked) |
| ce | meteorology | - | 0.0013 | - | (locked) |

## Backup Strategy

Before starting calibration:
```bash
cp /root/glm3.nml /root/glm3.nml.backup
```

If config becomes corrupted, restore:
```bash
cp /root/glm3.nml.backup /root/glm3.nml
```

## Multi-Iteration Record

For tracking iterations, use a log:
```json
{
  "iteration": 1,
  "parameters": {
    "Kw": 0.30,
    "coef_mix_hyp": 0.50,
    "wind_factor": 1.0,
    "lw_factor": 1.0,
    "ch": 0.0013
  },
  "rmse": {
    "overall": 1.82,
    "annual_deep": 1.90,
    "summer_deep": 1.95
  },
  "timestamp": "2024-03-23T10:30:00Z"
}
```

This allows retracing steps if needed.
