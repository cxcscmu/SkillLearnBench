---
name: convert-keyframes-to-grayscale
description: Use this skill to convert extracted keyframe PNG images to grayscale in-place using Python3 and PIL/Pillow. Only convert keyframe images, NOT template images (coin.png, enemy.png, turtle.png).
---

## Convert keyframes to grayscale in-place

**Important**: Only convert the extracted keyframe images to grayscale. Do NOT convert the template images (`coin.png`, `enemy.png`, `turtle.png`) — those must remain in their original color format.

### Using Python3 with Pillow

```python
import glob
from PIL import Image

# Only convert keyframes, NOT templates
keyframe_files = sorted(glob.glob('/root/keyframes_*.png'))

for fpath in keyframe_files:
    img = Image.open(fpath).convert('L')  # Convert to grayscale
    img.save(fpath)  # Override in place
    print(f"Converted {fpath} to grayscale")
```

### Alternative: Using a bash loop with Python3 one-liner

```bash
for f in /root/keyframes_*.png; do
    python3 -c "from PIL import Image; Image.open('$f').convert('L').save('$f')"
done
```

### Verification

Check that the images are indeed grayscale:

```python
from PIL import Image
img = Image.open('/root/keyframes_001.png')
print(img.mode)  # Should print 'L' for grayscale
```