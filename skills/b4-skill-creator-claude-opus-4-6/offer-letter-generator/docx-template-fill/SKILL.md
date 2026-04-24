---
name: docx-template-fill
description: >
  Fill Word document (.docx) templates that use placeholder syntax like {{PLACEHOLDER}}.
  Handles split placeholders (where Word splits a placeholder across multiple XML runs),
  conditional sections ({{IF_X}}...{{END_IF_X}}), and preserves formatting.
  Use this skill whenever the user asks to fill a Word template, generate a document
  from a template, or replace placeholders in a .docx file.
---

# DOCX Template Fill

## Core Challenge: Split Placeholders

Word internally splits text into "runs" based on formatting changes, spell-check boundaries,
or editing history. A placeholder like `{{COMPANY_NAME}}` may become three runs:
`{{COMP` + `ANY_` + `NAME}}`. Naive per-run replacement will fail.

## Strategy

1. **Merge-then-replace at the run level**: For each paragraph (and header/footer/table cell
   paragraph), concatenate all run texts, perform regex replacements on the merged string,
   then redistribute text back to runs — putting all text in the first run and clearing the rest.
   This preserves the first run's formatting.

2. **Process all text containers**: Paragraphs live in the document body, but also in:
   - Table cells (iterate `doc.tables[*].rows[*].cells[*].paragraphs`)
   - Section headers (`doc.sections[*].header.paragraphs`)
   - Section footers (`doc.sections[*].footer.paragraphs`)

3. **Conditional sections**: For `{{IF_KEY}}...content...{{END_IF_KEY}}`:
   - If condition is true (value is "Yes"), remove only the markers, keep content
   - If condition is false, remove markers and all content between them
   - Conditionals may span a single paragraph or the markers may be in separate runs

## Implementation Pattern

```python
import re, json
from docx import Document

def replace_in_paragraph(paragraph, replacements):
    """Replace placeholders in a paragraph, handling split runs."""
    full_text = "".join(run.text for run in paragraph.runs)
    if not full_text:
        return
    new_text = full_text
    for key, value in replacements.items():
        new_text = new_text.replace("{{" + key + "}}", value)
    if new_text != full_text:
        # Put all text in first run, clear the rest (preserves first run's formatting)
        for i, run in enumerate(paragraph.runs):
            if i == 0:
                run.text = new_text
            else:
                run.text = ""

def handle_conditional(paragraph, key, keep):
    """Handle {{IF_key}}...{{END_IF_key}} within a single paragraph."""
    full_text = "".join(run.text for run in paragraph.runs)
    pattern = r"\{\{IF_" + key + r"\}\}(.*?)\{\{END_IF_" + key + r"\}\}"
    if re.search(pattern, full_text):
        if keep:
            new_text = re.sub(pattern, r"\1", full_text)
        else:
            new_text = re.sub(pattern, "", full_text)
        for i, run in enumerate(paragraph.runs):
            run.text = new_text if i == 0 else ""

def process_all_paragraphs(doc, func, *args):
    """Apply a function to every paragraph in the document."""
    for p in doc.paragraphs:
        func(p, *args)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    func(p, *args)
    for section in doc.sections:
        for p in section.header.paragraphs:
            func(p, *args)
        for p in section.footer.paragraphs:
            func(p, *args)
```

## Workflow

1. Load data (JSON) and template (docx)
2. Handle conditionals first (before placeholder replacement)
3. Replace all `{{KEY}}` placeholders with values from data
4. Save the filled document
