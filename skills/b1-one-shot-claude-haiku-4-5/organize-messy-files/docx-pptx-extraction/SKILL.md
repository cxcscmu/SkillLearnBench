---
name: docx-pptx-extraction
description: Extract text from DOCX and PPTX files for content analysis
---

# DOCX and PPTX Text Extraction

## Overview
Extract text content from Microsoft Office files (.docx, .pptx) for subject classification.

## Installation
```bash
pip install python-docx python-pptx
```

## DOCX Extraction

```python
from docx import Document

def extract_docx_text(docx_path, max_chars=5000):
    """Extract text from DOCX files"""
    try:
        doc = Document(docx_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
            if len(text) > max_chars:
                break
        return text[:max_chars]
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
```

## PPTX Extraction

```python
from pptx import Presentation

def extract_pptx_text(pptx_path, max_chars=5000):
    """Extract text from PPTX files"""
    try:
        prs = Presentation(pptx_path)
        text = ""
        for slide_num, slide in enumerate(prs.slides):
            if slide_num >= 5:  # First 5 slides
                break
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
                    if len(text) > max_chars:
                        return text[:max_chars]
        return text[:max_chars]
    except Exception as e:
        return f"Error reading PPTX: {str(e)}"
```

## Combined Handler

```python
def extract_text_by_type(file_path):
    """Route to appropriate extraction method based on file extension"""
    ext = file_path.lower().split('.')[-1]

    if ext == 'pdf':
        return extract_pdf_text(file_path)
    elif ext == 'docx':
        return extract_docx_text(file_path)
    elif ext == 'pptx':
        return extract_pptx_text(file_path)
    else:
        return ""
```

## Best Practices
- Extract from first 3-5 pages/slides only
- Handle missing text shapes gracefully
- Use consistent character limits across all file types
