---
name: batch_grayscale_conversion_inplace
description: Converts all extracted keyframe images in a directory from RGB to grayscale and overwrites the original files.
---

Use `python3` and OpenCV to process the images. This reduces the complexity for subsequent template matching tasks.

```python
import cv2
import glob
import os

def convert_to_grayscale(path_pattern="/root/keyframes_*.png"):
    image_files = sorted(glob.glob(path_pattern))
    for image_path in image_files:
        img = cv2.imread(image_path)
        if img is not None:
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(image_path, gray_img)

if __name__ == "__main__":
    convert_to_grayscale()
```