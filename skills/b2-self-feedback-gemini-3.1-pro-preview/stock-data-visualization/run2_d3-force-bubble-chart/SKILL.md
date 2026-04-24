---
name: run2_d3-force-bubble-chart
description: Guide to building a polished D3.js (v6) force-directed bubble chart and a synchronized data table, including integrating secondary data for sparklines.
---

# D3.js Force-Directed Bubble Chart with Synchronized Table

This skill explains how to build a D3.js (v6) force-directed bubble chart where nodes (bubbles) are scaled by a specific attribute (e.g., market capitalization), colored by category (e.g., sector), and clustered using D3 forces. It also covers synchronizing interaction (hover/click) between the bubble chart and an HTML table.

## 1. Setup Data & Sizing
When scaling bubbles by an area metric (like market cap), use a square root scale:
```javascript
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.marketCap)])
  .range([minRadius, maxRadius]);
```
Handle missing data by assigning a default radius.

## 2. Force Simulation
To cluster bubbles by category, you define a central point for each category, or use `forceX` and `forceY` keyed to the category.
```javascript
const simulation = d3.forceSimulation(data)
  .force('x', d3.forceX(d => clusterCenters[d.category].x).strength(0.1))
  .force('y', d3.forceY(d => clusterCenters[d.category].y).strength(0.1))
  .force('collide', d3.forceCollide(d => radiusScale(d.value) + 1).iterations(4))
  .force('charge', d3.forceManyBody().strength(-2)); // Repel to prevent overlapping initially
```
For "close together and centered reasonably", calculate dynamic centers based on category indices mapped in a tight circle or a grid layout around the middle.

## 3. Rendering Nodes
Append SVG groups (`g`) for each data point containing a `circle` and `text`.
```javascript
const nodeGroup = svg.selectAll('.node')
  .data(data)
  .enter().append('g')
  .attr('class', 'node');

nodeGroup.append('circle')
  .attr('r', d => radiusScale(d.value))
  .style('fill', d => colorScale(d.category));

nodeGroup.append('text')
  .text(d => d.label)
  .each(function(d) {
      const r = radiusScale(d.value);
      d3.select(this).style('font-size', r > 15 ? '12px' : r > 10 ? '10px' : '0px');
  });

simulation.on('tick', () => {
  nodeGroup.attr('transform', d => `translate(${d.x},${d.y})`);
});
```

## 4. Synchronizing with HTML Table
Render the table:
```javascript
const rows = d3.select('tbody').selectAll('tr')
  .data(data)
  .enter().append('tr')
  .attr('id', d => `row-${d.id}`);
```

Add interaction:
```javascript
function highlightItem(id) {
  d3.selectAll('.node circle').classed('selected', false);
  d3.selectAll('tr').classed('selected-row', false);
  
  d3.select(`#circle-${id}`).classed('selected', true);
  d3.select(`#row-${id}`).classed('selected-row', true);
  
  const row = document.getElementById(`row-${id}`);
  if (row) row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

nodeGroup.on('click', (event, d) => highlightItem(d.id));
rows.on('click', (event, d) => highlightItem(d.id));
```

## 5. Integrating Secondary Data (Sparklines)
If required to display secondary data (like price history), load it concurrently:
```javascript
Promise.all([
  d3.csv('data1.csv'),
  d3.csv('data2.csv') // Or fetch within an interaction
]).then(([data1, data2]) => { ... })
```
Sparklines can be rendered inside a tooltip when a node is hovered over.