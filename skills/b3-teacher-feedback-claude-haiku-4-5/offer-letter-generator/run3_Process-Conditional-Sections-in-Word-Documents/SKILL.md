---
name: Process Conditional Sections in Word Documents
description: Use this skill to handle conditional content blocks marked with {{IF_CONDITION}}...{{END_IF_CONDITION}} in Word documents. Keep or remove the entire block based on a condition, and clean up the marker text. Apply this during paragraph processing, not as a separate pass, to avoid structural issues with modified paragraphs.
---

## Key Principles

1. **Process conditionals inline**: Handle `{{IF_*}}` and `{{END_IF_*}}` markers during the same pass as placeholder replacement, not in a separate preprocessing step
2. **Track state across paragraphs**: Use a flag to track whether you're inside a conditional block
3. **Clean marker text properly**: Use regex-based replacement on runs to completely remove markers, not just `.replace()` on paragraph text
4. **Process all locations**: Check paragraphs in `doc.paragraphs`, tables, headers, and footers

## Algorithm

```
inside_conditional = False
condition_keep = None
paragraphs_to_delete = []

for each paragraph in all_locations (doc.paragraphs, tables, headers, footers):
    if paragraph contains {{IF_*}}:
        inside_conditional = True
        condition_name = extract_condition_name()
        condition_keep = evaluate_condition(condition_name)
        remove_marker_from_paragraph(paragraph, regex-based)
    
    elif paragraph contains {{END_IF_*}}:
        inside_conditional = False
        remove_marker_from_paragraph(paragraph, regex-based)
    
    else:
        if inside_conditional and not condition_keep:
            paragraphs_to_delete.append(paragraph)
        else:
            process_placeholder_replacements(paragraph)

delete_all_marked_paragraphs(paragraphs_to_delete)
```

## Implementation Notes

- Extract condition name with regex: `r'{{IF_(\w+)}}'`
- Use `paragraph._element.getparent().remove(paragraph._element)` to delete paragraphs safely
- Remove markers with the same regex-based `replace_placeholders_in_text()` function used for other placeholders
- Collect paragraphs to delete first, then delete them after iteration (never modify a list while iterating)