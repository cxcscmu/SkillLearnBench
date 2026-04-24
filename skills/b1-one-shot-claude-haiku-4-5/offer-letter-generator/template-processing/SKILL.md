---
name: template-processing
description: Process templates with placeholder substitution and conditional sections
---

# Template Processing: Placeholders and Conditionals

## Overview
When filling document templates, you often need to:
1. Replace placeholders like `{{PLACEHOLDER}}` with actual data
2. Handle conditional sections (show/hide content based on data)
3. Clean up formatting markers

This skill covers patterns for template processing in both text and document contexts.

## Placeholder Patterns

### Basic Placeholders
```
{{CANDIDATE_FULL_NAME}}
{{POSITION}}
{{START_DATE}}
{{BASE_SALARY}}
```

### Parsing from JSON
```python
import json

with open('employee_data.json', 'r') as f:
    data = json.load(f)

# Access placeholder values
name = data['CANDIDATE_FULL_NAME']
position = data['POSITION']
```

## Conditional Section Pattern

### Template Format
```
{{IF_CONDITION_NAME}}
  Content to show if CONDITION_NAME is "Yes"
{{END_IF_CONDITION_NAME}}
```

### Processing Conditionals

```python
def process_conditional_section(text, condition_key, condition_value):
    """Remove conditional markers based on condition value"""
    start_marker = f'{{{{IF_{condition_key}}}}}'
    end_marker = f'{{{{END_IF_{condition_key}}}}}'

    # Find section
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        return text  # No conditional section found

    # Extract the content between markers
    before = text[:start_idx]
    content = text[start_idx + len(start_marker):end_idx]
    after = text[end_idx + len(end_marker):]

    if condition_value.lower() == 'yes':
        # Keep content, remove markers
        return before + content + after
    else:
        # Remove entire section
        return before + after
```

## Workflow for Template Processing

### Step 1: Load Data
```python
import json
from docx import Document

with open('employee_data.json', 'r') as f:
    data = json.load(f)

doc = Document('template.docx')
```

### Step 2: Replace Basic Placeholders
```python
def replace_placeholders(doc, data):
    """Replace all {{PLACEHOLDER}} with data values"""

    # Replace in paragraphs
    for para in doc.paragraphs:
        para_text = para.text
        for key, value in data.items():
            placeholder = f'{{{{{key}}}}}'
            para_text = para_text.replace(placeholder, str(value))

        # Update paragraph (handle text fragmentation)
        if para_text != para.text:
            for run in para.runs:
                run.text = ''
            para.text = para_text

    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell_text = cell.text
                for key, value in data.items():
                    placeholder = f'{{{{{key}}}}}'
                    cell_text = cell_text.replace(placeholder, str(value))

                if cell_text != cell.text:
                    for para in cell.paragraphs:
                        for run in para.runs:
                            run.text = ''
                        para.text = cell_text
                    cell_text = cell.text  # Reset after first cell
```

### Step 3: Handle Conditionals
```python
def process_conditionals(doc, data):
    """Process {{IF_*}}...{{END_IF_*}} sections"""

    for para in doc.paragraphs:
        para_text = para.text

        # Find all conditional markers
        import re
        pattern = r'{{\s*IF_(\w+)\s*}}(.*?){{\s*END_IF_\1\s*}}'

        def replace_conditional(match):
            condition_key = match.group(1)
            content = match.group(2)

            condition_value = data.get(condition_key, 'No')

            if condition_value == 'Yes':
                return content.strip()
            else:
                return ''

        new_text = re.sub(pattern, replace_conditional, para_text, flags=re.DOTALL)

        if new_text != para_text:
            for run in para.runs:
                run.text = ''
            para.text = new_text
```

## Important Considerations

1. **Text Fragmentation in Word**: Placeholders might be split across multiple runs. Always work at the paragraph level (`para.text`) not individual run level.

2. **Order of Operations**:
   - First handle conditionals (remove sections)
   - Then replace placeholders

3. **Multiline Content**: When using regex for conditionals, use `re.DOTALL` flag to match across newlines

4. **Data Type Conversion**: Convert all data values to strings when replacing:
   ```python
   placeholder_value = str(data[key])
   ```

5. **Preserve Formatting**: The simple approach loses formatting. For preserving formatting:
   - Replace in individual runs while checking full paragraph
   - Or use a more sophisticated run-level replacement with formatting preservation

## Complete Example
```python
import json
import re
from docx import Document

def fill_offer_letter(template_path, data_path, output_path):
    # Load data
    with open(data_path) as f:
        data = json.load(f)

    doc = Document(template_path)

    # Process all paragraphs
    for para in doc.paragraphs:
        text = para.text

        # Handle conditionals first
        pattern = r'{{\s*IF_(\w+)\s*}}(.*?){{\s*END_IF_\1\s*}}'
        def replace_cond(m):
            key = m.group(1)
            content = m.group(2)
            return content.strip() if data.get(key) == 'Yes' else ''

        text = re.sub(pattern, replace_cond, text, flags=re.DOTALL)

        # Replace placeholders
        for key, value in data.items():
            text = text.replace(f'{{{{{key}}}}}', str(value))

        # Update paragraph
        if text != para.text:
            for run in para.runs:
                run.text = ''
            para.text = text

    # Similarly for tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    text = para.text
                    pattern = r'{{\s*IF_(\w+)\s*}}(.*?){{\s*END_IF_\1\s*}}'
                    text = re.sub(pattern, replace_cond, text, flags=re.DOTALL)
                    for key, value in data.items():
                        text = text.replace(f'{{{{{key}}}}}', str(value))
                    if text != para.text:
                        for run in para.runs:
                            run.text = ''
                        para.text = text

    doc.save(output_path)
```
