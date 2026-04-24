---
name: run2_anthropic-brand-tokens
description: Precise Anthropic brand color tokens and typography guidelines for design artifacts, with matplotlib-specific notes.
---

# Anthropic Brand Tokens (Refined)

## Color Palette

| Token Name | Design Role | HEX |
|---|---|---|
| **Identity Light** | Page / poster background (never pure white) | `#FAF9F7` |
| **Corporate Dark** | Outer casing, headings, dark UI elements | `#1A1816` |
| **Primary Brand Accent** | Connectors, CTAs, interaction highlights | `#CF6E35` |
| **Secondary Brand Accent** | Thermal management, supporting hardware | `#8C9FA0` |
| **Tertiary Brand Accent** | PCB substrate, circuit-board elements | `#7A8B72` |
| **Muted Mid Gray** | Annotation leader lines, dividers | `#9B9B9B` |

### Supporting Colors (derived, not brand tokens)
| Name | Usage | HEX |
|---|---|---|
| Battery Warm Neutral | Battery pack layer | `#C8BFB4` |
| Metadata Bar | Footer/header subtle bar | `#EDEAE5` |

## Color Rationale
- **Identity Light** (#FAF9F7): warm off-white; the subtle sepia undertone prevents sterility
- **Corporate Dark** (#1A1816): very dark warm charcoal; never cold pure black
- **Primary** (#CF6E35): Anthropic's terracotta/coral signature — used sparingly for maximum impact
- **Secondary** (#8C9FA0): muted teal-gray — a cool industrial complement for thermal hardware
- **Tertiary** (#7A8B72): muted sage/olive — organic feel suits PCB green substrate
- **Mid Gray** (#9B9B9B): exactly mid-brightness neutral for structural lines

## Typography

### matplotlib Font Guidance
- **System font for matplotlib on Linux**: `DejaVu Sans` (always available, sans-serif)
- **Preferred when installed**: `Inter`, `Helvetica Neue`, or `Arial`
- Check available fonts: `from matplotlib import font_manager; [f.name for f in font_manager.fontManager.ttflist]`

### Letter-spacing in matplotlib
- **IMPORTANT**: `letter_spacing` is NOT a valid matplotlib Text property — it will raise AttributeError
- Simulate letter-spacing by inserting spaces between characters: `"N O V A"` instead of `"NOVA"`
- For large display titles, spaces of 1–2 characters work well

### Text Hierarchy
| Level | Size | Weight | Color |
|---|---|---|---|
| Display title (NOVA) | 52–60pt | bold | Identity Light on dark bg |
| Subtitle | 9–10pt | light | Muted Mid Gray |
| Layer label | 9pt | regular | Corporate Dark |
| Annotation text | 8pt | light | Corporate Dark |
| Metadata | 7.5pt | regular | Muted Mid Gray |

## Brand Constraints
1. Background MUST be Identity Light (#FAF9F7), never pure #FFFFFF
2. No neon colors, no high-saturation gradients
3. Primary accent appears only for focal interaction points (not for backgrounds)
4. Low saturation overall — muted, professional, warm-neutral aesthetic
5. Dark bars (title/footer) use Corporate Dark, NOT pure black
