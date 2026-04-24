---
name: pdf-text-extraction
description: Extract text content from PDF files for analysis and classification
---

# PDF Text Extraction

## Overview
Extract text content from PDF files to analyze their content and classify them by subject.

## Installation
```bash
pip install pdfplumber PyPDF2
```

## Usage Examples

### Using pdfplumber (Recommended)
```python
import pdfplumber

def extract_pdf_text(pdf_path, max_chars=5000):
    """Extract text from PDF with character limit for efficiency"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            # Read first few pages to get representative content
            for page_num in range(min(3, len(pdf.pages))):
                text += pdf.pages[page_num].extract_text() or ""
                if len(text) > max_chars:
                    break
            return text[:max_chars]
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
```

### Using PyPDF2 (Fallback)
```python
from PyPDF2 import PdfReader

def extract_pdf_text_pypdf(pdf_path):
    """Alternative PDF text extraction"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages[:3]:  # First 3 pages
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error: {str(e)}"
```

## Best Practices
- Extract from first 2-3 pages only (faster, usually contains abstracts/titles)
- Handle errors gracefully for corrupted PDFs
- Cache extracted text to avoid re-processing
- Use reasonable character limits (3000-5000 chars) for classification
