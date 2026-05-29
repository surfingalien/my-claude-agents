---
name: industrial-brutalist-ui
description: >-
  Raw mechanical interfaces fusing Swiss typographic print with military
  terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian
  color, analog degradation effects (halftones, CRT scanlines, bitmap dithering).
  TRIGGER when: user asks for brutalist, industrial, terminal, Swiss-type,
  data-heavy dashboard, portfolio, or editorial site that should feel like a
  declassified blueprint.
origin: taste-skill
owner: surfingalien
---

# industrial-brutalist-ui

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Architect web interfaces that synthesize mid-century Swiss Typographic design, industrial manufacturing manuals, and retro-futuristic aerospace/military terminal interfaces. Rigid modular grids, extreme typographic scale contrast, purely utilitarian color palettes, and programmatic simulation of analog degradation.

**Ship > Perfect. Raw functionality is a design choice — execute it with precision.**

## Visual Mode — Pick ONE Per Project

**Do not mix both modes within the same interface.**

### Swiss Industrial Print
Derived from 1960s corporate identity systems and heavy machinery blueprints.
- High-contrast light modes (newsprint/off-white substrates)
- Monolithic heavy sans-serif typography
- Unforgiving structural grids with visible dividing lines
- Aggressive asymmetric use of negative space with oversized viewport-bleeding numerals
- Heavy use of primary red as alert/accent

### Tactical Telemetry & CRT Terminal
Derived from classified military databases, legacy mainframes, and aerospace HUDs.
- Dark mode exclusively
- High-density tabular data presentation
- Absolute dominance of monospaced typography
- Technical framing devices (ASCII brackets, crosshairs)
- Simulated hardware limitations (phosphor glow, scanlines, low bit-depth)

## Typographic Architecture

### Macro-Typography (Structural Headers)
- **Fonts**: Neue Haas Grotesk Black, Inter Extra Bold/Black, Archivo Black, Monument Extended
- **Scale**: `clamp(4rem, 10vw, 15rem)`
- **Tracking**: Very tight, negative (`-0.03em` to `-0.06em`)
- **Line-height**: Highly compressed (`0.85` to `0.95`)
- **Case**: Exclusively uppercase

### Micro-Typography (Data & Telemetry)
- **Fonts**: JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime
- **Scale**: Fixed small (`10px`–`14px` / `0.7rem`–`0.875rem`)
- **Tracking**: Generous (`0.05em` to `0.1em`)
- **Case**: Exclusively uppercase — all metadata, navigation, unit IDs, coordinates

### Textural Contrast (Artistic Disruption — use sparingly)
- **Fonts**: Playfair Display, EB Garamond, Times New Roman
- Must be subjected to halftone/1-bit dithering post-processing
- Used for juxtaposition only, never as the primary type

## Color System

**CRITICAL: Choose ONE substrate palette per project. Never mix light and dark substrates.**

### Swiss Industrial Print (Light)
- Background: `#F4F4F0` or `#EAE8E3` (matte unbleached documentation paper)
- Foreground: `#050505` to `#111111` (carbon ink)
- Accent: `#E61919` or `#FF2A2A` (aviation/hazard red) — the ONLY accent

### Tactical Telemetry (Dark)
- Background: `#0A0A0A` or `#121212` (never pure `#000000`)
- Foreground: `#EAEAEA` (white phosphor)
- Accent: `#E61919` or `#FF2A2A` (same red, same rules)
- Terminal Green `#4AF626`: optional, ONLY for one specific UI element — never general text

## Layout & Spatial Engineering

- **The Blueprint Grid**: Strict CSS Grid. Elements anchored to grid tracks and intersections.
- **Visible Compartmentalization**: Solid `1px` or `2px` borders to delineate zones. Horizontal `<hr>` spanning full container width.
- **Bimodal Density**: Tightly packed monospace metadata alternating with vast expanses of negative space framing macro-typography.
- **Geometry**: Absolute rejection of `border-radius`. All corners exactly 90°.

## UI Components & Symbology

- **Syntax Decoration**: `[ DELIVERY SYSTEMS ]`, `< RE-IND >`, `>>>`, `///`
- **Industrial Markers**: `®`, `©`, `™` as structural geometric elements
- **Technical Assets**: `+` crosshairs at grid intersections, repeating vertical lines (barcodes), thick warning stripes, randomized strings (`REV 2.6`, `UNIT / D-01`)

## Textural & Post-Processing Effects

- **Halftone/1-Bit Dithering**: CSS `mix-blend-mode: multiply` + SVG radial dot patterns
- **CRT Scanlines**: `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`
- **Mechanical Noise**: Low-opacity SVG static/noise filter on DOM root

## Engineering Directives

1. **Grid Determinism**: `display: grid; gap: 1px;` with contrasting parent/child backgrounds — mathematical, razor-thin dividers without complex border declarations
2. **Semantic Rigidity**: `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>` — reflect the technical nature of the telemetry
3. **Typography Clamping**: CSS `clamp()` exclusively for macro-typography

## FinSurfing Context

Brutalist/terminal aesthetic fits specific FinSurfing screens:
- **Trading terminal views** — High-density stock data in Tactical Telemetry mode: ticker symbols, OHLC data, volume — all monospace, all uppercase, `#4AF626` for live price, red for negative
- **System/debug views** — Claude API call logs, Railway deploy logs, PostgreSQL query inspector
- **Market data dashboards** — Swiss Industrial Print mode works well for dense comparison tables

## Related Skills

- `minimalist-ui` — Opposite aesthetic; use when the brief calls for calm over tension
- `soft-skill` — Premium agency-level output; use for consumer-facing surfaces
- `full-output-enforcement` — Pair to ensure complete component output
