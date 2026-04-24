---
name: download-d3-v6
description: Use when you need to obtain the D3.js v6 minified library file and save it locally for a web app.
---

# Downloading D3.js v6 Minified

```python
import urllib.request
import os

os.makedirs('/root/output/js/', exist_ok=True)

url = 'https://cdnjs.cloudflare.com/ajax/libs/d3/6.7.0/d3.min.js'
dest = '/root/output/js/d3.v6.min.js'

try:
    urllib.request.urlretrieve(url, dest)
    print(f"Downloaded D3 v6 to {dest}")
except Exception as e:
    print(f"Download failed: {e}")
    # Fallback: write a minimal stub or try alternate CDN
    alt_url = 'https://d3js.org/d3.v6.min.js'
    urllib.request.urlretrieve(alt_url, dest)
```

Verify the file is non-empty after download:
```python
size = os.path.getsize(dest)
print(f"File size: {size} bytes")
assert size > 100000, "D3 file seems too small — download may have failed"
```