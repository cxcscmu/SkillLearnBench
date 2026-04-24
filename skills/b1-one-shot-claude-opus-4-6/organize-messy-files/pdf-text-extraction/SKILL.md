---
name: pdf-text-extraction
description: Extract text from PDF files using Python libraries (PyPDF2, pdfplumber) for content analysis and classification.
---

# PDF Text Extraction

## Libraries
- **PyPDF2**: Fast, good for simple text extraction
- **pdfplumber**: Better for complex layouts, tables

## Usage Pattern

```python
import PyPDF2

def extract_pdf_text(filepath, max_pages=3):
    """Extract text from first few pages of a PDF for classification."""
    text = ""
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages[:max_pages]):
                text += page.extract_text() or ""
    except Exception:
        pass
    return text
```

## Tips
- Reading only the first 2-3 pages is usually sufficient for topic classification
- Some PDFs have no extractable text (scanned images) - fallback to filename
- Always wrap in try/except as some PDFs may be corrupted
