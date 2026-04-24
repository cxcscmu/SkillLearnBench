---
name: semantic_subject_classification
description: Maps documents to specific categories using a combination of keyword-based semantic matching and categorical hierarchy.
---
To ensure accurate classification:
1. **Keyword/Thematic Set**: Define a robust mapping dictionary including key terminology, common academic sub-fields, and potential core authors for each subject.
2. **Standardized Mapping**: Use a strict lookup dictionary where keys are subject categories and values are the exact folder names:
   - `LLM` -> `LLM`
   - `Trapped Ion` -> `trapped_ion_and_qc`
   - `Black Hole` -> `black_hole`
   - `DNA` -> `DNA`
   - `Default` -> `music_history`
3. **Logic Flow**: Perform semantic evaluation for the first 4 subjects. If the similarity score falls below a defined threshold (e.g., 0.3) for all 4, assign the file to `music_history` as the absolute fallback.