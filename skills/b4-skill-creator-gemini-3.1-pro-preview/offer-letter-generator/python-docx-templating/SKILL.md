---
name: python-docx-templating
description: How to process Word documents (.docx) with python-docx. Use this skill whenever the user mentions Word templates, docx templating, replacing placeholders, or processing Word files, even if they don't explicitly ask for it.
---
# Word Document Manipulation with python-docx

## Critical: Split Placeholder Problem
Word often splits placeholder text across multiple XML runs (e.g., `{{CANDIDATE_NAME}}` split into `{{CANDI` and `DATE_NAME}}`). Never search for placeholders at the run level!

### Correct Approach: Paragraph-Level Search and Rebuild

```python
import re

def replace_in_paragraph(para, data):
    """Replace placeholders in a single paragraph, handling split runs."""
    text = para.text
    # Find all placeholders like {{PLACEHOLDER}}
    pattern = r'\{\{([A-Z_]+)\}\}'
    matches = re.findall(pattern, text)

    if not matches:
        return

    # Build new text with replacements
    new_text = text
    for key in set(matches):
        placeholder = '{{' + key + '}}'
        if key in data:
            new_text = new_text.replace(placeholder, str(data[key]))

    # Rebuild paragraph, preserving the first run's formatting
    if new_text != text and para.runs:
        para.runs[0].text = new_text
        for run in para.runs[1:]:
            run.text = ''
```

## Conditional Sections
For conditional patterns like `{{IF_CONDITION}}...{{END_IF_CONDITION}}`, handle them before general placeholder replacement:

```python
def process_conditional_paragraph(para, condition_key, should_include):
    start_marker = '{{IF_' + condition_key + '}}'
    end_marker = '{{END_IF_' + condition_key + '}}'

    text = para.text
    if start_marker in text and end_marker in text:
        if should_include:
            # Remove just the markers
            new_text = text.replace(start_marker, '').replace(end_marker, '')
        else:
            # Clear text
            new_text = ''
        
        if new_text != text and para.runs:
            para.runs[0].text = new_text
            for run in para.runs[1:]:
                run.text = ''
        return True # Handled conditional
    return False
```

## Traversing All Elements
You must traverse paragraphs, tables, nested tables, headers, and footers:

```python
def process_document(doc, data):
    # Main document
    for para in doc.paragraphs:
        # e.g. Handle conditionals first, then replace placeholders
        replace_in_paragraph(para, data)

    # Tables (with nesting)
    def process_table(table):
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_in_paragraph(para, data)
                for nested in cell.tables:
                    process_table(nested)

    for table in doc.tables:
        process_table(table)

    # Headers/Footers
    for section in doc.sections:
        for para in section.header.paragraphs:
            replace_in_paragraph(para, data)
        for para in section.footer.paragraphs:
            replace_in_paragraph(para, data)
```

## Common Pitfalls
1. **Forgetting headers/footers** - Accessed via `doc.sections[x].header.paragraphs`
2. **Missing nested tables** - Must recurse `cell.tables`
3. **Split placeholders** - Work at paragraph level, clear other runs.
