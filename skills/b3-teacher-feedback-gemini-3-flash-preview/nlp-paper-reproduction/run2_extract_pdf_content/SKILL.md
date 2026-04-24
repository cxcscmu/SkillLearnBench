---
name: extract_pdf_content
description: Extracts text and mathematical descriptions from a PDF file to identify specific algorithm parameters and loss functions. This is used to ensure the implementation matches the theoretical definition in the paper.
---

1. Install necessary extraction tools: `pip install pdfplumber`.
2. Use a Python script to parse `/root/SimPO/paper.pdf`.
3. Target sections involving "SimPO", "Loss Function", "Length Normalization", and "Reward Margin".
4. Specifically look for:
   - The formula for $\mathcal{L}_{\text{SimPO}}$.
   - The definition of the reward margin ($\gamma$) and the scaling factor ($\beta$).
   - How length normalization is applied to log probabilities (e.g., dividing by sequence length).
5. Save the extracted text or key formulas to a temporary file or variable for reference during implementation.

```python
import pdfplumber

def extract_simpo_details(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text

# Example usage to find specific parameters
# text = extract_simpo_details("/root/SimPO/paper.pdf")
# print(text)
```