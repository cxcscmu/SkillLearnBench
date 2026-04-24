---
name: offer-letter-docx
description: >
  Fill Word offer letter templates with employee data, replacing {{PLACEHOLDER}}
  tokens and handling {{IF_CONDITION}}...{{END_IF_CONDITION}} conditional blocks.
  Use this skill whenever the user asks to generate, fill, or produce an offer
  letter from a .docx template and a JSON data file, or whenever you need to
  merge HR data into a Word document template with placeholders and optional
  sections (e.g. relocation package, signing bonus).
---

# Offer Letter Template Filling

## Overview

Fill a `.docx` offer letter template by:
1. Replacing every `{{KEY}}` placeholder with values from a JSON data file.
2. Handling `{{IF_KEY}}...{{END_IF_KEY}}` conditional blocks — keep content
   (and strip markers) when the data field equals `"Yes"`, else remove the
   entire block.
3. Saving the result to a new `.docx` file.

## Key Technical Notes

- Use the **paragraph-level rebuild** strategy (see `docx` skill) to handle
  placeholders that Word has split across XML runs.
- Process: main body paragraphs → table cells (recursive) → headers/footers.
- Conditional blocks may span **multiple paragraphs**, so collect paragraphs
  between IF/END_IF markers and remove or keep them as a group.

## Algorithm

### 1. Load document and data

```python
from docx import Document
import json, re

with open('employee_data.json') as f:
    data = json.load(f)

doc = Document('offer_letter_template.docx')
```

### 2. Handle multi-paragraph conditional blocks first

Conditional blocks often span several paragraphs. Scan all paragraphs, track
state, and remove or keep the block:

```python
def process_conditionals(paragraphs, data):
    """
    Walk paragraph list; for each IF/END_IF pair decide to keep or drop.
    Returns list of paragraphs to DELETE from the document.
    """
    to_delete = []
    in_block = False
    condition_met = False
    block_paras = []
    condition_key = None

    for para in paragraphs:
        text = para.text

        # Detect opening marker  (may also contain content on same line)
        if_match = re.search(r'\{\{IF_([A-Z_]+)\}\}', text)
        end_match = re.search(r'\{\{END_IF_([A-Z_]+)\}\}', text)

        if if_match and not in_block:
            condition_key = if_match.group(1)
            condition_met = data.get(condition_key, '').strip().lower() == 'yes'
            in_block = True
            block_paras = [para]

        elif end_match and in_block and end_match.group(1) == condition_key:
            block_paras.append(para)
            if condition_met:
                # Keep content but strip IF/END_IF markers
                for p in block_paras:
                    clean = p.text
                    clean = re.sub(r'\{\{IF_[A-Z_]+\}\}', '', clean)
                    clean = re.sub(r'\{\{END_IF_[A-Z_]+\}\}', '', clean)
                    if p.runs:
                        p.runs[0].text = clean.strip()
                        for r in p.runs[1:]:
                            r.text = ''
            else:
                to_delete.extend(block_paras)
            in_block = False
            block_paras = []

        elif in_block:
            block_paras.append(para)

    return to_delete


def delete_paragraphs(para_list):
    """Remove paragraphs from the document XML."""
    from docx.oxml.ns import qn
    for para in para_list:
        p = para._element
        p.getparent().remove(p)
```

### 3. Replace placeholders in a paragraph

```python
def replace_in_para(para, data):
    text = para.text
    if not re.search(r'\{\{[A-Z_]+\}\}', text):
        return
    new_text = text
    for key, val in data.items():
        new_text = new_text.replace('{{' + key + '}}', str(val))
    if new_text != text and para.runs:
        para.runs[0].text = new_text
        for run in para.runs[1:]:
            run.text = ''
```

### 4. Process all locations

```python
def process_table(table, data):
    for row in table.rows:
        for cell in row.cells:
            to_del = process_conditionals(cell.paragraphs, data)
            delete_paragraphs(to_del)
            for para in cell.paragraphs:
                replace_in_para(para, data)
            for nested in cell.tables:
                process_table(nested, data)

# Main body
to_del = process_conditionals(list(doc.paragraphs), data)
delete_paragraphs(to_del)

for para in doc.paragraphs:
    replace_in_para(para, data)

for table in doc.tables:
    process_table(table, data)

# Headers / footers
for section in doc.sections:
    for para in section.header.paragraphs:
        replace_in_para(para, data)
    for para in section.footer.paragraphs:
        replace_in_para(para, data)
```

### 5. Save

```python
doc.save('/root/offer_letter_filled.docx')
```

## Conditional Field Mapping

| JSON field            | Condition key  | Trigger value |
|-----------------------|----------------|---------------|
| RELOCATION_PACKAGE    | RELOCATION     | Yes           |

Check `data.get('RELOCATION_PACKAGE')` against `'Yes'` (case-insensitive) to
decide whether to keep `{{IF_RELOCATION}}...{{END_IF_RELOCATION}}` blocks.

## Common Pitfalls

- Conditional markers may appear inline with other text on the same paragraph.
- Always process conditionals **before** placeholder replacement so markers
  are gone before the final text pass.
- `doc.paragraphs` is a flat list; tables have their own paragraph trees.
- Deleting paragraphs modifies the XML tree — build the delete list first,
  then remove after the scan loop.
