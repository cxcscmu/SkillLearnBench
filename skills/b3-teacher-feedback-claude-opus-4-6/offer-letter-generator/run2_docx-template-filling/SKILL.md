---
name: docx-template-filling
description: How to open a .docx Word document template with python-docx, replace placeholder tags like {{PLACEHOLDER}} in all document locations (body, headers, footers, tables including nested tables), handle conditional sections, and save the result.
---

## Core Approach

Use `python-docx` to open the template, collect ALL paragraphs from every possible location, perform text replacement, and save.

## Collecting ALL Paragraphs (Critical: Must Be Recursive)

The biggest pitfall is missing paragraphs in nested tables, headers, footers, and tables within headers/footers. Use a recursive approach:

```python
from docx import Document

def get_all_paragraphs(doc):
    """Collect every paragraph in the document, including nested tables, headers, and footers."""
    paragraphs = []

    # Body paragraphs
    paragraphs.extend(doc.paragraphs)

    # Tables in body (recursive)
    for table in doc.tables:
        paragraphs.extend(_get_paragraphs_from_table(table))

    # Headers and footers
    for section in doc.sections:
        for header_footer in [section.header, section.footer, section.first_page_header, section.first_page_footer, section.even_page_header, section.even_page_footer]:
            if header_footer is not None:
                paragraphs.extend(header_footer.paragraphs)
                for table in header_footer.tables:
                    paragraphs.extend(_get_paragraphs_from_table(table))

    return paragraphs


def _get_paragraphs_from_table(table):
    """Recursively collect paragraphs from a table, including nested tables within cells."""
    paragraphs = []
    for row in table.rows:
        for cell in row.cells:
            paragraphs.extend(cell.paragraphs)
            # CRITICAL: Recurse into nested tables
            for nested_table in cell.tables:
                paragraphs.extend(_get_paragraphs_from_table(nested_table))
    return paragraphs
```

### Why Recursive?

Templates often have nested tables (a table inside a table cell). `doc.tables` only gives top-level tables. You MUST call `cell.tables` on each cell and recurse to find all nested content. Without this, placeholders in nested tables will remain unreplaced.

## Replacing Placeholders in Paragraphs (Run-Aware)

Placeholders like `{{CANDIDATE_FULL_NAME}}` may be split across multiple runs within a paragraph. Always work at the full paragraph text level, then rewrite runs:

```python
def replace_placeholder_in_paragraph(paragraph, placeholder, value):
    """Replace a placeholder in a paragraph, handling split runs."""
    full_text = ''.join(run.text for run in paragraph.runs)
    if placeholder not in full_text:
        return False
    new_text = full_text.replace(placeholder, value)
    # Clear all runs, put new text in first run, preserve formatting
    for i, run in enumerate(paragraph.runs):
        if i == 0:
            run.text = new_text
        else:
            run.text = ''
    return True
```

## Full Replacement Over All Paragraphs

```python
def replace_all(doc, placeholder, value):
    for para in get_all_paragraphs(doc):
        replace_placeholder_in_paragraph(para, placeholder, value)
```

## Handling Conditional Sections

For `{{IF_RELOCATION}}...{{END_IF_RELOCATION}}`:

- If the condition is **true** (e.g., RELOCATION_PACKAGE == "Yes"): remove only the marker lines `{{IF_RELOCATION}}` and `{{END_IF_RELOCATION}}`, keep content between them.
- If the condition is **false**: remove the markers AND all content between them.

```python
def handle_conditional(doc, tag_name, keep_content):
    """Handle conditional blocks like {{IF_RELOCATION}}...{{END_IF_RELOCATION}}."""
    start_tag = '{{IF_' + tag_name + '}}'
    end_tag = '{{END_IF_' + tag_name + '}}'
    all_paras = get_all_paragraphs(doc)
    
    inside = False
    for para in all_paras:
        full_text = ''.join(run.text for run in para.runs)
        
        if start_tag in full_text:
            inside = True
            # Remove the start tag (or the whole paragraph if it's only the tag)
            replace_placeholder_in_paragraph(para, start_tag, '')
            # Check if paragraph is now empty/whitespace — if so, remove it
            remaining = ''.join(run.text for run in para.runs).strip()
            if not remaining:
                _remove_paragraph(para)
            continue
        
        if end_tag in full_text:
            inside = False
            replace_placeholder_in_paragraph(para, end_tag, '')
            remaining = ''.join(run.text for run in para.runs).strip()
            if not remaining:
                _remove_paragraph(para)
            continue
        
        if inside and not keep_content:
            _remove_paragraph(para)


def _remove_paragraph(paragraph):
    """Remove a paragraph from the document."""
    p = paragraph._element
    p.getparent().remove(p)
```

## Handling Conditional When Tags Are Inline

Sometimes the IF/END_IF markers are inline within a paragraph alongside other text. In that case, just replace them with empty string rather than removing the paragraph:

```python
# Simpler approach: always just replace the tags with ''
# Then remove content paragraphs if not keeping
```

## Complete Workflow

```python
import json
from docx import Document

# Load data
with open('employee_data.json', 'r') as f:
    data = json.load(f)

doc = Document('offer_letter_template.docx')

# Handle conditional FIRST (before replacing other placeholders)
keep_relocation = data.get('RELOCATION_PACKAGE', 'No').strip().lower() == 'yes'
handle_conditional(doc, 'RELOCATION', keep_relocation)

# Replace all placeholders
for key, value in data.items():
    placeholder = '{{' + key + '}}'
    replace_all(doc, placeholder, str(value))

doc.save('/root/offer_letter_filled.docx')
```

## Verification

After saving, reopen and verify no `{{` placeholders remain:

```python
doc2 = Document('/root/offer_letter_filled.docx')
for para in get_all_paragraphs(doc2):
    text = ''.join(run.text for run in para.runs)
    assert '{{' not in text, f"Unreplaced placeholder found: {text}"
```

## Common Pitfalls

1. **Nested tables**: MUST recurse into `cell.tables` — this is the #1 cause of unreplaced placeholders
2. **Headers/footers**: Must iterate ALL section headers and footers, including first-page and even-page variants
3. **Tables in headers/footers**: Headers/footers can contain tables too — must process those
4. **Split runs**: A placeholder like `{{NAME}}` might be split as `{{` in one run and `NAME}}` in another — always join all run texts before matching
5. **Deduplication**: When iterating cells, the same cell object can appear multiple times if cells are merged. Consider deduplicating by element identity: `seen = set(); ... if id(para._element) in seen: continue`