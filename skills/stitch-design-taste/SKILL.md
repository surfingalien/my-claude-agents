---
name: stitch-design-taste
description: >-
  Generates DESIGN.md files optimized for Google Stitch screen generation.
  Translates anti-slop frontend engineering directives into Stitch's semantic
  design language — typography, color, component behaviors, layout principles,
  motion philosophy, and explicit anti-pattern bans.
  TRIGGER when: user wants to create a DESIGN.md for Stitch, or wants
  agent-friendly design system documentation for any AI code generator.
origin: taste-skill
owner: surfingalien
---

# stitch-design-taste

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Generate `DESIGN.md` files that serve as the **single source of truth** for prompting AI agents (Google Stitch, Codex, Cursor, Claude Code) to produce premium, non-generic interfaces. Translates design intent into semantic, natural-language rules paired with precise values.

**Automate Ruthlessly. One DESIGN.md → consistent premium output across all sessions.**

## Prerequisites

- Google Stitch via [labs.google.com/stitch](https://labs.google.com/stitch)
- Optional: Stitch MCP Server for programmatic integration with Cursor or Gemini CLI

## Analysis & Synthesis Instructions

### 1. Define the Atmosphere

Use evocative adjectives from the taste spectrum:
- **Density**: "Art Gallery Airy" (1–3) → "Daily App Balanced" (4–7) → "Cockpit Dense" (8–10)
- **Variance**: "Predictable Symmetric" (1–3) → "Offset Asymmetric" (4–7) → "Artsy Chaotic" (8–10)
- **Motion**: "Static Restrained" (1–3) → "Fluid CSS" (4–7) → "Cinematic Choreography" (8–10)

**Default baseline**: Variance 8, Motion 6, Density 4. Adapt dynamically from the brief.

### 2. Map the Color Palette

For each color provide: **Descriptive Name** + **Hex Code** + **Functional Role**.

**Mandatory constraints:**
- Maximum 1 accent color. Saturation below 80%
- "AI Purple/Blue Neon" aesthetic strictly BANNED
- Absolute neutral bases (Zinc/Slate) with high-contrast singular accents
- One palette for the entire output — no warm/cool gray fluctuation
- Never pure black (`#000000`) — use Off-Black, Zinc-950, or Charcoal

### 3. Establish Typography Rules

- **Display/Headlines**: Track-tight, controlled scale. Hierarchy through weight and color, not just size
- **Body**: Relaxed leading, max 65 characters per line
- **Font selection**: `Inter` BANNED for premium/creative contexts. Use `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`
- **Serif Ban**: Generic serifs (`Times New Roman`, `Georgia`, `Garamond`) BANNED. If serif is needed, use only: `Fraunces`, `Gambarino`, `Editorial New`, or `Instrument Serif`
- **Dashboard Constraint**: Sans-Serif exclusively (`Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`)
- **High-Density Override**: When density exceeds 7, all numbers must use Monospace

### 4. Define the Hero Section

- **Inline Image Typography**: Embed small contextual photos directly between words in headlines
- **No Overlapping**: Text must never overlap images or other text
- **No Filler Text**: "Scroll to explore", "Swipe down", scroll arrows BANNED
- **Asymmetric Structure**: Centered Hero layouts BANNED when variance exceeds 4
- **CTA Restraint**: Maximum one primary CTA

### 5. Describe Component Stylings

- **Buttons**: Tactile push feedback on active state. No neon outer glows. No custom mouse cursors
- **Cards**: Only when elevation communicates hierarchy. Tint shadows to background hue. For high-density, replace cards with `border-top` dividers or negative space
- **Inputs/Forms**: Label above input, helper text optional, error text below. Standard gap spacing
- **Loading States**: Skeletal loaders matching layout dimensions — no generic circular spinners
- **Empty States**: Composed compositions indicating how to populate data

### 6. Define Layout Principles

- No overlapping elements — every element occupies its own clear spatial zone
- Centered Hero sections BANNED when variance exceeds 4 — force Split Screen, Left-Aligned, or Asymmetric Whitespace
- The generic "3 equal cards horizontally" feature row BANNED — use 2-column Zig-Zag or asymmetric grid
- CSS Grid over Flexbox math — never use `calc()` percentage hacks
- Full-height sections must use `min-h-[100dvh]` — never `h-screen` (iOS Safari)

### 7. Define Responsive Rules

- **Mobile-First Collapse (< 768px)**: All multi-column layouts collapse to single column
- **No Horizontal Scroll**: Horizontal overflow on mobile is a critical failure
- **Typography Scaling**: Headlines via `clamp()`. Body minimum `1rem`/`14px`
- **Touch Targets**: All interactive elements minimum `44px`
- **Spacing**: `clamp(3rem, 8vw, 6rem)` for section gaps

### 8. Encode Motion Philosophy

- **Spring Physics default**: `stiffness: 100, damping: 20` — premium, weighty feel. No linear easing
- **Perpetual Micro-Interactions**: Every active component has an infinite loop state (Pulse, Typewriter, Float, Shimmer)
- **Staggered Orchestration**: Never mount lists instantly — cascade delays for waterfall reveals
- **Performance**: Animate exclusively via `transform` and `opacity`. Grain/noise filters on fixed pseudo-elements only

### 9. List Anti-Patterns

Encode as explicit "NEVER DO" rules:
- No emojis anywhere
- No `Inter` font
- No generic serif fonts (`Times New Roman`, `Georgia`, `Garamond`)
- No pure black (`#000000`)
- No neon/outer glow shadows
- No oversaturated accents
- No excessive gradient text on large headers
- No custom mouse cursors
- No overlapping elements
- No 3-column equal card layouts
- No generic names ("John Doe", "Acme", "Nexus")
- No fake round numbers (`99.99%`, `50%`)
- No AI copywriting clichés ("Elevate", "Seamless", "Unleash", "Next-Gen")
- No filler UI text ("Scroll to explore", "Swipe down", bouncing chevrons)
- No broken Unsplash links — use `picsum.photos` or SVG avatars

## DESIGN.md Output Format

```markdown
# Design System: [Project Title]

## 1. Visual Theme & Atmosphere
(Evocative description of mood, density, variance, and motion intensity.
Example: "A restrained, gallery-airy interface with confident asymmetric
layouts and fluid spring-physics motion. Clinical yet warm — like a
well-lit architecture studio.")

## 2. Color Palette & Roles
- **Canvas White** (#F9FAFB) — Primary background surface
- **Pure Surface** (#FFFFFF) — Card and container fill
- **Charcoal Ink** (#18181B) — Primary text, Zinc-950 depth
- **Muted Steel** (#71717A) — Secondary text, descriptions, metadata
- **Whisper Border** (rgba(226,232,240,0.5)) — Card borders, 1px structural lines
- **[Accent Name]** (#XXXXXX) — Single accent for CTAs, active states, focus rings

## 3. Typography Rules
- **Display:** [Font Name] — Track-tight, controlled scale, weight-driven hierarchy
- **Body:** [Font Name] — Relaxed leading, 65ch max-width, neutral secondary color
- **Mono:** [Font Name] — For code, metadata, timestamps, high-density numbers
- **Banned:** Inter, generic system fonts for premium contexts. Serif fonts banned in dashboards.

## 4. Component Stylings
* **Buttons:** Flat, no outer glow. Tactile -1px translate on active. Accent fill for primary, ghost/outline for secondary.
* **Cards:** Generously rounded (2.5rem). Diffused whisper shadow. Used only when elevation serves hierarchy.
* **Inputs:** Label above, error below. Focus ring in accent color. No floating labels.
* **Loaders:** Skeletal shimmer matching exact layout dimensions. No circular spinners.
* **Empty States:** Composed, illustrated compositions.

## 5. Layout Principles
(Grid-first responsive architecture. Asymmetric splits for Hero sections.
Strict single-column collapse below 768px. Max-width containment.
No flexbox percentage math. Generous internal padding.)

## 6. Motion & Interaction
(Spring physics for all interactive elements. Staggered cascade reveals.
Perpetual micro-loops on active dashboard components. Hardware-accelerated
transforms only. Isolated Client Components for CPU-heavy animations.)

## 7. Anti-Patterns (Banned)
(Explicit list of forbidden patterns.)
```

## FinSurfing Context

For FinSurfing's DESIGN.md:

```markdown
# Design System: FinSurfing

## 1. Visual Theme & Atmosphere
Confident, data-dense financial intelligence platform. Ethereal glass
on dark — OLED blacks with precise cyan/amber accents. Feels like a
professional trading terminal elevated to consumer premium. Motion is
purposeful: stock data animates in, AI analysis fades up, no decorative
motion for its own sake. Density: 6/10 — enough breathing room to feel
premium, enough density to feel like a real tool.

## 2. Color Palette & Roles
- **Deep Background** (#090E1A) — OLED dark base
- **Surface** (#111827) — Card and panel fill
- **Border** (rgba(255,255,255,0.06)) — Structural lines
- **Primary Text** (#F1F5F9) — Headlines and data
- **Secondary Text** (#64748B) — Labels, metadata, secondary copy
- **Cyan Accent** (#06B6D4) — CTAs, active states, live data indicators
- **Gain Green** (#10B981) — Positive P&L (desaturated, not neon)
- **Loss Red** (#EF4444) — Negative P&L (desaturated, not alarm-red)
```

## Related Skills

- `taste-skill` — Full anti-slop frontend framework for implementing DESIGN.md specs
- `soft-skill` — Premium component architecture referenced by DESIGN.md
- `minimalist-ui` — Alternate aesthetic direction for DESIGN.md generation
- `design-is` — Audit existing UI before generating replacement DESIGN.md
