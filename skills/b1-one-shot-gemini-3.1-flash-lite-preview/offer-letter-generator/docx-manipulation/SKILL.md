---
name: docx-manipulation
description: Manipulate Word documents using python-docx, including text replacement and handling conditional sections.
---

# python-docx Skill

Use `python-docx` to read, modify, and save .docx files.

## Replacing Placeholders
Iterate through paragraphs and runs to find and replace placeholders like `{{KEY}}`.

```python
from docx import Document

def replace_text(doc, replacements):
    for paragraph in doc.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)
    # Also check tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for key, value in replacements.items():
                        if key in paragraph.text:
                            paragraph.text = paragraph.text.replace(key, value)
    return doc
```

## Handling Conditional Sections
For sections like `{{IF_CONDITION}}...{{END_IF_CONDITION}}`, identify the range of paragraphs and remove/retain based on the condition.
