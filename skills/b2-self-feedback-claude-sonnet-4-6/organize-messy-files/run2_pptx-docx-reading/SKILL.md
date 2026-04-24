---
name: run2_pptx-docx-reading
description: Extract text from PPTX and DOCX files using python-pptx and python-docx, including tables and all shapes.
---

# PPTX and DOCX Reading Skill (Improved)

## Overview
Extract text from PowerPoint and Word documents for classification.

## Installation
```bash
pip install python-pptx python-docx --break-system-packages
```

## PPTX Extraction (All slide content)
```python
from pptx import Presentation

def extract_pptx_text(filepath):
    """Extract all text from a PPTX file including titles, bodies, notes."""
    try:
        prs = Presentation(filepath)
        text_parts = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    text_parts.append(shape.text)
                # Also handle tables in slides
                if shape.has_table:
                    for row in shape.table.rows:
                        for cell in row.cells:
                            if cell.text.strip():
                                text_parts.append(cell.text)
        return "\n".join(text_parts)
    except Exception as e:
        return f"Error: {e}"
```

## DOCX Extraction (Paragraphs + Tables)
```python
from docx import Document

def extract_docx_text(filepath):
    """Extract all text from a DOCX file including paragraphs and tables."""
    try:
        doc = Document(filepath)
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        text_parts.append(cell.text)
        return "\n".join(text_parts)
    except Exception as e:
        return f"Error: {e}"
```

## Notes
- DAMOP.pptx is a DAMOP (Division of Atomic Molecular and Optical Physics) conference presentation - likely trapped ion / quantum computing
- python-pptx reads all shapes; python-docx reads paragraphs and tables
- These don't modify files, just read content
