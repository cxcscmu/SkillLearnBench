---
name: glm-nml-edit
description: A skill to edit GLM's namelist file (glm3.nml) by safely updating parameter values within specific blocks.
---

# GLM Namelist Editor

## Overview
The General Lake Model (GLM) uses Fortran namelist (`.nml`) files for configuration. This skill covers how to parse and update specific parameters in these files.

## Setup
No special installation is required if using standard CLI tools like `sed` or `python` for string replacement. For more robust parsing, use a regex-based approach.

## Usage Pattern: Python (Regex)
```python
import re

def update_nml(file_path, section, parameter, value):
    with open(file_path, 'r') as f:
        content = f.read()

    # Find the section and update the parameter within it
    pattern = rf"(&{section}.*?\b{parameter}\s*=\s*)[^,\n]*"
    replacement = rf"\g<1>{value}"
    
    # Use flags=re.DOTALL to match across lines if needed, 
    # but GLM parameters are usually on one line.
    new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(new_content)
```

## Example: Bash (sed)
```bash
# Update Kw in &light section
sed -i '/&light/,/\// s/Kw *= *[0-9.]*/Kw = 0.45/' glm3.nml
```

## Considerations
- GLM parameters are case-insensitive but usually lowercase.
- Parameters are grouped into blocks (e.g., `&glm_setup`, `&light`).
- Some parameters are arrays (e.g., `the_depths = 0.0, 1.0, 2.0`). Update these carefully to maintain format.
- Always verify the change with `grep` after modification.
