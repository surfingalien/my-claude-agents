---
name: build
description: Run the full build pipeline and report any failures. Lint, typecheck, test, then build.
---

Run the full quality gate pipeline for this project:

1. **Lint** — Run `npm run lint` (or equivalent). Fix any errors before continuing.
2. **Typecheck** — Run `npx tsc --noEmit`. Fix all type errors before continuing.
3. **Test** — Run `npm test`. All tests must pass.
4. **Build** — Run `npm run build`. Report bundle sizes if available.
5. **Audit** — Run `npm audit --audit-level=high`. Report any high/critical vulnerabilities.

Report results for each step. If any step fails, stop and fix before proceeding.

At the end, summarize:
- Pass/fail for each step
- Any warnings worth noting
- Build output size (if available)
