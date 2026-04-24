---
name: generate_anthropic_technical_artifact
description: Create technical diagrams and posters adhering to Anthropic's official brand guidelines. Use this skill to produce exploded-view hardware visualizations with specific brand color tokens, typography, and minimalist styling.
---

### Anthropic Brand Design Standards

When generating technical artifacts for Anthropic, adhere to the following color palette and typography standards:

| Token Name | Hex Code | Usage |
| :--- | :--- | :--- |
| **Identity Light** | `#f5f2ed` | Backgrounds, primary canvas color |
| **Corporate Dark** | `#191919` | Outer casings, primary text, dark hardware components |
| **Primary Brand Accent** | `#d97757` | Interaction points, connector highlights, primary emphasis |
| **Secondary Brand Accent** | `#3e76d1` | Thermal management units, cooling systems, secondary highlights |
| **Tertiary Brand Accent** | `#788c5d` | PCB substrate, environmental/internal hardware logic |
| **Muted Mid Gray** | `#999999` | Annotation leader lines, secondary mechanical details |

**Typography:**
- **Heading Font:** `LL Replay` (Standard Anthropic heading font)
- **Body/Annotation Font:** `Inter` or `LL Replay` (Regular weight)

### Task Execution: Nova Technical Poster

#### 1. Image Composition (`/root/nova_technical_poster.png`)
- **Background:** Fill the entire canvas with `#f5f2ed`.
- **Title Block:** Place the text "NOVA" in the top-left corner using the `LL Replay` font in `#191919`.
- **Exploded View Layers:** Arrange at least 5 layers vertically or diagonally:
    1. **Casing (Top/Outer):** Rendered in `#191919` (Corporate Dark).
    2. **Thermal Unit:** Rendered in `#3e76d1` (Secondary Brand Accent).
    3. **PCB:** Rendered in `#788c5d` (Tertiary Brand Accent).
    4. **Battery:** Rendered in a neutral tone (e.g., `#d1cdc7`).
    5. **Interface/Connectors:** Highlights rendered in `#d97757` (Primary Brand Accent).
- **Annotations:** Use thin leader lines in `#999999` (Muted Mid Gray) to label the components.
- **Styling:** Maintain a minimalist, low-saturation technical look. Avoid all neon effects, glows, or high-intensity "AI gradients."

#### 2. Design Parameters (`/root/design_parameters.json`)
Generate a JSON file containing the exact values used in the poster:
```json
{
  "background_hex": "#f5f2ed",
  "corporate_dark_hex": "#191919",
  "primary_accent_hex": "#d97757",
  "secondary_accent_hex": "#3e76d1",
  "tertiary_accent_hex": "#788c5d",
  "muted_mid_gray_hex": "#999999",
  "applied_heading_font": "LL Replay"
}
```