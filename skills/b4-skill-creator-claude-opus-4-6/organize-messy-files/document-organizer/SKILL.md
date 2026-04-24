---
name: document-organizer
description: Organizes mixed document files (PDF, PPTX, DOCX) into subject-based folders by analyzing content. Use this skill when sorting, categorizing, or organizing documents into topic folders.
---

# Document Organizer

Sorts documents of various formats into predefined subject folders based on content analysis.

## Workflow

1. **Inventory** all files in the source directory
2. **Extract text** from each file format:
   - PDF: use PyPDF2 to extract text from first pages
   - DOCX: use python-docx to read paragraphs
   - PPTX: use python-pptx to read slide text
3. **Classify** each file using keyword-based scoring (see pdf-classifier skill)
4. **Move** files to target folders using shutil.move()
5. **Verify** all files are moved, none left behind

## Target Folder Structure

```
papers/
├── LLM/
├── trapped_ion_and_qc/
├── black_hole/
├── DNA/
└── music_history/
```

## Key Principles

- Never rename files — preserve original filenames
- Never modify file content
- Each file goes to exactly one folder
- If a file doesn't clearly match any of the first 4 categories, assign it to `music_history` (the catch-all)
- Process all file types (PDF, DOCX, PPTX) with format-appropriate text extraction

## Python Dependencies

- `PyPDF2` for PDFs
- `python-docx` for DOCX files
- `python-pptx` for PPTX files
- All available via pip if not already installed
