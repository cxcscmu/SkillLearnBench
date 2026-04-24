[SKILL]
---
name: robust_text_extraction
description: Extracts text from PDFs, PPTX, DOCX, and other documents robustly using CLI tools like pdftotext and markitdown. Includes proper exception handling, timeouts, and fallbacks to ensure the extraction loop does not fail on complex encodings or shapes.
---

```python
import subprocess
import os

def extract_text_robustly(file_path, max_length=50000):
    """
    Robust text extraction handling various formats gracefully.
    Uses pdftotext for PDFs and markitdown for PPTX/DOCX.
    Returns the extracted text, capped at max_length to save memory during classification.
    """
    ext = file