---
name: text-classification-heuristics
description: Classifies text into predefined categories using keyword matching heuristics.
---

# Text Classification Heuristics

Classifies text into categories: LLM, Trapped Ion and Quantum Computing, Black Hole, DNA, and Music History.

## Python Example

```python
import re

def classify_text(text):
    text = text.lower()
    
    # Define keywords for each category
    keywords = {
        'LLM': ['llm', 'large language model', 'gpt', 'transformer', 'attention mechanism', 'chatgpt', 'natural language processing', 'prompt', 'few-shot', 'zero-shot'],
        'trapped_ion_and_qc': ['quantum', 'qubit', 'trapped ion', 'entanglement', 'ion trap', 'quantum computing', 'superposition', 'decoherence'],
        'black_hole': ['black hole', 'event horizon', 'singularity', 'hawking radiation', 'general relativity', 'schwarzschild', 'accretion disk', 'gravitational wave'],
        'DNA': ['dna', 'genome', 'gene', 'chromosome', 'crispr', 'nucleotide', 'sequencing', 'genetics', 'rna', 'double helix', 'mutation'],
        'music_history': ['music', 'composer', 'symphony', 'baroque', 'classical period', 'renaissance', 'mozart', 'beethoven', 'bach', 'harmony', 'melody', 'musical instrument']
    }
    
    scores = {category: 0 for category in keywords}
    
    for category, words in keywords.items():
        for word in words:
            # Count occurrences using regex to match whole words/phrases
            scores[category] += len(re.findall(r'\b' + re.escape(word) + r'\b', text))
            
    # Return the category with the highest score
    # Default to a specific category if all scores are 0 (e.g. music_history as per instructions)
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return 'music_history' # or whichever default is suitable
        
    return best_category
```
