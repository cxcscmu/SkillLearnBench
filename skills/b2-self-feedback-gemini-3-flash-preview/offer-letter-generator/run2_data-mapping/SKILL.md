---
name: run2_data-mapping
description: Techniques for preparing and formatting data from JSON/API sources for inclusion in documents.
---

# Data Mapping and Formatting

Before inserting data into a document, ensure it is correctly formatted.

## Currency Formatting
```python
def format_currency(value):
    try:
        # Assuming value is a string like "185,000" or a number
        clean_val = str(value).replace(',', '')
        return f"${float(clean_val):,.2f}"
    except:
        return value
```

## Date Formatting
Standardize date formats if necessary.
```python
from datetime import datetime

def format_date(date_str):
    # If the input is "January 15, 2024"
    return date_str # or convert to a specific format
```

## Mapping Placeholders
Create a dictionary that matches the `{{PLACEHOLDER}}` keys in the document.
```python
mapping = {f"{{{{{k}}}}}": str(v) for k, v in employee_data.items()}
```
