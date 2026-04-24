---
name: exploded-view-generator
description: How to generate 2D isometric or exploded-view technical posters programmatically. Use this skill whenever the user asks for a technical exploded-view, internal hardware layers, or an isometric hardware diagram.
---

# Exploded-View Generator

This skill outlines how to generate an exploded-view diagram of a hardware device using Python (e.g., PIL or Matplotlib), particularly for the "Nova" edge device or similar multi-layer hardware.

## Diagram Elements
A technical exploded view typically shows hardware layers pulled apart along an isometric axis.

### Layers Required (Bottom to Top)
1. **Outer Casing (Bottom)**: Base shell.
2. **PCB (Printed Circuit Board)**: The logic substrate.
3. **Battery**: Power unit.
4. **Thermal Management Unit**: Heat sink or thermal spreader.
5. **Interface / Outer Casing (Top)**: The top cover or user-facing interface.

## Generation Guidelines
- **Perspective**: Use an isometric or pseudo-isometric projection (e.g., drawing parallelograms stacked diagonally to represent layers).
- **Styling**: 
  - Apply provided corporate colors (e.g., Anthropic Identity Light for background, Corporate Dark for casing, specific accents for PCB, Thermal, and Interface).
  - Include annotation lines (Muted Mid Gray) pointing from the layers to descriptive text.
- **Typography**: Place the title block in the top-left using the required corporate font.
- **Tools**: `Pillow` (PIL) or `Matplotlib` can be used to draw shapes. For basic 2D representation, drawing polygons for each layer with offsets along the Y-axis simulates the "exploded" effect.

## Output Generation Steps
1. Define a canvas with the specified background color.
2. Draw a clear Title block in the top-left corner.
3. Define polygon coordinates for the isometric layers.
4. Draw each layer from back to front (bottom to top), applying the requested fill colors.
5. Draw thin annotation lines (`width=1` or `width=2`) connecting each layer to text labels.
6. Render the final image and save it to the specified output path.