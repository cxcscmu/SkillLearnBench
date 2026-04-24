---
name: run2_keyword-classification
description: Classifies unstructured text into specific categories based on keyword presence, falling back to a default category when no matches are found.
---

# Keyword-Based Text Classification Skill

## Description
This skill leverages simple keyword occurrence counting to categorize textual documents. It is faster than using an LLM and is effective when categories are highly distinct (e.g., DNA vs. Black Holes).

## Python Implementation
```python
def classify_by_keywords(text, category_keywords, default_category):
    """
    Classifies text based on the frequency of predefined keywords per category.
    
    :param text: Lowercase text string to classify.
    :param category_keywords: A dictionary mapping category names to a list of keywords.
    :param default_category: The category to return if no keywords match.
    :return: The string name of the matched category.
    """
    scores = {cat: 0 for cat in category_keywords}
    
    for cat, keywords in category_keywords.items():
        for kw in keywords:
            # Simple substring matching, can be enhanced with regex if needed
            scores[cat] += text.count(kw.lower())
            
    best_cat = max(scores, key=scores.get)
    
    if scores[best_cat] > 0:
        return best_cat
    else:
        return default_category

# Example Usage
categories = {
    "LLM": ["llm", "large language model", "transformer", "chatgpt", "gpt-", "natural language processing"],
    "DNA": ["dna", "genome", "gene ", "genetic", "chromosome", "biology"]
}

text_sample = "the human genome project mapped all the genes in our dna."
result = classify_by_keywords(text_sample, categories, "unknown")
print(result) # Output: DNA
```
