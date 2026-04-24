---
name: styling_and_formatting
description: Defines the layout, chart aesthetics, and table styling in style.css.
---
Implement `style.css` to ensure:
1. Side-by-side layout: Use `.container { display: flex; }` for the bubble chart and table.
2. Table formatting: Style the table to be scrollable if it exceeds screen height. Ensure numbers are formatted using `d3.format(".2s")` or similar logic within the JS to convert raw numbers to strings like "1.64T".
3. Visual feedback: Define a `.highlight` class with a distinct background or border color to sync the bubble chart selection with the table row selection.
4. Responsive sizing: Ensure the bubble chart SVG has a defined width/height and that bubbles are contained within the viewbox.