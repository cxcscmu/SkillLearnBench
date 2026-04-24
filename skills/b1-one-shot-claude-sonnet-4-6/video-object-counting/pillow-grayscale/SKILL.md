---
name: pillow-grayscale
description: Convert images to grayscale in-place using Pillow (PIL), overwriting original RGB files.
---

# Pillow Grayscale Conversion

## Installation
```bash
pip install Pillow
```

## Convert Single Image In-Place
```python
from PIL import Image

def convert_to_grayscale_inplace(image_path):
    img = Image.open(image_path)
    gray = img.convert("L")      # "L" mode = 8-bit grayscale
    gray.save(image_path)        # overwrite the original file
```

## Convert Multiple Images
```python
from PIL import Image
import glob

def batch_convert_grayscale(pattern):
    for path in glob.glob(pattern):
        img = Image.open(path).convert("L")
        img.save(path)
```

## Modes Reference
| Mode | Description |
|------|-------------|
| `"L"` | 8-bit grayscale (0-255) |
| `"RGB"` | 24-bit color |
| `"RGBA"` | 32-bit color with alpha |
| `"1"` | 1-bit black & white |

## Notes
- `.convert("L")` handles all source formats (RGB, RGBA, etc.)
- Saving back to PNG preserves lossless quality
- After conversion, the file on disk is grayscale but retains the `.png` extension
- OpenCV's `cv2.imread()` will still read the file; use `cv2.IMREAD_GRAYSCALE` or the image will have 3 identical channels
