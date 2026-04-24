---
name: document-classifier
description: How to classify and organize documents (PDFs, DOCX, PPTX) into categories based on their content. Use this skill whenever the user mentions organizing, sorting, or classifying documents into subjects or folders, even if they don't explicitly ask for it.
---
# Document Classifier

A guide for classifying and organizing a large number of documents (PDFs, DOCX, PPTX) into specific folders based on their subject matter.

## Overview

When asked to organize files into categories, use text extraction libraries and an LLM classification script to efficiently process and move the files.

## Workflow

1. **Create Target Folders**: Ensure the destination folders exist.
2. **Text Extraction**: Read a small snippet of text from each document (e.g., first few pages or paragraphs).
   - **PDF**: Use `pdftotext` (via `subprocess`) or `pdfplumber`/`pypdf` to extract the first page.
   - **DOCX**: Use `pandoc` or extract the raw XML and read a bit of it, or use `python-docx` if available, or just grep for text.
   - **PPTX**: Extract text using `python -m markitdown` or by unpacking.
3. **Classification**: 
   - Write a python script to process all files.
   - For each file, extract text (first page is usually enough for academic papers).
   - Use simple keyword matching or regex if categories are distinct (e.g., "LLM", "quantum", "black hole", "DNA", "music").
   - Move the file to the corresponding folder based on the match.
   - If a file doesn't match the first 4 specific categories, move it to the 5th default category.
4. **Execution**: Run the script and verify that all files have been moved and no files are left out.

## Example Classification Logic

```python
import os
import shutil
import subprocess

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        result = subprocess.run(['pdftotext', '-l', '2', file_path, '-'], capture_output=True, text=True)
        return result.stdout.lower()
    elif file_path.endswith('.docx'):
        result = subprocess.run(['pandoc', file_path, '-t', 'plain'], capture_output=True, text=True)
        return result.stdout.lower()
    elif file_path.endswith('.pptx'):
        result = subprocess.run(['python', '-m', 'markitdown', file_path], capture_output=True, text=True)
        return result.stdout.lower()
    return ""

def classify_and_move(source_dir, dest_dirs):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            text = extract_text(file_path)
            
            # Simple keyword matching
            if 'llm' in text or 'language model' in text or 'transformer' in text:
                target = dest_dirs['LLM']
            elif 'quantum' in text or 'trapped ion' in text or 'qubit' in text:
                target = dest_dirs['trapped_ion_and_qc']
            elif 'black hole' in text or 'schwarzschild' in text or 'hawking' in text:
                target = dest_dirs['black_hole']
            elif 'dna' in text or 'gene' in text or 'genome' in text or 'chromosome' in text:
                target = dest_dirs['DNA']
            else:
                target = dest_dirs['music_history']
                
            shutil.move(file_path, os.path.join(target, file))
```

## Troubleshooting

- If `pdftotext` is missing, install it via `sudo apt-get install poppler-utils`.
- Only process files with known extensions to avoid errors.
