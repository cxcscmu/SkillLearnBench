You are working as a Brand Design Engineer at Anthropic. We need to generate a "Technical Exploded-View" for the upcoming Nova edge device to be used in our internal engineering handbook. Apply Anthropic’s official brand colors and typography to the artifact wherever brand styling is relevant. Use Anthropic’s company design standards, visual formatting, and brand tokens consistently across the poster, including background, hardware accents, annotation lines, and title typography.

The requirements are: 
1.  Create a clean technical poster showing the Nova device as an exploded-view showing at least 5 layers of internal hardware (Casing, Thermal Unit, PCB, Battery, Interface).
2.  Color Application Strategy:
    * The outer casing should use Anthropic Corporate Dark.
    * The entire poster background must be the Anthropic Identity Light color.
    * Use the Tertiary Brand Accent for the PCB substrate and the Secondary Brand Accent for the Thermal Management unit.
    * The primary interaction details and connector highlights should use the Primary Brand Accent.
    * Annotation leader lines should appear in a thin Muted Mid Gray.
3.  Place the product title "NOVA" in the top-left as a clear heading block.
4.  The overall image must remain minimalist, low-saturation, and explicitly avoid neon or high-intensity "AI gradient" styling.

Generate `/root/nova_technical_poster.png` as the final poster image. Also generate `/root/design_parameters.json`, which must contain only the applied HEX color values and the heading font name used in the poster, using exactly the following JSON structure:
{
  "background_hex": "",
  "corporate_dark_hex": "",
  "primary_accent_hex": "",
  "secondary_accent_hex": "",
  "tertiary_accent_hex": "",
  "muted_mid_gray_hex": "",
  "applied_heading_font": ""
}