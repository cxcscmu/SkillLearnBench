---
name: python-docx
description: Programmatically read, modify, and create Word documents (.docx) with python-docx library
---

# Python-docx: Working with Word Documents

## Overview
The `python-docx` library allows you to create, read, and update Microsoft Word (.docx) files programmatically. It's essential for automating document generation, template filling, and Word document manipulation in Python.

## Installation
```bash
pip install python-docx
```

## Core Concepts

### Document Structure
- **Document**: Root object representing the entire .docx file
- **Paragraphs**: Text blocks in the document
- **Runs**: Individual text segments within a paragraph (can have different formatting)
- **Tables**: Structured data with rows/cells
- **Sections**: Document sections with different headers/footers

## Common Operations

### Loading and Saving Documents
```python
from docx import Document

# Open existing document
doc = Document('template.docx')

# Create new document
doc = Document()

# Save document
doc.save('output.docx')
```

### Working with Paragraphs and Text
```python
# Access all paragraphs
for para in doc.paragraphs:
    print(para.text)

# Add new paragraph
new_para = doc.add_paragraph('Text here')

# Add text with formatting
run = new_para.add_run('Bold text')
run.bold = True
```

### Finding and Replacing Text
```python
# Search through all paragraphs and runs
for para in doc.paragraphs:
    for run in para.runs:
        if '{{PLACEHOLDER}}' in run.text:
            run.text = run.text.replace('{{PLACEHOLDER}}', 'replacement')

# Note: Text can be split across multiple runs!
# A safer approach:
full_text = ''.join(run.text for run in para.runs)
if '{{PLACEHOLDER}}' in full_text:
    # Clear all runs and recreate with replacement
    for run in para.runs:
        run.text = ''
    para.text = full_text.replace('{{PLACEHOLDER}}', 'replacement')
```

### Working with Tables
```python
# Access table rows and cells
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
            # Replace text in cell
            cell.text = cell.text.replace('{{PLACEHOLDER}}', 'value')
```

### Handling Multiple Runs
The trickiest part of python-docx is that text in a paragraph can be split across multiple "runs" (especially in templates). For placeholder replacement:

```python
def replace_text_in_paragraph(para, old_text, new_text):
    """Replace text handling split runs"""
    if old_text in para.text:
        # Clear existing runs
        for run in para.runs:
            run.text = ''
        # Add new text as single run
        para.text = new_text
```

## Important Considerations

1. **Text Fragmentation**: When you open a .docx file (especially templates), the same logical text might be split across multiple `run` objects due to formatting. Always check the full paragraph text before manipulating individual runs.

2. **Preserve Formatting**: When replacing text, consider whether you want to preserve the original formatting or apply new formatting.

3. **Iterating Safely**: If modifying document structure while iterating, make copies of lists first:
   ```python
   paragraphs = list(doc.paragraphs)  # Create copy
   for para in paragraphs:
       # Safe to modify now
   ```

4. **Headers/Footers**: Accessed via `doc.sections[0].header` and `doc.sections[0].footer`

## Example: Template Filling
```python
from docx import Document

def fill_template(template_path, replacements, output_path):
    doc = Document(template_path)

    # Replace in paragraphs
    for para in doc.paragraphs:
        for key, value in replacements.items():
            if key in para.text:
                para.text = para.text.replace(key, value)

    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in replacements.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, value)

    doc.save(output_path)
```

## Debugging Tips
- Always print `para.text` (full paragraph) to see actual content vs individual `run.text`
- Check `len(para.runs)` to see if text is fragmented
- Use `doc.element.xml` to inspect underlying XML structure if needed
