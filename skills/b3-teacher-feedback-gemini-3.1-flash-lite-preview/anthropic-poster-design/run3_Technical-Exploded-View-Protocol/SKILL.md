---
name: Technical-Exploded-View-Protocol
description: Provides the workflow for creating minimalist, low-saturation technical illustrations using the Nova device as a template.
---

1.  **Exploded-View Architecture:** Organize layers in a vertical, non-intersecting axis (Casing, Thermal Unit, PCB, Battery, Interface).
2.  **Color Assignment:**
    *   **Casing:** `#191919`
    *   **Thermal Management Unit:** `#6a9bcc`
    *   **PCB Substrate:** `#788c5d`
    *   **Interaction Highlights:** `#d97757`
    *   **Leader Lines:** `#8f8c87` (0.5pt weight)
3.  **Visual Aesthetic:** Apply a flat, minimalist rendering style. Avoid shadows, glows, or high-intensity gradients. Ensure the background remains solid `#faf9f5`.
4.  **Output Generation:** Export final raster as `/root/nova_technical_poster.png` and finalize the configuration as `/root/design_parameters.json` using the verified HEX values and *Graphik* font.