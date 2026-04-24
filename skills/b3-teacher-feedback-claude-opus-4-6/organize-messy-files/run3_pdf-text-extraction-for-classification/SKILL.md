---
name: pdf-text-extraction-for-classification
description: How to extract text from PDF files for content-based classification. Use this when you need to read PDF content to determine what subject/topic a paper belongs to. Covers both text-based and scanned PDFs.
---

## PDF Text Extraction for Classification

### Primary Method: PyMuPDF (fitz)

PyMuPDF is the most reliable library for extracting text from PDFs. Install with `pip install PyMuPDF`.

```python
import fitz  # PyMuPDF

def extract_text_from_pdf(filepath, max_pages=20):
    """Extract text from a PDF, reading up to max_pages pages."""
    text = ""
    try:
        doc = fitz.open(filepath)
        num_pages = min(len(doc), max_pages)
        for page_num in range(num_pages):
            page = doc[page_num]
            page_text = page.get_text()
            text += page_text + "\n"
        doc.close()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return text
```

### Key Details

- **Always read at least 15-20 pages** — some papers have long introductions and the key subject matter doesn't appear until later pages. Reading only 3-5 pages is NOT enough.
- **Extract ALL available text** — for short papers (< 20 pages), read the entire document.
- **Fallback for empty text** — if `get_text()` returns empty or very short strings (< 50 chars total), the PDF may be scanned/image-based. In that case, try OCR or fall back to filename analysis.

### Fallback: pdfminer

```python
from pdfminer.high_level import extract_text

def extract_text_pdfminer(filepath):
    try:
        return extract_text(filepath)
    except Exception:
        return ""
```

### Fallback: OCR with pdf2image + pytesseract

For scanned PDFs where text extraction returns nothing:

```python
from pdf2image import convert_from_path
import pytesseract

def ocr_pdf(filepath, max_pages=5):
    text = ""
    try:
        images = convert_from_path(filepath, last_page=max_pages)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
    except Exception:
        pass
    return text
```

### Reading PPTX and DOCX files

```python
from pptx import Presentation
import docx

def extract_text_from_pptx(filepath):
    text = ""
    try:
        prs = Presentation(filepath)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
    except Exception:
        pass
    return text

def extract_text_from_docx(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception:
        pass
    return text
```