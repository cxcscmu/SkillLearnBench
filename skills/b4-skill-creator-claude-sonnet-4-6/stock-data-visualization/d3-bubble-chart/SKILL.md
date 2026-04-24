---
name: d3-bubble-chart
description: >
  How to build a D3.js v6 force-directed bubble chart with sector clustering,
  size encoding, color legends, tooltips, and interactive selection.
  Use this skill whenever the user wants a bubble chart, force simulation,
  cluster layout, or interactive SVG circles with D3.
---

# D3 v6 Force-Directed Bubble Chart

## Core Pattern

```js
const simulation = d3.forceSimulation(nodes)
  .force("x", d3.forceX(d => sectorX(d.sector)).strength(0.08))
  .force("y", d3.forceY(d => sectorY(d.sector)).strength(0.08))
  .force("collide", d3.forceCollide(d => d.r + 2).strength(0.9))
  .force("charge", d3.forceManyBody().strength(-5))
  .on("tick", ticked);
```

## Sizing Bubbles by Market Cap

Use `d3.scaleSqrt` so that *area* (not radius) encodes value — this is perceptually correct:

```js
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.marketCap)])
  .range([minR, maxR]);  // e.g. [8, 60]
```

ETFs (no market cap) get a fixed uniform radius (e.g. 18).

## Sector Clustering with forceX/forceY

Pre-compute sector center positions on a grid or circle, then use them as force targets:

```js
const sectors = [...new Set(data.map(d => d.sector))];
const sectorCenters = {};
sectors.forEach((s, i) => {
  const angle = (i / sectors.length) * 2 * Math.PI;
  sectorCenters[s] = {
    x: cx + Math.cos(angle) * clusterRadius,
    y: cy + Math.sin(angle) * clusterRadius
  };
});
```

Strength 0.05–0.12 creates visible clustering without forcing everything to a single point.

## Tick Handler

```js
function ticked() {
  node.attr("cx", d => d.x).attr("cy", d => d.y);
  labels.attr("x", d => d.x).attr("y", d => d.y);
}
```

## Color Legend

```js
const legend = svg.append("g").attr("transform", `translate(${legendX}, ${legendY})`);
sectors.forEach((sector, i) => {
  legend.append("circle").attr("r", 7).attr("cx", 0).attr("cy", i * 22).attr("fill", color(sector));
  legend.append("text").attr("x", 12).attr("y", i * 22 + 5).text(sector);
});
```

## Tooltip

Create a `div` tooltip with `position: absolute; pointer-events: none`:

```js
const tooltip = d3.select("body").append("div").attr("class", "tooltip");
node.on("mouseover", (event, d) => {
  tooltip.style("display", "block")
    .html(`<b>${d.ticker}</b><br>${d.name}<br>${d.sector}`)
    .style("left", event.pageX + 12 + "px")
    .style("top",  event.pageY - 28 + "px");
}).on("mousemove", (event) => {
  tooltip.style("left", event.pageX + 12 + "px")
         .style("top",  event.pageY - 28 + "px");
}).on("mouseout", () => tooltip.style("display", "none"));
```

## Click Selection

Dispatch a custom event so other components can react:

```js
node.on("click", (event, d) => {
  d3.selectAll(".bubble").classed("selected", false);
  d3.select(event.currentTarget).classed("selected", true);
  document.dispatchEvent(new CustomEvent("stockSelected", { detail: d.ticker }));
});
```

## Key Tips

- Run the simulation with `alphaDecay(0.02)` and `velocityDecay(0.3)` for smoother settling.
- Call `.stop()` then manually run ticks with `simulation.tick(300)` for static initial layout.
- Clamp node positions within the SVG viewBox to prevent overflow.
- Use `viewBox` + `preserveAspectRatio` for responsive sizing.
