---
name: run2_pdf-extraction
description: Robust PDF text extraction with fallback strategies and error handling for academic papers and documents
---

# PDF Text Extraction Skill (Improved)

## Overview
Extract text from PDF files with improved robustness, handling corrupt PDFs gracefully.
Multiple extraction strategies ensure maximum content recovery.

## Installation
```bash
pip install pdfplumber pypdf pymupdf -q
```

## Usage Examples

### Primary Strategy: pdfplumber (Most Reliable)
```python
import pdfplumber
import PyPDF2

def extract_pdf_content_robust(pdf_path, max_pages=5):
    """
    Extract text from PDF with fallback strategies.
    Tries pdfplumber first, then falls back to PyPDF2.
    """
    text = ""

    # Strategy 1: pdfplumber (best for modern PDFs)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages[:max_pages]):
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
        if len(text.strip()) > 100:  # If we got substantial text
            return text
    except Exception as e:
        pass  # Try fallback

    # Strategy 2: PyPDF2 (fallback for problematic PDFs)
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages[:max_pages]:
                text += page.extract_text() + " "
        if len(text.strip()) > 100:
            return text
    except Exception as e:
        pass

    return text or ""
```

### Optimized Extraction for Academic Papers
```python
def extract_paper_metadata(pdf_path, max_pages=3):
    """
    Extract key content from academic papers:
    - Title (usually on first page)
    - Abstract (usually first 3 pages)
    - Keywords (sometimes in abstract area)
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract first 3 pages which contain title and abstract
            text = ""
            for page in pdf.pages[:max_pages]:
                text += page.extract_text() or ""
            return text
    except:
        return ""
```

## Key Improvements
- **Dual extraction strategy**: pdfplumber + PyPDF2 fallback
- **Robustness**: Handles corrupt/damaged PDFs gracefully
- **Academic focus**: Optimized for extracting paper abstracts and titles
- **Efficiency**: Returns early if sufficient text extracted
- **Error isolation**: Failures in one method don't prevent trying alternatives

## Best Practices
- For academic papers, first 3-5 pages contain most essential information
- Title and abstract are usually in first 2 pages
- Some PDFs are scanned images - these need OCR (pymupdf with OCR)
- Check text length to verify successful extraction
- Handle encoding issues gracefully
