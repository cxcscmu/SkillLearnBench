---
name: run2_json-validation
description: Validate, format, and write JSON output with schema enforcement and error handling.
---

# JSON Output with Validation

## Overview
Write JSON output with strict schema validation and comprehensive error handling.

## Schema Definition

The report must follow this exact structure:

```python
SCHEMA = {
    "pr": {
        "total": int,
        "merged": int,
        "closed": int,
        "avg_merge_days": float,
        "top_contributor": str  # May be None/null
    },
    "issue": {
        "total": int,
        "bug": int,
        "resolved_bugs": int
    }
}
```

## Validation Implementation

```python
import json
from typing import Any, Dict

def validate_report(report: Dict[str, Any]) -> list:
    """Validate report structure and content."""
    errors = []

    # Check top-level sections
    required_sections = ["pr", "issue"]
    for section in required_sections:
        if section not in report:
            errors.append(f"Missing section: {section}")

    # Validate PR section
    if "pr" in report:
        pr_data = report["pr"]
        pr_required = ["total", "merged", "closed", "avg_merge_days", "top_contributor"]
        for field in pr_required:
            if field not in pr_data:
                errors.append(f"Missing pr.{field}")
            else:
                value = pr_data[field]
                if field == "avg_merge_days":
                    if not isinstance(value, (int, float)):
                        errors.append(f"pr.{field} must be numeric, got {type(value)}")
                    if value < 0:
                        errors.append(f"pr.{field} cannot be negative")
                elif field == "top_contributor":
                    if value is not None and not isinstance(value, str):
                        errors.append(f"pr.{field} must be string or null")
                elif field in ["total", "merged", "closed"]:
                    if not isinstance(value, int):
                        errors.append(f"pr.{field} must be integer")
                    if value < 0:
                        errors.append(f"pr.{field} cannot be negative")

    # Validate issue section
    if "issue" in report:
        issue_data = report["issue"]
        issue_required = ["total", "bug", "resolved_bugs"]
        for field in issue_required:
            if field not in issue_data:
                errors.append(f"Missing issue.{field}")
            else:
                value = issue_data[field]
                if not isinstance(value, int):
                    errors.append(f"issue.{field} must be integer")
                if value < 0:
                    errors.append(f"issue.{field} cannot be negative")

    return errors

def write_report(report: Dict[str, Any], filepath: str) -> bool:
    """Write validated report to JSON file."""
    # Validate before writing
    errors = validate_report(report)
    if errors:
        print(f"Validation errors found:")
        for error in errors:
            print(f"  - {error}")
        return False

    try:
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report written to {filepath}")
        return True
    except IOError as e:
        print(f"Error writing file: {e}")
        return False
```

## JSON Formatting Best Practices

```python
# Use indent=2 for readability
json.dump(report, f, indent=2)

# Ensure proper escaping (handled by json.dump)
# Don't manually escape strings

# Handle special values
# - None becomes null in JSON
# - floats are preserved
# - integers stay as-is
```

## Pre-Write Verification

Before writing:
1. Validate schema completeness
2. Check numeric ranges (no negatives)
3. Verify float precision (1 decimal place)
4. Check file path is writable

## Error Recovery

```python
import os

def safe_write_report(report, filepath):
    """Write with backup of existing file."""
    # Check directory exists
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print(f"Cannot create directory: {e}")
            return False

    # Backup existing file
    if os.path.exists(filepath):
        backup = f"{filepath}.backup"
        try:
            os.rename(filepath, backup)
        except OSError:
            pass  # Non-critical

    # Write new file
    return write_report(report, filepath)
```

## Output Example

```json
{
  "pr": {
    "total": 50,
    "merged": 34,
    "closed": 50,
    "avg_merge_days": 8.3,
    "top_contributor": "malancas"
  },
  "issue": {
    "total": 61,
    "bug": 28,
    "resolved_bugs": 26
  }
}
```
