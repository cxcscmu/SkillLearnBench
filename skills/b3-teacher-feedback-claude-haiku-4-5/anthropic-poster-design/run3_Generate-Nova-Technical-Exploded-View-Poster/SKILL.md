---
name: Generate Nova Technical Exploded-View Poster
description: Creates a minimalist technical exploded-view poster of the Nova edge device for Anthropic's internal engineering handbook. Displays at least 5 hardware layers (Casing, Thermal Unit, PCB, Battery, Interface) with official Anthropic brand colors, typography, and design standards. Outputs a PNG poster and a JSON file with applied brand color hex values and heading font name.
---

## Overview
This skill generates a technical exploded-view poster of the Nova device that adheres to Anthropic's official brand guidelines and design standards. The poster maintains a minimalist, low-saturation aesthetic with clean typography and precise color application.

## Anthropic Brand Color Palette (Ground-Truth)
- **Background (Identity Light)**: `#faf9f5`
- **Corporate Dark**: `#141413`
- **Primary Brand Accent**: `#d97757` (Orange)
- **Secondary Brand Accent**: `#6a9bcc` (Blue)
- **Tertiary Brand Accent**: `#788c5d` (Green)
- **Muted Mid Gray (Annotation Lines)**: `#b0aea5`
- **Heading Font**: Inter (or equivalent sans-serif aligned with Anthropic guidelines)

## Step 1: Set Up Canvas and Background
- Canvas dimensions: 1200 × 1600 pixels
- Background color: Apply Anthropic Identity Light (`#faf9f5`)
- Ensure all edges are clean with no gradient overlays or decorative elements

## Step 2: Create Title Block
- Position "NOVA" heading in the top-left corner
- Font: Inter, Bold, 64px
- Color: Corporate Dark (`#141413`)
- Padding: 40px from top and left edges
- Add a subtle underline accent in Primary Brand Accent (`#d97757`), 3px height, 60px width

## Step 3: Build Exploded-View Layers (Center of Poster)
Create five distinct hardware layers, each exploded vertically with consistent spacing:

### Layer 1: Outer Casing
- Shape: Rounded rectangle (12px corner radius)
- Color: Corporate Dark (`#141413`)
- Dimensions: 320 × 200px
- Position: Centered horizontally, starting at Y=250px
- Label: "Casing" in 12px Inter, Corporate Dark
- Add thin border in Muted Mid Gray (`#b0aea5`), 1.5px

### Layer 2: Interface/Connector Assembly
- Shape: Horizontal bar with connector ports
- Color: Primary Brand Accent (`#d97757`)
- Dimensions: 300 × 40px
- Position: Centered, exploded 180px above Layer 1
- Connector highlights: 3 small circles (8px diameter each) in Corporate Dark
- Label: "Interface & Connectors"

### Layer 3: Thermal Management Unit
- Shape: Grid-pattern rectangle (representing heat-sink fins)
- Color: Secondary Brand Accent (`#6a9bcc`)
- Dimensions: 310 × 60px
- Position: Centered, 120px above Layer 1
- Internal pattern: 5 horizontal lines in white (20% opacity) to suggest fins
- Label: "Thermal Management Unit"

### Layer 4: PCB (Main Board)
- Shape: Rectangle with component placeholders
- Color: Tertiary Brand Accent (`#788c5d`)
- Dimensions: 300 × 80px
- Position: Centered, 40px below Layer 1
- Component dots: 8 small circles (4px) scattered across surface in Corporate Dark (30% opacity)
- Label: "PCB & Processing Core"

### Layer 5: Battery Module
- Shape: Rounded rectangle
- Color: Secondary Brand Accent (`#6a9bcc`)
- Dimensions: 280 × 70px
- Position: Centered, 140px below Layer 4
- Battery terminals: 2 small rectangles (15 × 8px) at top in Primary Brand Accent (`#d97757`)
- Label: "Battery Module"

## Step 4: Add Annotation Leader Lines and Labels
- Leader line color: Muted Mid Gray (`#b0aea5`)
- Leader line weight: 1px (thin, as specified)
- Annotation style:
  - Draw leader lines from each layer to the right margin
  - Place technical specifications beside each line in 11px Inter, Corporate Dark
  - Example annotations: "Aluminum alloy, 2.1mm thickness", "Passive cooling matrix", "2-layer substrate", etc.
  - Keep annotations concise and technical

## Step 5: Add Technical Details and Connectors
- Highlight key interaction points (ports, buttons) in Primary Brand Accent (`#d97757`)
- Use 2px strokes for connector outlines
- Add 1–2 dimension lines (showing scale) in Muted Mid Gray with endpoint circles

## Step 6: Export Files

### File 1: PNG Poster
- Export as `/root/nova_technical_poster.png`
- Resolution: 1200 × 1600 pixels at 72 DPI
- Format: PNG with full alpha channel support (for clean edges)
- Compression: Standard PNG compression

### File 2: Design Parameters JSON
- Export as `/root/design_parameters.json`
- Use the exact JSON structure provided:

```json
{
  "background_hex": "#faf9f5",
  "corporate_dark_hex": "#141413",
  "primary_accent_hex": "#d97757",
  "secondary_accent_hex": "#6a9bcc",
  "tertiary_accent_hex": "#788c5d",
  "muted_mid_gray_hex": "#b0aea5",
  "applied_heading_font": "Inter"
}
```

## Step 7: Quality Assurance Checklist
- [ ] All hex values match ground-truth Anthropic brand guidelines
- [ ] Muted Mid Gray is `#b0aea5` (not `#999999`)
- [ ] Background is `#faf9f5` (not `#f5f5f5`)
- [ ] Primary Accent is `#d97757` orange (not `#6366f1`)
- [ ] Corporate Dark is `#141413` (not `#1a1a1a`)
- [ ] Secondary Accent and Tertiary Accent values verified
- [ ] No neon colors, gradients, or high-intensity "AI" styling applied
- [ ] Poster maintains minimalist, low-saturation aesthetic
- [ ] Title "NOVA" is clearly visible in top-left
- [ ] All 5 hardware layers are distinct and labeled
- [ ] Annotation lines are thin (1px) in Muted Mid Gray
- [ ] JSON file contains only hex values and heading font name
- [ ] Both PNG and JSON files are saved to `/root/`

## Notes
- Keep the overall design clean, technical, and professional
- Avoid decorative elements; prioritize clarity and information hierarchy
- Ensure sufficient contrast between colors and background for readability
- All typography should use Inter or Anthropic-aligned sans-serif
- The exploded view should convey a sense of depth and layer separation without appearing cluttered