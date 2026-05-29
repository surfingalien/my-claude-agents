---
name: design-taste-frontend-v1
description: >-
  The original v1 taste-skill, preserved for projects depending on its exact
  behavior. The current default is design-taste-frontend (v2), which is a
  substantial rewrite. Use this v1 install name only if you need exact
  backward compatibility with projects built on v1.
origin: taste-skill
owner: surfingalien
---

# design-taste-frontend-v1

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

> **Note:** This is the preserved v1 skill. For new projects, use `design-taste-frontend` (v2). Use this only when a project was explicitly built against v1 behavior.

## Active Baseline Configuration

```
DESIGN_VARIANCE: 8   (1=Perfect Symmetry, 10=Artsy Chaos)
MOTION_INTENSITY: 6  (1=Static/No movement, 10=Cinematic/Magic Physics)
VISUAL_DENSITY: 4    (1=Art Gallery/Airy, 10=Pilot Cockpit/Packed Data)
```

AI Instruction: Baseline is strictly 8/6/4. Do not ask the user to edit this file. Adapt values dynamically from explicit user requests.

## Default Architecture & Conventions

- **Framework**: React or Next.js. Default to Server Components (RSC).
- **RSC Safety**: Global state in Client Components only. Wrap providers in `"use client"`.
- **Interactivity Isolation**: Motion/scroll/pointer components must be isolated leaf components with `'use client'`.
- **Styling**: Tailwind CSS (v3/v4). Check `package.json` for version before modifying config.
- **Anti-Emoji Policy**: NEVER use emojis in code, markup, text content, or alt text.
- **Viewport Stability**: NEVER `h-screen`. ALWAYS `min-h-[100dvh]`.
- **Grid over Flex-Math**: NEVER `w-[calc(33%-1rem)]`. ALWAYS CSS Grid.
- **Icons**: `@phosphor-icons/react` or `@radix-ui/react-icons`. Standardize `strokeWidth`.
- **Dependency Verification**: Check `package.json` before importing any 3rd-party library.

## Design Engineering Directives

### Rule 1: Typography
- Display: `text-4xl md:text-6xl tracking-tighter leading-none`
- Body: `text-base text-gray-600 leading-relaxed max-w-[65ch]`
- Font: `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi` — not Inter
- Technical UI Rule: Serif fonts BANNED for Dashboard/Software UIs

### Rule 2: Color Calibration
- Max 1 accent color. Saturation < 80%
- THE LILA BAN: "AI Purple/Blue" aesthetic strictly BANNED
- One palette for the entire output. No warm/cool gray fluctuation

### Rule 3: Layout Diversification
- Centered Hero BANNED when `DESIGN_VARIANCE > 4`
- Force "Split Screen", "Left-Aligned content/Right-Aligned asset", or "Asymmetric White-space"

### Rule 4: Materiality, Shadows, Cards
- Dashboard (`VISUAL_DENSITY > 7`): generic card containers BANNED — use `border-t`, `divide-y`, or negative space
- Cards only when elevation communicates hierarchy. Tint shadows to background hue

### Rule 5: Interactive UI States
- **Loading**: Skeletal loaders matching layout sizes
- **Empty States**: Beautifully composed empty states
- **Error States**: Clear, inline error reporting
- **Tactile Feedback**: `-translate-y-[1px]` or `scale-[0.98]` on `:active`

### Rule 6: Data & Form Patterns
- Label ABOVE input. Helper text optional. Error text BELOW. `gap-2` for input blocks

## Creative Proactivity (Anti-Slop)

- **Liquid Glass Refraction**: `backdrop-blur` + `border-white/10` + `shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`
- **Magnetic Micro-physics** (if `MOTION_INTENSITY > 5`): Framer Motion `useMotionValue` + `useTransform` ONLY — never `useState`
- **Perpetual Micro-Interactions** (if `MOTION_INTENSITY > 5`): Pulse, Typewriter, Float, Shimmer — spring physics (`stiffness: 100, damping: 20`)
- **Layout Transitions**: Framer Motion `layout` and `layoutId` props
- **Staggered Orchestration**: `staggerChildren` or `animation-delay: calc(var(--index) * 100ms)`

## Performance Guardrails

- Grain/noise: fixed `pointer-events-none` pseudo-elements only — never on scrolling containers
- Animate via `transform` and `opacity` only
- No arbitrary `z-50` / `z-10` — use systemic z-index layers

## Dial Definitions

### DESIGN_VARIANCE
- 1-3: Flexbox `justify-center`, strict symmetrical grids
- 4-7: Overlapping `-2rem`, varied aspect ratios, left-aligned headers
- 8-10: Masonry, fractional grid units, `padding-left: 20vw`
- Mobile override: asymmetric layouts above `md:` → strict single-column `< 768px`

### MOTION_INTENSITY
- 1-3: CSS `:hover` / `:active` states only
- 4-7: `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`, `animation-delay` cascades
- 8-10: Scroll-triggered reveals, parallax, Framer Motion hooks. NEVER `window.addEventListener('scroll')`

### VISUAL_DENSITY
- 1-3: Huge section gaps, very expensive and clean
- 4-7: Normal web app spacing
- 8-10: Tight paddings, 1px data dividers, `font-mono` for all numbers

## AI Tells (Forbidden Patterns)

- NO neon/outer glows
- NO pure black (`#000000`)
- NO oversaturated accents
- NO excessive gradient text
- NO custom mouse cursors
- NO Inter font
- NO oversized H1s that just scream
- NO 3-column equal feature cards
- NO generic names ("John Doe", "Jane Smith")
- NO fake-perfect numbers (`99.99%`, `50%`)
- NO startup-slop names ("Acme", "Nexus", "SmartFlow")
- NO broken Unsplash links — use `picsum.photos/seed/{string}/{w}/{h}`
- NO hand-rolled SVG icons

## Related Skills

- `design-taste-frontend` — v2 (current default, substantial rewrite)
- `full-output-enforcement` — Pair to ensure complete code output
- `redesign-existing-projects` — Upgrade an existing project using these rules
