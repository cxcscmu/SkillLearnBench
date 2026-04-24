---
name: run2_python-docx-split-placeholders
description: Robust python-docx template filling that handles split runs, conditional sections, nested tables, headers, and footers.
---

# Robust python-docx Template Filling

## Core Problem
python-docx stores paragraph text in "runs" (spans with uniform formatting). Placeholders like `{{COMPANY_NAME}}` often get split across runs (e.g., `['{{COMP', 'ANY_NAME}}']`), making naive per-run replacement fail.

## Recommended Approach

### 1. Paragraph-level replacement function

```python
import re

def replace_in_paragraph(para, replacements, keep_relocation=True):
    full_text = ''.join(run.text for run in para.runs)
    if not full_text:
        return

    # Handle conditional blocks BEFORE placeholder substitution
    if '{{IF_RELOCATION}}' in full_text:
        if keep_relocation:
            full_text = full_text.replace('{{IF_RELOCATION}}', '')
            full_text = full_text.replace('{{END_IF_RELOCATION}}', '')
        else:
            full_text = re.sub(
                r'\{\{IF_RELOCATION\}\}.*?\{\{END_IF_RELOCATION\}\}',
                '', full_text, flags=re.DOTALL
            )

    for placeholder, value in replacements.items():
        full_text = full_text.replace(placeholder, value)

    # Preserve first run's formatting, clear others
    if para.runs:
        para.runs[0].text = full_text
        for run in para.runs[1:]:
            run.text = ''
```

### 2. Process ALL text locations in the document

Locations that can contain placeholders:
- **Body paragraphs**: `doc.paragraphs`
- **Headers/Footers**: `section.header.paragraphs`, `section.footer.paragraphs`
- **Table cells**: `table.rows[i].cells[j].paragraphs`
- **Nested tables**: cells can contain sub-tables (recurse!)

```python
def process_table(table, replacements, keep_relocation):
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                replace_in_paragraph(para, replacements, keep_relocation)
            for nested in cell.tables:
                process_table(nested, replacements, keep_relocation)
```

### 3. Conditional sections spanning multiple paragraphs

If `{{IF_RELOCATION}}` and `{{END_IF_RELOCATION}}` are in separate paragraphs (not same paragraph), you need a multi-paragraph approach: find the start/end paragraph indices and either remove content between them or just strip the markers. In this template they're in the same paragraph, but for robustness consider both cases.

### 4. Formatting note

Putting all text in `runs[0]` loses formatting differences between runs (e.g., bold words within a sentence). For templates where each paragraph has uniform formatting, this is fine. For mixed-formatting paragraphs, a more sophisticated approach is needed: walk through runs tracking character positions and only modify runs that contain placeholder characters.

## Quick Reference

```python
from docx import Document
import json, re

with open('data.json') as f:
    data = json.load(f)

doc = Document('template.docx')
replacements = {f'{{{{{k}}}}}': v for k, v in data.items()}
keep_reloc = data.get('RELOCATION_PACKAGE') == 'Yes'
# Remove non-placeholder keys from replacements
for key in ['{{RELOCATION_PACKAGE}}']:
    replacements.pop(key, None)

# Process body, headers, footers, tables (including nested)
```
