---
name: pdf-extraction
description: Extracts text from PDF documents for content analysis.
---

# PDF Extraction Skill

This skill provides methods for extracting text from PDF files, which is essential for categorizing academic papers and documents.

## Methods

### 1. Using `pdftotext` (Command Line)
`pdftotext` is a fast utility for converting PDF files to plain text.

```bash
pdftotext "filename.pdf" "output.txt"
```

To read the first few pages (often enough for classification):
```bash
pdftotext -f 1 -l 2 "filename.pdf" - | head -n 50
```

### 2. Using Gemini CLI `pdf` Skill
If the `pdf` skill is activated, you can use its tools to extract text or analyze forms.

```javascript
// Example usage after activating skill
await pdf.extractText({ file_path: "document.pdf" });
```

## Usage Pattern for Classification
1. Extract the first page or the abstract.
2. Search for key terms related to the target subjects.
3. Use the extracted text to decide the destination folder.
