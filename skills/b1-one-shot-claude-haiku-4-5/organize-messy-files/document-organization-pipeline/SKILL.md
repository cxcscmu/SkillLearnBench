---
name: document-organization-pipeline
description: End-to-end pipeline for extracting, classifying, and organizing documents by subject
---

# Complete Document Organization Pipeline

## Overview
Orchestrates the full workflow: scan files → extract text → classify → organize into folders.

## Complete Implementation

```python
import os
import shutil
from pathlib import Path
import pdfplumber
from docx import Document
from pptx import Presentation

class DocumentOrganizer:
    def __init__(self, source_dir, output_dir):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.target_categories = [
            'LLM',
            'trapped_ion_and_qc',
            'black_hole',
            'DNA',
            'music_history'
        ]
        self.results = {
            'total': 0,
            'classified': {},
            'errors': []
        }

    def scan_files(self):
        """Find all processable files"""
        valid_extensions = {'.pdf', '.docx', '.pptx'}
        files = []

        for root, dirs, filenames in os.walk(self.source_dir):
            for filename in filenames:
                if Path(filename).suffix.lower() in valid_extensions:
                    files.append(os.path.join(root, filename))

        return files

    def extract_text(self, file_path):
        """Extract text from any supported file type"""
        try:
            ext = Path(file_path).suffix.lower()

            if ext == '.pdf':
                return self._extract_pdf(file_path)
            elif ext == '.docx':
                return self._extract_docx(file_path)
            elif ext == '.pptx':
                return self._extract_pptx(file_path)
        except Exception as e:
            self.results['errors'].append((file_path, str(e)))
            return ""

    def _extract_pdf(self, pdf_path):
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num in range(min(3, len(pdf.pages))):
                    text += pdf.pages[page_num].extract_text() or ""
                    if len(text) > 5000:
                        break
        except:
            return ""
        return text[:5000]

    def _extract_docx(self, docx_path):
        """Extract text from DOCX"""
        text = ""
        try:
            doc = Document(docx_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
                if len(text) > 5000:
                    break
        except:
            return ""
        return text[:5000]

    def _extract_pptx(self, pptx_path):
        """Extract text from PPTX"""
        text = ""
        try:
            prs = Presentation(pptx_path)
            for slide_num, slide in enumerate(prs.slides):
                if slide_num >= 5:
                    break
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
                        if len(text) > 5000:
                            return text[:5000]
        except:
            return ""
        return text[:5000]

    def classify_document(self, text):
        """Classify document into one of 5 categories"""
        keywords = {
            'LLM': ['transformer', 'bert', 'gpt', 'language model', 'attention',
                   'token', 'embedding', 'fine-tuning', 'prompt', 'nlp', 'neural'],
            'trapped_ion_and_qc': ['trapped ion', 'quantum', 'qubit', 'quantum gate',
                                  'ion trap', 'quantum algorithm', 'quantum circuit'],
            'black_hole': ['black hole', 'event horizon', 'singularity', 'hawking',
                          'gravitational', 'spacetime', 'relativistic'],
            'DNA': ['dna', 'gene', 'genome', 'genomics', 'protein', 'mutation',
                   'sequencing', 'nucleotide', 'crispr', 'rna', 'chromosome'],
            'music_history': ['music', 'composer', 'symphony', 'opera', 'melody',
                             'harmony', 'rhythm', 'baroque', 'classical', 'mozart',
                             'beethoven', 'wagner', 'concert', 'musical']
        }

        text_lower = text.lower()
        scores = {}

        for category, words in keywords.items():
            score = sum(text_lower.count(word) for word in words)
            scores[category] = score

        best_category = max(scores, key=scores.get)
        if scores[best_category] == 0:
            return 'music_history'  # Default catch-all

        return best_category

    def organize(self):
        """Run the complete organization pipeline"""
        print("Step 1: Creating target folders...")
        self._create_folders()

        print("Step 2: Scanning files...")
        files = self.scan_files()
        print(f"Found {len(files)} files to process")

        print("Step 3: Processing files...")
        for file_path in files:
            print(f"Processing: {os.path.basename(file_path)}")

            # Extract text
            text = self.extract_text(file_path)
            if not text:
                self.results['errors'].append((file_path, "Failed to extract text"))
                continue

            # Classify
            category = self.classify_document(text)

            # Move file
            self._move_file(file_path, category)

            self.results['total'] += 1
            self.results['classified'][category] = self.results['classified'].get(category, 0) + 1

        print("\nStep 4: Organization complete!")
        self._print_summary()

    def _create_folders(self):
        """Create target category folders"""
        for category in self.target_categories:
            folder = os.path.join(self.output_dir, category)
            os.makedirs(folder, exist_ok=True)

    def _move_file(self, source_path, category):
        """Move file to category folder"""
        dest_folder = os.path.join(self.output_dir, category)
        filename = os.path.basename(source_path)
        dest_path = os.path.join(dest_folder, filename)

        # Handle duplicates
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1

        try:
            shutil.move(source_path, dest_path)
        except Exception as e:
            self.results['errors'].append((source_path, str(e)))

    def _print_summary(self):
        """Print organization summary"""
        print("\n" + "="*50)
        print("ORGANIZATION SUMMARY")
        print("="*50)
        print(f"Total files processed: {self.results['total']}")
        for category in self.target_categories:
            count = self.results['classified'].get(category, 0)
            print(f"  {category}: {count} files")

        if self.results['errors']:
            print(f"\nErrors ({len(self.results['errors'])}):")
            for file_path, error in self.results['errors'][:5]:  # Show first 5
                print(f"  {os.path.basename(file_path)}: {error}")
            if len(self.results['errors']) > 5:
                print(f"  ... and {len(self.results['errors']) - 5} more")

# Usage
if __name__ == "__main__":
    organizer = DocumentOrganizer(
        source_dir="/path/to/source/files",
        output_dir="/path/to/output"
    )
    organizer.organize()
```

## Pipeline Flow
1. **Scan** - Find all PDF, DOCX, PPTX files
2. **Extract** - Pull text from first few pages/slides
3. **Classify** - Match keywords to determine subject
4. **Organize** - Move files to category folders
5. **Report** - Summary of results and errors

## Usage
```python
organizer = DocumentOrganizer(source_dir, output_dir)
organizer.organize()
```
