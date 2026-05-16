---name: performance-optimization
description: Optimizes application performance. Use when investigating slow load times, runtime lag, or poor Core Web Vitals scores. Always measure first — never optimize without data.---

# Performance Optimization Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# Performance Optimization

## Overview

Measure first. Never optimize based on intuition. Every optimization should be driven by a measured baseline, a specific target, and a measured result that confirms improvement.

**The Golden Rule:** A perceived performance improvement that isn't measured is not a performance improvement — it's a guess.

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |

## The Measure-First Workflow

```
1. BASELINE  → Record current metrics (Lighthouse, WebPageTest, profiler)
2. IDENTIFY  → Find the top bottleneck (not all bottlenecks — the worst one)
3. HYPOTHESIZE → Why is it slow? Form a specific hypothesis
4. FIX       → Address the hypothesis
5. MEASURE   → Record new metrics
6. COMPARE   → Quantify the improvement
7. REPEAT    → Back to step 2 until targets are met
```

## LCP Fixes

The LCP element is usually a hero image or large heading. Make it load as fast as possible.

```html
<!-- Preload the LCP image -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- Correct img attributes -->
<img
  src="/hero.webp"
  alt="Hero"
  width="1200"
  height="630"
  fetchpriority="high"
  loading="eager"
>
```

**LCP root causes:**
- Large unoptimized images (use WebP/AVIF, srcset, correct sizes)
- Render-blocking resources (defer scripts, inline critical CSS)
- Slow server response (TTFB > 800ms → optimize server or add CDN)
- No preload for LCP element

## INP Fixes

INP measures how fast the page responds to user input. Long tasks (>50ms) on the main thread cause poor INP.

```typescript
// Break up long tasks with scheduler.yield()
async function processLargeList(items: Item[]) {
  const results = [];
  for (let i = 0; i < items.length; i++) {
    results.push(processItem(items[i]));
    if (i % 50 === 0) {
      await scheduler.yield(); // yield to browser between batches
    }
  }
  return results;
}
```

**INP root causes:**
- Long event handlers (> 50ms)
- Synchronous heavy computation on main thread
- Excessive re-renders triggered by events
- Third-party scripts blocking the main thread

## CLS Fixes

Cumulative Layout Shift happens when elements move unexpectedly after initial render.

```html
<!-- Always set width and height on images -->
<img src="/photo.jpg" width="400" height="300" alt="Photo">

<!-- Reserve space for ads/embeds -->
<div style="min-height: 250px;">
  <!-- ad loads here -->
</div>

<!-- Avoid inserting content above existing content -->
```

**CLS root causes:**
- Images without dimensions
- Dynamically injected banners/ads above content
- Web fonts causing FOUT/FOIT (use font-display: optional)
- Animations that change layout properties (use transform instead)

## N+1 Query Fix

```typescript
// Bad: N+1 — 1 query for tasks + N queries for assignees
const tasks = await Task.findAll();
for (const task of tasks) {
  task.assignee = await User.findById(task.assigneeId); // N queries
}

// Good: 2 queries total
const tasks = await Task.findAll();
const userIds = [...new Set(tasks.map(t => t.assigneeId))];
const users = await User.findByIds(userIds);
const userMap = new Map(users.map(u => [u.id, u]));
tasks.forEach(t => { t.assignee = userMap.get(t.assigneeId); });
```

## React Re-render Prevention

```tsx
// Memoize expensive computations
const sortedTasks = useMemo(
  () => tasks.slice().sort((a, b) => a.priority - b.priority),
  [tasks]
);

// Memoize callbacks passed to children
const handleTaskComplete = useCallback(
  (taskId: string) => dispatch({ type: 'COMPLETE_TASK', taskId }),
  [dispatch]
);

// Memoize components that receive stable props
const TaskRow = memo(function TaskRow({ task, onComplete }: Props) {
  return <li onClick={() => onComplete(task.id)}>{task.title}</li>;
});
```

## Image Optimization

```html
<!-- Modern format with fallback -->
<picture>
  <source srcset="/image.avif" type="image/avif">
  <source srcset="/image.webp" type="image/webp">
  <img src="/image.jpg" alt="Description" width="800" height="600" loading="lazy">
</picture>

<!-- Responsive images -->
<img
  src="/hero-800.webp"
  srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1600.webp 1600w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1600px"
  alt="Hero"
  width="1600"
  height="900"
>
```

## Bundle Size

```bash
# Analyze bundle
npx vite-bundle-visualizer  # for Vite
npx webpack-bundle-analyzer  # for webpack

# Check what a package adds
npx bundlephobia <package-name>

# Find duplicate packages
npx npm-dedupe
```

**Bundle reduction strategies:**
- Code split at route boundaries (dynamic import)
- Tree-shake by importing named exports, not full packages
- Replace heavy libraries with lighter alternatives
- Remove unused polyfills

## Caching Strategy

```
HTML:           Cache-Control: no-cache (must revalidate)
JS/CSS assets:  Cache-Control: max-age=31536000, immutable (1 year, content-hashed)
API responses:  Vary by endpoint — stale-while-revalidate where appropriate
Images:         Cache-Control: max-age=86400 (1 day)
```

## Verification

- [ ] Baseline metrics recorded before any changes
- [ ] Specific bottleneck identified (not "everything is slow")
- [ ] LCP ≤ 2.5s on mobile
- [ ] INP ≤ 200ms for all interactions
- [ ] CLS ≤ 0.1
- [ ] No N+1 query patterns in data fetching
- [ ] Images have explicit dimensions and use modern formats
- [ ] Bundle size within budget (main bundle < 100KB gzipped)
- [ ] Post-fix metrics recorded and compared to baseline