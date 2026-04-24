---
name: environment_setup_and_file_generation
description: Creates the directory structure, copies data, and writes the specific JS/CSS/HTML files required for the web application.
---
To execute the file generation:
1. Create directories: `/root/output/js/`, `/root/output/css/`, `/root/output/data/`.
2. Write `d3.v6.min.js` by fetching the official minified source and writing it to `/root/output/js/d3.v6.min.js`.
3. Read all files from `/root/data/stock-descriptions.csv` and the files in `/root/data/indiv-stock/` and write them into `/root/output/data/`.
4. Generate `index.html` with explicit relative links: `<link rel="stylesheet" href="css/style.css">`, `<script src="js/d3.v6.min.js"></script>`, and `<script src="js/visualization.js"></script>`.
5. Ensure `index.html` contains the container divs `#bubble-chart` and `#data-table` arranged with flexbox.