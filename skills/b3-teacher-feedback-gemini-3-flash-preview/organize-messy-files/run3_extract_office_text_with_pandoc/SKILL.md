---
name: extract_office_text_with_pandoc
description: Extracts text from .docx and .pptx files using `pandoc`. This tool is preferred for its robustness in handling various document schemas and converting them into plain text for analysis.
---

```python
import subprocess
import shutil

def extract_office_text(file_path):
    """
    Extracts text from docx or pptx files using pandoc.
    """
    if not shutil.which("pandoc"):
        return None

    try:
        # Convert to plain text
        result = subprocess.run(
            ["pandoc", "-f", "docx" if file_path.endswith(".docx") else "pptx", "-t", "plain", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None
```