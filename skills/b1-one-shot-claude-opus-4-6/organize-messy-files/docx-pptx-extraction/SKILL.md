---
name: docx-pptx-extraction
description: Extract text from DOCX and PPTX files using python-docx and python-pptx for content analysis.
---

# DOCX and PPTX Text Extraction

## DOCX Extraction

```python
from docx import Document

def extract_docx_text(filepath, max_paragraphs=50):
    doc = Document(filepath)
    text = "\n".join(p.text for p in doc.paragraphs[:max_paragraphs])
    return text
```

## PPTX Extraction

```python
from pptx import Presentation

def extract_pptx_text(filepath, max_slides=5):
    prs = Presentation(filepath)
    text = ""
    for i, slide in enumerate(prs.slides[:max_slides]):
        for shape in slide.shapes:
            if shape.has_text_frame:
                text += shape.text_frame.text + "\n"
    return text
```

## Tips
- DOCX paragraphs include headings and body text
- PPTX text is in shapes within slides
- Always wrap in try/except for robustness
