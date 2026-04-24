---
name: image-grayscale
description: Convert images to grayscale in-place.
---

# Image Grayscale Conversion

You can use python to convert an image to grayscale and override the original file.

```python
import cv2
import sys

image_path = sys.argv[1]
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(image_path, gray)
```
