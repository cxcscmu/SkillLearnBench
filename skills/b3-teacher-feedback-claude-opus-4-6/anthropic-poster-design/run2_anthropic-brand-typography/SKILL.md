---
name: anthropic-brand-typography
description: Use this skill when selecting and applying fonts for Anthropic brand materials. Specifies the official heading and body typefaces with correct fallback chains.
---

# Anthropic Brand Typography

## Heading Font

- **Primary**: **Poppins** (geometric sans-serif)
- **Fallback**: Arial
- **Usage**: All headings, product titles (e.g., "NOVA"), section headers
- **Weight**: Bold (700) for primary titles; SemiBold (600) for subheadings
- **Style**: Typically uppercase or title-case for product names

## Body Font

- **Primary**: **Lora** (serif)
- **Fallback**: Georgia
- **Usage**: Body text, annotations, technical descriptions, captions
- **Weight**: Regular (400) for body; Medium (500) for emphasized annotations

## Font Discovery Logic (Python / Pillow)

When rendering with Pillow, use this search order:

```python
import os
from PIL import ImageFont

def find_font(font_names, size=48):
    """Search for fonts in common system paths, return first found."""
    search_paths = [
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        "/root/.fonts",
        "/root/.local/share/fonts",
        "/System/Library/Fonts",
    ]
    for font_name in font_names:
        # Try direct load
        for ext in [".ttf", ".otf"]:
            try:
                return ImageFont.truetype(font_name + ext, size), font_name
            except (OSError, IOError):
                pass
        # Walk search paths
        for base in search_paths:
            if not os.path.isdir(base):
                continue
            for root, dirs, files in os.walk(base):
                for f in files:
                    if font_name.lower().replace(" ", "") in f.lower().replace(" ", ""):
                        if f.endswith((".ttf", ".otf")):
                            try:
                                path = os.path.join(root, f)
                                return ImageFont.truetype(path, size), font_name
                            except (OSError, IOError):
                                pass
    # Ultimate fallback: Pillow default
    return ImageFont.load_default(), "default"

# For headings:
heading_font, heading_font_name = find_font(["Poppins-Bold", "Poppins", "Arial-Bold", "Arial"], size=72)

# For body/annotations:
body_font, body_font_name = find_font(["Lora-Regular", "Lora", "Georgia", "Arial"], size=24)
```

## Important Notes

- The `applied_heading_font` field in `design_parameters.json` must reflect whichever font was **actually loaded** — "Poppins" if found, otherwise the fallback name (e.g., "Arial").
- **Never** use Styrene A, Inter, or IBM Plex Sans as Anthropic brand fonts.
- Install Poppins via `pip install fonts-poppins` or download from Google Fonts if not present on the system. Attempt `apt-get install -y fonts-poppins` or manually download to `/root/.fonts/`.