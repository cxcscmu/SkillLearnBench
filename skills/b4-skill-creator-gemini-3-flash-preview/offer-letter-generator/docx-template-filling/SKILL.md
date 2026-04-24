---
name: docx-template-filling
description: Robustly fill Word (.docx) templates with JSON data. Handles split placeholders, nested tables, headers/footers, and conditional logic like IF/END_IF blocks. Use this skill whenever you need to generate professional documents from templates.
---

# docx-template-filling

## Overview
This skill provides a robust framework for filling Microsoft Word templates using the `python-docx` library. It specifically addresses the "Split Placeholder" problem and supports conditional content blocks.

## Core Principles
1. **Paragraph-Level Processing**: Always modify text at the paragraph level (`para.text`) rather than the run level (`run.text`) to avoid issues where Word splits placeholders like `{{NAME}}` into multiple runs (e.g., `{{NA` and `ME}}`).
2. **Formatting Preservation**: When replacing text in a paragraph, clear all runs except the first one. Update the first run's text to the new content to preserve the paragraph's initial formatting.
3. **Comprehensive Traversal**: Process the main document body, tables (including nested ones), and headers/footers of all sections.

## Handling Conditional Sections
Conditional sections are marked with `{{IF_CONDITION}}...{{END_IF_CONDITION}}`.
- **If condition is True**: Remove the markers but keep the content in between.
- **If condition is False**: Remove the entire block including markers and content.

### Implementation Pattern for Conditionals
```python
def process_conditionals(doc, condition_key, is_enabled):
    start_marker = f"{{{{IF_{condition_key}}}}}"
    end_marker = f"{{{{END_IF_{condition_key}}}}}"
    
    # Track paragraphs to delete if condition is False
    paras_to_delete = []
    in_block = False
    
    for para in doc.paragraphs:
        if start_marker in para.text:
            in_block = True
            # Remove marker from this paragraph
            para.text = para.text.replace(start_marker, "")
        
        if in_block and not is_enabled:
            paras_to_delete.append(para)
            
        if end_marker in para.text:
            in_block = False
            # Remove marker from this paragraph
            para.text = para.text.replace(end_marker, "")
```

## Handling Split Placeholders
Use a regex-based replacement strategy at the paragraph level.

```python
import re

def replace_placeholders(para, data):
    text = para.text
    pattern = r"\{\{([A-Z_0-9]+)\}\}"
    matches = re.findall(pattern, text)
    
    if not matches:
        return False
        
    new_text = text
    for key in matches:
        placeholder = f"{{{{{key}}}}}"
        if key in data:
            new_text = new_text.replace(placeholder, str(data[key]))
            
    if new_text != text:
        # Preserve first run formatting
        if para.runs:
            para.runs[0].text = new_text
            for run in para.runs[1:]:
                run.text = ""
        else:
            para.text = new_text
        return True
    return False
```

## Traversal Logic
Ensure all parts of the document are reached:
- `doc.paragraphs`
- `doc.tables` (recurse into `cell.paragraphs` and `cell.tables`)
- `doc.sections` (iterate `section.header.paragraphs` and `section.footer.paragraphs`)
