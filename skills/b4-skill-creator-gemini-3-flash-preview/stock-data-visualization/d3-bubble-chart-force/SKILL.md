name: d3-bubble-chart-force
description: How to create a bubble chart with D3.js v6 using force simulations for clustering and preventing overlaps. Use this skill whenever a bubble chart with clustered layouts is requested.

## Implementation Guide

### 1. Data Preparation
Ensure each data point has:
- A unique identifier (e.g., `ticker`)
- A value for sizing (e.g., `marketCap`)
- A categorical value for clustering (e.g., `sector`)

### 2. Sizing Scale
Use `d3.scaleSqrt()` for bubble radii to ensure the area of the bubble is proportional to the value.
```javascript
const radiusScale = d3.scaleSqrt()
    .domain([0, d3.max(data, d => d.marketCap || constantValue)])
    .range([minRadius, maxRadius]);
```

### 3. Force Simulation
Set up `d3.forceSimulation()` with multiple forces:
- `forceX` and `forceY`: Pull nodes toward their sector's cluster center.
- `forceCollide`: Prevent bubbles from overlapping.
- `forceManyBody`: Add slight repulsion if needed to avoid overcrowding.

```javascript
const simulation = d3.forceSimulation(data)
    .force("x", d3.forceX(d => sectorCenters[d.sector].x).strength(0.1))
    .force("y", d3.forceY(d => sectorCenters[d.sector].y).strength(0.1))
    .force("collide", d3.forceCollide(d => radiusScale(d.marketCap || constantValue) + padding))
    .on("tick", () => {
        node.attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });
```

### 4. Tooltips
Use a hidden `div` and update its position and content on mouse events.
```javascript
const tooltip = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);

node.on("mouseover", (event, d) => {
    tooltip.transition().duration(200).style("opacity", .9);
    tooltip.html(`Ticker: ${d.ticker}<br>Name: ${d.full_name}`)
           .style("left", (event.pageX + 10) + "px")
           .style("top", (event.pageY - 28) + "px");
})
.on("mouseout", () => {
    tooltip.transition().duration(500).style("opacity", 0);
});
```
