---
name: pdf-analyzer
description: Extracting text and metadata from PDF documents.
---

# PDF Analyzer Skill
Use this skill for reading content from PDF files, especially for structured data layouts like calendars.

## Usage
Utilize `read_file` with the appropriate path for PDF analysis. If complex extraction is needed, use standard library `PyPDF2` if installed, or rely on OCR-based extraction via `read_file` tool output.
