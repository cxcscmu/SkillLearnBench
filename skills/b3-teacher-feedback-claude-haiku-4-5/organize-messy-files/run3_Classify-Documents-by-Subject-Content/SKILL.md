---
name: Classify Documents by Subject Content
description: Use this skill to analyze extracted text content from documents and classify them into the correct subject folder based on keyword matching and content analysis.
---

## When to use this skill
- After extracting content from PDF, PPTX, or DOCX files
- To determine which of the 5 subject folders a document belongs to
- Before moving files to their destination folders

## Classification rules

### Subject-specific keyword sets

**LLM (Large Language Models)**
- Keywords: "language model", "transformer", "neural network", "NLP", "large language model", "BERT", "GPT", "attention mechanism", "embedding", "tokenization", "natural language processing", "deep learning"
- Context: Papers about AI models trained on text data, language processing, machine learning models for text

**Trapped ion and quantum computing**
- Keywords: "trapped ion", "quantum computer", "qubit", "quantum gate", "quantum algorithm", "quantum circuit", "ion trap", "quantum computing", "quantum simulation", "quantum error correction"
- Context: Papers about quantum computing systems, quantum information processing, trapped ion technologies

**Black hole**
- Keywords: "black hole", "event horizon", "gravitational", "spacetime", "Hawking", "relativity", "general relativity", "singularity", "gravitational wave", "astrophysics", "cosmology"
- Context: Papers about gravitational physics, cosmology, astrophysical objects and phenomena

**DNA**
- Keywords: "DNA", "genetics", "gene", "molecular biology", "sequence", "protein", "genetic", "genomics", "mutation", "chromosome", "RNA", "amino acid"
- Context: Papers about biological molecules, genetics, molecular biology, genomics, biological sequences

**Music history**
- Keywords: "music", "composer", "symphony", "song", "musical", "historical", "concert", "notation", "harmony", "melody", "rhythm", "performance", "musician"
- Context: Papers or documents about music, composers, historical musical analysis, musical theory in historical context

### Classification process

1. **Extract key phrases** from the document's title, abstract, and first 500 words
2. **Count keyword matches** for each of the 5 subject categories
3. **Identify dominant subject**: The category with the most keyword matches
4. **Check context**: Read surrounding sentences to confirm the subject matches
5. **Handle ambiguous cases**: 
   - If two subjects match equally, read more content
   - If still unclear, examine introduction/abstract more carefully
   - Only assign to music_history as fallback if truly cannot match the other 4 categories

### Confidence assessment

- **High confidence**: 5+ keywords match from one category, and no other category has more than 1-2 matches
- **Medium confidence**: 3-4 keywords match, but need to verify with context reading
- **Low confidence**: Only 1-2 keywords match; read full abstract/introduction before deciding

### Decision output
For each document, record:
- Filename
- Detected subject
- Confidence level (high/medium/low)
- Key matching keywords