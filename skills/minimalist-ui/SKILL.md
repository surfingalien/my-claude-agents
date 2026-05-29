---
name: minimalist-ui
description: >-
  Premium utilitarian minimalism — editorial-style interfaces with warm
  monochrome palettes, typographic contrast, flat bento grids, and muted pastel
  accents. No gradients, no heavy shadows, no generic defaults.
  TRIGGER when: user asks for clean, editorial, Notion-style, Linear-style,
  calm, or document-UI vibes.
origin: taste-skill
owner: surfingalien
---

# minimalist-ui

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Engineer refined, ultra-minimalist "document-style" web interfaces analogous to top-tier workspace platforms (Notion, Linear, Vercel). High-contrast warm monochrome palette, bespoke typographic hierarchies, meticulous macro-whitespace, bento-grid layouts, and an ultra-flat component architecture with deliberate muted pastel accents.

**Ship > Perfect. But every detail must be intentional.**

## Absolute Bans

Never use these defaults:

- `Inter`, `Roboto`, or `Open Sans` typefaces
- Generic thin-line icon libraries like `Lucide`, `Feather`, or standard `Heroicons`
- Tailwind heavy drop shadows (`shadow-md`, `shadow-lg`, `shadow-xl`)
- Primary colored backgrounds for large elements (no bright blue/green/red hero sections)
- Gradients, neon colors, or 3D glassmorphism
- `rounded-full` for large containers, cards, or primary buttons
- Emojis anywhere in code, markup, or text content
- Generic names like "John Doe", "Acme Corp", or "Lorem Ipsum"
- AI copy clichés: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer"

## Typographic Architecture

Extreme typographic contrast establishes the editorial feel.

- **Primary Sans-Serif** (body, UI, buttons): `'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`
- **Editorial Serif** (hero headings, quotes): `'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif` — tight tracking (`-0.02em` to `-0.04em`), tight line-height (`1.1`)
- **Monospace** (code, keystrokes, metadata): `'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`
- Body text: never `#000000` — use off-black `#111111` or `#2F3437`, generous `line-height: 1.6`. Secondary text: muted gray `#787774`

## Color Palette

Color is a scarce resource — used only for semantic meaning or subtle accents.

- **Canvas**: Pure White `#FFFFFF` or Warm Bone `#F7F6F3` / `#FBFBFA`
- **Primary Surface** (cards): `#FFFFFF` or `#F9F9F8`
- **Borders/Dividers**: Ultra-light gray `#EAEAEA` or `rgba(0,0,0,0.06)`
- **Accent Colors** (tags, inline code backgrounds only):
  - Pale Red: `#FDEBEC` (text `#9F2F2D`)
  - Pale Blue: `#E1F3FE` (text `#1F6C9F`)
  - Pale Green: `#EDF3EC` (text `#346538`)
  - Pale Yellow: `#FBF3DB` (text `#956400`)

## Component Specifications

### Bento Box Feature Grids
- Asymmetrical CSS Grid layouts
- Cards: `border: 1px solid #EAEAEA`, border-radius max `8px` or `12px`, internal padding `24px`–`40px`

### Primary CTAs
- Solid `#111111` background, `#FFFFFF` text
- Radius `4px`–`6px`. No box-shadow
- Hover: `#333333` shift or `transform: scale(0.98)`

### Tags & Status Badges
- Pill-shaped (`border-radius: 9999px`), `text-xs`, uppercase `letter-spacing: 0.05em`
- Background: muted pastels from palette above

### Accordions
- Strip all container boxes. Separate with `border-bottom: 1px solid #EAEAEA`
- Clean `+` / `-` toggle icon

### Keystroke Micro-UIs
- `<kbd>` tags: `border: 1px solid #EAEAEA`, `border-radius: 4px`, `background: #F7F6F3`, monospace font

### Faux-OS Window Chrome
- White top bar with three small light-gray circles (macOS window controls)

## Execution Protocol

1. Establish macro-whitespace first — `py-24` or `py-32` between sections
2. Constrain main content to `max-w-4xl` or `max-w-5xl`
3. Apply custom typographic hierarchy and monochromatic color variables immediately
4. Every card, divider, border: `1px solid #EAEAEA` rule
5. Add scroll-entry animations to all major content blocks
6. Sections need visual depth — use low-opacity background imagery, soft radial gradients (`opacity: 0.03`), or minimal geometric patterns. No empty flat backgrounds.

## Motion (Invisible Sophistication)

Motion should feel present but never distracting.

- **Scroll Entry**: `translateY(12px)` + `opacity: 0` → `translateY(0)` + `opacity: 1` over `600ms` `cubic-bezier(0.16, 1, 0.3, 1)`. Use `IntersectionObserver`.
- **Hover**: Cards lift with `box-shadow: 0 2px 8px rgba(0,0,0,0.04)` over `200ms`.
- **Staggered Reveals**: `animation-delay: calc(var(--index) * 80ms)`.
- **Background Ambient**: Single slow-moving radial gradient (`20s+`, `opacity: 0.02–0.04`) on `position: fixed; pointer-events: none`. Never on scrolling containers.
- **Animate only**: `transform` and `opacity`. Never `top`, `left`, `width`, `height`.

## FinSurfing Context

For FinSurfing's stock intelligence UI:
- Stock data tables → use `divide-y divide-[#EAEAEA]` instead of card containers per row
- Positive/negative P&L → pale green / pale red accent backgrounds (from palette above), never bright green/red
- AI analysis panels → faux-OS window chrome treatment makes Claude's output feel like a "document", not a chat bubble
- Settings and watchlist screens → perfect for this style: clean, data-dense, no visual noise

## Related Skills

- `design-is` — Audit existing UI against Dieter Rams principles before applying this style
- `redesign-existing-projects` — Upgrade an existing messy codebase to this aesthetic
- `taste-skill` — More expressive default; use minimalist-ui when the brief calls for restraint
- `full-output-enforcement` — Pair to ensure full component output, not truncated skeletons
