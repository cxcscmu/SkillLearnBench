---
name: python-docx-nested-table-recursion
description: Detailed guidance on recursively processing nested tables in python-docx documents. Use this when a Word template contains tables inside table cells and you need to reach all paragraphs.
---

## The Problem

`python-docx`'s `Document.tables` only returns **top-level** tables. If a table cell contains another table (nested table), you must explicitly access `cell.tables` to reach it. This can nest arbitrarily deep.

## Recursive Function

```python
def iter_all_paragraphs_in_table(table):
    """Recursively yield all paragraphs in a table, including nested tables."""
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                yield paragraph
            # Recurse into nested tables
            for nested_table in cell.tables:
                yield from iter_all_paragraphs_in_table(nested_table)
```

## Handling Duplicate Cells from Merged Cells

When cells are merged in a table, iterating `row.cells` can return the same `Cell` object multiple times. To avoid processing the same paragraph twice:

```python
def iter_all_paragraphs_in_table_deduped(table):
    seen = set()
    for row in table.rows:
        for cell in row.cells:
            cell_id = id(cell._element)
            if cell_id in seen:
                continue
            seen.add(cell_id)
            for paragraph in cell.paragraphs:
                yield paragraph
            for nested_table in cell.tables:
                yield from iter_all_paragraphs_in_table_deduped(nested_table)
```

## Full Document Traversal

```python
def iter_all_doc_paragraphs(doc):
    """Yield every paragraph in the entire document."""
    seen = set()
    
    def _yield_para(p):
        pid = id(p._element)
        if pid not in seen:
            seen.add(pid)
            yield p
    
    # Body paragraphs
    for p in doc.paragraphs:
        yield from _yield_para(p)
    
    # Body tables
    for table in doc.tables:
        for p in iter_all_paragraphs_in_table_deduped(table):
            yield from _yield_para(p)
    
    # All sections: headers and footers
    for section in doc.sections:
        for hf in [section.header, section.footer,
                    section.first_page_header, section.first_page_footer,
                    section.even_page_header, section.even_page_footer]:
            if hf is None or not hf.is_linked_to_previous:
                pass  # process anyway to be safe
            if hf is not None:
                for p in hf.paragraphs:
                    yield from _yield_para(p)
                for table in hf.tables:
                    for p in iter_all_paragraphs_in_table_deduped(table):
                        yield from _yield_para(p)
```

**Note on `is_linked_to_previous`**: Even if a header/footer is linked to previous, it's safer to process it. The `is_linked_to_previous` property means it shares content with the previous section's header/footer, but iterating it won't cause harm.

## Testing Nested Tables

To verify your code reaches nested table content:

```python
doc = Document('template.docx')
all_texts = []
for p in iter_all_doc_paragraphs(doc):
    text = ''.join(run.text for run in p.runs)
    if '{{' in text:
        all_texts.append(text)
print(f"Found {len(all_texts)} paragraphs with placeholders")
for t in all_texts:
    print(f"  - {t}")
```

This helps identify all placeholders that need replacement, including those buried in nested tables.