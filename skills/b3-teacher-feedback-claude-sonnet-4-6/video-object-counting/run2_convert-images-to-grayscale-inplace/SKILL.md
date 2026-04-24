---
name: convert-images-to-grayscale-inplace
description: Convert all extracted keyframe PNG images from RGB to grayscale inplace, overwriting the original files. Also convert template images (coin.png, enemy.png, turtle.png) to grayscale. Use this before running object counting.
---

## Convert Images to Grayscale Inplace

Use a Python script to convert all keyframe images and template images to grayscale, overwriting the originals.

```python
#!/usr/bin/env python3
import glob
import os
from PIL import Image

# Convert all keyframes to grayscale
keyframes = sorted(glob.glob('/root/keyframes_*.png'))
for frame_path in keyframes:
    img = Image.open(frame_path).convert('L')
    img.save(frame_path)
    print(f"Converted {frame_path} to grayscale")

# Convert template images to grayscale
templates = ['/root/coin.png', '/root/enemy.png', '/root/turtle.png']
for tmpl_path in templates:
    if os.path.exists(tmpl_path):
        img = Image.open(tmpl_path).convert('L')
        img.save(tmpl_path)
        print(f"Converted {tmpl_path} to grayscale")
```

Save as `/root/convert_grayscale.py` and run:
```bash
python3 /root/convert_grayscale.py
```