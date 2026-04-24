name: paper-classifier
description: Classifies academic papers and documents into 5 specific categories: LLM, Trapped Ion & Quantum Computing, Black Hole, DNA, and Music History. Use this skill whenever academic papers or documents need to be categorized based on their content, titles, or metadata.

# Paper Classifier Skill

## Categories and Keywords

### 1. LLM (Large Language Models)
- **Keywords**: LLM, Large Language Model, Transformer, GPT, BERT, Attention Mechanism, Natural Language Processing, NLP, Prompt Engineering, Inference, Tokenization.
- **Context**: Focuses on artificial intelligence, specifically language modeling and text generation.

### 2. Trapped Ion and Quantum Computing
- **Keywords**: Trapped Ion, Quantum Computing, Qubit, Quantum Gate, Entanglement, Superposition, Ion Trap, Pauli, Quantum Circuit, Quantum Information.
- **Context**: Focuses on quantum mechanics applied to computing, specifically using trapped ions.

### 3. Black Hole
- **Keywords**: Black Hole, Event Horizon, Hawking Radiation, Schwarzschild, Singularity, General Relativity, Spacetime, Accretion Disk, Gravitational Waves.
- **Context**: Focuses on astrophysics and gravitational physics.

### 4. DNA
- **Keywords**: DNA, Genome, Nucleotide, Double Helix, Base Pair, Genetics, RNA, Sequencing, CRISPR, Mutation, Protein Synthesis.
- **Context**: Focuses on molecular biology and genetics.

### 5. Music History
- **Keywords**: Music History, Symphony, Composer, Beethoven, Mozart, Baroque, Classical Era, Romanticism, Jazz, Opera, Musicology, Composition.
- **Context**: Focuses on the historical development of music and its composers.

## Classification Logic
- **Step 1**: Extract the title and available text from the document (using `pdfgrep`, `pdftotext`, or similar tools for PDFs; `pandoc` or `docx2txt` for DOCX/PPTX).
- **Step 2**: Check for dominant keywords in the title and the first few pages/paragraphs.
- **Step 3**: Assign the document to the category with the highest keyword frequency.
- **Step 4**: If no category is an obvious fit, use the "Music History" category as the default (based on the "last one" instruction if applicable, or if it's the catch-all).

## Verification
- Cross-reference the assigned category with the file name to ensure logical consistency.
