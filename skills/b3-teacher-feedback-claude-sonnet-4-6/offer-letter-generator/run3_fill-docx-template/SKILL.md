---
name: fill-docx-template
description: Use this skill to fill placeholders in a .docx template file with data from a JSON file, handle conditional sections, and save the result. Covers body paragraphs, tables, and headers/footers.
---

# Fill DOCX Template with JSON Data

## Overview
This skill fills `{{PLACEHOLDER}}` tokens in a Word `.docx` template using data from a JSON file. It handles:
- Body paragraphs and table cells
- Headers and footers in all sections
- Split-run placeholders (where a token is split across multiple runs)
- Conditional blocks `{{IF_KEY}}...{{END_IF_KEY}}`

## Implementation

```python
import json
import re
from docx import Document
from docx.oxml.ns import qn
from copy import deepcopy


def load_data(json_path):
    with open(json_path, "r") as f:
        return json.load(f)


def rebuild_para_text(para):
    """Return full text of paragraph, concatenating all runs."""
    return "".join(run.text for run in para.runs)


def set_para_text_replacing(para, old, new):
    """
    Replace all occurrences of `old` with `new` in a paragraph,
    preserving run formatting as much as possible.
    First, consolidate split tokens, then replace.
    """
    full_text = rebuild_para_text(para)
    if old not in full_text:
        return False

    # Strategy: merge all runs into the first run, replace, redistribute
    # This is safe for header/footer paragraphs too.
    if not para.runs:
        return False

    # Consolidate: put everything into runs[0], clear the rest
    new_full = full_text.replace(old, new)

    # Distribute new text: put all in first run, blank the others
    para.runs[0].text = new_full
    for run in para.runs[1:]:
        run.text = ""
    return True


def fix_split_placeholders(para):
    """
    If a placeholder like {{KEY}} is split across runs, merge those runs
    into one run so replacement works cleanly.
    """
    full_text = rebuild_para_text(para)
    # Check if there are any placeholders potentially split
    if "{{" not in full_text:
        return

    # Rebuild: merge all run texts, assign back to first run
    if len(para.runs) <= 1:
        return

    # Only consolidate if a placeholder might be split
    combined = "".join(r.text for r in para.runs)
    if re.search(r'\{\{[^}]*$', combined) or re.search(r'^[^{]*\}\}', combined):
        # There's a split — merge all into first run
        para.runs[0].text = combined
        for run in para.runs[1:]:
            run.text = ""


def replace_in_paragraph(para, data):
    """Replace all known placeholders in a paragraph."""
    fix_split_placeholders(para)
    for key, value in data.items():
        placeholder = f"{{{{{key}}}}}"
        set_para_text_replacing(para, placeholder, str(value))


def iter_all_paragraphs(doc):
    """
    Yield every paragraph in the document:
    - Body paragraphs
    - Table cell paragraphs (all nesting levels)
    - Header and footer paragraphs for every section
    """
    # Body paragraphs
    for para in doc.paragraphs:
        yield para

    # Table cells
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    yield para
                # nested tables
                for nested_table in cell.tables:
                    for nrow in nested_table.rows:
                        for ncell in nrow.cells:
                            for para in ncell.paragraphs:
                                yield para

    # Headers and footers for each section
    for section in doc.sections:
        # Header
        if section.header:
            for para in section.header.paragraphs:
                yield para
            for table in section.header.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for para in cell.paragraphs:
                            yield para
        # Footer
        if section.footer:
            for para in section.footer.paragraphs:
                yield para
            for table in section.footer.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for para in cell.paragraphs:
                            yield para
        # First page header/footer
        if section.first_page_header:
            for para in section.first_page_header.paragraphs:
                yield para
        if section.first_page_footer:
            for para in section.first_page_footer.paragraphs:
                yield para
        # Even page header/footer
        if section.even_page_header:
            for para in section.even_page_header.paragraphs:
                yield para
        if section.even_page_footer:
            for para in section.even_page_footer.paragraphs:
                yield para


def handle_conditional_sections(doc, data):
    """
    Handle {{IF_KEY}}...{{END_IF_KEY}} blocks.
    - If data[KEY] == 'Yes': keep content, remove marker paragraphs
    - If data[KEY] != 'Yes': remove entire block including markers
    """
    # We need to work on the XML level for reliable paragraph removal
    # Collect paragraph elements with their text
    body = doc.element.body
    paras = list(body)  # includes paragraphs and tables etc.

    # Find all IF keys used in the document
    full_body_text = "\n".join(
        "".join(run.text for run in p.runs)
        for p in doc.paragraphs
    )

    if_keys = re.findall(r'\{\{IF_(\w+)\}\}', full_body_text)

    for key in set(if_keys):
        start_marker = f"{{{{IF_{key}}}}}"
        end_marker = f"{{{{END_IF_{key}}}}}"
        condition_value = data.get(key, "No")
        keep_content = (str(condition_value).strip().lower() == "yes")

        # Find paragraph indices
        all_body_paras = list(doc.element.body)
        start_idx = None
        end_idx = None

        for i, elem in enumerate(all_body_paras):
            # Get text of element
            if elem.tag.endswith('}p'):
                text = "".join(t.text or "" for t in elem.iter() if t.tag.endswith('}t'))
                if start_marker in text:
                    start_idx = i
                if end_marker in text:
                    end_idx = i

        if start_idx is None or end_idx is None:
            continue

        if keep_content:
            # Remove only the marker paragraphs (start and end)
            # Remove end first (higher index), then start
            end_elem = all_body_paras[end_idx]
            start_elem = all_body_paras[start_idx]
            end_elem.getparent().remove(end_elem)
            start_elem.getparent().remove(start_elem)
        else:
            # Remove everything from start_idx to end_idx inclusive
            to_remove = all_body_paras[start_idx:end_idx + 1]
            for elem in to_remove:
                elem.getparent().remove(elem)


def fill_template(template_path, json_path, output_path):
    doc = Document(template_path)
    data = load_data(json_path)

    # Step 1: Handle conditional sections first (before placeholder replacement)
    handle_conditional_sections(doc, data)

    # Step 2: Replace all placeholders everywhere (body + tables + headers + footers)
    for para in iter_all_paragraphs(doc):
        replace_in_paragraph(para, data)

    # Step 3: Save
    doc.save(output_path)
    print(f"Saved filled offer letter to {output_path}")


if __name__ == "__main__":
    fill_template(
        template_path="offer_letter_template.docx",
        json_path="employee_data.json",
        output_path="/root/offer_letter_filled.docx",
    )
```

## Key Points

- **`iter_all_paragraphs`** explicitly yields paragraphs from `section.header`, `section.footer`, `section.first_page_header`, `section.first_page_footer`, `section.even_page_header`, and `section.even_page_footer` for every section — this ensures `DOC_ID` and other header/footer placeholders are replaced.
- **`fix_split_placeholders`** merges run text before replacement to handle tokens split across runs.
- **`handle_conditional_sections`** processes `{{IF_KEY}}...{{END_IF_KEY}}` blocks before placeholder replacement to avoid leaving stale markers.
- Conditional check is case-insensitive (`"yes"` match).