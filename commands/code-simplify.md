---
name: code-simplify
description: Simplify recently changed code for clarity without changing behavior.
---

Apply the code-simplification skill to the recently modified code.

Follow this process:

1. **Identify scope** — Which files changed recently? (`git diff --name-only HEAD~1`)
2. **Understand first** — Read each file before touching it. Apply Chesterton's Fence: understand why each piece exists before removing it.
3. **Find opportunities** — Look for:
   - Deep nesting (3+ levels) → extract to guard clauses or helpers
   - Long functions (50+ lines) → split into focused functions
   - Generic names (`data`, `result`, `temp`) → rename meaningfully
   - Duplicated logic → extract to shared function
   - Dead code → remove (confirm it's truly dead first)
4. **Apply incrementally** — One simplification at a time. Run tests after each change.
5. **Verify** — Run tests. Confirm all pass without modification.

The test: "Would a new team member understand this faster than the original?"

Reference: `skills/code-simplification/SKILL.md`
