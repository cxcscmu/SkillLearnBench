---
name: Define CSS Classes for Selection and Highlighting States
description: Create CSS styling for `.selected` (bubbles), `.highlighted` (table rows), and `.tooltip` classes to provide clear visual feedback for user interactions
---

```css
/* Bubble chart selection styling */
circle.selected {
  stroke: #ff6b6b;
  stroke-width: 3px;
}

/* Table row highlighting styling */
tr.highlighted {
  background-color: #fff3cd;
}

tr.highlighted:hover {
  background-color: #ffe69c;
}

/* Tooltip styling */
.tooltip {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  pointer-events: none;
  z-index: 1000;
  max-width: 200px;
  word-wrap: break-word;
}

/* Ensure tooltips don't interfere with other elements */
.tooltip strong {
  display: block;
  margin-bottom: 4px;
}

.tooltip em {
  display: block;
  font-style: italic;
  margin-top: 4px;
  font-size: 11px;
  opacity: 0.9;
}
```

Key styling points:
- `.selected` on circles: use distinct stroke color and width for visibility
- `.highlighted` on table rows: use background color that contrasts with default row color
- `.tooltip`: ensure it has proper positioning and doesn't block interaction
- Test that selection/highlight states are clearly visible in the browser
- Ensure colors don't conflict with existing color scheme (sector colors in bubbles)