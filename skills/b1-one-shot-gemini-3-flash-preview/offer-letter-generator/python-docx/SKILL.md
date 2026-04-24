---
name: python-docx
description: Manipulate Word documents (.docx) using Python, including placeholder replacement and conditional section handling.
---

# python-docx Skill

`python-docx` is a Python library for creating and updating Microsoft Word (.docx) files.

## Installation

```bash
pip install python-docx
```

## Basic Usage

### Loading and Saving
```python
from docx import Document

doc = Document('template.docx')
# ... modify doc ...
doc.save('output.docx')
```

### Placeholder Replacement
To replace placeholders like `{{NAME}}` while preserving formatting, iterate through paragraphs and their runs.

```python
def replace_placeholders(doc, data):
    for p in doc.paragraphs:
        for run in p.runs:
            for key, value in data.items():
                placeholder = f'{{{{{key}}}}}'
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, str(value))
```

### Conditional Sections
For sections like `{{IF_CONDITION}}...{{END_IF_CONDITION}}`, you can identify the start and end points and remove the content or just the markers.

```python
def handle_conditionals(doc, condition_key, keep_content):
    start_marker = f'{{{{IF_{condition_key}}}}}'
    end_marker = f'{{{{END_IF_{condition_key}}}}}'
    
    # This is a simplified approach for text-based conditionals within paragraphs
    for p in doc.paragraphs:
        if start_marker in p.text and end_marker in p.text:
            if keep_content:
                p.text = p.text.replace(start_marker, "").replace(end_marker, "")
            else:
                # Remove content between markers (regex or string find)
                import re
                p.text = re.sub(f'{re.escape(start_marker)}.*?{re.escape(end_marker)}', '', p.text)
```

Note: Complex conditionals spanning multiple paragraphs require more advanced logic iterating through the document element tree.
