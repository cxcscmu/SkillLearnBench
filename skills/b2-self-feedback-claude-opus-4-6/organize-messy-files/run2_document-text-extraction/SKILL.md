---
name: run2_document-text-extraction
description: Extract text from PDF, PPTX, and DOCX files for content classification, with error handling and fallback strategies.
---

# Document Text Extraction (Improved)

## Libraries
- `PyPDF2` for PDF text extraction
- `python-pptx` for PowerPoint text extraction
- `python-docx` for Word document text extraction

## Installation
```bash
pip3 install PyPDF2 python-pptx python-docx --break-system-packages
```

## Key Lessons from Round 1
1. **Read enough pages**: 3 pages is usually sufficient for classification, but some papers have long introductions. Consider reading more pages for borderline cases.
2. **Error handling**: Always wrap extraction in try/except - some files may be corrupted.
3. **Empty text handling**: PyPDF2 may return empty strings for scanned PDFs. Have a fallback plan.

## PDF Extraction
```python
import PyPDF2

def extract_pdf_text(filepath, max_pages=3):
    """Extract text from first few pages of a PDF."""
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:max_pages]:
                text += page.extract_text() or ""
        return text
    except Exception:
        return ""
```

## PPTX Extraction
```python
from pptx import Presentation

def extract_pptx_text(filepath):
    """Extract all text from slides including shapes and tables."""
    try:
        prs = Presentation(filepath)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
                # Also check tables
                if shape.has_table:
                    for row in shape.table.rows:
                        for cell in row.cells:
                            text += cell.text + " "
        return text
    except Exception:
        return ""
```

## DOCX Extraction
```python
from docx import Document

def extract_docx_text(filepath):
    """Extract text from all paragraphs in a Word document."""
    try:
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""
```
