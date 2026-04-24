---
name: python-docx-templating
description: A skill for replacing placeholders and handling conditional blocks in python-docx.
---

# python-docx-templating

This skill covers how to read a Word document template, replace `{{VAR}}` style placeholders with actual values, and conditionally remove or keep sections of text based on `{{IF_COND}}...{{END_IF_COND}}` logic.

## Installation

Ensure `python-docx` is installed:
```bash
pip install python-docx
```

## Basic Replacement

When replacing placeholders, be mindful that `python-docx` splits paragraph text into multiple `Run` objects. For simple documents where inline formatting (bold, italic) inside the placeholder itself doesn't matter, you can replace `paragraph.text` directly, which will clear run-level formatting but keep paragraph-level styling. If run-level formatting is critical, use a regex or custom run-merging logic.

```python
import docx

doc = docx.Document('template.docx')
context = {'NAME': 'John Doe', 'COMPANY': 'Acme Corp'}

for paragraph in doc.paragraphs:
    for key, value in context.items():
        placeholder = f"{{{{{key}}}}}"
        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, str(value))

doc.save('output.docx')
```

## Conditional Sections

To handle conditional blocks like `{{IF_RELOCATION}} ... {{END_IF_RELOCATION}}`:

```python
import re

def process_conditionals(text, condition_true):
    if condition_true:
        # Keep content, remove tags
        text = re.sub(r'\{\{IF_RELOCATION\}\}(.*?)\{\{END_IF_RELOCATION\}\}', r'\1', text, flags=re.DOTALL)
    else:
        # Remove entire block including tags
        text = re.sub(r'\{\{IF_RELOCATION\}\}.*?\{\{END_IF_RELOCATION\}\}', '', text, flags=re.DOTALL)
    return text
```
This regex approach can be applied to `paragraph.text` to correctly render the conditional.

