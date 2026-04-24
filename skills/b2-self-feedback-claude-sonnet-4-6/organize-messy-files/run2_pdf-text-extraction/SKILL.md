---
name: run2_pdf-text-extraction
description: Extract text from PDF files using PyPDF2 with pdfplumber fallback; optimized for title/abstract extraction for classification.
---

# PDF Text Extraction Skill (Improved)

## Overview
Extract text from PDF files for content analysis. The first 3-4 pages contain title, abstract, and introduction — sufficient for classification.

## Installation
```bash
pip install PyPDF2 pdfplumber --break-system-packages
```

## Key Insight
- PyPDF2 is faster but may miss some text
- pdfplumber handles complex layouts better
- For classification, extracting title + abstract (first 2 pages) is usually sufficient
- Always use both libraries with fallback for robustness

## Robust Extraction Function
```python
import PyPDF2
import pdfplumber

def extract_pdf_text(filepath, max_pages=4):
    """Extract text from PDF, trying PyPDF2 first, then pdfplumber fallback."""
    text = ""
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages[:max_pages]:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except:
                    pass
    except Exception:
        pass

    # If PyPDF2 didn't get much, try pdfplumber
    if len(text.strip()) < 200:
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages[:max_pages]:
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except:
                        pass
        except Exception:
            pass

    return text
```

## Notes
- Some PDFs with score=0 may need manual review — check the title from the first few lines
- arXiv PDFs generally work well with both libraries
- PDFs with equations may have garbled text but keywords like "trapped ion", "DNA" still appear
