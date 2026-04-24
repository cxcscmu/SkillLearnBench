---
name: run2_file-text-extraction
description: Robustly extracts text from PDF, DOCX, and PPTX files in Python using PyPDF2, python-docx, and python-pptx, suitable for document classification workflows.
---

# Robust File Text Extraction Skill

## Description
When classifying a large number of documents (PDFs, PPTXs, DOCXs), extracting a sample of text (e.g., the first few pages) is sufficient and highly performant. This skill handles text extraction robustly, catching errors to avoid failing the entire batch.

## Prerequisites
Install required Python packages:
```bash
pip install PyPDF2 python-docx python-pptx
```

## Python Implementation
```python
import os
from PyPDF2 import PdfReader
import docx
from pptx import Presentation

def extract_text_for_classification(file_path, pdf_pages=3):
    """
    Extracts text from a file based on its extension.
    Returns lowercase text to simplify keyword matching.
    """
    ext = file_path.lower().split('.')[-1]
    text = ""
    
    try:
        if ext == "pdf":
            reader = PdfReader(file_path)
            for i in range(min(pdf_pages, len(reader.pages))):
                page_text = reader.pages[i].extract_text()
                if page_text:
                    text += page_text + " "
        
        elif ext == "docx":
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
                
        elif ext == "pptx":
            prs = Presentation(file_path)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + " "
        else:
            print(f"Warning: Unsupported file type '{ext}' for file {file_path}")
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return text.lower()
```
