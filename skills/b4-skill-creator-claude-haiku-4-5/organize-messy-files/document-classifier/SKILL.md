---
name: document-classifier
description: Classify documents by subject matter. Use this skill when you need to determine which category (LLM, Trapped Ion & Quantum Computing, Black Hole, DNA, Music History) a PDF, DOCX, or PPTX file belongs to based on its content. Analyzes titles, abstracts, keywords, and text content to accurately categorize documents.
---

# Document Classifier

## Overview

This skill helps classify documents into one of five subject categories by analyzing their content. Each document belongs to exactly one category, so use clear decision criteria to avoid misclassification.

## Subject Categories and Keywords

### 1. LLM (Large Language Models)
**Keywords**: transformer, BERT, GPT, neural network, language model, NLP, text generation, attention mechanism, embedding, tokenization, fine-tuning, prompt engineering, instruction tuning

### 2. Trapped Ion and Quantum Computing
**Keywords**: trapped ion, quantum computing, quantum gate, qubit, quantum algorithm, ion trap, quantum entanglement, quantum error correction, quantum simulation, quantum advantage

### 3. Black Hole
**Keywords**: black hole, gravitational singularity, event horizon, Hawking radiation, gravitational collapse, spacetime curvature, general relativity, accretion disk, cosmic string

### 4. DNA
**Keywords**: DNA, deoxyribonucleic acid, genetics, genomics, protein, amino acid, mutation, genetic code, sequencing, chromosome, gene expression, CRISPR, molecular biology

### 5. Music History
**Keywords**: music, composer, symphony, sonata, classical, baroque, jazz, rhythm, melody, harmony, musical instrument, concert, opera, historical period

## Classification Process

1. **Extract content**: Read the document title, abstract/summary, and first few paragraphs
2. **Identify keywords**: Look for subject-specific terminology from the sections above
3. **Analyze context**: Consider the overall theme, methodology, and references
4. **Make determination**: Classify into the best-matching category
5. **Handle edge cases**: If uncertain between two categories, prioritize based on:
   - Primary focus area (main topic vs. secondary mentions)
   - Author expertise and publication venue
   - Methodological approach (computational vs. theoretical vs. experimental)

## File Format Handling

### PDF Files
- Extract text using PDF parsing (text layer or OCR if needed)
- Check metadata (title, author, keywords)
- Read abstract and introduction

### DOCX Files
- Extract all text content
- Check document title and any metadata
- Read opening paragraphs

### PPTX Files
- Extract slide titles and content from all slides
- Focus on early slides which typically contain overview/subject matter

## Decision Boundaries

**LLM vs Trapped Ion/QC**: LLM focuses on language/text processing; quantum computing on quantum systems
**Black Hole vs Physics**: Black hole is astrophysics-specific; general physics belongs elsewhere
**DNA vs Biology**: DNA is specifically about genetics and molecular biology
**Music History vs Music Theory**: Music history is about historical context and composers; music theory is about structure

## Output Format

For each document, provide:
- Filename
- Determined category (1-5)
- Confidence level (high/medium/low)
- Key indicators that led to this classification
