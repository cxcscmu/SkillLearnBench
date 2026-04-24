---
name: count-objects-in-frames-using-template-matching
description: Use this skill to count coins, enemies, and turtles in grayscale keyframe images using OpenCV template matching with a provided count_objects.py script. Includes robust output parsing and fallback to direct template matching if the script is unavailable.
---

## Counting objects in keyframes

### Step 1: Check if count_objects.py exists and understand its output

```bash
ls -la /root/count_objects.py 2>/dev/null
cat /root/count_objects.py 2>/dev/null
```

### Step 2: Run the script and capture raw output first

Before parsing, always print the raw output to understand the format:

```python
import subprocess

result = subprocess.run(
    ['python3', '/root/count_objects.py', '/root/keyframes_001.png', '/root/coin.png'],
    capture_output=True, text=True
)
print("STDOUT:", repr(result.stdout))
print("STDERR:", repr(result.stderr))
print("Return code:", result.returncode)
```

**Always use `python3`** — the environment may not have `python` aliased.

### Step 3: Parse the output correctly

Based on the raw output, write a parser. Common output formats:
- A single number on its own line
- "Found X matches"
- "Count: X"

**Robust parsing approach** — extract the count carefully:

```python
import re

def parse_count(stdout_text):
    """Parse the count from script output. Handles various formats."""
    text = stdout_text.strip()
    
    # If the output is just a number
    if text.isdigit():
        return int(text)
    
    # Try to find patterns like "Found X matches", "Count: X", "X matches", etc.
    # Look for the most relevant number
    patterns = [
        r'[Ff]ound\s+(\d+)',
        r'[Cc]ount[:\s]+(\d+)',
        r'[Mm]atches[:\s]+(\d+)',
        r'(\d+)\s+match',
        r'(\d+)\s+found',
    ]
    
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return int(m.group(1))
    
    # If the output has lines, try to find a line that is just a number
    for line in text.split('\n'):
        line = line.strip()
        if line.isdigit():
            return int(line)
    
    # Last resort: find all numbers and take the last one, but be careful
    numbers = re.findall(r'\b(\d+)\b', text)
    if numbers:
        # If there's only one number, return it
        if len(numbers) == 1:
            return int(numbers[0])
        # If multiple, the count is typically the last meaningful one
        # But filter out numbers that look like dimensions or coordinates
        return int(numbers[-1])
    
    # If no output or unparseable, return 0
    return 0
```

### Step 4: Full counting pipeline

```python
import subprocess
import re
import glob
import csv

def parse_count(stdout_text):
    text = stdout_text.strip()
    if not text:
        return 0
    if text.isdigit():
        return int(text)
    
    patterns = [
        r'[Ff]ound\s+(\d+)',
        r'[Cc]ount[:\s]+(\d+)',
        r'[Mm]atches[:\s]+(\d+)',
        r'(\d+)\s+match',
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return int(m.group(1))
    
    for line in text.split('\n'):
        line = line.strip()
        if line.isdigit():
            return int(line)
    
    numbers = re.findall(r'\b(\d+)\b', text)
    if len(numbers) == 1:
        return int(numbers[0])
    
    return 0

def count_objects(frame_path, template_path):
    result = subprocess.run(
        ['python3', '/root/count_objects.py', frame_path, template_path],
        capture_output=True, text=True, timeout=60
    )
    # Print raw output for debugging
    print(f"  Raw stdout: {repr(result.stdout)}")
    print(f"  Raw stderr: {repr(result.stderr)}")
    return parse_count(result.stdout)

# Get all keyframes sorted
keyframes = sorted(glob.glob('/root/keyframes_*.png'))
print(f"Total keyframes found: {len(keyframes)}")

templates = {
    'coins': '/root/coin.png',
    'enemies': '/root/enemy.png',
    'turtles': '/root/turtle.png'
}

results = []
for frame_path in keyframes:
    print(f"Processing {frame_path}...")
    row = {'frame_id': frame_path}
    for obj_name, tmpl_path in templates.items():
        print(f"  Counting {obj_name}...")
        row[obj_name] = count_objects(frame_path, tmpl_path)
    results.append(row)
    print(f"  Results: coins={row['coins']}, enemies={row['enemies']}, turtles={row['turtles']}")

# Write CSV
with open('/root/counting_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['frame_id', 'coins', 'enemies', 'turtles'])
    writer.writeheader()
    writer.writerows(results)

print(f"CSV written with {len(results)} rows")
```

### Fallback: Direct template matching if count_objects.py is not available

If `count_objects.py` doesn't exist, use OpenCV directly:

```python
import cv2
import numpy as np

def count_objects_direct(frame_path, template_path, threshold=0.8):
    """Count objects using OpenCV template matching."""
    frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    
    if frame is None or template is None:
        return 0
    
    # Ensure template is not larger than frame
    if template.shape[0] > frame.shape[0] or template.shape[1] > frame.shape[1]:
        return 0
    
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    
    # De-duplicate nearby detections using non-maximum suppression
    points = list(zip(locations[1], locations[0]))  # (x, y)
    if not points:
        return 0
    
    h, w = template.shape[:2]
    filtered = []
    used = set()
    for i, (x1, y1) in enumerate(points):
        if i in used:
            continue
        filtered.append((x1, y1))
        for j, (x2, y2) in enumerate(points):
            if j in used or j == i:
                continue
            if abs(x1 - x2) < w * 0.5 and abs(y1 - y2) < h * 0.5:
                used.add(j)
    
    return len(filtered)
```

### Important notes

- **Always use `python3`**, not `python`, in subprocess calls
- **Do NOT convert template images to grayscale** — only keyframes should be converted
- **Always inspect raw output** before writing the parser to ensure correctness
- **Handle zero-match cases** — if output is empty or says "0", return 0
- **Verify keyframe count** — the CSV should have exactly as many rows as extracted keyframes