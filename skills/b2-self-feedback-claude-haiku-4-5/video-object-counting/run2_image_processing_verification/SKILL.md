---
name: run2_image_processing_verification
description: Robust image processing with format conversion, in-place modification, and comprehensive verification of image properties.
---

# Image Processing with Verification

## Overview
Convert images between formats and color spaces with verification and error handling.

## Installation
```bash
apt-get install python3-pil
# or
pip install Pillow
```

## Grayscale Conversion with Verification

### Basic In-Place Conversion
```python
from PIL import Image
import os

def convert_to_grayscale_inplace(filepath):
    """
    Convert image to grayscale and overwrite original

    Args:
        filepath: Path to image file

    Returns:
        (success: bool, message: str)
    """

    # Validate file exists
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"

    try:
        # Open and get original info
        img = Image.open(filepath)
        original_mode = img.mode
        original_size = img.size

        # Convert to grayscale
        gray_img = img.convert('L')

        # Save back to same path
        gray_img.save(filepath)

        return True, (
            f"Converted {filepath} "
            f"({original_mode} {original_size} -> L)"
        )

    except IOError as e:
        return False, f"IO Error: {e}"

    except Exception as e:
        return False, f"Error: {e}"
```

### Batch Conversion with Verification

```python
import glob

def batch_convert_grayscale(pattern):
    """
    Convert all matching images to grayscale

    Args:
        pattern: Glob pattern (e.g., '/root/keyframes_*.png')

    Returns:
        (success_count, failure_count, messages)
    """

    files = sorted(glob.glob(pattern))

    if not files:
        return 0, 0, [f"No files matching: {pattern}"]

    messages = []
    successes = 0
    failures = 0

    for filepath in files:
        success, msg = convert_to_grayscale_inplace(filepath)

        if success:
            successes += 1
            messages.append(f"✓ {msg}")
        else:
            failures += 1
            messages.append(f"✗ {msg}")

    return successes, failures, messages
```

## Image Verification

### Verify Image Format
```python
def verify_image_format(filepath, expected_mode='L'):
    """
    Verify image is in expected format

    Args:
        filepath: Path to image
        expected_mode: Expected image mode ('L' for grayscale, 'RGB', etc.)

    Returns:
        (is_valid: bool, info: dict)
    """

    info = {
        'filepath': filepath,
        'exists': False,
        'readable': False,
        'mode': None,
        'size': None,
        'matches_expected': False,
        'file_size': None
    }

    if not os.path.exists(filepath):
        return False, info

    info['exists'] = True
    info['file_size'] = os.path.getsize(filepath)

    try:
        img = Image.open(filepath)
        info['readable'] = True
        info['mode'] = img.mode
        info['size'] = img.size
        info['matches_expected'] = img.mode == expected_mode

        return img.mode == expected_mode, info

    except Exception as e:
        info['error'] = str(e)
        return False, info
```

### Quality Checks
```python
def check_image_quality(filepath):
    """
    Check image quality and properties

    Args:
        filepath: Path to image

    Returns:
        (is_valid: bool, report: dict)
    """

    report = {}

    try:
        img = Image.open(filepath)

        # File size check
        file_bytes = os.path.getsize(filepath)
        file_kb = file_bytes / 1024

        report['file_size_kb'] = round(file_kb, 2)
        report['dimensions'] = img.size
        report['mode'] = img.mode
        report['format'] = img.format

        # Pixel value analysis (for grayscale)
        if img.mode == 'L':
            import numpy as np
            arr = np.array(img)
            report['pixel_min'] = int(arr.min())
            report['pixel_max'] = int(arr.max())
            report['pixel_mean'] = round(float(arr.mean()), 2)
            report['pixel_std'] = round(float(arr.std()), 2)

            # Check for contrast
            if report['pixel_max'] - report['pixel_min'] < 10:
                report['warning'] = 'Low contrast image'

        return True, report

    except Exception as e:
        return False, {'error': str(e)}
```

## Batch Processing with Reports

```python
def process_and_verify_batch(input_pattern, target_mode='L'):
    """
    Process batch of images and generate verification report

    Args:
        input_pattern: Glob pattern for input files
        target_mode: Target image mode

    Returns:
        Comprehensive report dictionary
    """

    files = sorted(glob.glob(input_pattern))

    report = {
        'total_files': len(files),
        'processed': 0,
        'failures': 0,
        'verification_results': [],
        'quality_checks': []
    }

    # Process files
    for filepath in files:
        success, msg = convert_to_grayscale_inplace(filepath)

        if success:
            report['processed'] += 1
        else:
            report['failures'] += 1
            continue

        # Verify after conversion
        is_valid, info = verify_image_format(filepath, target_mode)
        report['verification_results'].append({
            'file': filepath,
            'valid': is_valid,
            'info': info
        })

        # Quality check
        quality_ok, quality = check_image_quality(filepath)
        report['quality_checks'].append({
            'file': filepath,
            'ok': quality_ok,
            'report': quality
        })

    return report


def print_report(report):
    """Print processing report"""

    print(f"\n{'='*60}")
    print(f"Processing Report")
    print(f"{'='*60}")
    print(f"Total files:     {report['total_files']}")
    print(f"Processed:       {report['processed']}")
    print(f"Failures:        {report['failures']}")
    print(f"Success rate:    {100*report['processed']/report['total_files']:.1f}%")

    # Verification summary
    valid_count = sum(1 for v in report['verification_results'] if v['valid'])
    print(f"\nVerification: {valid_count}/{len(report['verification_results'])} valid")

    # Print failures
    for vr in report['verification_results']:
        if not vr['valid']:
            print(f"  ✗ {vr['file']}: {vr['info']}")

    print(f"\n{'='*60}\n")
```

## Complete Workflow Example

```python
from PIL import Image
import glob
import os

# Step 1: Convert keyframes
print("Converting keyframes to grayscale...")
success_count, failure_count, messages = batch_convert_grayscale('/root/keyframes_*.png')

for msg in messages:
    print(msg)

print(f"\nResult: {success_count} succeeded, {failure_count} failed\n")

# Step 2: Verify all conversions
print("Verifying converted images...")
files = sorted(glob.glob('/root/keyframes_*.png'))

for filepath in files:
    is_valid, info = verify_image_format(filepath, 'L')
    status = "✓" if is_valid else "✗"
    print(f"{status} {filepath}: {info['mode']} {info['size']}")

# Step 3: Quality check
print("\nQuality analysis...")
report = process_and_verify_batch('/root/keyframes_*.png', 'L')
print_report(report)
```

## Best Practices

1. **Always verify conversions** - don't assume success
2. **Use absolute paths** - avoid working directory issues
3. **Check file permissions** - before attempting save
4. **Preserve metadata** - when possible
5. **Validate mode before processing** - template matching requires consistent formats
6. **Batch process safely** - continue on individual failures
7. **Generate reports** - document what was processed
