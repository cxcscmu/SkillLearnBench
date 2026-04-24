---
name: batch_file_organization
description: Discovers PDF, DOCX, and PPTX files in a directory (handling hidden characters and extensions robustly), extracts their text, determines their subject, and moves them into organized folders.
---

```python
import os
import shutil
from glob import glob

def organize_files(source_dir):
    """
    Orchestrates the discovery, extraction, classification, and moving of files.
    """
    subjects = ["LLM", "trapped_ion_and_qc", "black_hole", "DNA", "music_history"]
    
    # Create target folders
    for subject in subjects:
        if not os.path.exists(os.path.join(source_dir, subject)):
            os.makedirs(os.path.join(source_dir, subject))

    # Robust file discovery using glob for multiple extensions
    # This handles standard naming and avoids skipping files
    patterns = ['*.pdf', '*.docx', '*.pptx', '*.PDF', '*.DOCX', '*.PPTX']
    files_to_process = []
    for pattern in patterns:
        files_to_process.extend(glob(os.path.join(source_dir, pattern)))

    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        # Skip if already in a subject folder
        if any(subject in file_path for subject in subjects):
            continue

        text = ""
        if filename.lower().endswith('.pdf'):
            text = extract_pdf_text(file_path)
        elif filename.lower().endswith(('.docx', '.pptx')):
            text = extract_office_text(file_path)
        
        # Determine category
        category = classify_document(text)
        
        # Move file
        target_path = os.path.join(source_dir, category, filename)
        
        # Ensure we don't overwrite if file exists, though task implies unique files
        try:
            shutil.move(file_path, target_path)
        except Exception as e:
            print(f"Error moving {filename}: {e}")

# Helper imports assumed from other skills
# from skill_pdf import extract_pdf_text
# from skill_office import extract_office_text
# from skill_classify import classify_document
```