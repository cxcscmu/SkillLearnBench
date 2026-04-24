---
name: run2_keyword-classification
description: Classify academic papers into subject categories using weighted keyword matching with regex word boundaries and case-insensitive search.
---

# Keyword-Based Document Classification (Improved)

## Key Improvements from Round 1
1. **Use `re.IGNORECASE`** instead of lowercasing text - preserves case-sensitive acronyms like DNA, RNA, LLM in patterns while matching case-insensitively.
2. **Use `\b` word boundaries** in regex patterns to avoid substring false positives (e.g., "bar" in "Raman" matching music keyword "bar", "opera" matching "operator").
3. **Weight keywords by specificity**: Highly specific terms (e.g., "Schwarzschild", "CRISPR-Cas9") get higher weights than generic terms (e.g., "model", "system").
4. **Avoid ambiguous single-word keywords**: Words like "bar", "note", "rest", "measure", "scale", "opera" are common across domains. Either use multi-word phrases or add word boundaries.

## Algorithm
1. Extract text from each document (first 3 pages for PDFs, full text for PPTX/DOCX)
2. For each category, compute a weighted score by matching regex patterns case-insensitively
3. Assign document to the highest-scoring category
4. Default to `music_history` if no keywords matched (catch-all)

## Pattern Design Guidelines
- Use `\b` word boundaries for short/ambiguous words: `r"\bDNA\b"` not `"DNA"`
- Use multi-word phrases where possible: `"trapped ion"` not `"trapped"` or `"ion"`
- Assign higher weights (10) to domain-specific terms that uniquely identify a field
- Assign lower weights (1-2) to generic terms that appear across domains
- Use `re.findall(pattern, text, re.IGNORECASE)` to count matches

## Example Score Computation
```python
import re

def classify(text, keywords_dict):
    scores = {}
    for category, keywords in keywords_dict.items():
        score = 0
        for pattern, weight in keywords:
            matches = re.findall(pattern, text, re.IGNORECASE)
            score += len(matches) * weight
        scores[category] = score

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "music"  # catch-all
    return best
```

## Category Keyword Strategy
- **LLM**: Focus on NLP/ML terminology, model names (GPT, BERT, Llama), training methods (RLHF, SFT, DPO)
- **Trapped Ion & QC**: Focus on quantum hardware terms (qubit, entanglement, gate), ion-specific terms (paul trap, Lamb-Dicke, sideband)
- **Black Hole**: Focus on GR/astrophysics terms (Schwarzschild, event horizon, spacetime, accretion)
- **DNA**: Focus on molecular biology terms (genome, nucleotide, CRISPR, polymerase, sequencing)
- **Music History**: Focus on music theory/history terms (composer, symphony, genre, melody, lyrics) - also serves as catch-all
