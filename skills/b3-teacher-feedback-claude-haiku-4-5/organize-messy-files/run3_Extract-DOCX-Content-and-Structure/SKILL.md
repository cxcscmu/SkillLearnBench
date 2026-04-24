---
name: Extract DOCX Content and Structure
description: Use this skill to extract text and structure from Word documents (.docx files) to determine their subject for classification into the correct folder.
---

## When to use this skill
- When you need to read content from .docx files
- Before sorting Word documents into subject folders
- When document filenames are generic or unclear

## How to extract DOCX content

### Using python-docx
```python
from docx import Document

def extract_docx_content(docx_path):
    doc = Document(docx_path)
    content = []
    
    for para in doc.paragraphs:
        if para.text.strip():
            content.append(para.text)
    
    # Also extract from tables if present
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    content.append(cell.text)
    
    return "\n".join(content)
```

### Using markitdown
```bash
python -m markitdown input.docx > output.md
```

### Key information to extract
1. **Document title/heading**: Top of document (usually styled as heading)
2. **First paragraph**: Introduces the document's main topic
3. **Section headers**: Reveal subject areas covered
4. **Keywords and technical terms**: Identify the subject domain

### Subject indicators
- Use same keyword patterns as PDF and PPTX extraction
- Pay attention to document structure and headings
- Read first page thoroughly as it typically establishes the subject

### Store extracted content
Retain the full text for subject classification analysis.