---
name: run2_python-docx-placeholders
description: Replace {{PLACEHOLDER}} tokens in Word .docx templates using python-docx, correctly handling split runs, nested tables, headers/footers, and verification.
---

# python-docx Placeholder Replacement (Improved)

## Installation

```bash
pip install python-docx
```

## The Split-Run Problem

Word internally splits paragraph text across multiple XML "runs". `{{CANDIDATE_NAME}}`
might be stored as Run1:`{{CANDI` + Run2:`DATE_NAME}}`. Always read `para.text` (which
concatenates all runs), apply changes, then write back to runs.

## Core Replacement Function

```python
def replace_in_paragraph(para, data):
    """Replace all {{KEY}} placeholders in a paragraph, safe against split runs."""
    text = para.text
    if '{{' not in text:
        return

    new_text = text
    for key, value in data.items():
        new_text = new_text.replace('{{' + key + '}}', str(value))

    if new_text != text and para.runs:
        # Collapse all text into run[0], preserving its formatting
        para.runs[0].text = new_text
        for run in para.runs[1:]:
            run.text = ''
```

> **Formatting note**: This preserves run[0]'s formatting (font, bold, size) but
> flattens any mid-paragraph formatting. Acceptable for offer letter templates.

## Important: `doc.paragraphs` vs Table Cell Paragraphs

`doc.paragraphs` only returns paragraphs in the document **body**, NOT inside tables.
You must separately iterate tables and recurse into cells.

```python
def process_table(table, data):
    """Process all paragraphs in a table, including nested tables."""
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                replace_in_paragraph(para, data)
            for nested in cell.tables:   # Word allows tables inside table cells
                process_table(nested, data)
```

## Full Template Fill Function

```python
import json
from docx import Document

def fill_template(template_path, data, output_path):
    """
    Fill a Word template by replacing all {{KEY}} placeholders.

    Args:
        template_path: Path to the .docx template
        data: dict of {KEY: value} pairs (keys without {{ }})
        output_path: Where to save the filled document
    """
    doc = Document(template_path)

    # 1. Body paragraphs
    for para in doc.paragraphs:
        replace_in_paragraph(para, data)

    # 2. Tables (with nested table support)
    for table in doc.tables:
        process_table(table, data)

    # 3. Headers and footers — these are NOT in doc.paragraphs!
    for section in doc.sections:
        for para in section.header.paragraphs:
            replace_in_paragraph(para, data)
        for para in section.footer.paragraphs:
            replace_in_paragraph(para, data)

    doc.save(output_path)


def verify_no_remaining_placeholders(doc_path):
    """Check that no {{...}} tokens remain in the filled document."""
    doc = Document(doc_path)
    remaining = []

    for para in doc.paragraphs:
        if '{{' in para.text:
            remaining.append(f'body: {para.text}')

    def check_table(table):
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if '{{' in para.text:
                        remaining.append(f'table: {para.text}')
                for nested in cell.tables:
                    check_table(nested)

    for table in doc.tables:
        check_table(table)

    return remaining  # empty list means success
```

## Recommended Workflow

```python
# 1. Load data (filter only string-valued keys needed for replacement)
with open('employee_data.json') as f:
    data = json.load(f)

# 2. Process conditionals FIRST (before general replacement)
#    See run2_docx-conditional-sections skill

# 3. Fill remaining placeholders
fill_template('template.docx', data, 'output.docx')

# 4. Verify
leftovers = verify_no_remaining_placeholders('output.docx')
if leftovers:
    print("Unfilled placeholders:", leftovers)
else:
    print("Success!")
```

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Searching `para.runs` for `{{...}}` | Always use `para.text` (handles split runs) |
| Only iterating `doc.paragraphs` | Also iterate `doc.tables` with recursion |
| Forgetting headers/footers | Iterate `doc.sections`, access `.header` and `.footer` |
| Processing placeholders before conditionals | Handle `{{IF_X}}...{{END_IF_X}}` first |
| No verification step | Always check for remaining `{{` tokens after filling |
