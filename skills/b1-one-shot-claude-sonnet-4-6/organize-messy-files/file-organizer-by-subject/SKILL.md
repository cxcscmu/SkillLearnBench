---
name: file-organizer-by-subject
description: Organize files into subject folders using keyword-based classification of titles and abstracts, with fallback to full text extraction.
---

# File Organizer by Subject Skill

## Overview
Classify and move files (PDF, PPTX, DOCX) into subject folders using keyword matching on metadata and text content.

## Folder Setup
```python
import os, shutil

def create_subject_folders(base_dir, subjects):
    for subject in subjects:
        os.makedirs(os.path.join(base_dir, subject), exist_ok=True)

SUBJECTS = ['LLM', 'trapped_ion_and_qc', 'black_hole', 'DNA', 'music_history']
```

## Keyword-Based Classifier
```python
KEYWORDS = {
    'LLM': [
        'language model', 'large language', 'llm', 'gpt', 'bert', 'transformer',
        'attention mechanism', 'natural language', 'nlp', 'text generation',
        'chatgpt', 'instruction tuning', 'rlhf', 'tokenization', 'embedding',
        'fine-tuning', 'prompt', 'in-context learning', 'chain of thought'
    ],
    'trapped_ion_and_qc': [
        'trapped ion', 'ion trap', 'quantum computing', 'qubit', 'quantum gate',
        'quantum circuit', 'quantum error', 'decoherence', 'quantum entanglement',
        'quantum supremacy', 'quantum advantage', 'quantum processor',
        'laser cooling', 'penning trap', 'paul trap', 'quantum memory',
        'quantum simulation', 'quantum algorithm', 'shor', 'grover'
    ],
    'black_hole': [
        'black hole', 'event horizon', 'hawking radiation', 'singularity',
        'general relativity', 'gravitational wave', 'neutron star', 'pulsar',
        'accretion disk', 'kerr', 'schwarzschild', 'spacetime', 'cosmology',
        'dark matter', 'dark energy', 'galaxy', 'astrophysics', 'quasar',
        'gravitational lensing', 'wormhole', 'holography', 'ads/cft'
    ],
    'DNA': [
        'dna', 'rna', 'genome', 'gene', 'protein', 'crispr', 'sequencing',
        'mutation', 'chromosome', 'nucleotide', 'base pair', 'replication',
        'transcription', 'translation', 'epigenetics', 'pcr', 'molecular biology',
        'bioinformatics', 'phylogenetic', 'evolution', 'cell', 'enzyme'
    ],
    'music_history': [
        'music', 'musical', 'composer', 'symphony', 'opera', 'baroque',
        'renaissance', 'classical music', 'jazz', 'rock', 'instrument',
        'melody', 'harmony', 'rhythm', 'orchestra', 'sonata', 'concerto',
        'beethoven', 'mozart', 'bach', 'history of music', 'musicology'
    ]
}

def classify_by_keywords(text, title=""):
    """Return subject with highest keyword match score."""
    combined = (title + " " + text).lower()
    scores = {}
    for subject, keywords in KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        scores[subject] = score

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None  # No match found
    return best
```

## Moving Files
```python
def move_file(src_path, dest_folder):
    """Move file to destination folder, preserving filename."""
    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_folder, filename)
    shutil.move(src_path, dest_path)
    return dest_path
```

## Complete Pipeline
```python
def organize_files(source_dir, dest_base_dir, subjects):
    create_subject_folders(dest_base_dir, subjects)

    files = list(Path(source_dir).iterdir())
    unclassified = []

    for f in files:
        text = extract_text_from_file(f)
        title = extract_title(f)
        subject = classify_by_keywords(text, title)

        if subject:
            move_file(str(f), os.path.join(dest_base_dir, subject))
        else:
            unclassified.append(f)

    return unclassified
```

## Handling PPTX and DOCX
```python
from pptx import Presentation
from docx import Document

def extract_text_pptx(path):
    prs = Presentation(path)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return " ".join(text)

def extract_text_docx(path):
    doc = Document(path)
    return " ".join([p.text for p in doc.paragraphs])
```

## Strategy Notes
- Start with arxiv API for PDF files with arxiv-style names (fast, no local processing)
- Fall back to PDF text extraction for unrecognized files
- Use keyword scoring rather than LLM for reproducibility
- If score is tied, use arxiv category codes as tiebreaker
