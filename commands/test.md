---
name: test
description: Write tests before implementation using the Red-Green-Refactor cycle.
---

Apply the test-driven-development skill.

For **new features** — follow Red-Green-Refactor:
1. **RED** — Write a failing test that defines the expected behavior. Run it. Confirm it fails.
2. **GREEN** — Write the minimum code to make the test pass. Run all tests.
3. **REFACTOR** — Improve the code without changing behavior. Run all tests again.
4. Repeat for the next behavior.

For **bug fixes** — use the Prove-It pattern:
1. **REPRODUCE** — Write a test that reproduces the bug. It must fail.
2. **VERIFY** — Confirm it fails for the right reason.
3. **FIX** — Fix the bug.
4. **CONFIRM** — Confirm the test now passes.
5. **CHECK** — Run all tests to ensure no regression.

Test naming: describe behavior, not implementation.
- Good: `it('rejects titles longer than 200 characters')`
- Bad: `it('calls the validator')`

Tests should be DAMP (readable in isolation), not DRY.

Reference: `skills/test-driven-development/SKILL.md`
