---
name: run2_d3-bubble-chart
description: Creating D3.js v6 bubble charts with market cap sizing (scaleSqrt), sector coloring, inside ticker labels, and ETF uniform sizing — with correct tooltip suppression for ETFs.
---

# D3.js v6 Bubble Chart (Improved)

## Radius Scale
Use `d3.scaleSqrt()` so area is proportional to value:
```javascript
const UNIFORM_RADIUS = 18;
const marketCaps = data.filter(d => d.marketCapNum > 0).map(d => d.marketCapNum);

const radiusScale = d3.scaleSqrt()
    .domain([0, d3.max(marketCaps)])
    .range([8, 68]);

data.forEach(d => {
    d.radius = d.marketCapNum ? radiusScale(d.marketCapNum) : UNIFORM_RADIUS;
});
```

## Color Scheme — Explicit Sector Mapping
Define colors explicitly (not with d3.schemeOrdinal) for reproducibility:
```javascript
const SECTOR_COLORS = {
    'Information Technology': '#4e79a7',
    'Industry':               '#f28e2b',
    'Financial':              '#59a14f',
    'Energy':                 '#e15759',
    'ETF':                    '#76b7b2'
};
```

## Drawing Circles and Labels
```javascript
const circles = svg.selectAll('circle.bubble')
    .data(nodes, d => d.ticker)
    .join('circle')
    .attr('class', 'bubble')
    .attr('cx', d => d.x)
    .attr('cy', d => d.y)
    .attr('r', d => d.radius)
    .attr('fill', d => SECTOR_COLORS[d.sector])
    .attr('stroke', 'rgba(255,255,255,0.6)')
    .attr('stroke-width', 1.5);

// Labels — font-size proportional to radius, clamped to readable range
const labels = svg.selectAll('text.bubble-label')
    .data(nodes, d => d.ticker)
    .join('text')
    .attr('class', 'bubble-label')
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .attr('font-size', d => Math.max(7, Math.min(13, d.radius * 0.55)))
    .attr('fill', 'white')
    .attr('pointer-events', 'none')
    .text(d => d.ticker);
```

## Tooltip — Skip ETFs
```javascript
circles.on('mouseover', function(event, d) {
    if (d.sector === 'ETF') return;  // ETFs: no tooltip
    tooltip.classed('visible', true)
        .html(`<strong>${d.ticker}</strong><br>${d['full name']}<br>${d.sector}`)
        .style('left', (event.clientX + 14) + 'px')
        .style('top', (event.clientY - 10) + 'px');
})
.on('mousemove', function(event, d) {
    if (d.sector === 'ETF') return;
    tooltip.style('left', (event.clientX + 14) + 'px')
           .style('top',  (event.clientY - 10) + 'px');
})
.on('mouseout', () => tooltip.classed('visible', false));
```

## Color Legend (HTML, outside SVG)
Prefer HTML legend for easy wrapping:
```html
<div id="legend"></div>
```
```javascript
Object.entries(SECTOR_COLORS).forEach(([sector, color]) => {
    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `<span class="legend-dot" style="background:${color}"></span>
                      <span>${sector}</span>`;
    document.getElementById('legend').appendChild(item);
});
```

## Market Cap Formatting
```javascript
function formatMarketCap(v) {
    if (!v) return 'N/A';
    if (v >= 1e12) return (v / 1e12).toFixed(2) + 'T';
    if (v >= 1e9)  return (v / 1e9).toFixed(2) + 'B';
    if (v >= 1e6)  return (v / 1e6).toFixed(2) + 'M';
    return v.toString();
}
```
