---
name: python-docx
description: Manipulate Word .docx files with python-docx, including handling split placeholders across runs and conditional sections.
---

# python-docx: Word Document Manipulation

## Installation
```bash
pip install python-docx
```

## Core Concepts

### Split Placeholders Across Runs
Word often splits text into multiple XML runs due to spell-check, formatting changes, or editing history. A placeholder like `{{COMPANY_NAME}}` may be stored as separate runs: `['{{COMP', 'ANY_NAME}}']`.

**Solution**: Join all run texts in a paragraph, perform replacements on the joined text, then redistribute back to runs (clearing extra runs).

```python
import re
from docx import Document

def replace_in_paragraph(paragraph, replacements):
    """Replace placeholders in a paragraph, handling split runs."""
    full_text = ''.join(run.text for run in paragraph.runs)
    if not any(key in full_text for key in replacements):
        return
    for key, value in replacements.items():
        full_text = full_text.replace(key, value)
    # Put all text in the first run, clear the rest
    if paragraph.runs:
        paragraph.runs[0].text = full_text
        for run in paragraph.runs[1:]:
            run.text = ''
```

### Replacing in All Document Locations
Documents have paragraphs in the body, tables (including nested tables), headers, and footers.

```python
def replace_all_in_doc(doc, replacements):
    # Body paragraphs
    for p in doc.paragraphs:
        replace_in_paragraph(p, replacements)

    # Tables (including nested)
    def process_table(table):
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    replace_in_paragraph(p, replacements)
                for nested in cell.tables:
                    process_table(nested)

    for table in doc.tables:
        process_table(table)

    # Headers and footers
    for section in doc.sections:
        for p in section.header.paragraphs:
            replace_in_paragraph(p, replacements)
        for p in section.footer.paragraphs:
            replace_in_paragraph(p, replacements)
```

### Conditional Sections
For `{{IF_X}}...{{END_IF_X}}` patterns:
- If condition is true: remove the markers, keep the content
- If condition is false: remove markers and content entirely

```python
def handle_conditional(paragraph, tag, keep):
    full_text = ''.join(run.text for run in paragraph.runs)
    start_tag = '{{IF_' + tag + '}}'
    end_tag = '{{END_IF_' + tag + '}}'
    if start_tag in full_text:
        if keep:
            full_text = full_text.replace(start_tag, '').replace(end_tag, '')
        else:
            # Remove everything between and including tags
            pattern = re.escape(start_tag) + '.*?' + re.escape(end_tag)
            full_text = re.sub(pattern, '', full_text)
        if paragraph.runs:
            paragraph.runs[0].text = full_text
            for run in paragraph.runs[1:]:
                run.text = ''
```

## Saving
```python
doc.save('output.docx')
```
