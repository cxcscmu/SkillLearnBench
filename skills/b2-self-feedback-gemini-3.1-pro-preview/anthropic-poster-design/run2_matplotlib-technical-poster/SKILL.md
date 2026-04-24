---
name: run2_matplotlib-technical-poster
description: Advanced techniques for rendering 2D isometric exploded views of hardware using Matplotlib.
---

# Technical Isometric Posters with Matplotlib

To build high-quality technical diagrams such as exploded hardware views without a 3D engine, use Matplotlib's 2D `Polygon` objects to simulate an isometric perspective.

## Implementation Pattern

1. **Define an Isometric Base**: Create a base 2D array of coordinates representing a flat skewed plane (e.g., a rhombus or parallelogram).
2. **Extrude Layers (Thickness)**: To make layers look 3-dimensional, draw the bottom faces, side faces, and then the top face. This involves offsetting the base coordinates downwards by a `thickness` value.
3. **Exploded Vertical Separation**: Add a `z_offset` to each layer's coordinates to separate them vertically along the Y-axis.
4. **Highlights & Connectors**: Draw smaller polygons on the top faces to simulate chips, connectors, or interaction points using accent colors.
5. **Leader Lines & Annotations**: Use `ax.plot()` to draw thin, straight lines from the hardware components to the right side of the canvas. Use `ax.text()` to label each layer with sans-serif typography.
6. **Background & Canvas**: Set `fig.set_facecolor()` and `ax.set_facecolor()` to the brand's Identity Light color, and hide the axes.

## Layer Ordering

Always draw from bottom to top (in terms of Z-index or vertical offset) to ensure proper occlusion.
- Bottom casing/interface (Lowest `z_offset`, drawn first)
- Battery
- PCB
- Thermal Unit
- Top casing (Highest `z_offset`, drawn last)
