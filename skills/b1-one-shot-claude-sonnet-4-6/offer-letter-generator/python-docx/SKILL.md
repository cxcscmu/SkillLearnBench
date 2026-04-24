---
name: python-docx
description: Core python-docx usage for reading, modifying, and saving Word documents including paragraphs, runs, tables, headers, and footers.
---

# python-docx Core Usage

## Installation

```bash
pip install python-docx
```

## Basic Document Operations

```python
from docx import Document

# Open existing document
doc = Document('template.docx')

# Access paragraphs
for para in doc.paragraphs:
    print(para.text)           # Full paragraph text
    for run in para.runs:      # Individual styled runs
        print(run.text)

# Save
doc.save('output.docx')
```

## Document Structure

A `.docx` file has:
- `doc.paragraphs` — body paragraphs (does NOT include headers/footers)
- `doc.tables` — top-level tables in body
- `doc.sections` — page sections (each has `.header` and `.footer`)

### Paragraphs and Runs

A `Paragraph` is a block of text. It contains multiple `Run` objects, each with their own formatting (bold, italic, font size, etc.).

**Critical**: Word often splits a single logical text segment across multiple runs (due to spell-check marks, formatting, or XML internals). Always read `para.text` for the full text — never rely on individual runs.

```python
para.text          # Full concatenated text of all runs
para.runs          # List of Run objects
run.text           # Text of this run
run.bold           # Bold formatting
run.italic         # Italic formatting
run.font.size      # Font size (in EMUs; divide by 12700 for pt)
run.font.name      # Font name
```

### Tables

```python
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                print(para.text)
            for nested_table in cell.tables:  # recurse for nesting
                pass
```

### Headers and Footers

```python
for section in doc.sections:
    header = section.header
    footer = section.footer
    for para in header.paragraphs:
        print(para.text)
    for para in footer.paragraphs:
        print(para.text)
```

## Modifying Text While Preserving Formatting

When replacing text, preserve the first run's formatting and clear subsequent runs:

```python
def set_paragraph_text(para, new_text):
    """Replace all run text in a paragraph, keeping first run's formatting."""
    if not para.runs:
        return
    para.runs[0].text = new_text
    for run in para.runs[1:]:
        run.text = ''
```

## Common Pitfalls

- `doc.paragraphs` does NOT include paragraphs inside table cells
- `doc.paragraphs` does NOT include header/footer paragraphs
- Split runs are the norm, not the exception — always work at `para.text` level
- Clearing all runs and rebuilding loses per-run formatting (bold/italic on parts of text)
