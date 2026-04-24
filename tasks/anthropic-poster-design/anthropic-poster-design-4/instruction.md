You are working as a Brand Design Engineer at Anthropic. We need to generate a technical internal visual for the upcoming Orion edge control module to be used in our engineering handbook. Apply Anthropic’s official brand colors and typography to the artifact wherever brand styling is relevant. Use Anthropic’s company design standards, visual formatting, and brand tokens consistently across the poster, including the background, dominant hardware forms, annotation details, and title typography.

The requirements are:
1. Create a clean technical poster showing the Orion device as a separated internal hardware composition with multiple clearly readable modules, suitable for internal engineering documentation.
2.  Color Application Strategy:
    * The outer casing should use Anthropic Corporate Light.
    * The entire poster background must be the Anthropic Corporate Dark.
    * Use the Tertiary Brand Accent for the PCB substrate and the Secondary Brand Accent for the Thermal Management unit.
    * The primary interaction details and connector highlights should use the Primary Brand Accent.
    * Annotation leader lines should appear in a thin Muted Mid Gray.
3. The overall image must remain minimalist, low-saturation, and explicitly avoid neon or high-intensity "AI gradient" styling. The composition should feel precise, editorial, and technically legible rather than promotional.

Generate `/root/orion_technical_poster.png` as the final poster image. Also generate `/root/design_parameters.json`, which must contain only the applied HEX color values used in the poster, using exactly the following JSON structure:
{
  "background_hex": "",
  "corporate_light_hex": "",
  "primary_accent_hex": "",
  "secondary_accent_hex": "",
  "tertiary_accent_hex": "",
  "muted_mid_gray_hex": ""
}