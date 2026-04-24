---
name: data-filtering
description: How to filter tabular datasets. Use this skill whenever you need to process or filter CSV files, tabular data, or databases to find records that match specific criteria such as location, price, category, or flags (like pet-friendly).
---
# Data Filtering Guidelines

This skill provides guidance on filtering large tabular datasets efficiently.

## Approach
1. Identify the files containing the necessary data (e.g., accommodations, restaurants, attractions, distances).
2. Determine the key columns for filtering (e.g., city, price, rating, pet-friendly status, cuisine type).
3. Use text processing tools like `grep`, `awk`, or Python scripts to filter out irrelevant rows.
4. When applying multiple constraints (e.g., city = X AND pet-friendly = Y), chain filters or use a script for clarity.
5. Extract the specific fields needed for the final output (e.g., name, price, description) and format them correctly.
