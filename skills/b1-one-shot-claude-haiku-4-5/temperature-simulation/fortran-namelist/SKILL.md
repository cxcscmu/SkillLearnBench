---
name: fortran-namelist
description: Reading and modifying Fortran namelist configuration files for scientific models
---

# Fortran Namelist Skill

## Overview
Fortran namelists are human-readable configuration files used by many scientific models. They use `&section` syntax and key=value pairs. Parsing requires careful handling of Fortran syntax quirks.

## File Format

```fortran
&section_name
   parameter1 = value1
   parameter2 = value2, value3, value4
   array_param = 1, 2, 3, 4, 5
/
```

Key features:
- Sections enclosed with `&name` and `/`
- Each section ends with `/`
- Values can be scalars or comma-separated arrays
- Comments may appear (starting with `!`)
- Spaces and newlines are flexible

## Reading Namelists

### Using f90nml Library (Recommended)

```python
import f90nml

# Read entire namelist
nml = f90nml.read('/path/to/config.nml')

# Access values
kw = nml['light']['Kw']
coef_mix = nml['mixing']['coef_mix_hyp']

# Modify values
nml['light']['Kw'] = 0.35
nml['mixing']['wind_factor'] = 1.1

# Write back
nml.write('/path/to/config.nml', force=True)
```

### Installation
```bash
pip install f90nml
```

### Manual Parsing with Regex

For simple changes without additional dependencies:

```python
import re

def read_nml_parameter(nml_file, section, param):
    """Extract single parameter value from namelist"""
    with open(nml_file, 'r') as f:
        content = f.read()

    # Pattern: find section, then parameter
    pattern = (r'&' + section + r'.*?' +
               r'(\s+' + param + r'\s*=\s*)' +
               r'([^,\n/]+)')
    match = re.search(pattern, content, re.DOTALL)

    if match:
        value_str = match.group(2).strip()
        try:
            return float(value_str)
        except ValueError:
            return value_str
    return None

def update_nml_parameter(nml_file, section, param, value):
    """Update a parameter in namelist"""
    with open(nml_file, 'r') as f:
        content = f.read()

    # Pattern to find and replace parameter in section
    pattern = (r'(&' + section + r'.*?)' +
               r'(\s+' + param + r'\s*=\s*)' +
               r'([^,\n/]+)')
    replacement = r'\g<1>\g<2>' + str(value)

    new_content = re.sub(pattern, replacement, content,
                        count=1, flags=re.DOTALL)

    with open(nml_file, 'w') as f:
        f.write(new_content)
```

## Working with Arrays

Fortran namelists support array values:

```fortran
&init_profiles
   the_depths = 0, 1, 2, 3, 4, 5
   the_temps = 5.1, 5.1, 5.0, 4.9, 4.8, 4.7
/
```

### Reading Arrays
```python
import f90nml

nml = f90nml.read('glm3.nml')
depths = nml['init_profiles']['the_depths']  # List
temps = nml['init_profiles']['the_temps']    # List

print(depths[0])  # 0
print(temps[5])   # 4.7
```

### Modifying Arrays
Arrays should not be modified for this task, but if needed:

```python
# Only modify if changing array values entirely
nml['init_profiles']['the_depths'] = [0, 1, 2, 3, 4, 5, 6]
nml['init_profiles']['the_temps'] = [5.1, 5.1, 5.0, 4.9, 4.8, 4.7, 4.6]
```

## Best Practices

1. **Always use f90nml** when available—it handles quirks properly
2. **Make backup** before modifying: `cp glm3.nml glm3.nml.bak`
3. **Validate changes** by reading back after write
4. **Whitespace preservation**: f90nml maintains formatting
5. **Section case**: Fortran is case-insensitive for sections/params
6. **Comments**: f90nml preserves comments during read/write

## Validation Example

```python
import f90nml

# Read original
nml = f90nml.read('glm3.nml')
print(f"Original Kw: {nml['light']['Kw']}")

# Modify
nml['light']['Kw'] = 0.35
nml.write('glm3.nml', force=True)

# Verify change persisted
nml2 = f90nml.read('glm3.nml')
assert nml2['light']['Kw'] == 0.35
print("Verification passed!")
```

## Common Issues

1. **Array syntax**: Use `[...]` in Python, Fortran has `=` with commas
2. **Type mismatch**: Ensure values match expected types (int vs float)
3. **Spacing**: f90nml handles this; manual regex may fail on unexpected spacing
4. **Case sensitivity**: Parameter names are case-insensitive in Fortran
