---
name: run2_csv_validation_export
description: Generate and validate CSV files with data integrity checks, verification, and comprehensive error handling for reliable data export.
---

# CSV Generation with Validation

## Overview
Write structured data to CSV files with comprehensive validation, verification, and error handling.

## Installation
The `csv` module is built-in. Optional: `pandas` for advanced operations.

## Basic Safe CSV Writing

```python
import csv
import os

def write_results_csv(output_path, data, fieldnames):
    """
    Write data to CSV with validation

    Args:
        output_path: Output file path
        data: List of dictionaries with data
        fieldnames: List of column names

    Returns:
        True if successful, False otherwise
    """

    # Validate inputs
    if not output_path:
        print("Error: Output path cannot be empty")
        return False

    if not data:
        print("Error: No data to write")
        return False

    # Check for required fields in data
    for row in data:
        for field in fieldnames:
            if field not in row:
                print(f"Error: Missing field '{field}' in row")
                return False

            if row[field] is None:
                print(f"Error: None value for field '{field}'")
                return False

    # Write CSV
    try:
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"✓ CSV written: {output_path}")
        return True

    except IOError as e:
        print(f"Error writing to {output_path}: {e}")
        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
```

## Data Validation

### Pre-Write Validation
```python
def validate_data(data, fieldnames, field_types):
    """
    Validate data before writing

    Args:
        data: List of dictionaries
        fieldnames: Expected field names
        field_types: Dict of field_name -> type

    Returns:
        (is_valid, error_messages)
    """

    errors = []

    # Check structure
    if not isinstance(data, list):
        return False, ["Data must be a list"]

    # Check each row
    for i, row in enumerate(data):
        # Check all fields present
        for field in fieldnames:
            if field not in row:
                errors.append(f"Row {i}: Missing field '{field}'")

        # Type checking
        for field, expected_type in field_types.items():
            if field in row:
                value = row[field]
                if not isinstance(value, expected_type):
                    errors.append(
                        f"Row {i}, field '{field}': "
                        f"Expected {expected_type.__name__}, "
                        f"got {type(value).__name__}"
                    )

    return len(errors) == 0, errors
```

### Type-Safe Example
```python
# Define expected structure
field_types = {
    'frame_id': str,
    'coins': int,
    'enemies': int,
    'turtles': int
}

# Validate
is_valid, errors = validate_data(data, fieldnames, field_types)

if not is_valid:
    for error in errors:
        print(f"Validation error: {error}")
    exit(1)
```

## Verification After Writing

```python
def verify_csv(filepath, fieldnames, expected_rows=None):
    """
    Verify CSV file was written correctly

    Args:
        filepath: Path to CSV file to verify
        fieldnames: Expected column names
        expected_rows: Expected number of rows (excluding header)

    Returns:
        (is_valid, report)
    """

    report = []

    # Check file exists
    if not os.path.exists(filepath):
        return False, ["File does not exist"]

    # Check file size
    file_size = os.path.getsize(filepath)
    if file_size == 0:
        return False, ["File is empty"]

    report.append(f"✓ File exists, size: {file_size} bytes")

    # Read and validate
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Check headers
        if reader.fieldnames != fieldnames:
            return False, [
                f"Header mismatch. Expected {fieldnames}, got {reader.fieldnames}"
            ]

        report.append(f"✓ Headers correct: {reader.fieldnames}")

        # Check row count
        if expected_rows and len(rows) != expected_rows:
            report.append(
                f"⚠ Row count: {len(rows)} (expected {expected_rows})"
            )
        else:
            report.append(f"✓ Row count: {len(rows)}")

        # Check for empty values
        for i, row in enumerate(rows):
            for field in fieldnames:
                if not row[field] or row[field].strip() == '':
                    report.append(f"⚠ Row {i+1}, field '{field}': empty value")

        return True, report

    except csv.Error as e:
        return False, [f"CSV parse error: {e}"]

    except Exception as e:
        return False, [f"Verification error: {e}"]

# Usage
is_valid, report = verify_csv(
    '/root/counting_results.csv',
    ['frame_id', 'coins', 'enemies', 'turtles'],
    expected_rows=8
)

for line in report:
    print(line)

if not is_valid:
    exit(1)
```

## Complete Workflow

```python
import csv

def export_to_csv(output_path, frame_results, fieldnames):
    """
    Complete CSV export with validation

    Args:
        output_path: Output file path
        frame_results: List of {frame_id, coins, enemies, turtles}
        fieldnames: Column names

    Returns:
        Success status
    """

    # Validate data
    field_types = {
        'frame_id': str,
        'coins': int,
        'enemies': int,
        'turtles': int
    }

    is_valid, errors = validate_data(frame_results, fieldnames, field_types)

    if not is_valid:
        print("Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

    print(f"✓ Data validation passed ({len(frame_results)} rows)")

    # Write CSV
    if not write_results_csv(output_path, frame_results, fieldnames):
        return False

    # Verify
    is_valid, report = verify_csv(output_path, fieldnames, len(frame_results))

    print("Verification report:")
    for line in report:
        print(f"  {line}")

    return is_valid
```

## CSV Security Considerations

### Prevent Injection
```python
# Sanitize values before writing
def sanitize_value(value):
    """Remove potentially dangerous characters"""

    if isinstance(value, str):
        # Remove null bytes
        value = value.replace('\0', '')
        # Avoid formula injection
        if value.startswith(('=', '+', '-', '@')):
            value = "'" + value

    return value

# Use in CSV writing
sanitized_data = [
    {k: sanitize_value(v) for k, v in row.items()}
    for row in data
]
```

## Best Practices

1. **Always validate before writing** - prevents corrupted CSVs
2. **Use `newline=''`** - cross-platform compatibility
3. **Verify after writing** - confirm file integrity
4. **Handle exceptions** - graceful error reporting
5. **Use absolute paths** - avoid working directory issues
6. **Type check data** - ensure correct value types
