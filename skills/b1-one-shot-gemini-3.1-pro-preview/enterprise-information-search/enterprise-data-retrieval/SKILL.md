---
name: enterprise-data-retrieval
description: Patterns for cross-referencing multiple data sources (products, employees, etc.) to answer complex business questions.
---
# Enterprise Data Retrieval

## Introduction
Business questions often involve finding an entity in one file (e.g., a product file) and cross-referencing it with another (e.g., employee details).

## Cross-Referencing Pattern
```python
def resolve_employee_ids(names, employees_dict):
    ids = []
    for name in names:
        emp_id = employees_dict.get(name, None)
        if emp_id:
            ids.append(emp_id)
    return ids
```
