---
name: run2_python-docx-basics
description: Working with Word documents (DOCX) using python-docx library with proper text replacement strategies.
---

# Python-docx for Template Processing

## Installation
```bash
pip install python-docx
```

## Document Structure
A Word document (.docx) contains:
- **Document**: Root container
- **Paragraphs**: Text blocks with formatting (font, spacing, alignment)
- **Runs**: Individual text segments with consistent formatting within a paragraph
- **Tables**: Structured data with rows and cells

## Core Operations

### Loading and Saving
```python
from docx import Document

doc = Document('input.docx')
# ... modify document ...
doc.save('output.docx')
```

### Iterating Content
```python
# All paragraphs in document
for para in doc.paragraphs:
    print(para.text)  # Complete text of paragraph

# All tables
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)  # Text in cell
```

## Text Replacement Pattern

### Simple Approach: Paragraph-level
For templates where formatting is not critical, replace at paragraph level:

```python
def replace_in_paragraphs(doc, placeholder, replacement):
    """Replace placeholder in all paragraphs"""
    for para in doc.paragraphs:
        if placeholder in para.text:
            para.text = para.text.replace(placeholder, replacement)

def replace_in_tables(doc, placeholder, replacement):
    """Replace placeholder in all table cells"""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if placeholder in para.text:
                        para.text = para.text.replace(placeholder, replacement)
```

**Note**: Assigning to `para.text` replaces all runs in the paragraph, which removes formatting but is acceptable for template documents with mostly plain text.

### Complete Document Replacement
```python
def replace_all(doc, placeholder, replacement):
    """Replace in paragraphs and tables"""
    replace_in_paragraphs(doc, placeholder, replacement)
    replace_in_tables(doc, placeholder, replacement)
```

## Accessing Nested Content

### Cells contain Paragraphs
Each table cell contains one or more paragraphs:
```python
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            # Each cell has paragraphs
            for para in cell.paragraphs:
                para.text = 'modified'
```

### Preserving Structure
When iterating to remove elements, use reverse iteration:
```python
# Remove paragraphs in reverse order to avoid index shifting
for idx in range(len(doc.paragraphs) - 1, -1, -1):
    if should_remove(doc.paragraphs[idx]):
        p = doc.paragraphs[idx]._element
        p.getparent().remove(p)
```

## Key Constraints
1. **Text-only approach**: Simple `para.text` assignment removes all run-level formatting
2. **Paragraph boundary**: Cannot modify text that spans across paragraphs naturally (it's already split in source)
3. **Conditional markers**: Must fit within single paragraph or table cell for regex to work
4. **Placeholder format**: Use consistent delimiters like `{{KEY}}` for easy identification
