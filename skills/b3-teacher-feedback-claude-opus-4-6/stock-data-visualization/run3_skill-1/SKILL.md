[SKILL]
---
name: d3-stock-bubble-chart-and-table
description: Use when creating a D3.js v6 single-page web app that visualizes stock data as a bubble chart (sized by market cap, colored by sector, force-clustered) alongside a data table, with interactive linking between them. Covers CSV parsing, force simulation, tooltips, and table highlighting.
---

# D3.js Stock Bubble Chart + Data Table Visualization

## Overview
Create a single-page web app with:
1. A **bubble chart** (force-simulated, clustered by sector, sized by market cap)
2. A **data table** (50 stocks, formatted market cap)
3. **Interactive linking** (click bubble → highlight row, click row → highlight bubble)
4. **Tooltips** for non-ETF stocks only

## File Structure
```
/root/output/
├── index.html
├── js/
│   ├── d3.v6.min.js
│   └── visualization.js
├── css/
│   └── style.css
└── data/
    ├── stock-descriptions.csv
    └── indiv-stock/
        └── (copied .csv files)
```

## Step 1: Copy Data and D3 Library

```bash
# Copy input data
cp -r /root/data/* /root/output/data/

# Download D3.js v6 min
curl -o /root/output/js/d3.v6.min.js https://d3js.org/d3.v6.min.js
# If no internet, use: cp /path/to/d3.v6.min.js /root/output/js/d3.v6.min.js
```

## Step 2: index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Visualization</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>Stock Bubble Chart & Data Table</h1>
    <div id="main-container">
        <div id="chart-container">
            <svg id="bubble-chart"></svg>
            <div id="legend-container"></div>
        </div>
        <div id="table-container">
            <table id="stock-table">
                <thead>
                    <tr>
                        <th>Ticker symbol</th>
                        <th>Full company name</th>
                        <th>Sector</th>
                        <th>Market cap</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>
    <div id="tooltip" class="tooltip" style="opacity:0;"></div>
    <script src="js/d3.v6.min.js"></script>
    <script src="js/visualization.js"></script>
</body>
</html>
```

## Step 3: css/style.css

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    padding: 20px;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}

#main-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: flex-start;
    gap: 20px;
    width: 100%;
}

#chart-container {
    flex: 0 0 660px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 10px;
}

#bubble-chart {
    display: block;
    width: 640px;
    height: 600px;
}

#legend-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 10px;
    justify-content: center;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
}

.legend-color {
    width: 14px;
    height: 14px;
    border-radius: 50%;
}

#table-container {
    flex: 1 1 auto;
    max-height: 700px;
    overflow-y: auto;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

#stock-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

#stock-table thead th {
    background-color: #4a90d9;
    color: white;
    padding: 10px 8px;
    text-align: left;
    position: sticky;
    top: 0;
    z-index: 1;
}

#stock-table tbody td {
    padding: 8px;
    border-bottom: 1px solid #eee;
}

#stock-table tbody tr:hover {
    background-color: #f0f7ff;
}

#stock-table tbody tr.highlighted {
    background-color: #ffeb3b !important;
    font-weight: bold;
}

#stock-table tbody tr {
    cursor: pointer;
}

.tooltip {
    position: absolute;
    padding: 10px 14px;
    background: rgba(0, 0, 0, 0.85);
    color: #fff;
    border-radius: 6px;
    font-size: 13px;
    pointer-events: none;
    line-height: 1.5;
    z-index: 1000;
    max-width: 300px;
}

.bubble-selected {
    stroke: #ff0000;
    stroke-width: 3px;
}

.bubble-label {
    pointer-events: none;
    text-anchor: middle;
    dominant-baseline: central;
    font-size: 10px;
    font-weight: bold;
    fill: #fff;
}
```

## Step 4: js/visualization.js

**CRITICAL**: This must be the COMPLETE file — no truncation.

```javascript
(function() {
    const width = 640;
    const height = 600;

    const svg = d3.select("#bubble-chart")
        .attr("width", width)
        .attr("height", height);

    const tooltip = d3.select("#tooltip");

    d3.csv("data/stock-descriptions.csv").then(function(rawData) {
        // Parse data
        const data = rawData.map(function(d) {
            const mcRaw = d.marketCap ? d.marketCap.trim() : "";
            let marketCap = null;
            if (mcRaw !== "") {
                marketCap = parseFloat(mcRaw);
                if (isNaN(marketCap)) marketCap = null;
            }
            // Determine if ETF: no marketCap value in the data
            const isETF = (marketCap === null || marketCap === undefined);
            return {
                ticker: (d.ticker || d.Ticker || d.Symbol || "").trim(),
                name: (d.name || d.Name || d.Company || "").trim(),
                sector: (d.sector || d.Sector || "").trim(),
                marketCap: marketCap,
                country: (d.country || d.Country || "").trim(),
                website: (d.website || d.Website || "").trim(),
                isETF: isETF
            };
        });

        // Get unique sectors (non-empty)
        const sectors = Array.from(new Set(data.map(function(d) { return d.sector; }))).filter(function(s) { return s !== ""; }).sort();

        // Color scale
        const colorScale = d3.scaleOrdinal()
            .domain(sectors)
            .range(d3.schemeTableau10.concat(d3.schemePaired).slice(0, sectors.length));

        // Radius scale based on market cap for non-ETFs
        const nonETF = data.filter(function(d) { return !d.isETF && d.marketCap > 0; });
        const mcExtent = d3.extent(nonETF, function(d) { return d.marketCap; });
        const radiusScale = d3.scaleSqrt()
            .domain([mcExtent[0] || 1, mcExtent[1] || 1])
            .range([8, 50]);

        const defaultETFRadius = 12;

        data.forEach(function(d) {
            if (d.isETF) {
                d.radius = defaultETFRadius;
            } else {
                d.radius = radiusScale(d.marketCap);
            }
        });

        // Sector center positions — arrange sectors in a grid-like pattern centered
        const sectorCenters = {};
        const cols = Math.ceil(Math.sqrt(sectors.length));
        const rows = Math.ceil(sectors.length / cols);
        const xSpacing = width / (cols + 1);
        const ySpacing = height / (rows + 1);
        sectors.forEach(function(s, i) {
            const col = i % cols;
            const row = Math.floor(i / cols);
            sectorCenters[s] = {
                x: xSpacing * (col + 1),
                y: ySpacing * (row + 1)
            };
        });

        // For items with empty sector (ETFs possibly), place them in center
        sectorCenters[""] = { x: width / 2, y: height / 2 };

        // Force simulation
        const simulation = d3.forceSimulation(data)
            .force("x", d3.forceX(function(d) {
                return (sectorCenters[d.sector] || sectorCenters[""]).x;
            }).strength(0.4))
            .force("y", d3.forceY(function(d) {
                return (sectorCenters[d.sector] || sectorCenters[""]).y;
            }).strength(0.4))
            .force("collide", d3.forceCollide(function(d) {
                return d.radius + 2;
            }).iterations(3))
            .force("center", d3.forceCenter(width / 2, height / 2).strength(0.05))
            .on("tick", ticked);

        // Create bubble groups
        const bubbleGroup = svg.selectAll(".bubble-group")
            .data(data)
            .enter()
            .append("g")
            .attr("class", "bubble-group");

        const circles = bubbleGroup.append("circle")
            .attr("r", function(d) { return d.radius; })
            .attr("fill", function(d) { return d.sector ? colorScale(d.sector) : "#999"; })
            .attr("stroke", "#fff")
            .attr("stroke-width", 1)
            .attr("opacity", 0.85)
            .attr("data-ticker", function(d) { return d.ticker; })
            .style("cursor", "pointer");

        const labels = bubbleGroup.append("text")
            .attr("class", "bubble-label")
            .text(function(d) { return d.ticker; })
            .style("font-size", function(d) {
                return Math.max(7, Math.min(d.radius * 0.45, 14)) + "px";
            });

        // Tooltip handlers
        circles.on("mouseover", function(event, d) {
                // ETFs: do NOT show tooltip
                if (d.isETF) {
                    tooltip.style("opacity", 0);
                    return;
                }
                tooltip.style("opacity", 1);
                let html = "<strong>" + d.ticker + "</strong><br/>";
                html += "Name: " + d.name + "<br/>";
                html += "Sector: " + d.sector;
                tooltip.html(html);
                tooltip.style("left", (event.pageX + 15) + "px")
                       .style("top", (event.pageY - 10) + "px");
            })
            .on("mousemove", function(event, d) {
                if (d.isETF) {
                    tooltip.style("opacity", 0);
                    return;
                }
                tooltip.style("left", (event.pageX + 15) + "px")
                       .style("top", (event.pageY - 10) + "px");
            })
            .on("mouseout", function(event, d) {
                tooltip.style("opacity", 0);
                tooltip.html("");
            });

        // Click handler for bubbles
        circles.on("click", function(event, d) {
            selectStock(d.ticker);
        });

        function ticked() {
            bubbleGroup.attr("transform", function(d) {
                // Constrain to SVG bounds
                d.x = Math.max(d.radius, Math.min(width - d.radius, d.x));
                d.y = Math.max(d.radius, Math.min(height - d.radius, d.y));
                return "translate(" + d.x + "," + d.y + ")";
            });
        }

        // Build legend
        const legendContainer = d3.select("#legend-container");
        sectors.forEach(function(sector) {
            const item = legendContainer.append("div").attr("class", "legend-item");
            item.append("div")
                .attr("class", "legend-color")
                .style("background-color", colorScale(sector));
            item.append("span").text(sector);
        });

        // Build data table
        function formatMarketCap(mc) {
            if (mc === null || mc === undefined || isNaN(mc)) return "N/A";
            if (mc >= 1e12) return (mc / 1e12).toFixed(2) + "T";
            if (mc >= 1e9) return (mc / 1e9).toFixed(2) + "B";
            if (mc >= 1e6) return (mc / 1e6).toFixed(2) + "M";
            if (mc >= 1e3) return (mc / 1e3).toFixed(2) + "K";
            return mc.toString();
        }

        const tbody = d3.select("#stock-table tbody");
        const rows_el = tbody.selectAll("tr")
            .data(data)
            .enter()
            .append("tr")
            .attr("data-ticker", function(d) { return d.ticker; })
            .on("click", function(event, d) {
                selectStock(d.ticker);
            });

        rows_el.append("td").text(function(d) { return d.ticker; });
        rows_el.append("td").text(function(d) { return d.name; });
        rows_el.append("td").text(function(d) { return d.sector; });
        rows_el.append("td").text(function(d) { return formatMarketCap(d.marketCap); });

        // Selection / linking function
        function selectStock(ticker) {
            // Highlight bubble
            circles.classed("bubble-selected", false)
                .attr("stroke", "#fff")
                .attr("stroke-width", 1);
            circles.filter(function(d) { return d.ticker === ticker; })
                .classed("bubble-selected", true)
                .attr("stroke", "#ff0000")
                .attr("stroke-width", 3);

            // Highlight table row
            rows_el.classed("highlighted", false);
            const selectedRow = rows_el.filter(function(d) { return d.ticker === ticker; })
                .classed("highlighted", true);

            // Scroll table row into view
            if (!selectedRow