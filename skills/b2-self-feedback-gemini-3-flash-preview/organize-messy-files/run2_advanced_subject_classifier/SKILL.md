---
name: run2_advanced_subject_classifier
description: Advanced document classification using weighted keyword scores and expanded subject vocabularies.
---

# Advanced Subject Classifier Skill

## Expanded Keyword Sets
- **LLM**: Large Language Model, LLM, Transformer, GPT, BERT, Attention mechanism, Tokenization, Pre-training, Fine-tuning, RLHF, NLP, Generative AI.
- **trapped_ion_and_qc**: Trapped Ion, Quantum Computing, Qubit, Quantum Gate, Entanglement, Superposition, Ion Trap, Quantum Error Correction, Quantum Information, Paul Trap, Rydberg, NIST.
- **black_hole**: Black Hole, Event Horizon, Schwarzschild, Hawking Radiation, General Relativity, Singularity, Accretion Disk, Spacetime Curvature, LIGO, Gravitational Waves, Kerr metric.
- **DNA**: DNA, Genome, Genetic, Sequencing, Nucleotide, RNA, Protein Synthesis, Chromosome, CRISPR, Base Pair, Genomics, PCR, Polymerase.
- **music_history**: Music History, Composer, Symphony, Opera, Baroque, Classical, Romantic, Orchestra, Melody, Harmony, Polyphony, Sonata, Fugue, Jazz, Blues, Ethnomusicology.

## Scoring Algorithm
Assign weights to keywords. If multiple subjects match, the one with the highest total score wins.
Example: "LLM" (3 points), "Quantum" (1 point) -> Subject is LLM.
Special case: If a file contains very little text (e.g. just a title), prioritize the title content.
If no matches, the file goes to the last subject `music_history` by default as per instructions (but only if it truly fits nowhere else).
