---
name: GenerateD3VisualizationLogic
description: Creates the core D3.js logic in visualization.js. This includes data loading, custom market cap formatting (supporting "T" for Trillions), force simulation for sector clustering, bubble generation, and bidirectional table highlighting.
---

```bash
# Write JS to /root/output/js/visualization.js
cat << 'EOF' > /root/output/js/visualization.js
async function init() {
    const data = await d3.csv("data/stock-descriptions.csv");
    
    // Formatting logic: Convert to T, B, M
    const formatCap = (val) => {
        if (!val || isNaN(val)) return "N/A";
        const n = parseFloat(val);
        if (n >= 1e12) return (n / 1e12).toFixed(2) + "T";
        if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
        if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
        return n.toLocaleString();
    };

    const sectors = Array.from(new Set(data.map(d => d.sector))).filter(s => s);
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10).domain(sectors);
    
    // SVG Setup
    const width = 800, height = 600;
    const svg = d3.select("#bubble-chart").append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("width", "100%")
        .attr("height", "100%");

    // Map sectors to center points for force clustering
    const sectorCenters = {};
    sectors.forEach((s, i) => {
        const angle = (i / sectors.length) * 2 * Math.PI;
        sectorCenters[s] = {
            x: width / 2 + Math.cos(angle) * 150,
            y: height / 2 + Math.sin(angle) * 150
        };
    });

    // Size scale: Market Cap vs uniform for ETFs
    const radiusScale = d3.scaleSqrt()
        .domain([0, d3.max(data, d => parseFloat(d.marketCap) || 0)])
        .range([10, 50]);

    const nodes = data.map(d => ({
        ...d,
        radius: d.marketCap ? radiusScale(parseFloat(d.marketCap)) : 15,
        x: Math.random() * width,
        y: Math.random() * height
    }));

    const simulation = d3.forceSimulation(nodes)
        .force("x", d3.forceX(d => d.sector ? sectorCenters[d.sector].x : width / 2).strength(0.15))
        .force("y", d3.forceY(d => d.sector ? sectorCenters[d.sector].y : height / 2).strength(0.15))
        .force("collide", d3.forceCollide(d => d.radius + 2))
        .force("center", d3.forceCenter(width / 2, height / 2));

    const bubbleGroup = svg.selectAll(".node")
        .data(nodes)
        .enter().append("g")
        .attr("class", "node")
        .attr("id", d => `node-${d.ticker}`)
        .on("click", (event, d) => highlightStock(d.ticker));

    const circles = bubbleGroup.append("circle")
        .attr("class", "bubble")
        .attr("r", d => d.radius)
        .attr("fill", d => d.sector ? colorScale(d.sector) : "#ccc")
        .on("mouseover", (event, d) => {
            if (d.marketCap) {
                const tt = d3.select("#tooltip");
                tt.classed("hidden", false)
                  .style("left", (event.pageX + 10) + "px")
                  .style("top", (event.pageY + 10) + "px");
                d3.select("#tooltip-ticker").text(d.ticker);
                d3.select("#tooltip-name").text(d.name);
                d3.select("#tooltip-sector").text(d.sector);
            }
        })
        .on("mouseout", () => d3.select("#tooltip").classed("hidden", true));

    bubbleGroup.append("text")
        .attr("class", "label")
        .text(d => d.ticker);

    simulation.on("tick", () => {
        bubbleGroup.attr("transform", d => `translate(${d.x},${d.y})`);
    });

    // Render Table
    const tableBody = d3.select("#table-body");
    const rows = tableBody.selectAll("tr")
        .data(data)
        .enter().append("tr")
        .attr("id", d => `row-${d.ticker}`)
        .on("click", (event, d) => highlightStock(d.ticker));

    rows.append("td").text(d => d.ticker);
    rows.append("td").text(d => d.name);
    rows.append("td").text(d => d.sector || "N/A");
    rows.append("td").text(d => formatCap(d.marketCap));

    // Render Legend
    const legend = d3.select("#legend-container");
    sectors.forEach(s => {
        const item = legend.append("div").attr("class", "legend-item");
        item.append("div").attr("class", "legend-box").style("background", colorScale(s));
        item.append("span").text(s);
    });

    // Interaction Logic
    function highlightStock(ticker) {
        d3.selectAll("tr").classed("highlight", false);
        d3.selectAll("circle").style("stroke", "#fff").style("stroke-width", "1.5px");

        const selectedRow = d3.select(`#row-${ticker}`);
        selectedRow.classed("highlight", true);
        selectedRow.node().scrollIntoView({ behavior: 'smooth', block: 'center' });

        const selectedCircle = d3.select(`#node-${ticker} circle`);
        selectedCircle.style("stroke", "#000").style("stroke-width", "3px");
    }
}
init();
EOF
```