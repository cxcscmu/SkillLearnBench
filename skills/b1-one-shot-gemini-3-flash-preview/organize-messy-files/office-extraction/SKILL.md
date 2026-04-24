---
name: office-extraction
description: Extracts text from DOCX and PPTX documents for content analysis.
---

# Office Extraction Skill

This skill provides methods for extracting text from Microsoft Office documents (.docx, .pptx).

## Methods

### 1. Using `docx2txt` or `pandoc`
If installed, these tools can convert Office docs to text.

```bash
# For DOCX
pandoc -t plain "document.docx" -o "output.txt"
```

### 2. Using Gemini CLI `docx` and `pptx` Skills
These specialized skills provide direct tools for document manipulation.

```javascript
// For DOCX
await docx.read_file({ file_path: "paper.docx" });

// For PPTX
await pptx.read_presentation({ file_path: "slides.pptx" });
```

### 3. Manual Extraction (unzip)
DOCX and PPTX are ZIP archives. You can unzip them and read the XML.

```bash
unzip -p "document.docx" word/document.xml | sed -e 's/<[^>]*>//g'
```

## Usage Pattern
Extract the main body text or titles to identify the document's subject matter.
