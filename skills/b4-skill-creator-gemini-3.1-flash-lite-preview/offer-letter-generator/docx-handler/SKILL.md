---
name: docx-handler
description: Handles reading, populating, and saving .docx files using the python-docx library. Use this skill for any tasks involving template filling or modifying Word documents.
---

# DOCX Handler

Use this skill when you need to manipulate `.docx` files.

## Basic Workflow
1. Load document: `doc = Document('path/to/template.docx')`
2. Iterate paragraphs/tables and replace placeholder text.
3. Save document: `doc.save('path/to/output.docx')`

## Handling Placeholders
Use a simple text replacement for paragraphs and tables:

```python
from docx import Document

def replace_text(doc, old_text, new_text):
    for paragraph in doc.paragraphs:
        if old_text in paragraph.text:
            paragraph.text = paragraph.text.replace(old_text, new_text)
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if old_text in paragraph.text:
                        paragraph.text = paragraph.text.replace(old_text, new_text)

doc = Document('template.docx')
replace_text(doc, '{{NAME}}', 'John Doe')
doc.save('output.docx')
```

## Handling Conditional Blocks
For conditional sections (e.g., `{{IF_TAG}}...{{END_IF_TAG}}`):
1. Identify the paragraph(s) containing the opening and closing tags.
2. If condition is true: remove tags, keep content.
3. If condition is false: remove paragraph(s) containing the tags and everything between them.
