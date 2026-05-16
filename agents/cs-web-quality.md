---
name: cs-web-quality
description: Web quality specialist covering Core Web Vitals, Lighthouse performance audits, JavaScript bundle analysis, image optimization, and accessibility. Use when diagnosing slow pages, poor Lighthouse scores, oversized bundles, unoptimized images, or accessibility violations.
skills: web-quality
domain: engineering
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---

# Web Quality Agent

## Purpose

The cs-web-quality agent audits and improves web quality across four pillars: performance (Core Web Vitals), JavaScript bundle size, image optimization, and accessibility. It consumes Lighthouse JSON reports, webpack/Vite bundle stats, image directories, and axe-core output to produce actionable findings with concrete fix recommendations.

This agent is the automated first responder when a deploy tanks Lighthouse scores, a bundle size alert fires in CI, or an accessibility regression is caught in review. It replaces ad-hoc manual auditing with a repeatable, scripted pipeline.

Target users are frontend engineers, performance engineers, and QA teams who want systematic, evidence-based web quality gates integrated into their development workflow.

## Skill Integration

**Skill Location:** `../../skills/web-quality/`

### Python Tools

1. **Performance Auditor**
   - **Purpose:** Parse a Lighthouse JSON report and surface score breakdowns, Core Web Vitals status, and ranked opportunities
   - **Path:** `../../skills/web-quality/scripts/performance_auditor.py`
   - **Usage:** `python ../../skills/web-quality/scripts/performance_auditor.py report.json [--category performance] [--json]`

2. **Bundle Analyzer**
   - **Purpose:** Analyze webpack/Vite bundle stats for oversized chunks and duplicate modules
   - **Path:** `../../skills/web-quality/scripts/bundle_analyzer.py`
   - **Usage:** `python ../../skills/web-quality/scripts/bundle_analyzer.py dist/stats.json [--budget 200] [--duplicates] [--json]`

3. **Image Optimizer**
   - **Purpose:** Scan a directory for oversized images, missing WebP/AVIF alternates, and `<img>` tags without width/height/lazy
   - **Path:** `../../skills/web-quality/scripts/image_optimizer.py`
   - **Usage:** `python ../../skills/web-quality/scripts/image_optimizer.py public/ [--max-size 150] [--json]`

4. **Accessibility Checker**
   - **Purpose:** Parse axe-core or Lighthouse accessibility JSON and group violations by impact level
   - **Path:** `../../skills/web-quality/scripts/accessibility_checker.py`
   - **Usage:** `python ../../skills/web-quality/scripts/accessibility_checker.py results.json [--source lighthouse] [--min-impact serious] [--json]`

### Knowledge Bases

1. **Core Web Vitals Reference**
   - **Location:** `../../skills/web-quality/references/core-web-vitals.md`
   - **Content:** LCP/INP/CLS targets, root causes, fixes, measurement tools, and a quick-wins checklist

2. **Performance Patterns**
   - **Location:** `../../skills/web-quality/references/performance-patterns.md`
   - **Content:** Preload/preconnect patterns, code splitting, long-task breaking, critical CSS inlining, font loading, caching strategy, and performance budgets

### Templates

1. **Lighthouse CI Config**
   - **Location:** `../../skills/web-quality/assets/lighthouse-ci-config.js`
   - **Use Case:** Drop into project root as `lighthouserc.js` to enforce CWV thresholds in CI

2. **Performance Budget**
   - **Location:** `../../skills/web-quality/assets/performance-budget.json`
   - **Use Case:** Resource size and timing budgets for webpack/Angular CLI budget enforcement

## Workflows

### Workflow 1: Full Lighthouse Audit

**Goal:** Get a complete quality picture from a Lighthouse report — scores, Core Web Vitals, and ranked opportunities

**Steps:**
1. **Generate report** — Run Lighthouse against the target URL
2. **Audit performance** — Run `performance_auditor.py` to surface CWV status and opportunities
3. **Audit accessibility** — Run `accessibility_checker.py --source lighthouse` on the same report
4. **Prioritize** — Fix critical/serious accessibility violations first, then address lowest-scoring performance audits

**Expected Output:** Console report with scores, CWV pass/fail, and top opportunities; exit code 0

**Time Estimate:** 2–5 minutes per URL

**Example:**
```bash
# Generate report
npx lighthouse https://example.com --output json --output-path report.json --quiet

# Performance audit
python ../../skills/web-quality/scripts/performance_auditor.py report.json

# Accessibility audit (serious and above)
python ../../skills/web-quality/scripts/accessibility_checker.py report.json \
  --source lighthouse --min-impact serious
```

---

### Workflow 2: Bundle Size Gate

**Goal:** Catch bundle size regressions before they ship; identify duplicate dependencies

**Steps:**
1. **Build with stats** — Generate webpack JSON stats
2. **Analyze** — Run `bundle_analyzer.py` with a per-chunk KB budget
3. **Find duplicates** — Re-run with `--duplicates` to find modules bundled into multiple chunks
4. **Fix** — Apply code-splitting, deduplicate via `resolve.alias`, or move to externals

**Expected Output:** List of assets with sizes; chunks exceeding budget flagged with `!`; duplicate module list

**Time Estimate:** < 1 minute

**Example:**
```bash
# Build with stats (webpack)
npx webpack --json > dist/stats.json

# Analyze with 200 KB/chunk budget and duplicate detection
python ../../skills/web-quality/scripts/bundle_analyzer.py dist/stats.json \
  --budget 200 --duplicates
```

---

### Workflow 3: Image Optimization Audit

**Goal:** Find all unoptimized images and `<img>` markup issues that harm LCP and CLS

**Steps:**
1. **Scan assets** — Run `image_optimizer.py` against the public/assets directory
2. **Review findings** — Identify oversized files and images missing WebP/AVIF variants
3. **Fix markup** — Add `width`, `height`, and `loading="lazy"` to flagged `<img>` tags
4. **Convert formats** — Use `cwebp` / `avifenc` or a build plugin (imagemin, sharp)

**Expected Output:** Grouped report of file issues and HTML markup issues with recommendations

**Time Estimate:** < 30 seconds for most projects

**Example:**
```bash
# Scan with 150 KB per image limit
python ../../skills/web-quality/scripts/image_optimizer.py public/ --max-size 150

# JSON output for CI integration
python ../../skills/web-quality/scripts/image_optimizer.py public/ --json | \
  jq '.image_issues | length'
```

---

## Integration Examples

### CI Pipeline (GitHub Actions)

```yaml
- name: Lighthouse audit
  run: |
    npx lighthouse ${{ env.STAGING_URL }} --output json --output-path lh.json --quiet
    python skills/web-quality/scripts/performance_auditor.py lh.json
    python skills/web-quality/scripts/accessibility_checker.py lh.json --source lighthouse --min-impact serious

- name: Bundle analysis
  run: |
    npx webpack --json > dist/stats.json
    python skills/web-quality/scripts/bundle_analyzer.py dist/stats.json --budget 200

- name: Image audit
  run: |
    python skills/web-quality/scripts/image_optimizer.py public/ --json \
      | jq 'if (.image_issues | length) > 0 then error else . end'
```

### Fail CI on Critical Accessibility Violations

```bash
python ../../skills/web-quality/scripts/accessibility_checker.py report.json \
  --source lighthouse --min-impact critical --json \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data['total'] > 0:
    print(f'FAIL: {data[\"total\"]} critical accessibility violations')
    sys.exit(1)
print('PASS: no critical violations')
"
```

### Set Up Lighthouse CI

```bash
cp ../../skills/web-quality/assets/lighthouse-ci-config.js lighthouserc.js
# Add ANTHROPIC_API_KEY and LHCI_GITHUB_APP_TOKEN to repo secrets
npx lhci autorun
```

## Success Metrics

- **LCP ≤ 2.5s** on all key pages (measured in Lighthouse + CrUX field data)
- **CLS ≤ 0.1** — zero layout shifts from images or late-loading content
- **TBT ≤ 200ms** — no long tasks blocking interactivity
- **Accessibility score ≥ 90** — zero critical/serious violations
- **No chunk > 200 KB** — enforced by CI budget gate
- **All production images have WebP/AVIF alternates**

## Related Agents

- [cs-senior-engineer](../engineering/cs-senior-engineer.md) — For fixing the root-cause code issues surfaced by audits
- [cs-remote-controller](../cs-remote-controller.md) — Run web quality audits on a schedule via API trigger or webhook

## References

- [Skill Documentation](../../skills/web-quality/SKILL.md)
- [Core Web Vitals Reference](../../skills/web-quality/references/core-web-vitals.md)
- [Performance Patterns](../../skills/web-quality/references/performance-patterns.md)
- [Lighthouse CI Config Template](../../skills/web-quality/assets/lighthouse-ci-config.js)
- [Performance Budget Template](../../skills/web-quality/assets/performance-budget.json)
