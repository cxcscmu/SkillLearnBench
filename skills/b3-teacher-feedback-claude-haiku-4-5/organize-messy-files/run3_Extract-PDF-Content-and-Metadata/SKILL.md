---
name: Extract PDF Content and Metadata
description: Use this skill to extract the full text, title, abstract, and keywords from PDF files to determine their actual subject matter. Essential for content-based sorting when PDF filenames may be arXiv IDs or other non-descriptive identifiers.
---

## When to use this skill
- When you need to read the actual content of a PDF paper to determine its subject
- When PDF filenames are identifiers (like `2105.03431v1.pdf`) rather than descriptive titles
- Before sorting PDFs into subject folders to ensure accuracy

## How to extract PDF content

### Using PyPDF2 or pdfplumber
```python
import pdfplumber

def extract_pdf_content(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Extract first page (usually contains title and abstract)
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        # Also extract from next 1-2 pages for full abstract
        if len(pdf.pages) > 1:
            text += "\n" + pdf.pages[1].extract_text()
        
        return text
```

### Key information to extract
1. **Title**: Usually at the top of page 1
2. **Abstract**: Contains subject keywords and main topic
3. **Keywords section**: Often explicitly labeled
4. **Introduction**: First paragraph usually summarizes the field

### What to look for in content
- **LLM**: Keywords like "language model", "transformer", "neural network", "NLP", "large language model", "BERT", "GPT"
- **Trapped ion and quantum computing**: Keywords like "trapped ion", "quantum computer", "qubit", "quantum gate", "quantum algorithm"
- **Black hole**: Keywords like "black hole", "event horizon", "gravitational", "spacetime", "Hawking", "relativity"
- **DNA**: Keywords like "DNA", "genetics", "gene", "molecular biology", "sequence", "protein"
- **Music history**: Keywords like "music", "composer", "symphony", "historical", "musical"

### Store extracted content for analysis
Save the extracted text to a temporary variable or file for subject classification matching.