---
name: run2_file-classification-improved
description: Improved keyword-based document classification with false-positive prevention, manual review of zero-score files, and post-classification verification.
---

# File Classification Skill (Improved)

## Key Lessons from Run 1

### False Positive Problems
Several keywords caused misclassification:
- `rna` matched biological RNA but also papers containing "RNA" in physics/quantum contexts
- `rag` matched "Retrieval-Augmented Generation" (LLM term) but also appears in music papers
- `transcription` and `translation` are NLP terms that appear in both LLM and biology
- `few-shot` appeared in a music manuscript classification paper

### Solutions
1. **Use multi-word phrases** where possible (e.g., "rna polymerase" vs just "rna")
2. **Check zero-score files manually** — they likely contain niche vocabulary
3. **Manually verify borderline cases** (score difference < 2x between top-2)
4. **Read the title/first paragraph** when confidence is low

## Improved Keyword Set

```python
KEYWORDS = {
    "LLM": [
        "large language model", "language model", "llm", "gpt", "chatgpt", "gpt-4", "gpt-3",
        "bert", "natural language processing", "nlp", "text generation", "fine-tuning",
        "instruction tuning", "rlhf", "chain of thought", "in-context learning",
        "autoregressive", "pretrained language", "foundation model", "neural language",
        "word embedding", "retrieval-augmented generation", "alignment", "scaling law",
        "emergent capabilities", "zero-shot learning", "hallucination"
        # NOTE: Avoid 'translation', 'transcription', 'rag', 'few-shot' - too ambiguous
    ],
    "trapped_ion_and_qc": [
        "trapped ion", "ion trap", "quantum computing", "quantum computer", "qubit",
        "quantum gate", "quantum circuit", "quantum error correction", "quantum entanglement",
        "quantum processor", "quantum algorithm", "decoherence", "quantum coherence",
        "superconducting qubit", "quantum advantage", "quantum supremacy",
        "laser cooling", "penning trap", "paul trap", "quantum simulation", "quantum memory",
        "quantum information", "fault tolerant quantum", "topological qubit",
        "quantum optics", "ion chain", "motional mode", "rabi oscillation", "bloch sphere",
        "quantum phase estimation", "quantum thermodynamics", "quantum fluctuation"
    ],
    "black_hole": [
        "black hole", "event horizon", "schwarzschild", "hawking radiation",
        "gravitational wave", "spacetime", "general relativity", "singularity",
        "accretion disk", "neutron star", "ligo", "merger", "astrophysics",
        "dark matter", "dark energy", "einstein equation", "white dwarf", "pulsar",
        "x-ray binary", "supermassive black hole", "active galactic nuclei",
        "cosmological", "redshift", "quasar", "gamma ray burst", "stellar evolution",
        "compact object", "tidal disruption", "kerr metric", "reissner-nordstrom",
        "holographic principle", "ads/cft", "information paradox"
    ],
    "DNA": [
        "dna", "rna polymerase", "ribonucleic", "deoxyribonucleic", "genome", "genomic",
        "gene expression", "protein structure", "nucleotide", "base pair",
        "genetic code", "mutation", "crispr", "sequencing", "chromosome", "epigenetic",
        "methylation", "histone", "helicase", "molecular biology",
        "cell biology", "replication", "double helix", "codon", "amino acid",
        "nucleic acid", "mrna", "trna", "ribosome", "biochemistry",
        "bioinformatics", "phylogenetic", "evolutionary biology", "gene editing",
        "pcr", "western blot"
        # NOTE: Use 'rna polymerase' not just 'rna' to avoid false positives
        # NOTE: 'dna' alone is usually reliable
    ],
    "music_history": [
        "music history", "musical history", "composer", "symphony", "opera",
        "baroque", "classical music", "jazz", "piano", "orchestra", "harmonic analysis",
        "melody", "rhythm", "notation", "counterpoint", "sonata", "fugue", "concerto",
        "bach", "beethoven", "mozart", "renaissance music", "romantic period",
        "polyphony", "musical scale", "musical instrument", "conducting",
        "musicology", "ethnomusicology", "music theory", "tonality",
        "medieval music", "troubadour", "harpsichord", "chamber music", "oratorio",
        "cantata", "lieder", "impressionism music", "serialism", "atonal", "twelve-tone",
        "popular music", "music chart", "billboard", "music consumption"
    ]
}
```

## Post-Classification Verification

Always manually verify:
1. Files with score=0 (no keywords matched)
2. Files where top-2 scores are within 2x of each other
3. Read the title/first 3 lines of abstract for all low-confidence files

```python
def needs_manual_review(scores):
    sorted_scores = sorted(scores.values(), reverse=True)
    top = sorted_scores[0]
    second = sorted_scores[1] if len(sorted_scores) > 1 else 0
    if top == 0:
        return True  # No keywords matched
    if second > 0 and top / second < 2.0:
        return True  # Too close to call
    return False
```

## Known Edge Cases
- DAMOP.pptx → DAMOP = Division of Atomic, Molecular, and Optical Physics → trapped_ion_and_qc
- Papers about "quantum algorithms for DNA alignment" → use primary problem domain (DNA or QC based on which aspect dominates)
- Music papers about "music chart popularity" may not use standard music history keywords
- NLP papers may use "transcription" and "translation" in speech recognition/translation contexts
