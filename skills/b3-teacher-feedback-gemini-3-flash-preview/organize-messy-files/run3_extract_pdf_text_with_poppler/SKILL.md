---
name: extract_pdf_text_with_poppler
description: Extracts text from PDF files using the `pdftotext` command-line utility with the `-layout` flag to preserve multi-column formatting, which is essential for accurately parsing scientific papers.
---

```python
import subprocess
import shutil

def extract_pdf_text(file_path):
    """
    Extracts text from a PDF file using poppler-utils' pdftotext.
    Uses the -layout flag to handle multi-column layouts in scientific papers.
    """
    if not shutil.which("pdftotext"):
        # Fallback check for common tool availability
        return None

    try:
        # -layout maintains the visual arrangement of the text
        # -nopgbrk removes page breaks for a continuous stream
        result = subprocess.run(
            ["pdftotext", "-layout", "-nopgbrk", "-q", file_path, "-"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None
```