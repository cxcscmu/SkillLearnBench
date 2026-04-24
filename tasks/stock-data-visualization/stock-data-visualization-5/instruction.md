Please build a single-page web application using **D3.js (v6)** to visualize stock-related data. The final output should be accessible at:

- `/root/output/index.html` (viewable in a web browser)

---

## 📁 Project Structure Requirements

Ensure the following files and directories are created:

- `/root/output/js/d3.v6.min.js`  
- `/root/output/js/visualization.js`  
- `/root/output/css/style.css`  
- `/root/output/data/` → copy all provided input datasets into this directory  

---

## 📊 Data Sources

Use the following datasets:

- `/root/data/stock-descriptions.csv` → contains company metadata  
- `/root/data/indiv-stock/` → contains individual stock price histories  

---

## 📈 Visualization Layout

The application should display **two components arranged horizontally side by side**:

1. A **bubble chart**  
2. A **data table** listing all 50 stocks  

---

## 📋 Data Table Requirements

The table must include these columns: "Ticker symbol", "Full company name", "Sector", and "Market cap" (it should be formatted as an easy-to-read number e.g., "1.64T")

Interaction requirements:

- Clicking a table row highlights the corresponding bubble  
- Clicking a bubble highlights the corresponding table row  

---

## 🟢 Bubble Chart Requirements

Each bubble represents a **single stock**, with the following attributes:

- **Size**: proportional to market capitalization  
  - ETFs do not have market cap → assign them a uniform size  
- **Color**: based on sector  
- **Label**: display the ticker symbol inside each bubble  

---

## ⚙️ Force Simulation and Layout

Use D3 force simulation to position the bubbles:

- Apply **forceX / forceY** to cluster bubbles by sector  
- Keep clusters relatively **centered and compact** (avoid excessive dispersion)  
- Use **forceCollide** to prevent overlap between bubbles  

---

## 🏷️ Tooltip Behavior

- On hover, display a tooltip showing:
  - ticker  
  - company name  
  - sector  
- **Do not display tooltips for ETFs** (they lack marketCap, country, and website data)

---

## ⚠️ Critical Constraints

- **All SVG `<circle>` elements must represent stock bubbles only**  
- **No auxiliary or decorative SVG circles are allowed**
- **All text must be displayed in full without truncation**


## 🧩 Legend Requirement

- Include a legend that maps colors to sectors  
- The legend must be implemented using a **`<div>` element (not SVG)**  

---
