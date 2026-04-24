---
name: Save Modified Word Document to Disk
description: Use this skill to write a modified python-docx Document object back to a .docx file, handling file paths and permissions correctly.
---

## Algorithm

```
def save_document(doc, output_path):
    try:
        doc.save(output_path)
        return True
    except Exception as e:
        raise IOError(f"Failed to save document to {output_path}: {e}")
```

## Key Details

- The output path should be an absolute or relative path to the desired `.docx` file
- `doc.save()` overwrites existing files
- Ensure the output directory exists or the parent path is writable
- Catch and report errors explicitly for debugging