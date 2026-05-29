---
name: redesign-existing-projects
description: >-
  Upgrades existing websites and apps to premium quality. Audits current design,
  identifies generic AI patterns, and applies high-end design standards without
  breaking functionality. Works with any CSS framework or vanilla CSS.
  TRIGGER when: user asks to improve, modernize, upgrade, fix the design of,
  or make premium an existing codebase.
origin: taste-skill
owner: surfingalien
---

# redesign-existing-projects

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Audit → Diagnose → Fix. Work with the existing stack. Do not rewrite from scratch. Improve what's there. Keep changes reviewable and focused — small, targeted improvements over big rewrites.

**Measure Everything. Every change should have a visible impact.**

## Process

1. **Scan** — Read the codebase. Identify framework, styling method (Tailwind, vanilla CSS, styled-components, etc.), and current patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state.
3. **Fix** — Apply targeted upgrades. Do not break existing functionality. Test after every change.

## Fix Priority (Maximum Impact, Minimum Risk)

Apply in this order:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliché patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

## Design Audit

### Typography

- **Browser defaults or Inter everywhere** → Replace with `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`
- **Headlines lack presence** → Increase display size, tighten `letter-spacing`, reduce `line-height`
- **Body text too wide** → Limit paragraphs to `~65ch`, increase `line-height` for readability
- **Only Regular (400) and Bold (700)** → Introduce Medium (500) and SemiBold (600)
- **Numbers in proportional font** → Use monospace or `font-variant-numeric: tabular-nums` for data
- **Missing letter-spacing** → Negative tracking for large headers, positive for small caps/labels
- **Orphaned words** → Fix with `text-wrap: balance` or `text-wrap: pretty`

### Color and Surfaces

- **Pure `#000000` background** → Replace with `#0a0a0a`, `#121212`, or dark navy
- **Oversaturated accent colors** → Keep saturation below 80%
- **More than one accent color** → Pick one. Remove the rest
- **Mixing warm and cool grays** → Stick to one gray family, consistent hue
- **Purple/blue "AI gradient" aesthetic** → The #1 AI design fingerprint. Replace with neutral bases + single considered accent
- **Generic `box-shadow`** → Tint shadows to background hue (dark blue shadow on blue background)
- **Flat design with zero texture** → Add subtle noise, grain, or micro-patterns
- **Random dark section in light page** → Either commit to full dark mode or keep consistent. Never a sudden `#111` island in cream pages
- **Empty flat sections** → Add background imagery (blurred, overlaid), patterns, or ambient gradients. Use `picsum.photos/seed/{name}/1920/1080` for placeholders

### Layout

- **Everything centered and symmetrical** → Break with offset margins, mixed aspect ratios, left-aligned headers
- **Three equal card columns as feature row** → The most generic AI layout. Replace with 2-column zig-zag, asymmetric grid, or masonry
- **`height: 100vh` for full-screen sections** → Replace with `min-height: 100dvh` (iOS Safari viewport bug)
- **Complex flexbox percentage math** → Replace with CSS Grid
- **No max-width container** → Add `~1200–1440px` container with auto margins
- **Uniform border-radius on everything** → Vary: tighter on inner elements, softer on containers
- **No overlap or depth** → Use negative margins to create layering
- **Missing whitespace** → Double the spacing. Let the design breathe
- **Buttons not bottom-aligned in card groups** → Pin buttons to bottom of each card
- **Inconsistent vertical rhythm in side-by-side elements** → Align shared elements (titles, prices, buttons) across columns

### Interactivity and States

- **No hover states on buttons** → Add background shift, slight scale, or translate on hover
- **No active/pressed feedback** → Add `scale(0.98)` or `translateY(1px)` on press
- **Instant transitions** → Add smooth `200–300ms` transitions to all interactive elements
- **Missing focus ring** → Visible focus indicators for keyboard navigation (WCAG required)
- **No loading states** → Skeleton loaders matching layout shape. No generic spinners
- **No empty states** → Design a composed "getting started" view
- **No error states** → Inline error messages for forms. No `window.alert()`
- **No current page indicator in nav** → Style the active nav link differently
- **Scroll jumping** → Add `scroll-behavior: smooth`
- **Animations using `top`, `left`, `width`, `height`** → Switch to `transform` and `opacity`

### Content

- **Generic names** ("John Doe", "Jane Smith") → Use diverse, realistic-sounding names
- **Fake round numbers** (`99.99%`, `$100.00`) → Use organic data: `47.2%`, `$99.00`
- **Placeholder company names** ("Acme Corp", "Nexus") → Invent contextual, believable brand names
- **AI copy clichés** → Never "Elevate", "Seamless", "Unleash", "Next-Gen", "Delve". Write plain, specific language
- **Exclamation marks in success messages** → Remove. Be confident, not loud
- **"Oops!" error messages** → Be direct: "Connection failed. Please try again."
- **Lorem ipsum** → Write real draft copy

### Component Patterns

- **Generic card** (border + shadow + white background) → Remove the border, or use only background color, or only spacing
- **Pill "New" / "Beta" badges** → Try square badges, flags, or plain text labels
- **3-card carousel testimonials with dots** → Replace with masonry wall, embedded social posts, or single rotating quote
- **Pricing table with 3 equal towers** → Highlight the recommended tier with color and emphasis
- **Modals for everything** → Use inline editing, slide-over panels, or expandable sections for simple actions

### Iconography

- **Lucide or Feather icons exclusively** → Default AI icon choice. Use Phosphor, HugeIcons, or Tabler
- **Rocketship for "Launch", shield for "Security"** → Use less obvious icons (bolt, fingerprint, spark, vault)
- **Inconsistent stroke widths** → Audit and standardize to one stroke weight
- **Stock "diverse team" photos** → Use real team photos, candid shots, or consistent illustration style

### Code Quality

- **Div soup** → Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`
- **Hardcoded pixel widths** → Use `%`, `rem`, `em`, `max-width`
- **Missing alt text** → Describe image content. Never `alt=""` or `alt="image"` on meaningful images
- **Arbitrary `z-index: 9999`** → Establish a clean z-index scale
- **Missing meta tags** → Add `<title>`, `description`, `og:image`, social sharing meta tags

### Strategic Omissions (What AI Typically Forgets)

- **No legal links** → Add privacy policy and ToS in footer
- **No custom 404 page** → Design a helpful, branded "page not found"
- **No form validation** → Add client-side validation
- **No "skip to content" link** → Essential for keyboard users

## FinSurfing Context

Common issues to fix in FinSurfing UI:

- **AI analysis panels** — if using generic card styling, upgrade to Double-Bezel from `soft-skill`
- **Stock data tables** — replace generic `border` rows with `divide-y` on clean monospace type
- **Positive/negative P&L** — never bright red/green. Use muted palette from `minimalist-ui`
- **Anthropic API loading states** — replace spinners with skeleton loaders that match the analysis card shape
- **Railway deploy status** — use semantic `<output>` element, not a generic `<div>`
- **Forms** (watchlist add, alert settings) — label above input, inline validation, `min-height: 100dvh` on mobile

## Upgrade Techniques

For high-impact visual improvements beyond the audit:

- **Variable font animation** — interpolate weight/width on scroll or hover
- **Broken grid / asymmetry** — elements bleeding off-screen or offset with calculated randomness
- **Parallax card stacks** — sections physically stack during scroll
- **Spring physics** — replace linear easing with spring-based motion
- **Colored tinted shadows** — shadows that carry the background hue
- **Grain and noise overlays** — fixed `pointer-events-none` layer to break digital flatness

## Rules

- Work with the existing tech stack. Do not migrate frameworks
- Do not break existing functionality. Test after every change
- Before importing any new library, check `package.json` first
- If the project uses Tailwind, check v3 vs v4 before modifying config
- Keep changes reviewable and focused

## Related Skills

- `taste-skill` — The full anti-slop frontend framework for greenfield builds
- `soft-skill` — Premium agency-level component architecture
- `design-is` — Dieter Rams audit before the redesign
- `pathfinder` — Map architecture before redesigning component structure
- `full-output-enforcement` — Pair to ensure complete component output
