# Core Web Vitals Reference

## The Three Core Metrics

### LCP — Largest Contentful Paint

Measures loading performance. Time until the largest image or text block visible in the viewport is rendered.

**Targets:** Good ≤ 2.5s | Needs work 2.5–4.0s | Poor > 4.0s

**Common causes of poor LCP:**
- Slow server response times (TTFB > 600ms)
- Render-blocking resources (CSS/JS in `<head>`)
- Slow resource load times (hero images, web fonts)
- Client-side rendering without SSR/SSG

**Fixes:**
- Preload the LCP image: `<link rel="preload" as="image" href="hero.webp">`
- Use `fetchpriority="high"` on the LCP element
- Serve images as WebP/AVIF
- Enable CDN and HTTP/2 or HTTP/3
- Inline critical CSS; defer non-critical CSS
- Use `<link rel="preconnect">` for third-party origins

---

### INP — Interaction to Next Paint

Measures responsiveness. The 98th-percentile latency of all discrete interactions (click, tap, keyboard) during a page visit.

**Targets:** Good ≤ 200ms | Needs work 200–500ms | Poor > 500ms

**Common causes of poor INP:**
- Long tasks blocking the main thread (> 50ms)
- Large JavaScript bundles parsed synchronously
- Expensive event handlers (layout thrashing, forced reflow)
- Third-party scripts running on the main thread

**Fixes:**
- Break long tasks with `scheduler.yield()` or `setTimeout(..., 0)`
- Code-split and lazy-load non-critical JS
- Debounce expensive event handlers
- Move heavy computation to Web Workers
- Profile with Chrome DevTools Performance panel → Long Tasks

---

### CLS — Cumulative Layout Shift

Measures visual stability. Sum of all unexpected layout shift scores during the page's lifespan.

**Targets:** Good ≤ 0.1 | Needs work 0.1–0.25 | Poor > 0.25

**Common causes of poor CLS:**
- Images without `width` and `height` attributes
- Ads, embeds, iframes without reserved space
- Dynamically injected content above existing content
- Web fonts causing FOIT/FOUT

**Fixes:**
- Always set `width` and `height` on `<img>` and `<video>`
- Reserve space for ads with `min-height` on containers
- Use `font-display: optional` or preload fonts
- Avoid inserting content above existing DOM nodes
- Use CSS `aspect-ratio` for responsive media

---

## Supporting Metrics

### FCP — First Contentful Paint
Time until the first text or image is rendered. Target ≤ 1.8s.
- Reduce TTFB, eliminate render-blocking resources, inline critical CSS.

### TTFB — Time to First Byte
Server response time. Target ≤ 800ms.
- Use a CDN, enable caching headers, optimize server-side queries.

### TBT — Total Blocking Time
Proxy for INP in lab tests. Sum of blocking time for tasks > 50ms. Target ≤ 200ms.
- Reduce main-thread work; split bundles; defer third-party scripts.

---

## Measurement Tools

| Tool | Type | Best For |
|------|------|----------|
| Chrome DevTools → Performance | Lab | Detailed main-thread profiling |
| Lighthouse (CLI / DevTools) | Lab | Full audit with recommendations |
| PageSpeed Insights | Lab + Field | CrUX field data + lab scores |
| WebPageTest | Lab | Multi-location, filmstrip, waterfall |
| Chrome UX Report (CrUX) | Field | Real-user data by origin |
| `web-vitals` JS library | Field | Measure in your own RUM pipeline |

---

## Quick Wins Checklist

- [ ] LCP element has `fetchpriority="high"`
- [ ] LCP image is preloaded in `<head>`
- [ ] All `<img>` have `width` and `height`
- [ ] All below-fold `<img>` have `loading="lazy"`
- [ ] Hero images served as WebP or AVIF
- [ ] Critical CSS inlined; rest deferred
- [ ] No synchronous render-blocking scripts in `<head>`
- [ ] Fonts use `font-display: swap` or `optional`
- [ ] No layout shifts from late-loading ads or embeds
- [ ] Long tasks broken up with `scheduler.yield()`
