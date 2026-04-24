---
name: document_content_extraction
description: Robustly extracts text from PDF, DOCX, and PPTX files while maintaining structural integrity for multi-column layouts and nested elements.
---
To ensure high-fidelity text extraction:
1. **PDFs**: Utilize `pdfplumber` or `PyMuPDF` with layout-aware parsing enabled to prevent text jumbling in multi-column academic papers.
2. **DOCX**: Use `python-docx` to extract text from body paragraphs, tables, and headers while ignoring metadata that may cause noise.
3. **PPTX**: Use `python-pptx` to iterate through slides, specifically extracting text from text frames and shapes to capture slide content.
4. **Fallback**: If text extraction fails (e.g., scanned PDFs), use an OCR fallback (e.g., `pytesseract`) to ensure the file is still categorizable.