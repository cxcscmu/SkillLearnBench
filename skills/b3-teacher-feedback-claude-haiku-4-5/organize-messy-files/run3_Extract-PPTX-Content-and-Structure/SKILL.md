---
name: Extract PPTX Content and Structure
description: Use this skill to extract text, slide titles, and content from PowerPoint presentations to accurately determine their subject matter for classification.
---

## When to use this skill
- When you need to read the actual content from .pptx files
- Before sorting presentations into subject folders
- When filenames don't clearly indicate the presentation topic

## How to extract PPTX content

### Using markitdown for structured extraction
```bash
python -m markitdown input.pptx > output.md
```

### Using Python with python-pptx
```python
from pptx import Presentation

def extract_pptx_content(pptx_path):
    prs = Presentation(pptx_path)
    content = []
    
    for slide_num, slide in enumerate(prs.slides, 1):
        slide_text = f"--- SLIDE {slide_num} ---\n"
        
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text += shape.text + "\n"
        
        content.append(slide_text)
    
    return "\n".join(content)
```

### Key information to extract
1. **Title slide**: Main topic of presentation
2. **Slide titles**: Each slide's heading indicates content areas
3. **Body text**: Bullet points and paragraphs contain subject keywords
4. **First 5 slides**: Usually establish the presentation's main subject

### Subject indicators to look for
- Look for the same keyword patterns as PDF extraction
- Note technical terms, proper nouns, and repeated concepts
- Section headers often reveal the subject area

### Store extracted content
Keep the full extracted text for analysis during subject classification.