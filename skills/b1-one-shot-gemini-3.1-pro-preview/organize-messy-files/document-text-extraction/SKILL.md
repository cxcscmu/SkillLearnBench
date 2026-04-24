---
name: document-text-extraction
description: Extracts text from PDF, DOCX, and PPTX files using Python.
---

# Document Text Extraction

Use libraries like `PyMuPDF` (fitz), `python-docx`, and `python-pptx` to extract text from documents.

## Installation
```bash
pip install PyMuPDF python-docx python-pptx
```

## Python Code Examples

### PDF Extraction
```python
import fitz

def extract_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    # Just read the first few pages to save time/memory for classification
    for page in doc[:3]:
        text += page.get_text()
    return text
```

### DOCX Extraction
```python
from docx import Document

def extract_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs[:50]])
```

### PPTX Extraction
```python
from pptx import Presentation

def extract_pptx(file_path):
    prs = Presentation(file_path)
    text = ""
    for slide in prs.slides[:5]:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text
```
