---
name: file-analyzer
description: Robust extraction of text from various file formats (PDF, DOCX, etc).
---
# File Analyzer Skill

This skill provides a unified interface to extract text from different file formats for further classification.

## Dependencies
- `pypdf`, `python-docx`

## Usage
```python
from pypdf import PdfReader
import docx

def get_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])
    return ""
```
