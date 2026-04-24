---
name: word-placeholder-replacement
description: Replace placeholders in Word documents (.docx files) and handle conditional sections. Use this skill whenever you need to fill in {{PLACEHOLDER}} markers in a .docx template, or when working with conditional blocks like {{IF_CONDITION}}...{{END_IF_CONDITION}}.
---

# Word Placeholder Replacement

This skill demonstrates how to replace placeholders in Word documents (.docx) using the `python-docx` library and handle conditional sections.

## Overview

Word documents (.docx files) are XML-based. The `python-docx` library allows you to:
- Read and modify document content
- Replace placeholders like `{{CANDIDATE_FULL_NAME}}`
- Handle conditional blocks (`{{IF_*}}...{{END_IF_*}}`)
- Preserve formatting

## Key Concepts

### Placeholder Format
- Placeholders follow the format: `{{PLACEHOLDER_NAME}}`
- They can appear in paragraphs, tables, or headers/footers
- Text may be split across runs (XML nodes) in the document tree

### Conditional Sections
- Format: `{{IF_CONDITION}}content{{END_IF_CONDITION}}`
- If the condition is true, keep the content and remove markers
- If false, remove the entire section including markers

## Implementation Pattern

```python
from docx import Document

def replace_placeholders_in_docx(template_path, data_dict, output_path):
    """
    Replace placeholders in a Word document.

    Args:
        template_path: Path to the template .docx file
        data_dict: Dictionary with placeholder names as keys
        output_path: Where to save the filled document
    """
    doc = Document(template_path)

    # Reconstruct full text to handle split placeholders
    full_text = get_document_full_text(doc)

    # Replace placeholders
    for key, value in data_dict.items():
        full_text = full_text.replace(f'{{{{{key}}}}}', str(value))

    # Handle conditional sections
    full_text = process_conditionals(full_text)

    # Apply changes back to document
    apply_text_to_document(doc, full_text)

    doc.save(output_path)
```

## Handling Split Placeholders

Placeholders can be split across multiple runs. Example:
- Run 1: `{{CANDI`
- Run 2: `DATE_FULL_NAME}}`

**Solution**: Reconstruct the full text from all runs, perform replacement, then update the document.

## Processing Conditional Sections

Pattern for conditionals:
```
{{IF_RELOCATION_PACKAGE}}
This employee receives relocation support of $15,000.
{{END_IF_RELOCATION_PACKAGE}}
```

**Logic**:
1. Find all `{{IF_*}}...{{END_IF_*}}` blocks
2. Evaluate the condition against your data
3. If true: keep content, remove markers
4. If false: remove entire section

## Document Structure Reference

- `doc.paragraphs` - Access document paragraphs
- `doc.tables` - Access tables
- `paragraph.runs` - Individual formatted text segments
- `table.rows`, `table.cells` - Table structure

## Common Gotchas

1. **Split placeholders**: Always reconstruct full text before replacing
2. **Preserving formatting**: Use paragraph-level operations when possible
3. **Line breaks**: Conditional blocks may span multiple paragraphs
4. **Tables**: Replacements work within table cells too

## Testing

After replacement:
- Verify all placeholders were replaced
- Check conditional sections handled correctly
- Ensure document opens without errors
- Validate formatting is preserved
