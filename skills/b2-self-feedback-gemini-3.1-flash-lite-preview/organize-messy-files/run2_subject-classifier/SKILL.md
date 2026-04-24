---
name: subject-classifier
description: Maps extracted text to one of the 5 defined subjects.
---
# Subject Classifier Skill

Classifies text into: LLM, trapped_ion_and_qc, black_hole, DNA, or music_history.

## Usage
```python
def classify(text):
    text = text.lower()
    mapping = {
        'LLM': ['language model', 'transformer', 'attention', 'gpt', 'llm'],
        'trapped_ion_and_qc': ['trapped ion', 'quantum computer', 'qubit', 'entanglement'],
        'black_hole': ['black hole', 'event horizon', 'singularity'],
        'DNA': ['dna', 'genome', 'protein', 'gene', 'sequencing']
    }
    for category, keywords in mapping.items():
        if any(keyword in text for keyword in keywords):
            return category
    return 'music_history'
```
