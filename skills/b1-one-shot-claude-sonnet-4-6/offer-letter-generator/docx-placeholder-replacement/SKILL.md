---
name: docx-placeholder-replacement
description: Robustly replace {{PLACEHOLDER}} tokens in Word documents, handling split runs across paragraphs, tables, headers, and footers.
---

# Robust Placeholder Replacement in Word Documents

## The Split-Run Problem

Word's XML engine often breaks a single word like `{{CANDIDATE_NAME}}` across multiple runs:

```
run[0]: '{{CANDI'
run[1]: 'DATE_NAME}}'
```

A naive `run.text.replace()` will miss these. Always reconstruct from `para.text`.

## Safe Replacement Algorithm

```python
import re

def replace_in_paragraph(para, data):
    """Replace all {{KEY}} placeholders in paragraph, handling split runs."""
    full_text = para.text
    pattern = re.compile(r'\{\{([A-Z0-9_]+)\}\}')

    if not pattern.search(full_text):
        return  # Nothing to do

    # Build replacement
    def replacer(m):
        key = m.group(1)
        return str(data[key]) if key in data else m.group(0)

    new_text = pattern.sub(replacer, full_text)

    if new_text != full_text and para.runs:
        # Put all text in first run, clear the rest
        para.runs[0].text = new_text
        for run in para.runs[1:]:
            run.text = ''
```

## Apply to Entire Document

```python
def replace_all_placeholders(doc, data):
    """Replace placeholders everywhere: body, tables, headers, footers."""

    # Body paragraphs
    for para in doc.paragraphs:
        replace_in_paragraph(para, data)

    # Tables (with nested table recursion)
    def process_table(table):
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_in_paragraph(para, data)
                for nested in cell.tables:
                    process_table(nested)

    for table in doc.tables:
        process_table(table)

    # Headers and footers
    for section in doc.sections:
        for para in section.header.paragraphs:
            replace_in_paragraph(para, data)
        for para in section.footer.paragraphs:
            replace_in_paragraph(para, data)
```

## Notes

- Only the first run's formatting is preserved after merging. If parts of the placeholder text have different formatting (e.g., bold `{{NAME}}`), that formatting is lost — which is usually acceptable for template filling.
- Unknown placeholders (keys not in `data`) are left as-is by default. Adjust the `replacer` function to raise errors or substitute empty strings if needed.
