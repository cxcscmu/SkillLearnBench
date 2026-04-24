---
name: run2_robust_text_extraction
description: Robustly extracts text from various document formats with multiple fallback options.
---

# Robust Text Extraction Skill

Extract text from PDF, DOCX, and PPTX even when specialized tools are missing.

## PDF Extraction
Primary: `pdftotext -l 5 <file> -` (extracts first 5 pages).
Fallback: `strings <file> | head -n 100` (last resort to find metadata/titles).

## DOCX Extraction
Primary: `pandoc <file> -t plain`.
Fallback (Python):
```python
import zipfile, xml.etree.ElementTree as ET
def get_docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        return ' '.join(node.text for node in tree.iter() if node.text)
```

## PPTX Extraction
Primary: `python3 -m markitdown <file>`.
Fallback (Python):
```python
import zipfile, xml.etree.ElementTree as ET
def get_pptx_text(path):
    text = []
    with zipfile.ZipFile(path) as z:
        for f in sorted(z.namelist()):
            if f.startswith('ppt/slides/slide'):
                xml_content = z.read(f)
                tree = ET.fromstring(xml_content)
                text.append(' '.join(node.text for node in tree.iter() if node.text))
    return ' '.join(text)
```
