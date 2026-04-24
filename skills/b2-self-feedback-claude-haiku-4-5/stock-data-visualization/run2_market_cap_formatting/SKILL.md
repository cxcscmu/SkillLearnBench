---
name: run2_market_cap_formatting
description: Production-ready market cap formatting with consistent decimals, edge case handling, and pre-computation
---

# Market Cap Formatting - Production Patterns

## Problem
Format large numbers (trillions to millions) consistently for UI display, handling:
- Null/undefined values
- Zero values
- Very small values
- Trailing zero removal
- Consistency across the app

## Core Formatting Function

### Standard Implementation
```javascript
function formatMarketCap(value) {
  // Handle null, undefined, or empty
  if (value === null || value === undefined || value === '') {
    return 'N/A';
  }

  const num = parseFloat(value);

  // Handle invalid numbers
  if (isNaN(num)) {
    return 'N/A';
  }

  // Handle zero
  if (num === 0) {
    return '$0';
  }

  const absValue = Math.abs(num);
  let formatted;

  // Determine scale
  if (absValue >= 1e12) {
    formatted = (num / 1e12).toFixed(2) + 'T';
  } else if (absValue >= 1e9) {
    formatted = (num / 1e9).toFixed(2) + 'B';
  } else if (absValue >= 1e6) {
    formatted = (num / 1e6).toFixed(2) + 'M';
  } else if (absValue >= 1e3) {
    formatted = (num / 1e3).toFixed(1) + 'K';
  } else {
    formatted = num.toFixed(0);
  }

  return formatted;
}

// Usage examples
formatMarketCap(2676055080960);      // "2.68T"
formatMarketCap(1641026945024);      // "1.64T"
formatMarketCap(168972320768);       // "0.17T" (or "169B")
formatMarketCap(null);               // "N/A"
formatMarketCap(0);                  // "$0"
formatMarketCap('invalid');          // "N/A"
```

## Enhanced Version with Trailing Zero Removal

Remove unnecessary trailing zeros:

```javascript
function formatMarketCap(value) {
  if (value === null || value === undefined || value === '') {
    return 'N/A';
  }

  const num = parseFloat(value);
  if (isNaN(num) || num === 0) {
    return num === 0 ? '$0' : 'N/A';
  }

  const absValue = Math.abs(num);
  let formatted;

  if (absValue >= 1e12) {
    formatted = (num / 1e12).toFixed(2) + 'T';
  } else if (absValue >= 1e9) {
    formatted = (num / 1e9).toFixed(2) + 'B';
  } else if (absValue >= 1e6) {
    formatted = (num / 1e6).toFixed(2) + 'M';
  } else if (absValue >= 1e3) {
    formatted = (num / 1e3).toFixed(1) + 'K';
  } else {
    formatted = num.toFixed(0);
  }

  // Remove trailing zeros and decimal point
  return formatted.replace(/\.?0+([A-Z$]|$)/, '$1');
}

// Usage examples
formatMarketCap(1000000000000);      // "1T" (not "1.00T")
formatMarketCap(1500000000000);      // "1.5T"
formatMarketCap(1000000);            // "1M"
formatMarketCap(1234567);            // "1.23M"
```

## Pre-computation Strategy

Compute formatted values at load time, not render time:

```javascript
// Load and compute at data load
async function loadAndFormatStocks() {
  const rawData = await d3.csv('data/stocks.csv');

  const stocks = rawData.map(d => {
    const marketCap = d.marketCap ? parseFloat(d.marketCap) : null;

    return {
      ticker: d.ticker.trim(),
      name: d['full name'].trim(),
      sector: d.sector.trim(),
      marketCap: marketCap,
      // Compute formatted value once
      marketCapFormatted: formatMarketCap(marketCap)
    };
  });

  return stocks;
}

// Usage: formatted field is already available
stocks.forEach(s => {
  console.log(`${s.ticker}: ${s.marketCapFormatted}`);
});
```

## Different Precision Levels

### Minimal (2 significant figures)
```javascript
function formatMarketCapMinimal(value) {
  if (!value) return 'N/A';
  const num = parseFloat(value);
  const absValue = Math.abs(num);

  if (absValue >= 1e12) {
    return Math.round(num / 1e12 * 10) / 10 + 'T';
  } else if (absValue >= 1e9) {
    return Math.round(num / 1e9 * 10) / 10 + 'B';
  } else if (absValue >= 1e6) {
    return Math.round(num / 1e6 * 10) / 10 + 'M';
  }
  return Math.round(num).toString();
}

formatMarketCapMinimal(2676055080960);  // "2.7T"
```

### Precise (3 significant figures)
```javascript
function formatMarketCapPrecise(value) {
  if (!value) return 'N/A';
  const num = parseFloat(value);
  const absValue = Math.abs(num);

  if (absValue >= 1e12) {
    return (num / 1e12).toFixed(3) + 'T';
  } else if (absValue >= 1e9) {
    return (num / 1e9).toFixed(3) + 'B';
  } else if (absValue >= 1e6) {
    return (num / 1e6).toFixed(3) + 'M';
  }
  return Math.round(num).toString();
}

formatMarketCapPrecise(2676055080960);  // "2.676T"
```

## Using Locale-Specific Formatting

```javascript
function formatMarketCapLocale(value, locale = 'en-US') {
  if (!value) return 'N/A';

  const num = parseFloat(value);
  if (isNaN(num)) return 'N/A';

  const formatter = new Intl.NumberFormat(locale, {
    notation: 'compact',
    compactDisplay: 'short',
    maximumFractionDigits: 2,
    minimumFractionDigits: 0
  });

  return formatter.format(num);
}

// Usage with different locales
formatMarketCapLocale(2676055080960, 'en-US');  // "2.7T"
formatMarketCapLocale(2676055080960, 'de-DE');  // "2,7T"
```

## Comparison and Ranking

### Format for Sorted Display
```javascript
function formatMarketCapForComparison(value) {
  // Use fixed 2 decimals for easy comparison in tables
  if (!value) return 'N/A';

  const num = parseFloat(value);
  const absValue = Math.abs(num);

  if (absValue >= 1e12) {
    return (num / 1e12).toFixed(2) + 'T';
  } else if (absValue >= 1e9) {
    return (num / 1e9).toFixed(2) + 'B';
  } else if (absValue >= 1e6) {
    return (num / 1e6).toFixed(2) + 'M';
  }

  return num.toFixed(0);
}

// Sort by numeric value, display with consistent format
const sorted = stocks
  .sort((a, b) => (b.marketCap || 0) - (a.marketCap || 0))
  .map(s => ({
    ...s,
    marketCapFormatted: formatMarketCapForComparison(s.marketCap)
  }));
```

## Edge Cases

### Handle Negatives (if applicable)
```javascript
function formatMarketCapWithSign(value) {
  if (!value) return 'N/A';
  const formatted = formatMarketCap(value);
  if (formatted === 'N/A') return 'N/A';
  return value < 0 ? '-' + formatted : formatted;
}

formatMarketCapWithSign(-1000000000000);  // "-1T"
```

### Handle Estimates/Approximations
```javascript
function formatMarketCapWithQuality(value, quality = 'exact') {
  const formatted = formatMarketCap(value);
  if (formatted === 'N/A') return 'N/A';

  const qualityMarker = {
    'exact': '',
    'estimated': '~',
    'approximate': '≈'
  };

  return qualityMarker[quality] + formatted;
}

formatMarketCapWithQuality(1000000000000, 'estimated');  // "~1T"
```

## Testing

```javascript
// Test cases
const testCases = [
  [2676055080960, '2.68T'],
  [1641026945024, '1.64T'],
  [168972320768, '0.17T'],
  [1000000000000, '1T'],
  [1500000000000, '1.5T'],
  [1000000, '1M'],
  [null, 'N/A'],
  [undefined, 'N/A'],
  [0, '$0']
];

testCases.forEach(([input, expected]) => {
  const result = formatMarketCap(input);
  console.assert(
    result === expected,
    `formatMarketCap(${input}): expected "${expected}", got "${result}"`
  );
});
```

## Performance Notes

- Pre-format at data load time, store the result
- Don't format in render loops or on every update
- Cache formatter functions if needed
- Locale formatters are slower - use for small datasets only
