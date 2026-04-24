---
name: d3-color-legend
description: Add a categorical color legend to a D3 chart using colored rectangles or circles with text labels, supporting both SVG-inline and HTML overlay styles.
---

# D3 v6 Categorical Color Legend

## Overview

A color legend maps category names to colors, placed either inside the SVG or as an HTML overlay. Use this whenever a chart uses a categorical color scale.

## SVG Inline Legend

```javascript
const legend = svg.append('g')
    .attr('class', 'legend')
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

const legendItems = legend.selectAll('.legend-item')
    .data(categories)
    .join('g')
    .attr('class', 'legend-item')
    .attr('transform', (d, i) => `translate(0, ${i * 22})`);

// Color swatch (circle or rect)
legendItems.append('circle')
    .attr('r', 7)
    .attr('cx', 7)
    .attr('cy', 0)
    .attr('fill', d => colorScale(d));

// Label
legendItems.append('text')
    .attr('x', 18)
    .attr('y', 4)
    .style('font-size', '13px')
    .text(d => d);
```

## HTML Overlay Legend

Place outside the SVG for more flexible layout:

```html
<div class="legend-container" id="chart-legend"></div>
```

```javascript
const legendDiv = d3.select('#chart-legend');
legendDiv.selectAll('.legend-item')
    .data(categories)
    .join('div')
    .attr('class', 'legend-item')
    .html(d => `
        <span class="legend-swatch" style="background:${colorScale(d)}"></span>
        <span class="legend-label">${d}</span>
    `);
```

CSS:
```css
.legend-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px 20px;
    margin: 8px 0;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
}
.legend-swatch {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
```

## Recommended Color Scales

```javascript
// Tableau10 (10 distinguishable categorical colors)
const colorScale = d3.scaleOrdinal(d3.schemeTableau10);

// Custom palette for specific categories
const colorScale = d3.scaleOrdinal()
    .domain(['ETF', 'Energy', 'Financial', 'Industry', 'Information Technology'])
    .range(['#6baed6', '#fd8d3c', '#74c476', '#9e9ac8', '#f768a1']);

// Safe for colorblind users (Wong palette)
const WONG = ['#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7','#000000'];
const colorScale = d3.scaleOrdinal().range(WONG);
```

## Interactive Legend (Hover to Highlight)

```javascript
legendItems
    .style('cursor', 'pointer')
    .on('mouseover', function(event, cat) {
        // Dim all bubbles not in this category
        d3.selectAll('circle.bubble')
            .style('opacity', d => d.category === cat ? 1 : 0.2);
    })
    .on('mouseout', function() {
        d3.selectAll('circle.bubble').style('opacity', 1);
    });
```

## Placement Tips

- For a vertical legend, position at `(width - legendWidth, margin.top)`.
- For a horizontal legend under the chart, use flex-wrap HTML layout.
- Keep legend items 20–24px apart vertically for readability.
- Use consistent font-size (12–14px) and color contrast (dark text on light background).
