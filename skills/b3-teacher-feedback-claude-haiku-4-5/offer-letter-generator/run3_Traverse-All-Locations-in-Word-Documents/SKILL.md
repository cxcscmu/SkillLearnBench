---
name: Traverse All Locations in Word Documents
description: Use this skill when you need to find and process text in Word documents beyond just `doc.paragraphs`. Include tables, headers, and footers to ensure no content is missed.
---

## Locations to Process

1. **Main body paragraphs**: `doc.paragraphs`
2. **Table cells**: Iterate `doc.tables` → rows → cells → paragraphs
3. **Headers**: `doc.sections[*].header.paragraphs`
4. **Footers**: `doc.sections[*].footer.paragraphs`

## Algorithm

```
def get_all_paragraphs(doc):
    paragraphs = []
    
    # Main body
    paragraphs.extend(doc.paragraphs)
    
    # Tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                paragraphs.extend(cell.paragraphs)
    
    # Headers and footers
    for section in doc.sections:
        paragraphs.extend(section.header.paragraphs)
        paragraphs.extend(section.footer.paragraphs)
    
    return paragraphs
```

## Processing Strategy

- Use this function when you need to process all text locations (replacements, conditional handling, validation)
- Maintain iteration order to ensure markers like `{{IF_*}}` and `{{END_IF_*}}` are encountered in the correct sequence
- Collect elements to delete first, then delete after iteration completes