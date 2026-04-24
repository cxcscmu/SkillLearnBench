---
name: pdf-classifier
description: Classifies PDF academic papers by subject area using text extraction from first pages. Use this skill whenever you need to categorize, sort, or organize PDF papers by topic, research field, or subject matter.
---

# PDF Classifier

Extracts text from PDF files and classifies them into predefined subject categories based on title, abstract, and keywords.

## Approach

1. **Extract text** from the first 1-2 pages of each PDF using Python's `PyPDF2` or `pdfplumber` library
2. **Classify** based on keyword matching against subject-specific vocabulary
3. **Handle ambiguity** by scoring each category and picking the highest match

## Classification Strategy

For each document, extract text and look for domain-specific keywords:

### Keyword Sets by Subject

- **LLM**: language model, transformer, attention mechanism, GPT, BERT, token, prompt, fine-tuning, RLHF, LLM, neural network language, text generation, NLP, natural language processing, large language, instruction tuning, in-context learning, chain-of-thought, retrieval-augmented, embedding, tokenizer, decoder, encoder
- **Trapped ion & quantum computing**: trapped ion, quantum computing, quantum gate, qubit, quantum error correction, ion trap, quantum entanglement, quantum algorithm, quantum circuit, quantum processor, quantum simulation, quantum information, Paul trap, Coulomb crystal, motional mode, Raman transition, quantum logic, fault-tolerant quantum, surface code, topological quantum
- **Black hole**: black hole, event horizon, Hawking radiation, singularity, gravitational wave, general relativity, spacetime, Schwarzschild, Kerr metric, accretion disk, gravitational lensing, binary merger, LIGO, dark matter, cosmological, neutron star merger, gravitational collapse, Penrose, ergosphere, information paradox
- **DNA**: DNA, genomic, gene expression, nucleotide, genome, CRISPR, sequencing, transcription, chromosome, mutation, protein folding, epigenetic, RNA, polymerase, genetic, double helix, base pair, replication, molecular biology, bioinformatics
- **Music history**: music history, musical, composer, symphony, opera, baroque, classical period, romantic era, jazz history, musicology, ethnomusicology, sonata, concerto, counterpoint, harmony theory, musical form, orchestration, medieval music, renaissance music, blues history

## Implementation

Use Python with `PyPDF2` for text extraction. For each file:
1. Open PDF reader
2. Extract text from pages 0-1
3. Lowercase the text
4. Count keyword hits per category
5. Assign to category with most hits (default to music_history if no clear match as the catch-all)

## Edge Cases

- If text extraction fails (scanned PDFs), use the arXiv ID in the filename to infer subject via the ID prefix pattern
- arXiv categories: astro-ph, gr-qc, hep-th → black_hole; quant-ph → trapped_ion_and_qc; cs.CL, cs.AI, cs.LG → LLM; q-bio → DNA
