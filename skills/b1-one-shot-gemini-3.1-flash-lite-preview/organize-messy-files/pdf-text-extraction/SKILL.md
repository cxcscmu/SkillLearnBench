---
name: pdf-text-extraction
description: Use this skill to extract text from PDF files to determine their subject matter.
---
# PDF Text Extraction Skill

This skill provides a mechanism to extract text from PDF files using `pdftotext` (part of poppler-utils) to identify keywords for subject classification.

## Usage
`pdftotext <file.pdf> - | head -n 20`
This extracts the first 20 lines of a PDF, which is typically sufficient to determine the paper's subject (Title, Abstract, etc.).
