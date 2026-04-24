---
name: classify_scientific_document
description: Categorizes a document into one of five subjects (LLM, trapped_ion_and_qc, black_hole, DNA, music_history) based on an expanded technical keyword dictionary. It prioritizes the beginning of the text (titles and abstracts) where subject density is highest.
---

```python
import re

def classify_document(text):
    """
    Classifies text into one of five categories using weighted keyword matching.
    Focuses on the first 2500 characters to capture titles, abstracts, and intros.
    """
    if not text:
        return "music_history" # Default fallback per instructions

    # Focus on the beginning of the document
    header_text = text[:2500].lower()

    keywords = {
        "LLM": [
            "large language model", "transformer", "gpt-3", "gpt-4", "bert", "attention mechanism",
            "neural network", "natural language processing", "nlp", "pre-training", "fine-tuning",
            "tokenization", "rlhf", "parameter-efficient", "context window", "inference", "llm"
        ],
        "trapped_ion_and_qc": [
            "trapped ion", "qubit", "quantum computing", "quantum gate", "paul trap", "laser cooling",
            "decoherence", "superposition", "entanglement", "quantum state", "rydberg", "ion-trap",
            "quantum circuit", "quantum information", "fidelity", "penning trap"
        ],
        "black_hole": [
            "black hole", "event horizon", "schwarzschild", "hawking radiation", "accretion",
            "general relativity", "spacetime", "gravitational wave", "kerr metric", "singularity",
            "astrophysics", "neutron star", "einstein field equations"
        ],
        "DNA": [
            "dna", "genome", "nucleotide", "sequencing", "crispr", "polymerase", "double helix",
            "genetic", "rna", "chromosome", "genomics", "base pair", "molecular biology",
            "nucleic acid", "methylation", "histone"
        ],
        "music_history": [
            "renaissance", "baroque", "classical era", "romantic era", "composer", "symphony",
            "sonata", "musicology", "orchestration", "notation", "period instrument", "opera",
            "monophonic", "polyphonic", "organology", "music history"
        ]
    }

    scores = {category: 0 for category in keywords}

    for category, terms in keywords.items():
        for term in terms:
            # Look for whole words or specific technical phrases
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = re.findall(pattern, header_text)
            scores[category] += len(matches)

    # Filter out categories with zero scores
    active_scores = {k: v for k, v in scores.items() if v > 0}
    
    if not active_scores:
        return "music_history" # Final fallback if no technical keywords found

    # Return category with highest match count
    return max(active_scores, key=active_scores.get)
```