---
name: image-grayscale-conversion
description: Convert RGB color images to grayscale and save them in-place, overriding the original files. Use this skill whenever the user asks to convert images to gray-scale, desaturate photos, or prepare images for grayscale processing pipelines using OpenCV or Pillow.
---

# In-Place Image Grayscale Conversion

Convert one or more color (RGB) images to grayscale, overwriting the original files.

## Using OpenCV (recommended)

```python
import cv2
import glob

image_paths = sorted(glob.glob('/root/keyframes_*.png'))
for path in image_paths:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path, gray)
```

- `cv2.imread` loads image as BGR by default.
- `cv2.COLOR_BGR2GRAY` converts to single-channel grayscale.
- `cv2.imwrite` saves back to the same path, overwriting the original.

## Using Pillow

```python
from PIL import Image
img = Image.open(path).convert('L')
img.save(path)
```

## Notes

- After conversion the file is a single-channel (8-bit) PNG — verify with `cv2.imread(path).shape` which should show `(H, W)` instead of `(H, W, 3)`.
- Grayscale images are required for many template-matching and feature-detection algorithms.
