---
name: run2_professional-technical-layout
description: Professional technical diagram layout with grid systems, visual hierarchy, and spatial organization
---

# Professional Technical Layout Design

## Compositional Grid System

### Standard Technical Poster (16:9 Aspect Ratio)

For 1920×1440px poster:
```
+------+----+----+----+----+----+----+----+----+------+
| Safe | 80px margin                          | Safe |
| Area +----------------------------------+  Area
|      |       Content Area (1760×1280px)  |  |
|      | Title: 100px height               |  |
|      | Device: 800px height (centered)   |  |
|      | Labels: 120px below device        |  |
|      | Annotations: Sides (±350px from center)
|      +----------------------------------+  |
+------+----+----+----+----+----+----+----+----+------+
```

### Margin Standards
- Top/Bottom: 80-120px (breathing room)
- Left/Right: 80-100px (balanced gutters)
- Between sections: 40-60px (visual separation)

## Exploded-View Spatial Relationships

### Linear Offset Model
```
Layer 1 (Casing):        Y = 250px
Layer 2 (Interface):     Y = 340px (offset: +90px)
Layer 3 (Thermal):       Y = 430px (offset: +90px)
Layer 4 (PCB):           Y = 520px (offset: +90px)
Layer 5 (Battery):       Y = 610px (offset: +90px)
```

Consistency ensures viewers understand assembly progression.

### Horizontal Alignment
All layers:
- Left edge: center_x - (width/2)
- Center: center_x
- Right edge: center_x + (width/2)

Maintains single axis of assembly (reduces cognitive load).

## Visual Hierarchy with Typography

### Text Sizing Strategy
```
Title ("NOVA"):          72-96pt   Bold     Primary element
Subtitle:                14-16pt   Regular  Supporting info
Component Labels:        16-18pt   Bold     Primary callouts
Annotation Text:         12-14pt   Regular  Secondary info
Footer/Attribution:      10-12pt   Regular  Least important
```

### Spacing Between Components and Labels
```
Component Bottom → Label Top:  30-40px
Label Text → Next Component:  60-80px
Annotation Text ← Leader Line: 25-35px
```

## Annotation Organization

### Quadrant-Based Layout
```
         TOP AREA
           (Title)

LEFT       |     DEVICE CENTER     |      RIGHT
CALLOUTS   |    (Exploded View)    |    CALLOUTS

       BOTTOM AREA
    (Footer/Attribution)
```

### Callout Placement Rules
1. **Balance**: Equal annotations on left/right (visual equilibrium)
2. **Proximity**: Place callout near its component reference
3. **Avoid Overlap**: Never place text over component diagrams
4. **Visual Flow**: Read top-to-bottom, left-to-right naturally

### Leader Line Best Practices
- **Angle**: 45° or more from horizontal (clearer direction)
- **Direction**: Point outward from components (clarity)
- **Terminal**: Dot (4-6px) at component, arrow or nothing at label
- **Simplicity**: Direct lines, avoid bent/curved (technical aesthetic)

## Color Distribution Pattern

### Surface Treatment (Components)
- Base Color: Primary color (casing, thermal, PCB, battery)
- Accent Edge: Secondary or accent color (top/left edge)
- Highlight Detail: White or contrast color (internal features)
- Border: 1-2px subtle outline in same or darker variant

### Annotation System
- Leader Line: Muted gray (visual glue, low weight)
- Callout Dot: Muted gray with border
- Text: Dark text on light background (standard contrast)

## Component Sizing

### Relative Proportions
For exploded-view devices, components typically decrease in size:
```
Casing:           400 × 180px  (100%)
Interface:        360 × 150px  (90%)
Thermal:          320 × 140px  (80%)
PCB:              280 × 130px  (70%)
Battery:          240 × 120px  (60%)
```

Creates natural visual taper and spatial progression.

## Professional Finishing Touches

1. **Alignment**: Use grid helpers to ensure straight edges
2. **Consistency**: Match line weights and spacing precisely
3. **Breathing Room**: Generous margins around all content
4. **Contrast**: Sufficient color contrast for readability
5. **Finish**: Add subtle attribution/date footer for documentation
6. **Polish**: Review for visual balance before export

## Layout QA Checklist

- [ ] All layers horizontally aligned to center axis
- [ ] Vertical spacing consistent between components
- [ ] Annotations balance left/right
- [ ] No text overlaps components
- [ ] Leader lines point clearly to components
- [ ] Color contrast meets WCAG AA (4.5:1 minimum)
- [ ] All text legible at printed sizes
- [ ] Margins provide breathing room
- [ ] Title area clearly distinguished
- [ ] Footer provides proper attribution
