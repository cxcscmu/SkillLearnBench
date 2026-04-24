---
name: d3-fundamentals
description: Essential D3.js v6 concepts including selections, scales, SVG basics, and data binding for building interactive visualizations
---

# D3.js v6 Fundamentals

## Overview
D3.js v6 (Data-Driven Documents) is a JavaScript library for manipulating documents based on data. Essential for creating scalable vector graphics (SVG) visualizations.

## Core Concepts

### 1. Selections
Select DOM elements and bind data to them:

```javascript
// Select elements
d3.select("body")                    // single element
d3.selectAll(".dots")                // multiple elements

// Data binding
d3.selectAll("circle")
  .data(dataArray, d => d.id)       // bind data with key function
  .join(                             // handle enter/update/exit
    enter => enter.append("circle"),
    update => update,
    exit => exit.remove()
  )
```

### 2. Scales
Map data values to visual dimensions:

```javascript
// Linear scale (continuous input → continuous output)
const xScale = d3.scaleLinear()
  .domain([0, 100])           // input range
  .range([0, width]);         // output range

// Other common scales:
const colorScale = d3.scaleOrdinal()
  .domain(["A", "B", "C"])
  .range(["red", "blue", "green"]);

const sizeScale = d3.scaleSqrt()   // square root scale (better for areas)
  .domain([0, max])
  .range([0, 100]);
```

### 3. SVG Elements
Common SVG elements for visualization:

```javascript
// Circle (bubble chart)
g.append("circle")
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", d => rScale(d.value))
  .attr("fill", d => colorScale(d.category));

// Text (labels)
g.append("text")
  .text(d => d.label)
  .attr("text-anchor", "middle")
  .attr("dominant-baseline", "central");

// Rect (table cells, bars)
g.append("rect")
  .attr("width", width)
  .attr("height", height);
```

### 4. Margins Convention
Standard pattern for creating SVG containers:

```javascript
const margin = {top: 20, right: 20, bottom: 20, left: 20};
const width = 800 - margin.left - margin.right;
const height = 600 - margin.top - margin.bottom;

const svg = d3.select("body")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);
```

### 5. Transitions
Smooth animations:

```javascript
d3.selectAll("circle")
  .transition()
  .duration(750)
  .attr("cx", d => xScale(d.newX))
  .attr("r", d => rScale(d.newValue));
```

## Loading Data

### CSV with D3
```javascript
d3.csv("data.csv").then(data => {
  // Data is array of objects
  // Numeric strings are parsed as strings by default
  data.forEach(d => {
    d.value = +d.value;  // convert to number
    d.date = new Date(d.date);  // convert to date
  });
});
```

## Module Imports
D3.js v6 uses ES6 modules. For standalone HTML, use the bundled version:

```html
<script src="https://d3js.org/d3.v6.min.js"></script>
```

Or import specific modules:
```javascript
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@6/+esm";
```
