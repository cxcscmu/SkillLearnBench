---
name: technical-illustration-design
description: Design principles and techniques for creating technical exploded-view diagrams and engineering documentation posters.
---

# Technical Illustration & Exploded-View Design

## Exploded-View Fundamentals

### Purpose
An exploded-view diagram shows how a product is assembled by separating and offsetting each component along a central axis, revealing internal structure and layers.

### Key Design Elements

1. **Layering Strategy**
   - Arrange components vertically or along a diagonal axis
   - Each layer shows a distinct component or assembly
   - Maintain consistent spacing between layers
   - Typically 3-7 layers for clarity

2. **Assembly Axis**
   - Define clear direction: vertical (top-down), diagonal (45°), or horizontal
   - All components should follow this axis consistently
   - Creates visual harmony and understanding of assembly order

3. **Component Highlighting**
   - Use color coding to distinguish different component types
   - Each layer should be visually distinct
   - Maintain color consistency throughout poster

## Five Essential Hardware Layers

For the Nova device example:

1. **Casing/Enclosure** (Outermost)
   - Outer protective shell
   - Color: Corporate Dark
   - Style: Solid, structured, geometric

2. **Thermal Management Unit**
   - Heat dissipation fins or thermal pads
   - Color: Secondary Brand Accent
   - Shows cooling capability
   - Geometric, modern appearance

3. **PCB (Printed Circuit Board)**
   - Main electronics substrate
   - Color: Tertiary Brand Accent
   - Smaller, intricate details
   - Shows circuit layout

4. **Battery/Power System**
   - Energy storage component
   - Color: Primary Brand Accent or Secondary
   - Rectangular or cylindrical shape
   - Often positioned prominently

5. **Interface Connectors** (Innermost/Integrated)
   - Ports, connectors, user interface elements
   - Color: Primary Brand Accent
   - Highlight with annotation lines
   - Shows connectivity

## Visual Hierarchy

### Title & Headers
- **Primary Title**: Large, bold, left-aligned or centered
- **Font**: Bold sans-serif (Inter, DejaVuSans)
- **Color**: Corporate Dark
- **Size**: 48-72px

### Annotations
- **Leader Lines**: Thin (1-2px), Muted Gray
- **Text Labels**: Smaller font (12-18px), Muted Gray
- **Important Labels**: Corporate Dark for emphasis
- **Arrows**: Simple, geometric, pointing to components

## Composition Techniques

### Isometric/Perspective Rendering
```
For 3D-like appearance on 2D canvas:
- Use polygon shapes with shading
- Front face: lighter fill
- Top/side face: darker fill (creates depth)
- Outline: thin stroke in Corporate Dark
```

### Spacing & Alignment
- Central axis (vertical or diagonal) as anchor
- Consistent spacing: 60-100px between layers
- Left alignment for text annotations
- Right alignment for leader lines from top

### Color Distribution
- 60% background (Identity Light)
- 25% structural elements (Corporate Dark)
- 15% accents and highlights (Brand Accents)
- Keep color intensity low and professional

## Annotation Best Practices

### Leader Lines
- Start from component
- Thin stroke (1-2px)
- Soft color (Muted Gray)
- End with small arrow or circle
- No harsh angles - use smooth curves where possible

### Labels
- Positioned near leader line endpoint
- Sans-serif font, 14-16px
- Muted Gray for non-critical information
- Corporate Dark for important specifications

### Callouts
- Highlight critical features with Primary Brand Accent
- Keep callouts minimal and focused
- Use consistent icon style for callout markers

## Layout Structure

### Recommended Poster Dimensions
- **16:9 Aspect Ratio**: 1920×1080px (digital) or 3840×2160px (high-res)
- **4:3 Aspect Ratio**: 1600×1200px or higher
- Minimum resolution: 1440×1080px

### Safe Margins
- Top: 80-120px (for title)
- Sides: 60-100px
- Bottom: 60-80px
- Leave breathing room around central device

## Implementation Workflow

1. **Background**: Solid Identity Light color
2. **Central Axis**: Invisible guide for alignment
3. **Components** (from outer to inner):
   - Casing outline (Corporate Dark)
   - Thermal unit (Secondary Accent)
   - PCB (Tertiary Accent)
   - Battery (Primary Accent)
   - Interfaces (Primary Accent with highlights)
4. **Annotations**: Leader lines and labels (Muted Gray)
5. **Title**: Bold heading (Corporate Dark)
6. **Final Details**: Border, metadata if needed

## Common Mistakes to Avoid

- ❌ Components too crowded or overlapping
- ❌ Inconsistent spacing or axis alignment
- ❌ Too many colors or high saturation
- ❌ Annotations obscuring device
- ❌ Inconsistent line weights
- ❌ Poor contrast between text and background
- ✓ Maintain minimalism and professional appearance

## Technical Diagram Best Practices

### Color Coding System
- Establish consistent meaning for each color
- Document color assignments
- Use same colors for same component types across multiple diagrams

### Clarity Rules
- One concept per annotation
- Avoid text overlap
- Use consistent font sizing
- Keep lines non-crossing where possible

### Professional Polish
- Consistent stroke weights (1-3px)
- Aligned text and elements
- Balanced composition
- High-resolution output (minimum 150 DPI)
