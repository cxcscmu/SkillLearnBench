---
name: run2_docx_processing
description: A robust skill for template processing in DOCX files, handling placeholders and complex conditional blocks spanning multiple paragraphs.
---

### Overview
This skill improves upon the basic replacement pattern by providing a robust mechanism to process conditional blocks in DOCX files, even when they span across paragraphs.

### Code Pattern
```python
from docx import Document

def process_doc_with_conditionals(doc_path, output_path, data, conditional_map):
    doc = Document(doc_path)
    
    # 1. Simple replacements
    for paragraph in doc.paragraphs:
        for k, v in data.items():
            key = f"{{{{{k}}}}}"
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, str(v))

    # 2. Advanced Conditional Block Processing
    # This logic identifies {{IF_TAG}} and {{END_IF_TAG}} and handles the text in between
    for tag, should_keep in conditional_map.items():
        start_tag = f"{{{{IF_{tag}}}}}"
        end_tag = f"{{{{END_IF_{tag}}}}}"
        
        in_block = False
        for paragraph in doc.paragraphs:
            if start_tag in paragraph.text:
                paragraph.text = paragraph.text.replace(start_tag, "")
                in_block = True
            
            if end_tag in paragraph.text:
                paragraph.text = paragraph.text.replace(end_tag, "")
                in_block = False
            
            if in_block and not should_keep:
                paragraph.text = ""
                
    doc.save(output_path)
```
