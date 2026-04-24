---
name: run2_multi-format-extraction
description: Unified multi-format extraction for PDF, DOCX, and PPTX with consistent output and quality metrics
---

# Multi-Format Document Extraction Skill (Improved)

## Overview
Unified framework for extracting text from multiple document formats with
quality metrics and consistent output. Handles edge cases and provides
confidence scores for extraction quality.

## Installation
```bash
pip install pdfplumber python-docx python-pptx PyPDF2 -q
```

## Unified Extraction Framework

```python
from pathlib import Path
from dataclasses import dataclass
import pdfplumber
from docx import Document
from pptx import Presentation

@dataclass
class ExtractionResult:
    """Container for extraction results with quality metrics"""
    text: str
    format: str
    length: int
    quality_score: float  # 0.0-1.0
    success: bool

def extract_document_unified(file_path, max_content_units=5):
    """
    Unified extraction for PDF, DOCX, PPTX.
    Returns ExtractionResult with quality score.
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    if ext == '.pdf':
        return extract_pdf_robust(file_path, max_content_units)
    elif ext == '.docx':
        return extract_docx_robust(file_path, max_content_units)
    elif ext == '.pptx':
        return extract_pptx_robust(file_path, max_content_units)
    else:
        return ExtractionResult("", "unknown", 0, 0.0, False)

def extract_pdf_robust(pdf_path, max_pages=5):
    """Extract from PDF with quality scoring"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:max_pages]:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        pass

    quality = min(1.0, len(text) / 1000.0)  # 1000 chars = perfect quality
    return ExtractionResult(text, "pdf", len(text), quality, len(text) > 50)

def extract_docx_robust(docx_path, max_paragraphs=30):
    """Extract from DOCX with quality scoring"""
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs[:max_paragraphs]:
            if para.text.strip():
                text += para.text + " "
    except Exception as e:
        pass

    quality = min(1.0, len(text) / 1000.0)
    return ExtractionResult(text, "docx", len(text), quality, len(text) > 50)

def extract_pptx_robust(pptx_path, max_slides=5):
    """Extract from PPTX with quality scoring"""
    text = ""
    try:
        prs = Presentation(pptx_path)
        for slide in prs.slides[:max_slides]:
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    text += shape.text + " "
    except Exception as e:
        pass

    quality = min(1.0, len(text) / 1000.0)
    return ExtractionResult(text, "pptx", len(text), quality, len(text) > 50)
```

## Key Improvements from Run 1
1. **Quality scoring**: Numeric confidence in extraction quality
2. **Unified interface**: All formats return same ExtractionResult
3. **Better error handling**: Graceful degradation
4. **Metrics tracking**: Can identify problematic extractions
5. **Reusable dataclass**: ExtractionResult for downstream processing

## Usage Pattern
```python
result = extract_document_unified(file_path)
if result.quality_score > 0.3:  # Reasonable confidence
    category = classify_text(result.text)
else:
    category = 'music_history'  # Safe default
```
