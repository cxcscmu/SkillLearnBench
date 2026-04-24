---
name: docx_recursive_text_replacement
description: Replaces placeholders in a Word document across all sections, including headers, footers, body paragraphs, and deeply nested tables. It uses paragraph-level replacement to ensure placeholders split across multiple runs are correctly identified.
---

To ensure all placeholders (e.g., `{{PLACEHOLDER}}`) are replaced regardless of their location or document structure, follow this approach using `python-docx`:

1.  **Iterate all Sections**: Loop through `doc.sections` to access `header` and `footer`.
2.  **Recursive Table Processing**: Create a function that iterates through a table's rows and cells. For every cell, it must check `cell.paragraphs` and recursively call itself for any tables found in `cell.tables`.
3.  **Paragraph-Level Replacement**: Instead of iterating through `paragraph.runs`, perform the replacement on `paragraph.text`. This avoids issues where Word splits a single placeholder into multiple XML "runs".
4.  **Complete Coverage**: Apply the replacement logic to:
    *   `doc.paragraphs`
    *   `doc.tables` (using the recursive function)
    *   `section.header.paragraphs` and `section.header.tables`
    *   `section.footer.paragraphs` and `section.footer.tables`

Example logic:
```python
def replace_in_paragraph(paragraph, data):
    for key, value in data.items():
        placeholder = f"{{{{{key}}}}}"
        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, str(value))

def process_table(table, data):
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                replace_in_paragraph(paragraph, data)
            for nested_table in cell.tables:
                process_table(nested_table, data)
```