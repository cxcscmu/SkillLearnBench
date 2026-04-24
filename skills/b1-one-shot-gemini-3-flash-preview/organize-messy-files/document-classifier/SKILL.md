---
name: document-classifier
description: Logic for categorizing documents into subjects based on keyword matching.
---

# Document Classifier Skill

This skill outlines a strategy for classifying documents into predefined categories using keyword frequency and priority.

## Subjects and Keywords

1.  **LLM (Large Language Models)**
    - Keywords: LLM, transformer, GPT, pre-training, inference, attention mechanism, BERT, language model.
2.  **Trapped Ion and Quantum Computing**
    - Keywords: trapped ion, quantum computer, qubit, entanglement, Paul trap, laser cooling, gate fidelity, Rydberg.
3.  **Black Hole**
    - Keywords: black hole, event horizon, Schwarzschild, Hawking radiation, gravitational waves, accretion disk, singularity.
4.  **DNA**
    - Keywords: DNA, genome, sequencing, nucleotide, CRISPR, polymerase, genetic, chromosome, protein synthesis.
5.  **Music History**
    - Keywords: music, composer, symphony, baroque, classical era, opera, jazz, rhythmic, harmony, melody.

## Classification Logic
1.  **Extraction:** Extract the first 1000-2000 characters of the document.
2.  **Scoring:** Count occurrences of keywords for each category.
3.  **Tie-breaking:** If no keywords match or there is a tie, use the "last folder" rule as per user instruction (in this case, Music History if others fail, or simply the most likely fit).
4.  **Verification:** Check the title or abstract specifically if the score is low.

## Implementation Tip
Use a script or a loop to process files in batches to save time.
