---
name: file-classification
description: Classify academic papers and documents into subject categories using keyword-based text analysis.
---

# File Classification by Subject

## Approach: Keyword Scoring
For classifying documents into known categories, a keyword scoring approach is effective:

1. Define keyword sets for each category
2. Extract text from each document
3. Score text against each keyword set (count occurrences)
4. Assign document to highest-scoring category

## Keyword Sets for This Task

- **LLM**: language model, transformer, attention mechanism, GPT, BERT, token, prompt, fine-tuning, NLP, neural network, deep learning, text generation, embedding, LLM, large language, reinforcement learning from human feedback, RLHF, instruction tuning, pretraining, machine learning
- **Trapped ion / Quantum computing**: trapped ion, quantum computing, qubit, quantum gate, entanglement, quantum error, ion trap, quantum circuit, quantum algorithm, quantum processor, quantum information, Coulomb, motional mode, laser cooling, quantum simulation
- **Black hole**: black hole, event horizon, Hawking radiation, singularity, gravitational, spacetime, general relativity, accretion, Schwarzschild, Kerr, entropy, holographic, AdS/CFT, cosmological, dark energy, dark matter
- **DNA**: DNA, genome, gene expression, nucleotide, protein, sequencing, CRISPR, mutation, chromosome, transcription, RNA, epigenetic, genetic, molecular biology, bioinformatics, cell, amino acid
- **Music history**: music, composer, symphony, opera, baroque, classical period, jazz, rhythm, harmony, melody, instrument, musicology, sonata, concert, orchestra, musical

## Implementation Pattern

```python
def classify(text, keyword_sets):
    text_lower = text.lower()
    scores = {}
    for category, keywords in keyword_sets.items():
        scores[category] = sum(text_lower.count(kw.lower()) for kw in keywords)
    return max(scores, key=scores.get)
```
