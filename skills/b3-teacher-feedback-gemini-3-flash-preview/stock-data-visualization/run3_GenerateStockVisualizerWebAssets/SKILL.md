---
name: GenerateStockVisualizerWebAssets
description: Creates the HTML and CSS files for the stock visualization app. The HTML provides the structure for the side-by-side layout (bubble chart and table), while the CSS handles styling, scrolling, and highlighting logic.
---

```bash
# Write HTML to /root/output/index.html
cat << 'EOF' > /root/output/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Stock Market Visualization</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div id="app-container">
        <div id="viz-container">
            <div id="bubble-chart"></div>
            <div id="legend-container"></div>
        </div>
        <div id="table-container">
            <table id="stock-table">
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th>Name</th>
                        <th>Sector</th>
                        <th>Market Cap</th>
                    </tr>
                </thead>
                <tbody id="table-body"></tbody>
            </table>
        </div>
    </div>
    <div id="tooltip" class="hidden">
        <p><strong id="tooltip-ticker"></strong></p>
        <p id="tooltip-name"></p>
        <p id="tooltip-sector"></p>
    </div>
    <script src="js/d3.v6.min.js"></script>
    <script src="js/visualization.js"></script>
</body>
</html>
EOF

# Write CSS to /root/output/css/style.css
cat << 'EOF' > /root/output/css/style.css
body { font-family: sans-serif; margin: 0; padding: 20px; }
#app-container { display: flex; gap: 20px; height: 90vh; }
#viz-container { flex: 2; display: flex; flex-direction: column; border: 1px solid #ddd; }
#bubble-chart { flex-grow: 1; }
#legend-container { padding: 10px; display: flex; flex-wrap: wrap; gap: 10px; font-size: 12px; }
#table-container { flex: 1; overflow-y: auto; border: 1px solid #ddd; }

table { width: 100%; border-collapse: collapse; }
th { position: sticky; top: 0; background: #f4f4f4; padding: 8px; text-align: left; border-bottom: 2px solid #ccc; }
td { padding: 8px; border-bottom: 1px solid #eee; font-size: 13px; }

.highlight { background-color: #ffff99 !important; transition: background-color 0.3s; }
.bubble { cursor: pointer; stroke: #fff; stroke-width: 1.5px; }
.bubble:hover { stroke: #333; }
.label { pointer-events: none; text-anchor: middle; font-size: 10px; fill: #333; font-weight: bold; }

#tooltip {
    position: absolute;
    padding: 10px;
    background: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    pointer-events: none;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    font-size: 12px;
}
.hidden { display: none; }
.legend-item { display: flex; align-items: center; gap: 5px; }
.legend-box { width: 12px; height: 12px; }
EOF
```