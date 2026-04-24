---
name: Copy Input Data Directory Structure
description: Use Node.js file system operations to recursively copy the entire `/root/data/indiv-stock/` directory (including all subdirectories and files) to `/root/output/data/indiv-stock/` to preserve the original directory structure for the web app
---

```javascript
const fs = require('fs');
const path = require('path');

function copyDirRecursive(src, dest) {
  // Create destination directory if it doesn't exist
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  // Read all items in source directory
  const items = fs.readdirSync(src);

  items.forEach(item => {
    const srcPath = path.join(src, item);
    const destPath = path.join(dest, item);
    const stat = fs.statSync(srcPath);

    if (stat.isDirectory()) {
      // Recursively copy subdirectories
      copyDirRecursive(srcPath, destPath);
    } else {
      // Copy files
      fs.copyFileSync(srcPath, destPath);
    }
  });
}

// Copy the indiv-stock directory
const sourceDir = '/root/data/indiv-stock';
const destDir = '/root/output/data/indiv-stock';
copyDirRecursive(sourceDir, destDir);
console.log(`Copied ${sourceDir} to ${destDir}`);
```

Usage: Call this function during your build process after creating the `/root/output/data/` directory.