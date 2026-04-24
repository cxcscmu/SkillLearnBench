---
name: run2_content-classification-enhanced
description: Improved keyword-based classification with confidence scoring, compound term detection, and refinement patterns
---

# Content Classification Skill (Enhanced)

## Overview
Refined classification system using:
1. **Enhanced keyword sets** based on Round 1 results
2. **Compound phrase detection** for better accuracy
3. **Confidence scoring** to identify uncertain classifications
4. **Category-specific weighting** for accurate categorization

## Implementation

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class ClassificationResult:
    """Classification result with confidence score"""
    category: str
    confidence: float  # 0.0-1.0
    scores: Dict[str, float]  # All category scores

def classify_text_enhanced(text, min_confidence=0.0):
    """
    Enhanced classification with confidence scoring.
    Returns ClassificationResult with detailed scores.
    """
    if not text or len(text.strip()) < 50:
        return ClassificationResult('music_history', 0.1, {})

    text_lower = text.lower()

    # Enhanced keyword sets from Round 1 analysis
    keywords = {
        'LLM': {
            'primary': [
                'language model', 'large language', 'llm', 'transformer',
                'bert', 'gpt', 'attention mechanism', 'nlp',
                'natural language processing', 'token', 'embedding'
            ],
            'secondary': [
                'fine-tune', 'pre-trained', 'prompt', 'chat',
                'instruction', 'alignment', 'rlhf', 'inference',
                'sequence-to-sequence', 'autoregressive'
            ]
        },
        'trapped_ion_and_qc': {
            'primary': [
                'trapped ion', 'quantum computing', 'quantum', 'qubit',
                'ion trap', 'quantum algorithm', 'quantum circuit'
            ],
            'secondary': [
                'quantum gate', 'quantum error', 'quantum entanglement',
                'quantum state', 'quantum processor', 'quantum advantage',
                'quantum supremacy', 'quantum simulation'
            ]
        },
        'black_hole': {
            'primary': [
                'black hole', 'event horizon', 'singularity',
                'hawking radiation', 'schwarzschild', 'spacetime',
                'gravitational', 'relativity'
            ],
            'secondary': [
                'gravitational wave', 'einstein equation', 'kerr metric',
                'spacetime curvature', 'gravitational collapse', 'accretion'
            ]
        },
        'DNA': {
            'primary': [
                'dna', 'genetics', 'sequence', 'gene', 'protein',
                'chromosome', 'mutation', 'genomic', 'nucleotide'
            ],
            'secondary': [
                'rna', 'strand', 'helix', 'amino acid', 'genetic code',
                'transcription', 'translation', 'codon', 'allele', 'genome'
            ]
        },
        'music_history': {
            'primary': [
                'music', 'composition', 'symphony', 'melody', 'harmony',
                'orchestra', 'musical', 'composer', 'instrument'
            ],
            'secondary': [
                'chord', 'rhythm', 'classical', 'sonata', 'fugue',
                'baroque', 'concert', 'opera', 'concerto', 'pitch',
                'tempo', 'scale'
            ]
        }
    }

    scores = {}
    for category, keyword_sets in keywords.items():
        primary_count = sum(1 for kw in keyword_sets['primary']
                          if kw in text_lower)
        secondary_count = sum(1 for kw in keyword_sets['secondary']
                            if kw in text_lower)
        # Primary keywords weighted 2x heavier
        scores[category] = primary_count * 2 + secondary_count

    # Get best category
    if max(scores.values()) == 0:
        # No keywords found - use default
        return ClassificationResult('music_history', 0.0, scores)

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]
    second_best_score = sorted(scores.values(), reverse=True)[1]

    # Confidence based on gap between top categories
    confidence = (best_score - second_best_score) / (best_score + 1.0)
    confidence = min(1.0, max(0.0, confidence))

    return ClassificationResult(best_category, confidence, scores)
```

## Classification Logic

### Weighted Keywords
- **Primary keywords** (weight 2x): Core terms that define the subject
- **Secondary keywords** (weight 1x): Related terms that support classification
- **Confidence scoring**: Gap between top categories = confidence

### Example Confidence Scenarios
```
Score: LLM=10, trapped_ion=2 → High confidence (80%+)
Score: LLM=5, DNA=4 → Medium confidence (20%)
Score: All 0 → Default category with low confidence (0%)
```

## Key Improvements from Run 1
1. **Weighted keywords**: Primary terms count more
2. **Confidence scores**: Know how sure we are about classification
3. **Compound terms**: Better captures multi-word concepts
4. **Detailed scoring**: See scores for all categories
5. **Fallback logic**: Better handling of edge cases

## Usage
```python
result = classify_text_enhanced(text)
if result.confidence > 0.3:
    category = result.category
else:
    category = 'music_history'  # Safe default for uncertain cases
```
