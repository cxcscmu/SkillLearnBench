---
name: file-classifier
description: Use this skill to classify PDF, PPTX, or DOCX files into subject categories: LLM, trapped_ion_and_qc, black_hole, DNA, or music_history. Analyze filenames and available content to determine the correct category.
---

# File Classifier Skill

## Goal
Classify a document into exactly one of five subject folders:
1. LLM
2. trapped_ion_and_qc
3. black_hole
4. DNA
5. music_history

## Classification logic
1. **Analyze File Metadata (Name)**: Often, the filename contains keywords.
2. **Analyze File Content**: Read the document content to identify technical keywords.
   - **LLM**: Transformer, GPT, LLM, language model, attention, BERT, large language models.
   - **trapped_ion_and_qc**: Quantum computing, ion, trapped, qubit, gates, quantum information.
   - **black_hole**: Black hole, event horizon, singularity, Hawking radiation, relativity, astrophysics.
   - **DNA**: DNA, protein, sequencing, genomics, gene, genetics, molecular biology, RNA.
   - **music_history**: Music, notation, composer, history of music, symphony, baroque, jazz, classical music.
3. **Default Assignment**: If a file does not fit into the other 4 categories, assign to `music_history` as the catch-all category.

## Execution
For each file in the root:
1. Use `read_file` or `pdf` tool to sample content.
2. Apply the classification logic.
3. Move the file to the determined target folder.
