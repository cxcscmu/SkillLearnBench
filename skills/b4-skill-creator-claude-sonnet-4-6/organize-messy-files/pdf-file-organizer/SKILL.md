---
name: pdf-file-organizer
description: Organizes PDF, PPTX, and DOCX academic files into subject folders by extracting and analyzing their title/abstract text. Use this skill whenever the user needs to sort or categorize a batch of research papers or documents into topic-based folders (e.g., LLM, quantum computing, biology, physics, music). Handles arXiv papers and other academic documents automatically.
---

# PDF File Organizer Skill

Classifies and moves academic documents (PDF, PPTX, DOCX) into subject-specific folders based on their content.

## Workflow

### 1. Extract Text for Classification

Use `pdftotext` (first page only for speed) to get title + abstract:
```bash
pdftotext -l 1 file.pdf - 2>/dev/null | head -30
```

For PPTX/DOCX, use python-pptx or python-docx, or rely on filename/metadata.

### 2. Classify by Keywords

Match extracted text against subject keyword sets:

| Subject | Key terms |
|---------|-----------|
| LLM | transformer, language model, GPT, BERT, attention, token, fine-tuning, prompt, LLM, NLP, neural network, RAG, reasoning |
| trapped_ion_and_qc | trapped ion, qubit, quantum gate, quantum circuit, quantum error, entanglement, laser cooling, quantum computing, Jaynes-Cummings |
| black_hole | black hole, event horizon, Hawking, gravitational wave, neutron star, spacetime, singularity, general relativity, entropy |
| DNA | DNA, gene, genome, protein, RNA, nucleotide, CRISPR, mutation, sequence, chromosome, molecular biology |
| music_history | music, composer, symphony, baroque, classical period, opera, melody, harmony, instrument, jazz, folk |

### 3. Batch Processing Strategy

For 100+ files, use a shell script to extract text and classify in bulk:

```bash
for f in /path/to/files/*.pdf; do
    text=$(pdftotext -l 1 "$f" - 2>/dev/null | head -40)
    # classify based on text content
    # move to appropriate folder
done
```

### 4. Create Target Folders

```bash
mkdir -p base_dir/{LLM,trapped_ion_and_qc,black_hole,DNA,music_history}
```

### 5. Handle Edge Cases

- If classification is ambiguous, pick the best-matching single folder
- Every file must end up in exactly one folder
- Never rename files or modify their content
- For non-PDF files (PPTX, DOCX), extract text with appropriate tools or use filename heuristics

## Python Classification Script Pattern

```python
import subprocess, shutil, os

SUBJECTS = {
    'LLM': ['language model', 'transformer', 'gpt', 'bert', 'llm', 'attention mechanism',
            'neural network', 'nlp', 'fine-tun', 'token', 'prompt', 'rag', 'reasoning model'],
    'trapped_ion_and_qc': ['trapped ion', 'qubit', 'quantum gate', 'quantum circuit',
                            'quantum error', 'entanglement', 'quantum comput', 'laser cool',
                            'jaynes-cummings', 'quant-ph', 'ion trap'],
    'black_hole': ['black hole', 'event horizon', 'hawking', 'gravitational', 'neutron star',
                   'spacetime', 'singularity', 'general relativity', 'horizon entropy'],
    'DNA': ['dna', 'gene', 'genome', 'protein', 'rna', 'nucleotide', 'crispr',
            'chromosome', 'molecular biology', 'base pair', 'sequence'],
    'music_history': ['music', 'composer', 'symphony', 'baroque', 'opera', 'melody',
                      'harmony', 'instrument', 'jazz', 'folk', 'classical music'],
}

def classify(text):
    text_lower = text.lower()
    scores = {subj: sum(1 for kw in kws if kw in text_lower)
              for subj, kws in SUBJECTS.items()}
    return max(scores, key=scores.get)
```
