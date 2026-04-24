---
name: content-classification
description: Classify documents by subject using keyword matching and text analysis
---

# Document Content Classification

## Overview
Classify extracted text into one of 5 subject categories using keyword-based analysis.

## Subject Categories and Keywords

### 1. LLM (Large Language Models)
Keywords: transformer, BERT, GPT, language model, attention mechanism, token, embedding, fine-tuning, prompt, neural network, deep learning, NLP, natural language processing

### 2. Trapped Ion and Quantum Computing
Keywords: trapped ion, quantum computing, qubit, quantum gate, quantum circuit, ion trap, quantum algorithm, quantum error correction, quantum entanglement, quantum state

### 3. Black Hole
Keywords: black hole, event horizon, singularity, gravitational, spacetime, Hawking radiation, accretion disk, neutron star, gravitational wave, relativistic

### 4. DNA
Keywords: DNA, gene, genome, genomics, protein, mutation, sequencing, nucleotide, chromosome, genetic, CRISPR, RNA, molecular biology

### 5. Music History
Keywords: music, composer, symphony, opera, musical, concert, melody, harmony, rhythm, baroque, classical, romantic, jazz, folk, baroque, beethoven, mozart, wagner

## Classification Algorithm

```python
def classify_document(text):
    """Classify document based on keyword frequency"""

    keywords = {
        'LLM': ['transformer', 'bert', 'gpt', 'language model', 'attention', 'token', 'embedding', 'fine-tuning', 'prompt', 'nlp'],
        'trapped_ion_and_qc': ['trapped ion', 'quantum', 'qubit', 'quantum gate', 'ion trap', 'quantum algorithm'],
        'black_hole': ['black hole', 'event horizon', 'singularity', 'hawking', 'gravitational', 'spacetime'],
        'DNA': ['dna', 'gene', 'genome', 'genomics', 'protein', 'mutation', 'sequencing', 'nucleotide', 'crispr'],
        'music_history': ['music', 'composer', 'symphony', 'opera', 'melody', 'harmony', 'baroque', 'classical', 'mozart', 'beethoven']
    }

    text_lower = text.lower()
    scores = {}

    for category, words in keywords.items():
        score = 0
        for word in words:
            # Count occurrences (case-insensitive)
            score += text_lower.count(word)
        scores[category] = score

    # Return category with highest score
    best_category = max(scores, key=scores.get)

    # If all scores are 0, default to music_history (catch-all)
    if scores[best_category] == 0:
        return 'music_history'

    return best_category

def get_classification_confidence(text, category):
    """Return confidence score (0-1) for a classification"""
    keywords = {
        'LLM': ['transformer', 'bert', 'gpt', 'language model', 'attention'],
        'trapped_ion_and_qc': ['quantum', 'qubit', 'ion trap'],
        'black_hole': ['black hole', 'event horizon'],
        'DNA': ['dna', 'gene', 'genome'],
        'music_history': ['music', 'composer', 'symphony']
    }

    text_lower = text.lower()
    score = sum(text_lower.count(word) for word in keywords.get(category, []))

    # Normalize to 0-1 range
    max_possible = len(keywords.get(category, [])) * 10
    return min(score / max_possible, 1.0) if max_possible > 0 else 0
```

## Best Practices
- Use case-insensitive matching
- Count keyword occurrences, not just presence
- Handle edge cases with a default category
- Consider confidence scores for ambiguous documents
- Prioritize more specific keywords over generic ones
