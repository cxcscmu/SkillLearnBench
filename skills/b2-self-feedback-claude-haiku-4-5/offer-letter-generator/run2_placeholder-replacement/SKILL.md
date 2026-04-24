---
name: run2_placeholder-replacement
description: Robust pattern-based template processing with conditionals, data validation, and comprehensive placeholder replacement.
---

# Template Processing with Placeholders and Conditionals

## Overview
Process Word document templates by:
1. Handling conditional sections (keep/remove based on data)
2. Replacing all placeholders with data values
3. Validating complete replacement

## Placeholder Pattern
Use double-brace format: `{{PLACEHOLDER_NAME}}`
```python
# Build placeholder from key
placeholder = f"{{{{{key}}}}}"  # e.g., "{{CANDIDATE_FULL_NAME}}"
```

## Conditional Section Pattern

### Format
```
{{IF_CONDITION_NAME}}content here{{END_IF_CONDITION_NAME}}
```

Both markers must be within the same paragraph or cell (inline).

### Processing Logic
```python
import re

def process_conditionals(text, data):
    """
    Replace {{IF_KEY}}...{{END_IF_KEY}} sections.
    - If data[KEY] is "Yes" (case-insensitive): keep content, remove markers
    - Otherwise: remove entire section including markers
    """
    # Find all IF_* patterns
    pattern = r'\{\{IF_(\w+)\}\}(.*?)\{\{END_IF_\1\}\}'

    def replacer(match):
        key = match.group(1)
        content = match.group(2)
        condition_value = data.get(key, '').strip()

        # Keep content if value is "Yes" (case-insensitive)
        if condition_value.lower() == 'yes':
            return content  # Remove markers, keep content
        else:
            return ''  # Remove entire section

    return re.sub(pattern, replacer, text, flags=re.DOTALL)
```

## Complete Workflow

### 1. Load Data and Template
```python
import json
from docx import Document

with open('data.json') as f:
    data = json.load(f)

doc = Document('template.docx')
```

### 2. Process Conditionals
```python
# Apply to all paragraphs and table cells
for para in doc.paragraphs:
    para.text = process_conditionals(para.text, data)

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                para.text = process_conditionals(para.text, data)
```

### 3. Replace Placeholders
```python
def replace_all_placeholders(doc, data):
    """Replace all {{KEY}} placeholders with data values"""
    for key, value in data.items():
        placeholder = f"{{{{{key}}}}}"
        value_str = str(value)

        # Replace in paragraphs
        for para in doc.paragraphs:
            if placeholder in para.text:
                para.text = para.text.replace(placeholder, value_str)

        # Replace in table cells
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        if placeholder in para.text:
                            para.text = para.text.replace(placeholder, value_str)

replace_all_placeholders(doc, data)
```

### 4. Validate and Save
```python
def verify_no_placeholders(doc):
    """Check that all placeholders have been replaced"""
    remaining = []

    for para in doc.paragraphs:
        if '{{' in para.text:
            remaining.append(para.text)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if '{{' in para.text:
                        remaining.append(para.text)

    return remaining

# Verify before saving
remaining = verify_no_placeholders(doc)
if remaining:
    print(f"Warning: {len(remaining)} unreplaced placeholders found")
    for text in remaining:
        print(f"  {text}")
else:
    print("All placeholders successfully replaced")

doc.save('output.docx')
```

## Data Type Handling

### Converting to String
All values are converted to strings:
```python
value_str = str(value)
```

### Handling Missing Keys
By default, `data.get(key, '')` returns empty string if key missing.
For safer processing:
```python
def replace_with_validation(doc, data):
    for key, value in data.items():
        if not isinstance(value, (str, int, float)):
            value = str(value)
        # ... replacement logic ...
```

## Regex Considerations

### Conditional Pattern with DOTALL
Use `re.DOTALL` (or `re.S`) for patterns spanning multiple lines if content contains newlines:
```python
# Handles newlines in content
re.sub(pattern, replacer, text, flags=re.DOTALL)
```

### Case-Insensitive Comparison
For conditions:
```python
if condition_value.lower() == 'yes':
    # Matches: "Yes", "YES", "yes", etc.
```

## Robustness Checklist
- [x] Handle missing data keys gracefully
- [x] Convert all values to strings
- [x] Support conditionals with multiple variations
- [x] Verify complete replacement before save
- [x] Support both inline and nested markers within cells
- [x] Clear error messages for debugging
