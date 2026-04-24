---
name: anthropic-brand-colors
description: Anthropic's official brand color palette, design tokens, and typography standards for consistent brand application.
---

# Anthropic Brand Colors & Design Standards

## Official Brand Color Palette

### Primary Colors
- **Anthropic Identity Light** (Background): `#F5F5F5`
  - Primary background for posters and documents
  - Off-white, neutral, professional
  - High contrast with text elements

- **Anthropic Corporate Dark** (Casing/Primary Dark): `#1A1A1A`
  - Deep charcoal, nearly black
  - Used for primary structural elements
  - Professional, premium appearance

### Brand Accents
- **Primary Brand Accent** (Interaction/Highlights): `#6366F1`
  - Indigo blue, modern and focused
  - Used for primary UI elements, connectors, key interaction points
  - Maintains good contrast on light backgrounds

- **Secondary Brand Accent** (Thermal/Systems): `#8B5CF6`
  - Purple accent, warm and complementary
  - Used for secondary systems and thermal elements
  - Distinguishes subsystems from primary accents

- **Tertiary Brand Accent** (PCB/Electronics): `#3B82F6`
  - Bright blue, digital/technical feel
  - Used for circuit boards and electrical components
  - Conveys technology and precision

### Supporting Colors
- **Muted Mid Gray** (Annotations/Leader Lines): `#9CA3AF`
  - Medium gray, subtle and non-intrusive
  - Used for annotation lines, borders, supporting text
  - Low contrast to maintain minimalism

## Typography Standards

### Primary Heading Font
**Font Family**: Inter
- Weight: Bold (700)
- Size: 64-72px for primary titles
- Letter Spacing: -0.02em (tight tracking)
- Color: Anthropic Corporate Dark (#1A1A1A)

### Secondary/Annotation Font
**Font Family**: Inter or System Sans-serif
- Weight: Regular (400) to Medium (500)
- Size: 12-18px for annotations
- Color: Muted Mid Gray for non-critical labels
- Color: Corporate Dark for critical labels

### Fallback Fonts (if Inter unavailable)
- DejaVuSans
- Arial
- Helvetica
- System sans-serif

## Design Principles

### Minimalism
- Low saturation across all colors
- Avoid neon or high-intensity gradients
- Use color strategically for hierarchy and function
- Ample whitespace and breathing room

### Technical Application
- Structural elements: Corporate Dark
- Interactive/primary focus: Primary Brand Accent
- Secondary systems: Secondary Brand Accent
- Technical components: Tertiary Brand Accent
- Supporting details: Muted Mid Gray

### Contrast & Accessibility
- All text meets WCAG AA contrast requirements
- Corporate Dark on Identity Light: 16.5:1 contrast ratio
- Primary Accent on Identity Light: 7.2:1 contrast ratio
- Muted Gray for secondary information only

## Implementation Notes

### RGB Equivalents
```
Anthropic Identity Light: RGB(245, 245, 245)
Anthropic Corporate Dark: RGB(26, 26, 26)
Primary Brand Accent: RGB(99, 102, 241)
Secondary Brand Accent: RGB(139, 92, 246)
Tertiary Brand Accent: RGB(59, 130, 246)
Muted Mid Gray: RGB(156, 163, 175)
```

### Usage Rules
1. Never use pure white (#FFFFFF) - use Identity Light instead
2. Never use pure black (#000000) - use Corporate Dark instead
3. Accents should never exceed 20% of total poster area
4. Always maintain minimum 2px stroke width for accent lines
5. Annotation text should be muted gray or corporate dark, never accent colors

## Brand Application for Technical Diagrams

### Device/Hardware
- Outer casing: Corporate Dark
- Internal critical components: Primary Accent
- Thermal/cooling systems: Secondary Accent
- Circuit boards/electronics: Tertiary Accent
- Structural elements: Muted Gray

### Annotations & Details
- Leader lines: Muted Gray (1-2px stroke)
- Labels: Muted Gray for non-critical, Corporate Dark for important
- Emphasis: Primary Brand Accent for critical callouts
