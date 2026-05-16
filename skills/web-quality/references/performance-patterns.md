# Web Performance Patterns

## Loading Patterns

### Preload Critical Resources

```html
<!-- LCP image -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- Critical font -->
<link rel="preload" as="font" href="/fonts/inter.woff2" crossorigin>

<!-- Critical CSS (if not inlined) -->
<link rel="preload" as="style" href="/css/critical.css">
```

### Preconnect to Third Parties

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
<link rel="dns-prefetch" href="https://analytics.example.com">
```

### Responsive Images

```html
<!-- Modern format with fallback -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="..." width="1200" height="600"
       fetchpriority="high" decoding="async">
</picture>

<!-- Responsive srcset -->
<img src="image-800.jpg"
     srcset="image-400.jpg 400w, image-800.jpg 800w, image-1600.jpg 1600w"
     sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1600px"
     width="800" height="450" alt="..." loading="lazy">
```

---

## JavaScript Patterns

### Code Splitting with Dynamic Import

```js
// Route-level split (React)
const Dashboard = React.lazy(() => import('./Dashboard'));

// Feature-level split
button.addEventListener('click', async () => {
  const { heavyFeature } = await import('./heavyFeature.js');
  heavyFeature.init();
});
```

### Break Up Long Tasks

```js
// scheduler.yield() — yieldable loop
async function processItems(items) {
  for (const item of items) {
    process(item);
    if (shouldYield()) await scheduler.yield();
  }
}

// Fallback for browsers without scheduler
function shouldYield() {
  return performance.now() > deadline;
}
```

### Web Worker for Heavy Computation

```js
// main.js
const worker = new Worker('./compute.worker.js', { type: 'module' });
worker.postMessage({ data: largeDataset });
worker.onmessage = ({ data }) => renderResult(data);

// compute.worker.js
self.onmessage = ({ data }) => {
  const result = expensiveComputation(data.data);
  self.postMessage(result);
};
```

---

## CSS Patterns

### Critical CSS Inlining

Extract above-the-fold CSS and inline it in `<head>`. Defer the rest:

```html
<style>/* critical CSS here */</style>
<link rel="preload" as="style" href="/css/main.css"
      onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/main.css"></noscript>
```

Tools: `critical`, `critters` (webpack/Vite plugin)

### Contain Layout Thrashing

```js
// Bad: alternating read/write causes forced reflow
elements.forEach(el => {
  const h = el.offsetHeight;  // read → forces layout
  el.style.height = h * 2 + 'px';  // write
});

// Good: batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight);  // all reads
elements.forEach((el, i) => el.style.height = heights[i] * 2 + 'px');  // all writes
```

---

## Font Loading

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;   /* show fallback immediately, swap when loaded */
  font-weight: 400 700; /* variable font range */
}
```

Size-adjust to reduce CLS from font swap:
```css
@font-face {
  font-family: 'Inter-Fallback';
  src: local('Arial');
  size-adjust: 107%;
  ascent-override: 90%;
}
```

---

## Caching Strategy

| Resource | Cache-Control | Strategy |
|----------|---------------|----------|
| HTML | `no-cache` | Always revalidate |
| JS/CSS (hashed) | `max-age=31536000, immutable` | Cache forever |
| Images | `max-age=86400` | Cache 1 day |
| Fonts | `max-age=31536000, immutable` | Cache forever |
| API JSON | `no-cache` or short `max-age` | Depends on freshness needs |

---

## Performance Budget

Define in `package.json` or CI config:

```json
{
  "budgets": [
    { "type": "initial", "maximumWarning": "200kb", "maximumError": "300kb" },
    { "type": "anyScript", "maximumWarning": "100kb" },
    { "type": "anyStyle", "maximumWarning": "50kb" }
  ]
}
```

Enforce with Lighthouse CI:
```yaml
# lighthouserc.js
module.exports = {
  assert: {
    assertions: {
      'largest-contentful-paint': ['warn', { maxNumericValue: 2500 }],
      'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      'total-blocking-time': ['warn', { maxNumericValue: 200 }],
    }
  }
};
```
