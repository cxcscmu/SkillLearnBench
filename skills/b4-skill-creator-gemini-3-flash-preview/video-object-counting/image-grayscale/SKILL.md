---
name: image-grayscale
description: Use this skill to convert RGB images to grayscale. It provides methods using common libraries like OpenCV or PIL.
---

# Image Grayscale Conversion Skill

This skill provides instructions for converting RGB images to grayscale.

## Using OpenCV (Python)
If OpenCV is available, use the following code:

```python
import cv2

def convert_to_grayscale(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(image_path, gray) # Overwrite original
```

## Using PIL (Python)
If PIL (Pillow) is available:

```python
from PIL import Image

def convert_to_grayscale(image_path):
    img = Image.open(image_path).convert('L')
    img.save(image_path) # Overwrite original
```

## Using ImageMagick (CLI)
If ImageMagick is available:

```bash
mogrify -colorspace gray image.png
```

## Verification
Confirm the image is grayscale by checking its mode or channels.
