---
name: read-csv-files
description: Use when you need to read and parse CSV files from the filesystem in Python. Handles encoding, missing values, and returns structured data.
---

# Reading CSV Files

Use `pandas` to read CSV files. Always handle potential encoding issues and inspect the data structure first.

```python
import pandas as pd

# Basic read
df = pd.read_csv('/path/to/file.csv')

# With encoding fallback
try:
    df = pd.read_csv('/path/to/file.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('/path/to/file.csv', encoding='latin-1')

# Inspect structure
print(df.columns.tolist())
print(df.head())
print(df.dtypes)
print(df.shape)

# Handle missing values
df = df.where(pd.notnull(df), None)
```

Always print column names and sample rows before processing to understand the schema.