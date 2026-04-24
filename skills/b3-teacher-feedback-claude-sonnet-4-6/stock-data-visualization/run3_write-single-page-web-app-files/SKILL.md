---
name: write-single-page-web-app-files
description: Use when generating all files for a single-page web app: index.html, CSS, and JS. Ensures correct relative paths, proper script loading order, and valid HTML structure.
---

# Writing Single-Page Web App Files

## File Writing Pattern
```python
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {path} ({len(content)} bytes)")
```

## index.html Structure
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
  <div id="app">
    <div id="bubble-chart"></div>
    <div id="stock-table">
      <table>
        <thead>
          <tr>
            <th>Ticker Symbol</th>
            <th>Full Company Name</th>
            <th>Sector</th>
            <th>Market Cap</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>
  </div>
  <!-- Tooltip div at body level for correct absolute positioning -->
  <div class="tooltip" id="tooltip"></div>
  <!-- Scripts at end of body -->
  <script src="js/d3.v6.min.js"></script>
  <script src="js/visualization.js"></script>
</body>
</html>
```

## CSS Layout for Side-by-Side
```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: sans-serif; background: #f9f9f9; }

#app {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  min-height: 100vh;
}

#bubble-chart {
  flex: 0 0 auto;
  width: 700px;
}

#stock-table {
  flex: 1 1 auto;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
}

#stock-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

#stock-table th, #stock-table td {
  padding: 6px 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

#stock-table th {
  background: #37474f;
  color: #fff;
  position: sticky;
  top: 0;
}

#table-body tr:hover { background: #f0f0f0; cursor: pointer; }
#table-body tr.highlighted { background-color: #ffe082; font-weight: bold; }
```

## Relative Paths Rule
- From `index.html` at `/root/output/index.html`, use `js/`, `css/`, `data/` (no leading slash)
- From `visualization.js` at `/root/output/js/visualization.js`, data paths must be `../data/...`