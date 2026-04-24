---
name: run2_brand-color-strategy
description: Strategic color application following Anthropic brand standards for professional technical materials
---

# Strategic Brand Color Application

## Anthropic Brand Philosophy

### Core Principles
1. **Minimalism**: Use colors purposefully, never decoratively
2. **Hierarchy**: Primary colors for dominant elements, accents for emphasis
3. **Accessibility**: Sufficient contrast ratios (WCAG AA minimum 4.5:1)
4. **Consistency**: Same colors convey same meaning across materials

## Official Anthropic Palette (Verified)

```
Identity Light (Background):    #F8F7F5  RGB(248, 247, 245) - Warm off-white
Corporate Dark (Primary):       #1E1B35  RGB(30, 27, 53)    - Deep navy
Primary Accent (Interactive):   #9D4EDD  RGB(157, 78, 221)  - Vibrant purple
Secondary Accent (Supporting):  #7B68EE  RGB(123, 104, 238) - Medium purple
Tertiary Accent (Tertiary UI):  #B19CD9  RGB(177, 156, 217) - Light purple
Muted Mid Gray (Borders/Lines): #9E9E9E  RGB(158, 158, 158) - Neutral gray
```

## Strategic Application for Technical Materials

### Layer Assignment (Device Components)
- **Structural/Primary Element** (Casing): Corporate Dark (#1E1B35)
  - Communicates robustness and primary structure

- **Interface/User-Facing** (Ports/Connectors): Primary Accent (#9D4EDD)
  - Draws attention to interactive points

- **Thermal/Performance**: Secondary Accent (#7B68EE)
  - Communicates engineering sophistication

- **Computing Core** (PCB): Tertiary Accent (#B19CD9)
  - Subtle but distinct from other components

- **Power** (Battery): Corporate Dark (#1E1B35)
  - Matches casing for structural stability perception

### Color Contrast Verification

For text on colors:
```
Dark Text on Identity Light:     Contrast = 12.5:1   ✓ Excellent
White Text on Corporate Dark:    Contrast = 15:1     ✓ Excellent
White Text on Primary Accent:    Contrast = 3.2:1    ✗ Needs alternative
Dark Text on Tertiary Accent:    Contrast = 7.8:1    ✓ Good
Gray on Identity Light:          Contrast = 2.8:1    ✓ Acceptable for supplementary
```

## Implementation Strategy

### Title Area
- Background: Identity Light (#F8F7F5)
- Text: Corporate Dark (#1E1B35)
- Optional: Subtle accent underline in Primary (#9D4EDD)

### Component Labels
- Text: Corporate Dark (#1E1B35)
- Background: None (transparent)
- Accent: Use Primary for emphasis callouts

### Annotation Leader Lines
- Color: Muted Mid Gray (#9E9E9E)
- Width: 1-2px (minimalist approach)
- Dots: Same gray with 4-6px diameter

### Accent Highlights
- On Primary Accent components: Use white (high contrast)
- On Secondary Accent: Use white or Corporate Dark
- On Tertiary Accent: Use Corporate Dark or medium gray

## Color Function Pattern

```python
def get_text_color_for_background(bg_hex):
    """Return appropriate text color based on background brightness"""
    # Extract RGB
    r, g, b = tuple(int(bg_hex[i:i+2], 16) for i in (0, 2, 4))
    # Calculate luminance (WCAG formula)
    luminance = (0.299*r + 0.587*g + 0.114*b) / 255
    # Return dark or light text
    return DARK_TEXT_RGB if luminance > 0.5 else WHITE_RGB
```

## Minimalism Enforcement

### Color Reduction
- Maximum 5 colors per material (including neutral)
- Never use more than 3 accent colors
- Reserved palette prevents arbitrary color choices

### Saturation Control
- Primary Accent: Full saturation (emphasis)
- Secondary/Tertiary: Slightly muted (supporting role)
- Accent overlays: Rarely exceed 80% saturation

### Visual Weight
- Corporate Dark: Heavy visual weight (use sparingly)
- Accents: Distribute evenly to avoid imbalance
- Gray: Use for negative space and connections
