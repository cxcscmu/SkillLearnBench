---
name: pdf-text-extraction
description: Extract text from PDF files using pdfminer or PyMuPDF to read titles and abstracts for classification.
---

# PDF Text Extraction Skill

## Overview
When paper filenames don't contain enough information, extract text from the first page of PDFs to get titles and abstracts for classification.

## Installation
```bash
pip install pdfminer.six  # Pure Python, reliable
pip install pymupdf       # Faster, aka fitz
pip install pypdf2        # Lightweight alternative
```

## Using pdfminer.six (Recommended for accuracy)
```python
from pdfminer.high_level import extract_text

def get_first_page_text(pdf_path, max_chars=2000):
    """Extract text from first page only for fast classification."""
    try:
        text = extract_text(pdf_path, maxpages=1)
        return text[:max_chars]
    except Exception as e:
        return ""
```

## Using PyMuPDF (Recommended for speed)
```python
import fitz  # PyMuPDF

def get_first_page_text(pdf_path, max_chars=2000):
    try:
        doc = fitz.open(pdf_path)
        text = doc[0].get_text()
        doc.close()
        return text[:max_chars]
    except Exception as e:
        return ""
```

## Extracting Title from PDF
```python
def extract_title(pdf_path):
    """Try metadata first, then text extraction."""
    try:
        doc = fitz.open(pdf_path)
        # Try PDF metadata
        meta = doc.metadata
        if meta.get('title'):
            return meta['title']
        # Fallback: first non-empty line of text
        text = doc[0].get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        return lines[0] if lines else ""
    except:
        return ""
```

## Batch Processing Pattern
```python
import os
from pathlib import Path

def classify_papers(folder, classifier_fn):
    results = {}
    for pdf_file in Path(folder).glob("*.pdf"):
        text = get_first_page_text(str(pdf_file))
        subject = classifier_fn(str(pdf_file), text)
        results[pdf_file.name] = subject
    return results
```

## Notes
- First page usually contains title + abstract - sufficient for classification
- pdfminer is more reliable but slower; PyMuPDF is faster
- Some PDFs may be scanned images (OCR needed) - rare for arxiv papers
